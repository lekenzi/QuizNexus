import csv
import io
import json
import logging
from calendar import monthrange
from datetime import datetime, timedelta

from app.agent.student_advisor import get_advisor
from app.celery_app import celery_app
from app.email import send_email, send_email_with_attachment
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
        one_hour_ago = now - timedelta(hours=1)

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


@celery_app.task
def send_daily_reminders():
    """Send daily reminders to users about new quizzes and inactivity"""
    app = create_app_context()

    with app.app_context():
        now = datetime.now()
        current_time = now.time()
        today = now.date()
        yesterday = today - timedelta(seconds=1)

        logging.info(
            f"Running daily reminders check at {now.strftime('%Y-%m-%d %H:%M:%S')}"
        )

        users = User.query.filter_by(role="user").all()

        reminder_stats = {
            "total_users_checked": len(users),
            "users_due_for_reminders": 0,
            "reminders_sent": 0,
            "inactive_users": 0,
            "new_quiz_alerts": 0,
            "ai_suggestions_generated": 0,
            "errors": [],
        }

        new_quizzes = Quiz.query.filter(Quiz.date_of_quiz >= yesterday).all()
        logging.info(f"Found {len(new_quizzes)} new quizzes since yesterday")

        week_ahead = today + timedelta(days=7)
        upcoming_quizzes = Quiz.query.filter(
            Quiz.date_of_quiz >= today,
            Quiz.date_of_quiz <= week_ahead,
        ).all()
        logging.info(f"Found {len(upcoming_quizzes)} upcoming quizzes")

        try:
            advisor = get_advisor()
            ai_enabled = True
            logging.info("AI Advisor initialized successfully")
        except Exception as e:
            logging.error(f"Failed to initialize AI Advisor: {str(e)}")
            ai_enabled = False

        for user in users:
            try:
                user_pref = user.preferences
                if not user_pref:
                    user_pref = UserPreference(
                        user_id=user.id,
                        email_reminders=True,
                        monthly_report=True,
                        last_visit=now,
                        reminder_time=datetime.strptime("18:00", "%H:%M").time(),
                    )
                    db.session.add(user_pref)
                    db.session.commit()
                    db.session.refresh(user)
                    user_pref = user.preferences

                if not user_pref.email_reminders:
                    logging.info(f"User {user.username} has email reminders disabled")
                    continue

                user_reminder_time = user_pref.reminder_time
                if not user_reminder_time:
                    user_reminder_time = datetime.strptime("18:00", "%H:%M").time()

                current_minutes = current_time.hour * 60 + current_time.minute
                reminder_minutes = (
                    user_reminder_time.hour * 60 + user_reminder_time.minute
                )

                if abs(current_minutes - reminder_minutes) > 0:
                    continue

                reminder_stats["users_due_for_reminders"] += 1
                logging.info(
                    f"Processing reminder for user {user.username} at {user_reminder_time.strftime('%H:%M')}"
                )

                should_send_reminder = False
                reminder_reasons = []

                days_since_visit = 0
                if user_pref.last_visit:
                    days_since_visit = (now - user_pref.last_visit).days
                    logging.info(
                        f"User {user.username} last visited {days_since_visit} days ago"
                    )
                    if days_since_visit >= 1:
                        should_send_reminder = True
                        reminder_reasons.append(
                            f"You haven't visited in {days_since_visit} days"
                        )
                        reminder_stats["inactive_users"] += 1
                else:
                    should_send_reminder = True
                    reminder_reasons.append("Welcome back! Check out what's new")
                    reminder_stats["inactive_users"] += 1

                if new_quizzes:
                    should_send_reminder = True
                    reminder_reasons.append(
                        f"{len(new_quizzes)} new quiz(es) have been added"
                    )
                    reminder_stats["new_quiz_alerts"] += 1

                user_attempted_quizzes = (
                    db.session.query(Score.quiz_id).filter_by(user_id=user.id).all()
                )
                attempted_quiz_ids = [q[0] for q in user_attempted_quizzes]

                pending_quizzes = [
                    q for q in upcoming_quizzes if q.id not in attempted_quiz_ids
                ]

                if pending_quizzes:
                    should_send_reminder = True
                    reminder_reasons.append(
                        f"{len(pending_quizzes)} upcoming quiz(es) you haven't attempted yet"
                    )

                ai_advice = None
                if should_send_reminder and ai_enabled:
                    try:

                        user_scores = (
                            Score.query.filter_by(user_id=user.id)
                            .order_by(Score.timestamp.desc())
                            .limit(10)
                            .all()
                        )

                        recent_scores = [s.score for s in user_scores[:5]]
                        avg_score = (
                            sum(s.score for s in user_scores) / len(user_scores)
                            if user_scores
                            else 0
                        )

                        quiz_details = []
                        for score in user_scores:
                            quiz = Quiz.query.get(score.quiz_id)
                            if quiz:
                                subject = (
                                    Subject.query.get(quiz.subject_id)
                                    if quiz.subject_id
                                    else None
                                )
                                quiz_details.append(
                                    {
                                        "quiz_title": quiz.quiz_title,
                                        "score": score.score,
                                        "subject": (
                                            subject.name if subject else "General"
                                        ),
                                        "date": score.timestamp,
                                    }
                                )

                        if len(recent_scores) >= 2:
                            mid = len(recent_scores) // 2
                            first_half = sum(recent_scores[:mid]) / mid
                            second_half = sum(recent_scores[mid:]) / (
                                len(recent_scores) - mid
                            )
                            trend = (
                                "improving"
                                if second_half > first_half
                                else (
                                    "declining"
                                    if second_half < first_half
                                    else "stable"
                                )
                            )
                        else:
                            trend = "insufficient_data"

                        performance_data = {
                            "avg_score": avg_score,
                            "total_quizzes": len(user_scores),
                            "recent_scores": recent_scores,
                            "trend": trend,
                            "days_since_last": days_since_visit,
                            "quiz_details": quiz_details,
                        }

                        user_data = {"name": user.full_name, "email": user.username}

                        logging.info(f"Generating AI advice for {user.username}")
                        ai_advice = advisor.get_student_advice(
                            user_data, performance_data
                        )
                        reminder_stats["ai_suggestions_generated"] += 1
                        logging.info(f"AI advice generated for {user.username}")
                    except Exception as e:
                        logging.error(
                            f"Error generating AI advice for {user.username}: {str(e)}"
                        )
                        ai_advice = None

                logging.info(
                    f"Should send reminder to {user.username}: {should_send_reminder}, reasons: {reminder_reasons}"
                )

                if should_send_reminder:
                    logging.info(f"Sending reminder email to {user.username}")
                    email_sent = send_quiz_reminder_email(
                        user.username,
                        user.full_name,
                        reminder_reasons,
                        new_quizzes,
                        pending_quizzes,
                        ai_advice,
                    )

                    if email_sent:
                        reminder_stats["reminders_sent"] += 1
                        logging.info(
                            f"Reminder sent successfully to {user.username} at their preferred time {user_reminder_time.strftime('%H:%M')}"
                        )

                        user_pref.updated_at = now
                        db.session.commit()
                    else:
                        error_msg = f"Failed to send reminder to {user.username}"
                        logging.error(error_msg)
                        reminder_stats["errors"].append(error_msg)
                else:
                    logging.info(f"No reminder needed for {user.username}")

            except Exception as e:
                error_msg = f"Error processing reminder for user {user.id}: {str(e)}"
                logging.error(error_msg)
                reminder_stats["errors"].append(error_msg)

        if reminder_stats["users_due_for_reminders"] > 0:
            logging.info(f"Daily reminders completed: {reminder_stats}")

        return reminder_stats


