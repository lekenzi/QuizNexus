import os
from datetime import datetime, timedelta

from app.cache import cache_result
from app.middleware import jwt_auth_required, role_required
from app.models import Quiz, Score, User, db
from app.tasks import generate_user_stats_csv
from flask import request, send_file
from flask_restful import Resource


class CachedUserStats:
    @staticmethod
    @cache_result(expiration=600)
    def get_user_stats(user_id):
        """Get cached statistics for a user"""

        scores = Score.query.filter_by(user_id=user_id).all()
        quizzes_taken = len(scores)
        total_points = sum(score.score for score in scores) if scores else 0
        avg_score = total_points / quizzes_taken if quizzes_taken > 0 else 0

        return {
            "quizzes_taken": quizzes_taken,
            "total_points": total_points,
            "average_score": avg_score,
        }


class AdminDashboardResource(Resource):
    @jwt_auth_required
    @role_required(["admin"])
    @cache_result(expiration=300)
    def get(self):
        """Get admin dashboard statistics"""

        total_users = User.query.count()

        total_quizzes = Quiz.query.count()

        total_attempts = Score.query.count()

        thirty_days_ago = datetime.now() - timedelta(days=30)
        new_users = User.query.filter(User.date_of_birth >= thirty_days_ago).count()

        seven_days_ago = datetime.now() - timedelta(days=7)
        recent_quizzes = Quiz.query.filter(Quiz.date_of_quiz >= seven_days_ago).count()

        scores = [score.score for score in Score.query.all()]
        avg_score = sum(scores) / len(scores) if scores else 0

        return {
            "statistics": {
                "total_users": total_users,
                "total_quizzes": total_quizzes,
                "total_attempts": total_attempts,
                "new_users_30d": new_users,
                "recent_quizzes_7d": recent_quizzes,
                "average_score": round(avg_score, 2),
            }
        }, 200


class ExportUserStatsResource(Resource):
    @jwt_auth_required
    @role_required(["admin"])
    def post(self):
        """Trigger asynchronous CSV generation of user statistics"""
        task = generate_user_stats_csv.delay()

        return {
            "message": "Export started. You will receive an email when it's complete.",
            "task_id": str(task.id),
        }, 202

    @jwt_auth_required
    @role_required(["admin"])
    def get(self):
        """Check status of the export or download a specific file"""
        filename = request.args.get("filename")

        if filename:
            file_path = f"/tmp/{filename}"

            if os.path.exists(file_path):
                return send_file(
                    file_path,
                    mimetype="text/csv",
                    as_attachment=True,
                    download_name=filename,
                )
            else:
                return {"error": "File not found"}, 404

        exports = []
        for file in os.listdir("/tmp"):
            if file.startswith("user_stats_") and file.endswith(".csv"):
                file_stat = os.stat(f"/tmp/{file}")
                exports.append(
                    {
                        "filename": file,
                        "created": datetime.fromtimestamp(
                            file_stat.st_ctime
                        ).isoformat(),
                        "size": file_stat.st_size,
                    }
                )

        return {
            "exports": sorted(exports, key=lambda x: x["created"], reverse=True)
        }, 200


class AdminUsersResource(Resource):
    @jwt_auth_required
    @role_required(["admin"])
    def get(self):
        """Get list of users with their statistics"""
        page = int(request.args.get("page", 1))
        per_page = int(request.args.get("per_page", 10))

        users_pagination = User.query.paginate(
            page=page, per_page=per_page, error_out=False
        )
        users = users_pagination.items

        users_data = []
        for user in users:

            user_stats = CachedUserStats.get_user_stats(user.id)

            users_data.append(
                {
                    "id": user.id,
                    "username": user.username,
                    "full_name": user.full_name,
                    "role": user.role,
                    "stats": user_stats,
                }
            )

        return {
            "users": users_data,
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total": users_pagination.total,
                "pages": users_pagination.pages,
            },
        }, 200
