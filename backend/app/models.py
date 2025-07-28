from datetime import datetime

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


from datetime import datetime, timedelta, timezone

from werkzeug.security import check_password_hash, generate_password_hash


class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    full_name = db.Column(db.String(140))
    qualification = db.Column(db.String(140))
    date_of_birth = db.Column(db.DateTime)
    role = db.Column(db.String(20), default="user")
    scores = db.relationship("Score", backref="user", lazy="dynamic")
    preferences_id = db.Column(
        db.Integer, db.ForeignKey("user_preferences.id"), nullable=True
    )

    def __repr__(self):
        return "<User {}>".format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_hash(self, password):
        return check_password_hash(self.password_hash, password)


class Quiz(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    date_of_quiz = db.Column(
        db.DateTime,
        index=True,
        default=lambda: datetime.now(timezone.utc)
        + timedelta(days=8 if datetime.now(timezone.utc).weekday() == 6 else 7),
    )
    time_of_day = db.Column(db.Time, default=datetime.now().time())

    time_duration = db.Column(db.Integer, default=60, nullable=False)
    remarks = db.Column(db.String(140))
    quiz_title = db.Column(db.String(140))
    chapter_id = db.Column(db.Integer, db.ForeignKey("chapter.id"))
    subject_id = db.Column(db.Integer, db.ForeignKey("subject.id"))
    questions_id = db.relationship("Question", backref="quiz", lazy="dynamic")
    started = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return "<Quiz {}>".format(self.id)


class Question(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(140))
    option1 = db.Column(db.String(140))
    option2 = db.Column(db.String(140))
    option3 = db.Column(db.String(140))
    option4 = db.Column(db.String(140))
    answer = db.Column(db.String(140))
    quiz_id = db.Column(db.Integer, db.ForeignKey("quiz.id"))
    marks = db.Column(db.Integer, default=1)
    chapter_id = db.Column(db.Integer, db.ForeignKey("chapter.id"))
    subject_id = db.Column(db.Integer, db.ForeignKey("subject.id"))

    def __repr__(self):
        return "<Question {}>".format(self.question)


class Score(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    quiz_id = db.Column(db.Integer, db.ForeignKey("quiz.id"))
    score = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return "<Score {}>".format(self.score)


class Subject(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))
    description = db.Column(db.String(140))
    chapters = db.relationship("Chapter", backref="subject", lazy="dynamic")

    def __repr__(self):
        return "<Subject {}>".format(self.name)


class Chapter(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))
    description = db.Column(db.String(140))
    subject_id = db.Column(db.Integer, db.ForeignKey("subject.id"))
    quizzes = db.relationship("Quiz", backref="chapter", lazy="dynamic")

    def __repr__(self):
        return "<Chapter {}>".format(self.name)


class QuizResponse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey("quiz.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    question_id = db.Column(db.Integer, db.ForeignKey("question.id"))
    selected_option = db.Column(db.String(140))
    is_correct = db.Column(db.Boolean)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return "<QuizResponse {}>".format(self.id)


class UserPreference(db.Model):
    __tablename__ = "user_preferences"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    reminder_time = db.Column(
        db.Time, default=datetime.strptime("18:00", "%H:%M").time()
    )
    email_reminders = db.Column(db.Boolean, default=True)
    monthly_report = db.Column(db.Boolean, default=True)
    last_visit = db.Column(db.DateTime, default=lambda: datetime.now().astimezone())
    created_at = db.Column(db.DateTime, default=lambda: datetime.now().astimezone())
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now().astimezone(),
        onupdate=lambda: datetime.now().astimezone(),
    )

    user = db.relationship(
        "User", backref=db.backref("preferences", uselist=False), foreign_keys=[user_id]
    )

    def __repr__(self):
        return "<UserPreference {}>".format(self.id)