@celery_app.task
def send_monthly_reports():
    """Send monthly activity reports to users"""
    app = create_app_context()

    with app.app_context():
        now = datetime.now()

        if now.month == 1:
            prev_month = 12
            prev_year = now.year - 1
        else:
            prev_month = now.month - 1
            prev_year = now.year

        first_day = datetime(prev_year, prev_month, 1)
        last_day_num = monthrange(prev_year, prev_month)[1]
        last_day = datetime(prev_year, prev_month, last_day_num, 23, 59, 59)

        logging.info(f"Generating monthly reports for {first_day.strftime('%B %Y')}")

        users_with_reports = []
        all_users = User.query.filter_by(role="user").all()

        for user in all_users:

            if user.preferences and user.preferences.monthly_report:
                users_with_reports.append(user)

        report_stats = {
            "month": first_day.strftime("%B %Y"),
            "total_users": len(users_with_reports),
            "reports_sent": 0,
            "errors": [],
        }

        for user in users_with_reports:
            try:

                monthly_scores = Score.query.filter(
                    Score.user_id == user.id,
                    Score.timestamp >= first_day,
                    Score.timestamp <= last_day,
                ).all()

                if not monthly_scores:

                    logging.info(
                        f"No activity for user {user.username} in {first_day.strftime('%B %Y')}"
                    )
                    continue

                quiz_ids = [score.quiz_id for score in monthly_scores]
                quizzes = Quiz.query.filter(Quiz.id.in_(quiz_ids)).all()
                quiz_dict = {q.id: q for q in quizzes}

                total_quizzes = len(monthly_scores)
                total_score = sum(score.score for score in monthly_scores)
                average_score = total_score / total_quizzes if total_quizzes > 0 else 0

                quiz_rankings = []
                for score in monthly_scores:
                    all_scores_for_quiz = (
                        Score.query.filter_by(quiz_id=score.quiz_id)
                        .order_by(Score.score.desc())
                        .all()
                    )
                    user_rank = next(
                        (
                            i + 1
                            for i, s in enumerate(all_scores_for_quiz)
                            if s.user_id == user.id
                        ),
                        None,
                    )
                    total_participants = len(all_scores_for_quiz)

                    quiz_rankings.append(
                        {
                            "quiz": quiz_dict.get(score.quiz_id),
                            "score": score.score,
                            "rank": user_rank,
                            "total_participants": total_participants,
                            "date": score.timestamp,
                        }
                    )

                report_data = {
                    "user_name": user.full_name,
                    "month": first_day.strftime("%B %Y"),
                    "total_quizzes": total_quizzes,
                    "total_score": total_score,
                    "average_score": average_score,
                    "quiz_details": quiz_rankings,
                    "best_score": max(score.score for score in monthly_scores),
                    "improvement_trend": calculate_improvement_trend(
                        user.id, first_day, last_day
                    ),
                }

                email_sent = send_monthly_report_email(user.username, report_data)

                if email_sent:
                    report_stats["reports_sent"] += 1
                    logging.info(f"Monthly report sent to {user.username}")
                else:
                    report_stats["errors"].append(
                        f"Failed to send report to {user.username}"
                    )

            except Exception as e:
                error_msg = f"Error generating report for user {user.id}: {str(e)}"
                logging.error(error_msg)
                report_stats["errors"].append(error_msg)

        logging.info(f"Monthly reports completed: {report_stats}")
        return report_stats


