import email
import logging
import select
import time
from datetime import datetime, timedelta, timezone
from operator import ge

import jwt
from app.api.validators import (
    UserLoginParser,
    UserRegisterParser,
    add_chapter_parser,
    add_quiz_parser,
    add_subject_parser,
    checkTokenParser,
    questions_add_parser,
    take_response_parser,
)
from app.cache import CacheManager, cache_result, invalidate_cache
from app.middleware import jwt_auth_required, optional_jwt_auth, role_required
from app.models import (
    Chapter,
    Question,
    Quiz,
    QuizResponse,
    Score,
    Subject,
    User,
    UserPreference,
    db,
)
from flask import make_response, request
from flask_jwt_extended import (
    create_access_token,
    get_jwt,
    get_jwt_identity,
    jwt_required,
)
from flask_restful import Resource
from werkzeug.security import generate_password_hash


class CheckTokenValidResource(Resource):
    @jwt_auth_required
    def post(self):
        args = checkTokenParser.parse_args()
        jwt_claims = get_jwt()

        user = User.query.get(get_jwt_identity())
        if not user:
            return {"message": "User not found"}, 404

        user_preferences = UserPreference.query.filter_by(user_id=user.id).first()
        if user_preferences:
            user_preferences.last_visit = datetime.now().astimezone()
            db.session.commit()
        else:
            new_preferences = UserPreference(user_id=user.id)
            new_preferences.last_visit = datetime.now().astimezone()
            db.session.add(new_preferences)
            db.session.commit()

        return {"message": "Token is valid", "claims": jwt_claims}, 200

    @jwt_auth_required
    def get(self):
        """returns role of the user

        Keyword arguments:
        argument -- description
        Return: return_description
        """
        jwt_claims = get_jwt()
        return {"role": jwt_claims.get("role")}, 200


class UserLoginResource(Resource):
    @jwt_required()
    def get(self):
        return {"message": "This is a user login resource"}, 200

    def post(self):
        args = UserLoginParser.parse_args()
        username = args["username"]
        password = args["password"]

        user = User.query.filter_by(username=username).first()

        if not user:
            return {"message": "Invalid username or password"}, 401
        else:
            if not user.check_hash(password):
                return {"message": "Invalid username or password"}, 401
            else:

                access_token = create_access_token(
                    identity=str(user.id), additional_claims={"role": user.role}
                )

        user_preferences = UserPreference.query.filter_by(user_id=user.id).first()
        if user_preferences:
            user_preferences.last_visit = datetime.now().astimezone()
            db.session.commit()
        else:
            new_preferences = UserPreference(user_id=user.id)
            new_preferences.last_visit = datetime.now().astimezone()
            db.session.add(new_preferences)
            db.session.commit()
        return make_response(
            {
                "message": "Login successful",
                "access_token": access_token,
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "isAuthenticated": True,
                    "role": user.role,
                },
            },
            200,
        )


class UserRegisterResource(Resource):
    def post(self):
        args = UserRegisterParser.parse_args()
        username = args["username"]
        password = args["password"]
        full_name = args["full_name"]
        date_of_birth = args["date_of_birth"]

        print(
            f"""s
                {username}
                {password}
                {full_name}
                {date_of_birth}
        """
        )

        user = User.query.filter_by(username=username).first()

        if user:
            return {"message": "Username already exists"}, 400

        new_user = User()
        new_user.username = username
        new_user.full_name = full_name
        new_user.date_of_birth = datetime.strptime(date_of_birth, "%Y-%m-%d")
        new_user.password_hash = generate_password_hash(password)
        new_user.qualification = "Student"
        new_user.role = "user"

        db.session.add(new_user)
        db.session.commit()

        access_token = create_access_token(
            identity=str(new_user.id), additional_claims={"role": new_user.role}
        )

        return make_response(
            {
                "message": "User registered successfully",
                "access_token": access_token,
                "user": {
                    "id": new_user.id,
                    "username": new_user.username,
                    "isAuthenticated": True,
                    "role": new_user.role,
                },
            },
            201,
        )


