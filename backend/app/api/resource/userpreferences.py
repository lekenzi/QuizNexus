from datetime import datetime

from flask import request
from flask_jwt_extended import get_jwt_identity
from flask_restful import Resource

from app.cache import cache_result
from app.middleware.auth_middleware import jwt_auth_required, role_required
from app.models import User, UserPreference, db


class UserPreferencesResource(Resource):
    @jwt_auth_required
    @role_required(["user"])
    @cache_result()
    def get(self):
        """Return user preferences including reminder settings and other details."""
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user:
            return {"message": "User not found"}, 404

        user_preferences = UserPreference.query.filter_by(user_id=user_id).first()

        if not user_preferences:
            return {"message": "User preferences not found"}, 404

        preferences = {
            "notifications_enabled": True,
            "reminder_time": (
                user_preferences.reminder_time.strftime("%H:%M")
                if user_preferences.reminder_time
                else "18:00"
            ),
            "email_reminders": user_preferences.email_reminders,
            "monthly_report": user_preferences.monthly_report,
            "last_visit": (
                user_preferences.last_visit.isoformat()
                if user_preferences.last_visit
                else None
            ),
        }

        return {"preferences": preferences}, 200

    @jwt_auth_required
    @role_required(["user"])
    def post(self):
        """Update user preferences."""
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user:
            return {"message": "User not found"}, 404

        data = request.get_json()
        reminder_time = data.get("reminder_time")
        email_reminders = data.get("email_reminders", True)
        monthly_report = data.get("monthly_report", True)

        user_preferences = UserPreference.query.filter_by(user_id=user_id).first()

        if not user_preferences:
            user_preferences = UserPreference(user_id=user_id)

        if reminder_time:
            try:
                
                if len(reminder_time) == 5:  
                    user_preferences.reminder_time = datetime.strptime(
                        reminder_time, "%H:%M"
                    ).time()
                else:  
                    user_preferences.reminder_time = datetime.strptime(
                        reminder_time, "%H:%M:%S"
                    ).time()
            except ValueError:
                return {"message": "Invalid time format. Use HH:MM or HH:MM:SS"}, 400

        user_preferences.email_reminders = email_reminders
        user_preferences.monthly_report = monthly_report
        user_preferences.updated_at = datetime.now()

        db.session.add(user_preferences)
        db.session.commit()

        return {
            "message": "Preferences updated successfully",
            "reminder_time": user_preferences.reminder_time.strftime("%H:%M"),
        }, 200