@celery_app.task
def test_monthly_reports():
    """Test task to send monthly reports immediately for current month (for testing)"""
    app = create_app_context()

    with app.app_context():
        now = datetime.now()

        current_month = now.month
        current_year = now.year

        first_day = datetime(current_year, current_month, 1)
        last_day_num = monthrange(current_year, current_month)[1]
        last_day = datetime(current_year, current_month, last_day_num, 23, 59, 59)

        logging.info(
            f"TEST: Generating monthly reports for {first_day.strftime('%B %Y')} (current month)"
        )

        users_with_reports = []
        all_users = User.query.filter_by(role="user").all()

        for user in all_users:
            users_with_reports.append(user)

        report_stats = {
            "month": first_day.strftime("%B %Y"),
            "total_users": len(users_with_reports),
            "reports_sent": 0,
            "errors": [],
            "test_mode": True,
        }

        logging.info(f"TEST: Found {len(users_with_reports)} users for testing")

        for user in users_with_reports:
            try:
                monthly_scores = Score.query.filter(
                    Score.user_id == user.id,
                    Score.timestamp >= first_day,
                    Score.timestamp <= last_day,
                ).all()

                if not monthly_scores:
                    logging.info(
                        f"TEST: No activity for user {user.username}, creating mock report"
                    )

                    report_data = {
                        "user_name": user.full_name,
                        "month": first_day.strftime("%B %Y"),
                        "total_quizzes": 0,
                        "total_score": 0,
                        "average_score": 0,
                        "quiz_details": [],
                        "best_score": 0,
                        "improvement_trend": "insufficient_data",
                        "test_mode": True,
                    }

                    email_sent = send_test_monthly_report_email(
                        user.username, report_data
                    )

                    if email_sent:
                        report_stats["reports_sent"] += 1
                        logging.info(
                            f"TEST: Mock monthly report sent to {user.username}"
                        )
                    else:
                        report_stats["errors"].append(
                            f"Failed to send test report to {user.username}"
                        )

                    continue

                quiz_ids = [score.quiz_id for score in monthly_scores]
                quizzes = Quiz.query.filter(Quiz.id.in_(quiz_ids)).all()
                quiz_dict = {q.id: q for q in quizzes}

                total_quizzes = len(monthly_scores)
                total_score = sum(score.score for score in monthly_scores)
                average_score = total_score / total_quizzes if total_quizzes > 0 else 0

                quiz_rankings = []
                for score in monthly_scores:
                    all_scores_for_quiz = (
                        Score.query.filter_by(quiz_id=score.quiz_id)
                        .order_by(Score.score.desc())
                        .all()
                    )
                    user_rank = next(
                        (
                            i + 1
                            for i, s in enumerate(all_scores_for_quiz)
                            if s.user_id == user.id
                        ),
                        None,
                    )
                    total_participants = len(all_scores_for_quiz)

                    quiz_rankings.append(
                        {
                            "quiz": quiz_dict.get(score.quiz_id),
                            "score": score.score,
                            "rank": user_rank,
                            "total_participants": total_participants,
                            "date": score.timestamp,
                        }
                    )

                report_data = {
                    "user_name": user.full_name,
                    "month": first_day.strftime("%B %Y"),
                    "total_quizzes": total_quizzes,
                    "total_score": total_score,
                    "average_score": average_score,
                    "quiz_details": quiz_rankings,
                    "best_score": max(score.score for score in monthly_scores),
                    "improvement_trend": calculate_improvement_trend(
                        user.id, first_day, last_day
                    ),
                    "test_mode": True,
                }

                email_sent = send_monthly_report_email(user.username, report_data)

                if email_sent:
                    report_stats["reports_sent"] += 1
                    logging.info(f"TEST: Monthly report sent to {user.username}")
                else:
                    report_stats["errors"].append(
                        f"Failed to send report to {user.username}"
                    )

            except Exception as e:
                error_msg = f"Error generating test report for user {user.id}: {str(e)}"
                logging.error(error_msg)
                report_stats["errors"].append(error_msg)

        logging.info(f"TEST: Monthly reports completed: {report_stats}")
        return report_stats