class UserLogoutResource(Resource):
    @jwt_auth_required
    def post(self):
        try:
            jwt_claims = get_jwt()
            jti = jwt_claims.get("jti")
            current_user_id = get_jwt_identity()
            logging.info(f"User {current_user_id} logging out, JWT ID: {jti}")
            return {
                "message": "User logged out successfully",
                "logged_out": True,
                "user_id": current_user_id,
            }, 200
        except Exception as e:
            logging.error(f"Logout error: {str(e)}")
            return {
                "message": "An error occurred while logging out",
                "error": str(e),
            }, 500


class SubjectResources(Resource):
    @jwt_auth_required
    @optional_jwt_auth
    @cache_result()
    def get(self):
        subjects = Subject.query.all()
        subjects_data = []

        for subject in subjects:
            quiz_count = Quiz.query.filter_by(subject_id=subject.id).count()
            subjects_data.append(
                {
                    "subject_id": subject.id,
                    "subject_name": subject.name,
                    "subject_description": subject.description,
                    "number_of_quizzes": quiz_count,
                }
            )

        return {"subjects": subjects_data}, 200

    @jwt_auth_required
    @role_required(["admin"])
    def patch(self):
        args = add_subject_parser.parse_args()
        subject_name = args["name"]
        subject_description = args["description"]

        if not subject_name or not subject_description:
            return {"message": "Subject name and description are required"}, 400

        existing_subject = Subject.query.filter_by(name=subject_name).first()
        if existing_subject:
            return {"message": "Subject already exists"}, 400

        new_subject = Subject()
        new_subject.name = subject_name
        new_subject.description = subject_description

        db.session.add(new_subject)
        db.session.commit()

        CacheManager.invalidate_subjects_cache()

        return {
            "message": "Subject created successfully",
            "subject_id": new_subject.id,
        }, 201

    @jwt_auth_required
    @role_required(["admin"])
    def post(self):
        try:
            logging.info("POST request received to /api/home")
            logging.info(f"Request content type: {request.content_type}")
            logging.info(f"Request data: {request.get_data(as_text=True)}")

            if not request.is_json:
                return {"message": "Request must be JSON"}, 400

            json_data = request.get_json()
            logging.info(f"JSON data: {json_data}")

            if not json_data:
                return {"message": "No JSON data provided"}, 400

            subject_name = json_data.get("name")
            subject_description = json_data.get("description")

            if not subject_name:
                logging.warning("Missing 'name' field in request")
                return {"message": "Subject name is required"}, 400
            if not subject_description:
                logging.warning("Missing 'discription' field in request")
                return {"message": "Subject description is required"}, 400

            existing_subject = Subject.query.filter_by(name=subject_name).first()
            if existing_subject:
                return {"message": "Subject already exists"}, 400

            new_subject = Subject()
            new_subject.name = subject_name
            new_subject.description = subject_description

            db.session.add(new_subject)
            db.session.commit()

            return {"message": "Subject created successfully"}, 201

        except Exception as e:
            logging.error(f"Error creating subject: {str(e)}")
            logging.error(f"Exception type: {type(e).__name__}")
            return {"message": f"Error creating subject: {str(e)}"}, 500

    @jwt_auth_required
    @role_required(["admin"])
    def delete(self):
        args = add_subject_parser.parse_args()
        subject_name = args["name"]
        existing_subject = Subject.query.filter_by(name=subject_name).first()

        if not existing_subject:
            return {"message": "Subject not found"}, 404

        db.session.delete(existing_subject)
        db.session.commit()

        CacheManager.invalidate_subjects_cache()

        return {"message": "Subject deleted successfully"}, 200


class TestPostResource(Resource):
    @jwt_auth_required
    def post(self):
        return {"message": "POST test successful", "data": "Hello from POST"}, 200

    def get(self):
        return {"message": "GET test successful", "data": "Hello from GET"}, 200


