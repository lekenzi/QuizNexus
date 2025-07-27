"""
Script to check quiz data in the database
Run with: python check_quiz_data.py
"""

from datetime import datetime

from flask import Flask

from app.config import Config
from app.models import Quiz, db

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)


def check_quiz_data():
    with app.app_context():
        # Get current date and time
        now = datetime.now()
        today = now.date()
        current_time = now.time()

        print(f"Current date: {today}")
        print(f"Current time: {current_time}")

        # Get all quizzes
        all_quizzes = Quiz.query.all()
        print(f"\nTotal quizzes in database: {len(all_quizzes)}")

        # Check for specific quiz with ID 3
        quiz = Quiz.query.get(3)
        if quiz:
            print(f"\nQuiz ID 3 details:")
            print(f"  Title: {quiz.quiz_title}")
            print(f"  Date: {quiz.date_of_quiz} (Type: {type(quiz.date_of_quiz)})")
            print(f"  Time: {quiz.time_of_day} (Type: {type(quiz.time_of_day)})")
            print(f"  Started: {quiz.started} (Type: {type(quiz.started)})")
            print(f"  Duration: {quiz.time_duration} minutes")

            # Check date match
            date_match = quiz.date_of_quiz == today
            print(f"  Date matches today? {date_match}")

            # Check if quiz is within time window
            quiz_minutes = quiz.time_of_day.hour * 60 + quiz.time_of_day.minute
            current_minutes = current_time.hour * 60 + current_time.minute
            time_diff = current_minutes - quiz_minutes

            print(f"  Time difference: {time_diff} minutes")
            print(f"  Within -5 to +60 minute window? {-5 <= time_diff <= 60}")

            # Update quiz date if needed
            update_quiz = input("\nUpdate quiz date to today? (y/n): ")
            if update_quiz.lower() == "y":
                quiz.date_of_quiz = today
                db.session.commit()
                print(f"Quiz date updated to {today}")

            # Reset started flag if needed
            reset_started = input("Reset 'started' flag to False? (y/n): ")
            if reset_started.lower() == "y":
                quiz.started = False
                db.session.commit()
                print("Quiz 'started' flag reset to False")


if __name__ == "__main__":
    check_quiz_data()