def calculate_improvement_trend(user_id, start_date, end_date):
    """Calculate if user is improving over the month"""
    scores = (
        Score.query.filter(
            Score.user_id == user_id,
            Score.timestamp >= start_date,
            Score.timestamp <= end_date,
        )
        .order_by(Score.timestamp.asc())
        .all()
    )

    if len(scores) < 2:
        return "insufficient_data"

    mid_point = len(scores) // 2
    first_half_avg = sum(s.score for s in scores[:mid_point]) / mid_point
    second_half_avg = sum(s.score for s in scores[mid_point:]) / (
        len(scores) - mid_point
    )

    if second_half_avg > first_half_avg + 5:
        return "improving"
    elif second_half_avg < first_half_avg - 5:
        return "declining"
    else:
        return "stable"


def send_quiz_reminder_email(
    email, user_name, reasons, new_quizzes, pending_quizzes, ai_advice=None
):
    """Send quiz reminder email to user with AI-powered suggestions"""
    subject = "🎯 QuizNexus Daily Reminder - Personalized Study Tips Inside!"

    ai_section = ""
    if ai_advice:
        weak_topics = ai_advice.get("weak_topics", [])
        suggestions = ai_advice.get("suggestions", [])
        motivation = ai_advice.get("motivation", "")
        focus_areas = ai_advice.get("focus_areas", [])

        if weak_topics or suggestions:
            ai_section = f"""
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 10px; margin: 20px 0; color: white;">
                <h3 style="margin-top: 0; color: white;">🤖 AI-Powered Study Insights</h3>
                <p style="color: #f0f0f0;">{motivation}</p>
            </div>
            
            {f'''
            <div style="background-color: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; margin: 15px 0; border-radius: 5px;">
                <h4 style="color: #856404; margin-top: 0;">📚 Topics That Need Your Attention:</h4>
                <ul style="color: #856404; margin: 10px 0;">
                    {''.join(f'<li><strong>{topic}</strong></li>' for topic in weak_topics)}
                </ul>
            </div>
            ''' if weak_topics else ''}
            
            {f'''
            <div style="background-color: #d1ecf1; border-left: 4px solid #0c5460; padding: 15px; margin: 15px 0; border-radius: 5px;">
                <h4 style="color: #0c5460; margin-top: 0;">💡 Personalized Study Suggestions:</h4>
                <ol style="color: #0c5460; margin: 10px 0;">
                    {''.join(f'<li style="margin: 8px 0;">{suggestion}</li>' for suggestion in suggestions)}
                </ol>
            </div>
            ''' if suggestions else ''}
            
            {f'''
            <div style="background-color: #f8d7da; border-left: 4px solid #721c24; padding: 15px; margin: 15px 0; border-radius: 5px;">
                <h4 style="color: #721c24; margin-top: 0;">🎯 Focus on These Quizzes:</h4>
                <ul style="color: #721c24; margin: 10px 0;">
                    {''.join(f'<li><strong>{area["quiz"]}</strong> - Score: {area["score"]}% (Subject: {area["subject"]})</li>' for area in focus_areas[:3])}
                </ul>
                <p style="color: #721c24; margin: 5px 0;"><em>Consider reviewing these topics for better understanding.</em></p>
            </div>
            ''' if focus_areas else ''}
            """

    html_body = f"""
    <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }}
                .container {{ max-width: 600px; margin: 0 auto; background-color: white; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; }}
                .content {{ padding: 30px; }}
                .reason {{ background-color: #f8f9fa; padding: 15px; margin: 10px 0; border-left: 4px solid #667eea; border-radius: 5px; }}
                .quiz-list {{ background-color: #e3f2fd; padding: 15px; border-radius: 5px; margin: 15px 0; }}
                .quiz-item {{ background-color: white; padding: 10px; margin: 5px 0; border-radius: 3px; border-left: 3px solid #2196f3; }}
                .button {{ display: inline-block; background-color: #667eea; color: white; padding: 12px 25px; text-decoration: none; border-radius: 5px; margin: 15px 5px; }}
                .footer {{ background-color: #f8f9fa; padding: 20px; text-align: center; color: #666; }}
                .ai-badge {{ background-color: #4CAF50; color: white; padding: 5px 10px; border-radius: 15px; font-size: 0.8em; font-weight: bold; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>📚 QuizNexus Reminder</h1>
                    <p>Stay on track with your learning journey!</p>
                    {f'<span class="ai-badge">✨ AI-Powered Insights</span>' if ai_advice else ''}
                </div>
                <div class="content">
                    <h2>Hi {user_name}! 👋</h2>
                    <p>We wanted to remind you about some exciting opportunities on QuizNexus:</p>
                    
                    {''.join(f'<div class="reason">📌 {reason}</div>' for reason in reasons)}
                    
                    {ai_section}
                    
                    {f'''
                    <h3>🆕 New Quizzes Added:</h3>
                    <div class="quiz-list">
                        {''.join(f'<div class="quiz-item"><strong>{quiz.quiz_title}</strong><br><small>📅 Scheduled for: {quiz.date_of_quiz.strftime("%B %d, %Y")}</small></div>' for quiz in new_quizzes)}
                    </div>
                    ''' if new_quizzes else ''}
                    
                    {f'''
                    <h3>⏰ Upcoming Quizzes You Haven't Attempted:</h3>
                    <div class="quiz-list">
                        {''.join(f'<div class="quiz-item"><strong>{quiz.quiz_title}</strong><br><small>📅 Date: {quiz.date_of_quiz.strftime("%B %d, %Y")} | ⏱️ Duration: {quiz.time_duration} minutes</small></div>' for quiz in pending_quizzes)}
                    </div>
                    ''' if pending_quizzes else ''}
                    
                    <p>Don't let these opportunities slip away! Every quiz is a step towards improving your knowledge and skills.</p>
                    
                    <div style="text-align: center;">
                        <a href="http://localhost:3000/dashboard" class="button">🚀 Visit Dashboard</a>
                        <a href="http://localhost:3000/quizzes" class="button">📝 Browse Quizzes</a>
                    </div>
                </div>
                <div class="footer">
                    <p>💡 <strong>Tip:</strong> Regular practice leads to better results!</p>
                    {f'<p>🤖 <em>Powered by AI to help you succeed</em></p>' if ai_advice else ''}
                    <p><small>You can manage your reminder preferences in your account settings.</small></p>
                </div>
            </div>
        </body>
    </html>
    """

    return send_email(email, subject, html_body, is_html=True)