class ChapterResources(Resource):
    @jwt_auth_required
    @cache_result()
    def get(self):
        subject_id = request.args.get("subject_id", type=int)
        if not subject_id:
            return {"message": "Missing subject_id in query parameters"}, 400

        cache_key = f"chapters:subject:{subject_id}"
        cached_data = CacheManager.get_cached_data(cache_key)
        if cached_data:
            return cached_data, 200

        chapters = Chapter.query.filter_by(subject_id=subject_id).all()
        if not chapters:
            return {"message": "No chapters found for the given subject"}, 404

        chapters_data = []
        for chapter in chapters:
            quiz_count = Quiz.query.filter_by(chapter_id=chapter.id).count()
            chapters_data.append(
                {
                    "id": chapter.id,
                    "name": chapter.name,
                    "description": chapter.description,
                    "number_of_quizzes": quiz_count,
                }
            )

        result = {"data": {"subject_id": subject_id, "chapters": chapters_data}}

        CacheManager.set_cached_data(cache_key, result, 300)

        return result, 200

    @jwt_auth_required
    @role_required(["admin"])
    def post(self):
        args = add_chapter_parser.parse_args()
        chapter_name = args["name"]
        chapter_description = args["description"]
        subject_id = args["subject_id"]

        if not chapter_name or not chapter_description:
            return {"message": "Chapter name and description are required"}, 400

        subject = Subject.query.get(subject_id)
        if not subject:
            return {"message": "Subject not found"}, 404

        new_chapter = Chapter(
            name=chapter_name, description=chapter_description, subject_id=subject_id
        )
        db.session.add(new_chapter)
        db.session.commit()

        invalidate_cache(f"chapters:subject:{subject_id}*")

        return {
            "message": "Chapter created successfully",
            "chapter_id": new_chapter.id,
        }, 201

    @jwt_auth_required
    @role_required(["admin"])
    def patch(self):
        args = request.get_json()
        chapter_id = args.get("id")
        chapter_name = args.get("name")
        chapter_description = args.get("description")

        chapter = Chapter.query.get(chapter_id)
        if not chapter:
            return {"message": "Chapter not found"}, 404

        if chapter_name:
            chapter.name = chapter_name
        if chapter_description:
            chapter.description = chapter_description

        db.session.commit()

        return {"message": "Chapter updated successfully"}, 200

    @jwt_auth_required
    @role_required(["admin"])
    def delete(self):
        args = request.get_json()
        chapter_id = args.get("id")
        chapter = Chapter.query.get(chapter_id)
        if not chapter:
            return {"message": "Chapter not found"}, 404

        db.session.delete(chapter)
        db.session.commit()

        return {"message": "Chapter deleted successfully"}, 200


