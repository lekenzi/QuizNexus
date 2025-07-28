import csv
import io
import logging  # Add logging import if not already present
from datetime import datetime, timedelta

from app.celery_app import celery_app
from app.email import send_email_with_attachment
from app.models import *


def create_app_context():
    """Create and return a Flask app context."""
    from app import create_app

    app = create_app()
    return app


@celery_app.task
def generate_user_stats_csv():
    """Generate a CSV with user statistics for admin"""
    app = create_app_context()

    with app.app_context():
        users = User.query.all()

        output = io.StringIO()
        writer = csv.writer(output)

        writer.writerow(
            [
                "User ID",
                "Username",
                "Full Name",
                "Quizzes Taken",
                "Average Score",
                "Total Points",
                "Last Quiz Date",
                "Most Active Subject",
                "Completion Rate",
            ]
        )

        for user in users:

            scores = Score.query.filter_by(user_id=user.id).all()

            quizzes_taken = len(scores)
            total_points = sum(score.score for score in scores) if scores else 0
            avg_score = total_points / quizzes_taken if quizzes_taken > 0 else 0

            last_quiz_date = (
                max([score.timestamp for score in scores]) if scores else None
            )
            last_quiz_date_str = (
                last_quiz_date.strftime("%Y-%m-%d") if last_quiz_date else "N/A"
            )

            subject_counts = {}
            for score in scores:
                quiz = Quiz.query.get(score.quiz_id)
                if quiz and quiz.subject_id:
                    subject = Subject.query.get(quiz.subject_id)
                    if subject:
                        subject_counts[subject.name] = (
                            subject_counts.get(subject.name, 0) + 1
                        )

            most_active_subject = (
                max(subject_counts.items(), key=lambda x: x[1])[0]
                if subject_counts
                else "N/A"
            )

            all_quizzes = Quiz.query.count()
            completion_rate = (
                (quizzes_taken / all_quizzes) * 100 if all_quizzes > 0 else 0
            )

            writer.writerow(
                [
                    user.id,
                    user.username,
                    user.full_name,
                    quizzes_taken,
                    f"{avg_score:.2f}",
                    total_points,
                    last_quiz_date_str,
                    most_active_subject,
                    f"{completion_rate:.2f}%",
                ]
            )

        csv_data = output.getvalue()

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"user_stats_{timestamp}.csv"
        file_path = f"/tmp/{filename}"

        with open(file_path, "w") as f:
            f.write(csv_data)

        admin_users = User.query.filter_by(role="admin").all()
        logging.info(f"Sending CSV report to {len(admin_users)} admin users")

        for admin in admin_users:
            logging.info(f"Attempting to send email to admin: {admin.username}")
            email_sent = send_email_with_attachment(
                admin.username,
                "User Statistics Export Complete",
                f"Your requested export of user statistics is complete. Please find the CSV file attached.",
                csv_data,
                f"user_stats_{timestamp}.csv",
            )
            logging.info(f"Email sent status: {email_sent}")

        return {
            "success": True,
            "filename": filename,
            "path": file_path,
            "timestamp": timestamp,
        }


@celery_app.task
def check_export_status(task_id):
    """Check if a CSV export task is complete"""
    result = celery_app.AsyncResult(task_id)
    status = result.status

    if status == "SUCCESS":
        result_data = result.get()
        return {
            "status": "complete",
            "filename": result_data.get("filename"),
            "timestamp": result_data.get("timestamp"),
        }
    elif status == "FAILURE":
        return {"status": "failed", "error": str(result.result)}
    else:
        return {"status": status}