def send_monthly_report_email(email, report_data):
    """Send monthly activity report email"""
    subject = f"📊 Your {report_data['month']} QuizNexus Activity Report"

    avg_score = report_data["average_score"]
    if avg_score >= 90:
        performance_badge = "🏆 Excellent"
        badge_color = "#ffd700"
    elif avg_score >= 80:
        performance_badge = "🥈 Great"
        badge_color = "#c0c0c0"
    elif avg_score >= 70:
        performance_badge = "🥉 Good"
        badge_color = "#cd7f32"
    else:
        performance_badge = "📈 Keep Improving"
        badge_color = "#87ceeb"

    trend_emoji = {
        "improving": "📈 Improving",
        "declining": "📉 Needs Focus",
        "stable": "📊 Consistent",
        "insufficient_data": "📋 Getting Started",
    }

    html_body = f"""
    <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }}
                .container {{ max-width: 700px; margin: 0 auto; background-color: white; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; }}
                .stats-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px; padding: 20px; }}
                .stat-card {{ background-color: #f8f9fa; padding: 20px; border-radius: 8px; text-align: center; border: 2px solid #e9ecef; }}
                .stat-value {{ font-size: 2em; font-weight: bold; color: #667eea; }}
                .stat-label {{ color: #6c757d; margin-top: 5px; }}
                .performance-badge {{ display: inline-block; background-color: {badge_color}; color: black; padding: 8px 15px; border-radius: 20px; font-weight: bold; margin: 10px; }}
                .quiz-table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
                .quiz-table th, .quiz-table td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
                .quiz-table th {{ background-color: #f8f9fa; font-weight: bold; }}
                .rank-good {{ color: #28a745; font-weight: bold; }}
                .rank-average {{ color: #ffc107; font-weight: bold; }}
                .rank-poor {{ color: #dc3545; font-weight: bold; }}
                .content {{ padding: 30px; }}
                .footer {{ background-color: #f8f9fa; padding: 20px; text-align: center; color: #666; }}
                .trend {{ padding: 15px; background-color: #e3f2fd; border-radius: 5px; margin: 15px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>📊 Monthly Activity Report</h1>
                    <h2>{report_data['month']}</h2>
                    <p>Hi {report_data['user_name']}! Here's your learning summary</p>
                </div>
                
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-value">{report_data['total_quizzes']}</div>
                        <div class="stat-label">Quizzes Taken</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">{report_data['average_score']:.1f}%</div>
                        <div class="stat-label">Average Score</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">{report_data['best_score']}%</div>
                        <div class="stat-label">Best Score</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value">{report_data['total_score']}</div>
                        <div class="stat-label">Total Points</div>
                    </div>
                </div>
                
                <div class="content">
                    <div style="text-align: center;">
                        <div class="performance-badge">{performance_badge}</div>
                    </div>
                    
                    <div class="trend">
                        <strong>📈 Learning Trend:</strong> {trend_emoji.get(report_data['improvement_trend'], '📋 Getting Started')}
                    </div>
                    
                    <h3>📝 Quiz Performance Details</h3>
                    <table class="quiz-table">
                        <thead>
                            <tr>
                                <th>Quiz</th>
                                <th>Score</th>
                                <th>Rank</th>
                                <th>Date</th>
                            </tr>
                        </thead>
                        <tbody>
                            {''.join(f'''
                            <tr>
                                <td>{detail["quiz"].quiz_title if detail["quiz"] else "Unknown Quiz"}</td>
                                <td>{detail["score"]}%</td>
                                <td class="{'rank-good' if detail['rank'] <= detail['total_participants']//3 else 'rank-average' if detail['rank'] <= 2*detail['total_participants']//3 else 'rank-poor'}">
                                    #{detail["rank"]} of {detail["total_participants"]}
                                </td>
                                <td>{detail["date"].strftime("%b %d")}</td>
                            </tr>
                            ''' for detail in report_data['quiz_details'])}
                        </tbody>
                    </table>
                    
                    <div style="background-color: #f8f9fa; padding: 20px; border-radius: 5px; margin: 20px 0;">
                        <h4>💡 Insights & Recommendations:</h4>
                        <ul>
                            {f'<li>🎉 Excellent work! You scored above 90% average. Keep it up!</li>' if avg_score >= 90 else ''}
                            {f'<li>📚 Try to attempt more quizzes to improve your ranking</li>' if report_data['total_quizzes'] < 5 else ''}
                            {f'<li>🎯 Focus on consistency - your performance is trending upward!</li>' if report_data['improvement_trend'] == 'improving' else ''}
                            {f'<li>💪 Challenge yourself with more difficult topics</li>' if avg_score >= 80 else ''}
                            {f'<li>🔄 Review topics where you scored below 70% for better understanding</li>' if any(d['score'] < 70 for d in report_data['quiz_details']) else ''}
                        </ul>
                    </div>
                </div>
                
                <div class="footer">
                    <p>🚀 <strong>Ready for {datetime.now().strftime('%B')}?</strong> New challenges await!</p>
                    <p><small>Keep learning, keep growing! 🌱</small></p>
                </div>
            </div>
        </body>
    </html>
    """

    return send_email(email, subject, html_body, is_html=True)