class QuizResources(Resource):
    @jwt_auth_required
    @role_required(["admin"])
    @cache_result()
    def get(self):
        """
        Return quizzes based on subject_id. If subject_id is 9999, return all quizzes.
        """
        subject_id = request.args.get("subject_id", type=int)

        cache_key = f"quizzes:subject:{subject_id if subject_id else 'all'}"
        cached_data = CacheManager.get_cached_data(cache_key)
        if cached_data:
            return cached_data, 200

        if subject_id is None or subject_id == 99999:
            quizzes = Quiz.query.all()
        else:
            quizzes = Quiz.query.filter_by(subject_id=subject_id).all()

        quizzes_data = []

        for quiz in quizzes:
            subject = Subject.query.get(quiz.subject_id)
            chapter = Chapter.query.get(quiz.chapter_id)

            quizzes_data.append(
                {
                    "quiz_id": quiz.id,
                    "quiz_title": quiz.quiz_title,
                    "subject_id": subject.id if subject else None,
                    "subject_name": subject.name if subject else None,
                    "chapter_id": chapter.id if chapter else None,
                    "chapter_name": chapter.name if chapter else None,
                    "number_of_questions": Question.query.filter_by(
                        quiz_id=quiz.id
                    ).count(),
                }
            )

        result = {"quizzes": quizzes_data}
        CacheManager.set_cached_data(cache_key, result, 180)

        return result, 200

    @jwt_auth_required
    @role_required(["admin"])
    def post(self):
        """
        Create a new quiz with the following JSON structure:
        """
        args = add_quiz_parser.parse_args()

        logging.info(f"Received args for quiz creation: {args}")
        quiz_title = args["title"]
        time_duration = args["timeduration"]
        time_of_day_str = args.get("time_of_day")
        if time_of_day_str:
            try:
                time_of_day = datetime.strptime(time_of_day_str, "%H:%M:%S").time()
            except ValueError:
                logging.warning(f"Invalid time_of_day format: {time_of_day_str}")
                return {"message": "Invalid time_of_day format. Use HH:MM."}, 400
        else:
            logging.info("time_of_day not provided, defaulting to None")
            time_of_day = None
        chapter_id = args["chapter_id"]
        subject_id = args["subject_id"]
        date = args["date"]
        remarks = args["remarks"]

        if not quiz_title or not time_duration or not chapter_id or not subject_id:
            return {
                "message": "Quiz title, time duration, chapter ID, and subject ID are required"
            }, 400

        chapter = Chapter.query.get(chapter_id)
        if not chapter:
            return {"message": "Chapter not found"}, 404

        subject = Subject.query.get(subject_id)
        if not subject:
            return {"message": "Subject not found"}, 404

        try:
            date_of_quiz = datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            return {"message": "Invalid date format. Use YYYY-MM-DD."}, 400

        new_quiz = Quiz(
            quiz_title=quiz_title,
            time_duration=time_duration,
            time_of_day=time_of_day,
            chapter_id=chapter_id,
            subject_id=subject_id,
            date_of_quiz=date_of_quiz,
            remarks=remarks,
        )

        db.session.add(new_quiz)
        db.session.commit()

        return {"message": "Quiz created successfully", "quiz_id": new_quiz.id}, 201

    @jwt_auth_required
    @role_required(["admin"])
    def delete(self):
        """
        Delete a quiz by its ID.
        Expects a JSON body with the quiz_id to delete.
        """
        if not request.is_json:
            return {"message": "Request must be JSON"}, 400

        args = request.get_json()
        quiz_id = args.get("quiz_id")

        if not quiz_id:
            return {"message": "Quiz ID is required"}, 400

        quiz = Quiz.query.get(quiz_id)
        if not quiz:
            return {"message": "Quiz not found"}, 404

        db.session.delete(quiz)
        db.session.commit()

        return {"message": "Quiz deleted successfully"}, 200

    @jwt_auth_required
    @role_required(["admin"])
    def patch(self):
        args = request.get_json()
        quiz_id = args.get("id")
        quiz_title = args.get("title")
        time_duration = args.get("time_duration")
        time_of_day_str = args.get("time_of_day")
        chapter_id = args.get("chapter_id")
        subject_id = args.get("subject_id")
        date = args.get("date")
        remarks = args.get("remarks")

        quiz = Quiz.query.get(quiz_id)
        if not quiz:
            return {"message": "Quiz not found"}, 404

        if quiz_title:
            quiz.quiz_title = quiz_title
        if time_duration:
            quiz.time_duration = time_duration
        if time_of_day_str:
            try:

                quiz.time_of_day = datetime.strptime(time_of_day_str, "%H:%M:%S").time()
            except ValueError:
                try:

                    quiz.time_of_day = datetime.strptime(
                        time_of_day_str, "%H:%M"
                    ).time()
                except ValueError:
                    return {
                        "message": "Invalid time format. Use HH:MM:SS or HH:MM."
                    }, 400
        if chapter_id:
            quiz.chapter_id = chapter_id
        if subject_id:
            quiz.subject_id = subject_id
        if date:
            try:
                quiz.date_of_quiz = datetime.strptime(date, "%Y-%m-%d").date()
            except ValueError:
                return {"message": "Invalid date format. Use YYYY-MM-DD."}, 400
        if remarks:
            quiz.remarks = remarks

        db.session.commit()

        return {"message": "Quiz updated successfully"}, 200