@celery_app.task
def calculate_ended_quiz_scores():
    """Calculate scores for all users who took quizzes that have ended"""
    app = create_app_context()

    with app.app_context():

        now = datetime.now()
        one_hour_ago = now - timedelta(hours=10)

        print(f"Running score calculation at {now.strftime('%Y-%m-%d %H:%M:%S')}")

        ended_quizzes = []

        quizzes = Quiz.query.all()

        for quiz in quizzes:

            quiz_start = datetime.combine(quiz.date_of_quiz, quiz.time_of_day)
            quiz_end = quiz_start + timedelta(minutes=quiz.time_duration)

            if now < quiz_end:
                print(
                    f"Skipping quiz {quiz.quiz_title} (ID: {quiz.id}) - still in progress until {quiz_end}"
                )
                continue

            if quiz_end <= now and quiz_end >= one_hour_ago:
                ended_quizzes.append(quiz)
                print(
                    f"Found ended quiz: {quiz.quiz_title} (ID: {quiz.id}), ended at {quiz_end}"
                )

        if not ended_quizzes:
            print("No quizzes have ended in the specified time window")
            return "No quizzes ended in the specified time window"

        results = []
        score_verification = {}

        for quiz in ended_quizzes:
            print(f"\n--- Processing Quiz: {quiz.quiz_title} (ID: {quiz.id}) ---")

            questions = Question.query.filter_by(quiz_id=quiz.id).all()
            total_questions = len(questions)

            if total_questions == 0:
                print(f"Quiz {quiz.id} has no questions. Skipping...")
                continue

            print(f"Quiz has {total_questions} questions")

            user_ids = (
                db.session.query(QuizResponse.user_id)
                .filter_by(quiz_id=quiz.id)
                .distinct()
                .all()
            )
            user_ids = [uid[0] for uid in user_ids]

            print(f"Found {len(user_ids)} users with responses for this quiz")

            score_verification[quiz.id] = {
                "quiz_title": quiz.quiz_title,
                "total_questions": total_questions,
                "total_users": len(user_ids),
                "users_processed": 0,
                "scores_created": 0,
                "scores_updated": 0,
                "scores_skipped": 0,
                "users_with_issues": [],
            }

            for user_id in user_ids:
                try:
                    user = User.query.get(user_id)
                    username = user.username if user else f"User ID: {user_id}"

                    existing_score = Score.query.filter_by(
                        user_id=user_id,
                        quiz_id=quiz.id,
                    ).first()

                    if existing_score:
                        print(
                            f"  → Score already exists for user {username} on quiz {quiz.quiz_title}. Skipping calculation."
                        )
                        score_verification[quiz.id]["scores_skipped"] += 1
                        score_verification[quiz.id]["users_processed"] += 1

                        results.append(
                            {
                                "user_id": user_id,
                                "username": username,
                                "quiz_id": quiz.id,
                                "quiz_title": quiz.quiz_title,
                                "score": existing_score.score,
                                "status": "skipped - already calculated",
                            }
                        )
                        continue

                    responses = QuizResponse.query.filter_by(
                        quiz_id=quiz.id, user_id=user_id
                    ).all()
                    response_count = len(responses)

                    completion_status = (
                        "complete"
                        if response_count >= total_questions
                        else "incomplete"
                    )
                    completion_pct = (response_count / total_questions) * 100

                    print(
                        f"User {username} ({user_id}): {response_count}/{total_questions} questions answered ({completion_pct:.1f}%)"
                    )

                    correct_answers = sum(1 for r in responses if r.is_correct)

                    score_value = int((correct_answers / total_questions) * 100)

                    print(
                        f"  → {correct_answers} correct answers out of {total_questions}"
                    )
                    print(f"  → Final score: {score_value}%")

                    new_score = Score(
                        user_id=user_id,
                        quiz_id=quiz.id,
                        score=score_value,
                        timestamp=now,
                    )
                    db.session.add(new_score)
                    print(f"  → Created new score for {username}")
                    score_verification[quiz.id]["scores_created"] += 1

                    score_verification[quiz.id]["users_processed"] += 1

                    results.append(
                        {
                            "user_id": user_id,
                            "username": username,
                            "quiz_id": quiz.id,
                            "quiz_title": quiz.quiz_title,
                            "score": score_value,
                            "correct_answers": correct_answers,
                            "total_questions": total_questions,
                            "questions_answered": response_count,
                            "completion_status": completion_status,
                            "completion_percentage": f"{completion_pct:.1f}%",
                        }
                    )

                except Exception as e:
                    print(
                        f"Error processing user {user_id} for quiz {quiz.id}: {str(e)}"
                    )
                    score_verification[quiz.id]["users_with_issues"].append(
                        {"user_id": user_id, "error": str(e)}
                    )

            try:
                db.session.commit()
                print(f"Committed scores for quiz {quiz.quiz_title}")
            except Exception as e:
                db.session.rollback()
                print(f"Error committing scores for quiz {quiz.id}: {str(e)}")

        verification_report = {
            "timestamp": now.strftime("%Y-%m-%d %H:%M:%S"),
            "quizzes_processed": len(ended_quizzes),
            "total_scores_calculated": len(results),
            "quiz_details": score_verification,
        }

        try:
            report_timestamp = now.strftime("%Y%m%d_%H%M%S")
            report_filename = f"/tmp/score_calculation_report_{report_timestamp}.json"

            with open(report_filename, "w") as f:
                import json

                json.dump(verification_report, f, indent=2)

            print(f"Score calculation report saved to {report_filename}")
        except Exception as e:
            print(f"Failed to save verification report: {str(e)}")

        return {
            "message": f"Calculated scores for {len(results)} user-quiz combinations",
            "quizzes_processed": len(ended_quizzes),
            "scores": results,
            "verification": verification_report,
        }