def send_test_monthly_report_email(email, report_data):
    """Send a test monthly activity report email with mock data"""
    subject = f"🧪 TEST: Your {report_data['month']} QuizNexus Activity Report"

    html_body = f"""
    <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }}
                .container {{ max-width: 700px; margin: 0 auto; background-color: white; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
                .header {{ background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%); color: white; padding: 30px; text-align: center; }}
                .test-banner {{ background-color: #ff4757; color: white; padding: 10px; text-align: center; font-weight: bold; }}
                .content {{ padding: 30px; }}
                .stats-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px; padding: 20px; }}
                .stat-card {{ background-color: #f8f9fa; padding: 20px; border-radius: 8px; text-align: center; border: 2px solid #e9ecef; }}
                .stat-value {{ font-size: 2em; font-weight: bold; color: #ff6b6b; }}
                .stat-label {{ color: #6c757d; margin-top: 5px; }}
                .footer {{ background-color: #f8f9fa; padding: 20px; text-align: center; color: #666; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="test-banner">
                    🧪 THIS IS A TEST EMAIL - Monthly Report Feature Test
                </div>
                <div class="header">
                    <h1>📊 Monthly Activity Report (TEST)</h1>
                    <h2>{report_data['month']}</h2>
                    <p>Hi {report_data['user_name']}! This is a test of the monthly report feature</p>
                </div>
                
                <div class="content">
                    {f'''
                    <div class="stats-grid">
                        <div class="stat-card">
                            <div class="stat-value">{report_data['total_quizzes']}</div>
                            <div class="stat-label">Quizzes Taken</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-value">{report_data['average_score']:.1f}%</div>
                            <div class="stat-label">Average Score</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-value">{report_data['best_score']}%</div>
                            <div class="stat-label">Best Score</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-value">{report_data['total_score']}</div>
                            <div class="stat-label">Total Points</div>
                        </div>
                    </div>
                    ''' if report_data['total_quizzes'] > 0 else '''
                    <div style="text-align: center; padding: 40px; background-color: #f8f9fa; margin: 20px 0; border-radius: 10px;">
                        <h3>📚 No Quiz Activity This Month</h3>
                        <p>This is a test email. In a real report, this would show your quiz performance data.</p>
                        <p><strong>This month:</strong> No quizzes were taken</p>
                        <p><strong>Recommendation:</strong> Try taking a quiz to see how the report looks with real data!</p>
                    </div>
                    '''}
                    
                    <div style="background-color: #fff3cd; border: 1px solid #ffeaa7; border-radius: 5px; padding: 20px; margin: 20px 0;">
                        <h4>🧪 Test Information:</h4>
                        <ul>
                            <li>This is a test of the monthly report email system</li>
                            <li>Real reports will be sent on the 1st of each month</li>
                            <li>The report includes your quiz performance, rankings, and personalized insights</li>
                            <li>You can manage your email preferences in your account settings</li>
                        </ul>
                    </div>
                </div>
                
                <div class="footer">
                    <p>🚀 <strong>Test completed successfully!</strong> The monthly report system is working.</p>
                    <p><small>This was a test email from QuizNexus 🌱</small></p>
                </div>
            </div>
        </body>
    </html>
    """

    return send_email(email, subject, html_body, is_html=True)