class QuestionResources(Resource):
    @jwt_auth_required
    @role_required(["admin"])
    def get(self):
        quiz_id = request.args.get("quiz_id", type=int)
        if not quiz_id:
            return {"message": "Missing quiz_id in query parameters"}, 400

        questions = Question.query.filter_by(quiz_id=quiz_id).all()
        if not questions:
            return {"data": {"quiz_id": quiz_id, "questions": []}}, 200

        questions_data = [
            {
                "id": question.id,
                "question": question.question,
                "options": [
                    question.option1,
                    question.option2,
                    question.option3,
                    question.option4,
                ],
                "answer": question.answer,
                "marks": question.marks,
            }
            for question in questions
        ]

        return {"data": {"quiz_id": quiz_id, "questions": questions_data}}, 200

    @jwt_auth_required
    @role_required(["admin"])
    def post(self):
        args = questions_add_parser.parse_args()
        question_text = args["question"]
        option1 = args["option1"]
        option2 = args["option2"]
        option3 = args["option3"]
        option4 = args["option4"]
        answer = args["answer"]
        marks = args["marks"]
        quiz_id = args["quiz_id"]
        chapter_id = args.get("chapter_id")
        subject_id = args.get("subject_id")

        if not question_text or not option1 or not option2 or not answer or not quiz_id:
            return {"message": "All fields are required"}, 400

        quiz = Quiz.query.get(quiz_id)
        if not quiz:
            return {"message": "Quiz not found"}, 404

        new_question = Question(
            question=question_text,
            option1=option1,
            option2=option2,
            option3=option3,
            option4=option4,
            answer=answer,
            marks=marks,
            quiz_id=quiz_id,
            chapter_id=chapter_id,
            subject_id=subject_id,
        )

        db.session.add(new_question)
        db.session.commit()

        return {
            "message": "Question added successfully",
            "question_id": new_question.id,
        }, 201

    @jwt_auth_required
    @role_required(["admin"])
    def delete(self):
        args = request.get_json()
        question_id = args.get("question_id")

        if not question_id:
            return {"message": "Question ID is required"}, 400

        question = Question.query.get(question_id)
        if not question:
            return {"message": "Question not found"}, 404

        db.session.delete(question)
        db.session.commit()

        return {"message": "Question deleted successfully"}, 200

    @jwt_auth_required
    @role_required(["admin"])
    def patch(self):
        args = request.get_json()
        question_id = args.get("id")
        question_text = args.get("question")
        option1 = args.get("option1")
        option2 = args.get("option2")
        option3 = args.get("option3")
        option4 = args.get("option4")
        answer = args.get("answer")
        marks = args.get("marks")

        question = Question.query.get(question_id)
        if not question:
            return {"message": "Question not found"}, 404

        if question_text:
            question.question = question_text
        if option1:
            question.option1 = option1
        if option2:
            question.option2 = option2
        if option3:
            question.option3 = option3
        if option4:
            question.option4 = option4
        if answer:
            question.answer = answer
        if marks is not None:
            question.marks = marks

        db.session.commit()

        return {"message": "Question updated successfully"}, 200


class UserDashboardResource(Resource):
    @jwt_auth_required
    @role_required(["user"])
    def get(self):
        """
        Return quizzes categorized into two parts: upcoming quizzes and past quizzes.
        """
        user_id = get_jwt_identity()

        cached_dashboard = CacheManager.get_user_quizzes(user_id)
        if cached_dashboard:
            return cached_dashboard, 200

        current_datetime = datetime.now()

        quizzes = Quiz.query.order_by(Quiz.date_of_quiz.asc()).all()
        upcoming_quizzes = []
        past_quizzes = []

        for quiz in quizzes:
            quiz_start_datetime = (
                datetime.combine(quiz.date_of_quiz, quiz.time_of_day)
                if quiz.time_of_day
                else datetime.combine(quiz.date_of_quiz, datetime.min.time())
            )
            quiz_end_datetime = quiz_start_datetime + timedelta(
                minutes=quiz.time_duration
            )
            quiz_data = {
                "id": quiz.id,
                "title": quiz.quiz_title,
                "date_of_quiz": quiz.date_of_quiz.isoformat(),
                "duration": quiz.time_duration,
                "chapter": quiz.chapter_id,
                "subject": quiz.subject_id,
                "time_of_day": (
                    quiz.time_of_day.isoformat() if quiz.time_of_day else None
                ),
            }
            if quiz_end_datetime > current_datetime:
                upcoming_quizzes.append(quiz_data)
            else:
                past_quizzes.append(quiz_data)

        result = {
            "upcoming_quizzes": upcoming_quizzes,
            "past_quizzes": past_quizzes,
        }

        CacheManager.set_user_quizzes(user_id, result, 180)

        return result, 200


