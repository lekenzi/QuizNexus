import email
import logging
from datetime import datetime

import jwt
from app.api.validators import (
    UserLoginParser,
    UserRegisterParser,
    add_chapter_parser,
    add_quiz_parser,
    add_subject_parser,
    checkTokenParser,
    questions_add_parser,
)
from app.middleware import jwt_auth_required, optional_jwt_auth, role_required
from app.models import Chapter, Question, Quiz, Score, Subject, User, db
from celery import chain
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
        new_user.qualification = "Student"  # Default qualification
        new_user.role = "user"  # Default role

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
            current_user_id = get_jwt_identity()  # now a string like "1"
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
    def get(self):
        subjects = Subject.query.all()
        subjects_data = []

        for subject in subjects:
            subjects_data.append(
                {
                    "subject_id": subject.id,
                    "subject_name": subject.name,
                    "subject_description": subject.description,
                }
            )

        return {"subjects": subjects_data}, 200

    @jwt_auth_required
    @role_required(["admin"])
    def post(self):
        try:
            logging.info("POST request received to /api/home")
            logging.info(f"Request content type: {request.content_type}")
            logging.info(f"Request data: {request.get_data(as_text=True)}")

            # Check if request has JSON data
            if not request.is_json:
                return {"message": "Request must be JSON"}, 400

            # Get JSON data
            json_data = request.get_json()
            logging.info(f"JSON data: {json_data}")

            if not json_data:
                return {"message": "No JSON data provided"}, 400

            # Extract fields
            subject_name = json_data.get("name")
            subject_description = json_data.get("description")

            # Check if required fields are present
            if not subject_name:
                logging.warning("Missing 'name' field in request")
                return {"message": "Subject name is required"}, 400
            if not subject_description:
                logging.warning("Missing 'discription' field in request")
                return {"message": "Subject description is required"}, 400

            # Check if subject already exists
            existing_subject = Subject.query.filter_by(name=subject_name).first()
            if existing_subject:
                return {"message": "Subject already exists"}, 400

            # Create new subject
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

    # @jwt_auth_required
    # @role_required(["admin"])
    # def patch(self):
    #     args = add_subject_parser.parse_args()
    #     subject_name = args["name"]
    #     subject_description = args["discription"]
    #     existing_subject = Subject.query.filter_by(name=subject_name).first()

    #     if not existing_subject:
    #         return {"message": "Subject not found"}, 404

    #     existing_subject.description = subject_description
    #     db.session.commit()

    #     return {"message": "Subject updated successfully"}, 200

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

        return {"message": "Subject deleted successfully"}, 200


class TestPostResource(Resource):
    @jwt_auth_required
    def post(self):
        return {"message": "POST test successful", "data": "Hello from POST"}, 200

    def get(self):
        return {"message": "GET test successful", "data": "Hello from GET"}, 200


class ChapterResources(Resource):
    @jwt_auth_required
    def get(self):
        subject_id = request.args.get("subject_id", type=int)
        if not subject_id:
            return {"message": "Missing subject_id in query parameters"}, 400

        chapters = Chapter.query.filter_by(subject_id=subject_id).all()
        if not chapters:
            return {"message": "No chapters found for the given subject"}, 404

        chapters_data = [
            {"id": chapter.id, "name": chapter.name} for chapter in chapters
        ]

        return {"data": {"subject_id": subject_id, "chapters": chapters_data}}, 200

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

        return {
            "message": "Chapter created successfully",
            "chapter_id": new_chapter.id,
        }, 201

    @jwt_auth_required
    @role_required(["admin"])
    def patch(self, chapter_id):
        args = request.get_json()
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
    def delete(self, chapter_id):
        chapter = Chapter.query.get(chapter_id)
        if not chapter:
            return {"message": "Chapter not found"}, 404

        db.session.delete(chapter)
        db.session.commit()

        return {"message": "Chapter deleted successfully"}, 200


class QuizResources(Resource):

    @jwt_auth_required
    @role_required(["admin"])
    def get(self):
        """
        Return quizzes based on subject_id. If subject_id is 9999, return all quizzes.
        {
            quizzes: [
                {
                    quiz_id: 1,
                    quiz_title: "Quiz 1",
                    subject_id: 1,
                    subject_name: "Mathematics",
                    chapter_id: 1,
                    chapter_name: "Algebra",
                    number_of_questions: 10,
                },
                ...
            ]
        }
        """
        subject_id = request.args.get("subject_id", type=int)

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

        return {"quizzes": quizzes_data}, 200

    @jwt_auth_required
    @role_required(["admin"])
    def post(self):
        """
        Create a new quiz with the following JSON structure:
            {title: 'hello', remarks: 'jhvjhv', timeduration: '1', date: '2025-07-15', subject_id: 2, …}
            chapter_id
            :
            2
            date
            :
            "2025-07-15"
            remarks
            :
            "jhvjhv"
            subject_id
            :
            2
            timeduration
            :
            "1"
            title
            :
            "hello"
        """
        args = add_quiz_parser.parse_args()
        # log args for debugging
        logging.info(f"Received args for quiz creation: {args}")
        quiz_title = args["title"]
        time_duration = args["timeduration"]
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

        # Convert date string to Python datetime object
        try:
            date_of_quiz = datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            return {"message": "Invalid date format. Use YYYY-MM-DD."}, 400

        new_quiz = Quiz(
            quiz_title=quiz_title,
            time_duration=time_duration,
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


class UserDashboardResource(Resource):
    @jwt_auth_required
    @role_required(["user"])
    def get(self):
        """
        return all the quizzes from the time the user started
        """
        quizzes = Quiz.query.order_by(Quiz.date_of_quiz.asc()).all()
        quizzes_data = []
        for quiz in quizzes:
            quizzes_data.append(
                {
                    "id": quiz.id,
                    "title": quiz.quiz_title,
                    "date_of_quiz": quiz.date_of_quiz.isoformat(),  # Convert datetime to ISO format
                    "duration": quiz.time_duration,
                    "chapter": quiz.chapter_id,
                    "subject": quiz.subject_id,
                }
            )
        return {"data": quizzes_data}, 200


class ScoresResource(Resource):
    @jwt_auth_required
    @role_required(["user"])
    def get(self):
        """
        return all the scores of the user
        """
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
        """return the quiz_id, number of questions, and time duration for the quiz, question_id, question, options, answer, marks
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
                "number_of_questions": len(questions),
                "time_duration": quiz.time_duration,
                "questions": questions_data,
            }
        }, 200