class ScoresResource(Resource):
    @jwt_auth_required
    @role_required(["user"])
    @cache_result()
    def get(self):
        """return all the scores of the user"""
        user_id = get_jwt_identity()

        scores = Score.query.filter_by(user_id=user_id).all()
        scores_data = []
        for score in scores:
            quiz = Quiz.query.get(score.quiz_id)
            subject = Subject.query.get(quiz.subject_id) if quiz else None
            chapter = Chapter.query.get(quiz.chapter_id) if quiz else None

            scores_data.append(
                {
                    "id": score.id,
                    "quiz_id": score.quiz_id,
                    "quiz_title": quiz.quiz_title if quiz else None,
                    "subject_name": subject.name if subject else None,
                    "chapter_name": chapter.name if chapter else None,
                    "score": score.score,
                    "timestamp": score.timestamp.isoformat(),
                }
            )
        return {"data": scores_data}, 200


class TakeQuizResource(Resource):
    def get(self):
        """return the quiz_id, number of questions, time duration, and time of day for the quiz, question_id, question, options, marks
        Expects a query parameter `quiz_id`.
        Keyword arguments:
        argument -- description
        Return: return_description
        """

        quiz_id = request.args.get("quiz_id")
        if not quiz_id:
            return {"message": "quiz_id is required"}, 400

        quiz = Quiz.query.get(quiz_id)
        if not quiz:
            return {"message": "Quiz not found"}, 404

        subject = Subject.query.get(quiz.subject_id)
        chapter = Chapter.query.get(quiz.chapter_id)

        questions = Question.query.filter_by(quiz_id=quiz_id).all()
        questions_data = []
        for question in questions:
            questions_data.append(
                {
                    "id": question.id,
                    "question": question.question,
                    "options": [
                        question.option1,
                        question.option2,
                        question.option3,
                        question.option4,
                    ],
                    "marks": question.marks,
                }
            )

        return {
            "data": {
                "quiz_id": quiz.id,
                "quiz_title": quiz.quiz_title,
                "number_of_questions": len(questions),
                "time_duration": quiz.time_duration,
                "time_of_day": (
                    quiz.time_of_day.isoformat() if quiz.time_of_day else None
                ),
                "subject_name": subject.name if subject else None,
                "chapter_name": chapter.name if chapter else None,
                "questions": questions_data,
            }
        }, 200


class TakeResponseResource(Resource):
    @jwt_auth_required
    @role_required(["user"])
    def post(self):
        """
        Submit the quiz responses and calculate the score.
        Expects a JSON body with quiz_id, question_id, and selected_option.
        """
        try:

            user_id = get_jwt_identity()
            if not user_id:
                return {"message": "Authentication required"}, 401

            args = take_response_parser.parse_args()
            quiz_id = args["quiz_id"]
            question_id = args["question_id"]
            selected_option = args["selected_option"]

            quiz = Quiz.query.get(quiz_id)
            if not quiz:
                return {"message": "Quiz not found"}, 404

            question = Question.query.get(question_id)
            if not question:
                return {"message": "Question not found"}, 404

            existing_response = QuizResponse.query.filter_by(
                quiz_id=quiz_id, user_id=user_id, question_id=question_id
            ).first()

            if existing_response:

                existing_response.selected_option = selected_option
                existing_response.is_correct = question.answer == selected_option
                existing_response.timestamp = datetime.now()
                response_id = existing_response.id
            else:

                quiz_response = QuizResponse(
                    quiz_id=quiz_id,
                    user_id=user_id,
                    question_id=question_id,
                    selected_option=selected_option,
                    is_correct=(question.answer == selected_option),
                    timestamp=datetime.now(),
                )
                db.session.add(quiz_response)
                response_id = quiz_response.id

            db.session.commit()

            return {
                "message": "Response recorded successfully",
                "quiz_response_id": response_id,
                "status": "success",
            }, 201

        except Exception as e:
            db.session.rollback()
            logging.error(f"Error recording response: {str(e)}")
            return {"message": "Error recording response", "error": str(e)}, 500


class ReturnUsersScoreBoard(Resource):
    @jwt_auth_required
    @role_required(["user"])
    def get(self):
        """
        Return the user's score board with detailed scores for each quiz.
        """
        user_id = get_jwt_identity()
        if not user_id:
            return {"message": "Authentication required"}, 401

        scores = Score.query.filter_by(user_id=user_id).all()
        if not scores:
            return {"message": "No scores found for this user"}, 404

        scores_data = []
        for score in scores:
            quiz = Quiz.query.get(score.quiz_id)
            subject = Subject.query.get(quiz.subject_id) if quiz else None
            chapter = Chapter.query.get(quiz.chapter_id) if quiz else None

            scores_data.append(
                {
                    "id": score.id,
                    "quiz_id": score.quiz_id,
                    "quiz_title": quiz.quiz_title if quiz else None,
                    "subject_name": subject.name if subject else None,
                    "chapter_name": chapter.name if chapter else None,
                    "score": score.score,
                    "timestamp": score.timestamp.isoformat(),
                }
            )

        return {"scores": scores_data}, 200


class MyQuizStats(Resource):
    @jwt_auth_required
    @role_required(["user"])
    def get(self):
        """
        Return comprehensive user quiz statistics including performance metrics, subject breakdown, and achievements.
        """
        user_id = get_jwt_identity()
        if not user_id:
            return {"message": "Authentication required"}, 401

        scores = Score.query.filter_by(user_id=user_id).all()

        total_quizzes_taken = len(scores)
        if total_quizzes_taken == 0:
            return {
                "message": "No quiz activity found",
                "stats": {
                    "total_quizzes_taken": 0,
                    "average_score": 0,
                    "best_score": 0,
                    "total_points": 0,
                    "subject_breakdown": [],
                    "performance_trend": "no_data",
                    "achievements": [],
                },
            }, 200

        total_points = sum(score.score for score in scores)
        average_score = round(total_points / total_quizzes_taken, 2)
        best_score = max(score.score for score in scores)
        worst_score = min(score.score for score in scores)

        total_correct_answers = QuizResponse.query.filter_by(
            user_id=user_id, is_correct=True
        ).count()

        total_questions_attempted = QuizResponse.query.filter_by(
            user_id=user_id
        ).count()

        accuracy_percentage = round(
            (
                (total_correct_answers / total_questions_attempted * 100)
                if total_questions_attempted > 0
                else 0
            ),
            2,
        )

        subject_stats = {}
        quiz_ids = [score.quiz_id for score in scores]
        quizzes = Quiz.query.filter(Quiz.id.in_(quiz_ids)).all()

        for quiz in quizzes:
            subject = Subject.query.get(quiz.subject_id)
            if subject:
                subject_name = subject.name
                user_scores_for_subject = [
                    s.score for s in scores if s.quiz_id == quiz.id
                ]

                if subject_name not in subject_stats:
                    subject_stats[subject_name] = {
                        "subject_id": subject.id,
                        "quizzes_taken": 0,
                        "total_score": 0,
                        "best_score": 0,
                        "worst_score": 100,
                    }

                for score_val in user_scores_for_subject:
                    subject_stats[subject_name]["quizzes_taken"] += 1
                    subject_stats[subject_name]["total_score"] += score_val
                    subject_stats[subject_name]["best_score"] = max(
                        subject_stats[subject_name]["best_score"], score_val
                    )
                    subject_stats[subject_name]["worst_score"] = min(
                        subject_stats[subject_name]["worst_score"], score_val
                    )

        subject_breakdown = []
        for subject_name, stats in subject_stats.items():
            avg_score = round(stats["total_score"] / stats["quizzes_taken"], 2)
            subject_breakdown.append(
                {
                    "subject_name": subject_name,
                    "subject_id": stats["subject_id"],
                    "quizzes_taken": stats["quizzes_taken"],
                    "average_score": avg_score,
                    "best_score": stats["best_score"],
                    "worst_score": (
                        stats["worst_score"]
                        if stats["worst_score"] != 100
                        else stats["best_score"]
                    ),
                }
            )

        subject_breakdown.sort(key=lambda x: x["quizzes_taken"], reverse=True)

        recent_scores = sorted(scores, key=lambda x: x.timestamp, reverse=True)
        performance_trend = "stable"

        if len(recent_scores) >= 6:
            recent_5_avg = sum(s.score for s in recent_scores[:5]) / 5
            previous_5_avg = sum(s.score for s in recent_scores[5:10]) / min(
                5, len(recent_scores[5:])
            )

            if recent_5_avg > previous_5_avg + 5:
                performance_trend = "improving"
            elif recent_5_avg < previous_5_avg - 5:
                performance_trend = "declining"

        achievements = []

        perfect_scores = [s for s in scores if s.score == 100]
        if perfect_scores:
            achievements.append(
                {
                    "type": "perfect_score",
                    "title": "Perfect Score!",
                    "description": f"Achieved perfect score {len(perfect_scores)} time(s)",
                    "icon": "🏆",
                }
            )

        if average_score >= 80:
            achievements.append(
                {
                    "type": "high_performer",
                    "title": "High Performer",
                    "description": f"Maintaining {average_score}% average score",
                    "icon": "⭐",
                }
            )

        if total_quizzes_taken >= 10:
            achievements.append(
                {
                    "type": "quiz_master",
                    "title": "Quiz Master",
                    "description": f"Completed {total_quizzes_taken} quizzes",
                    "icon": "🎓",
                }
            )

        if len(recent_scores) >= 5:
            recent_5_scores = [s.score for s in recent_scores[:5]]
            if all(score >= 70 for score in recent_5_scores):
                achievements.append(
                    {
                        "type": "consistent",
                        "title": "Consistent Performer",
                        "description": "No score below 70% in recent quizzes",
                        "icon": "📈",
                    }
                )

        for subject in subject_breakdown:
            if subject["quizzes_taken"] >= 3 and subject["average_score"] >= 80:
                achievements.append(
                    {
                        "type": "subject_specialist",
                        "title": f"{subject['subject_name']} Specialist",
                        "description": f"{subject['average_score']}% average in {subject['subject_name']}",
                        "icon": "🏅",
                    }
                )

        all_users_avg_scores = []
        all_users = User.query.filter_by(role="user").all()
        for user in all_users:
            user_scores = Score.query.filter_by(user_id=user.id).all()
            if user_scores:
                user_avg = sum(s.score for s in user_scores) / len(user_scores)
                all_users_avg_scores.append(user_avg)

        if all_users_avg_scores:
            better_than_count = sum(
                1 for avg in all_users_avg_scores if average_score > avg
            )
            percentile_rank = round(
                (better_than_count / len(all_users_avg_scores)) * 100, 1
            )
        else:
            percentile_rank = 0

        thirty_days_ago = datetime.now() - timedelta(days=30)
        recent_activity = (
            Score.query.filter_by(user_id=user_id)
            .filter(Score.timestamp >= thirty_days_ago)
            .count()
        )

        return {
            "stats": {
                "total_quizzes_taken": total_quizzes_taken,
                "total_points": total_points,
                "average_score": average_score,
                "best_score": best_score,
                "worst_score": worst_score,
                "total_correct_answers": total_correct_answers,
                "total_questions_attempted": total_questions_attempted,
                "accuracy_percentage": accuracy_percentage,
                "percentile_rank": percentile_rank,
                "recent_activity_30d": recent_activity,
                "performance_trend": performance_trend,
                "subject_breakdown": subject_breakdown,
                "achievements": achievements,
                "activity_summary": {
                    "most_active_subject": (
                        subject_breakdown[0]["subject_name"]
                        if subject_breakdown
                        else "None"
                    ),
                    "subjects_attempted": len(subject_breakdown),
                    "best_subject": (
                        max(subject_breakdown, key=lambda x: x["average_score"])[
                            "subject_name"
                        ]
                        if subject_breakdown
                        else "None"
                    ),
                    "best_subject_average": (
                        max(subject_breakdown, key=lambda x: x["average_score"])[
                            "average_score"
                        ]
                        if subject_breakdown
                        else 0
                    ),
                },
            }
        }, 200
