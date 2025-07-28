from flask_caching import Cache
from flask_restful import Api

api = Api()
cache = Cache()


from app.api.resource import (ChapterResources, CheckTokenValidResource,
                              QuestionResources, QuizResources,
                              ReturnUsersScoreBoard, ScoresResource,
                              SubjectResources, TakeQuizResource,
                              TakeResponseResource, TestPostResource,
                              UserDashboardResource, UserLoginResource,
                              UserLogoutResource, UserRegisterResource)
from app.api.resource.admin import (AdminDashboardResource, AdminUsersResource,
                                    ExportUserStatsResource)
from app.api.resource.userpreferences import UserPreferencesResource


api.add_resource(UserLoginResource, "/api/login", endpoint="login")
api.add_resource(UserRegisterResource, "/api/register", endpoint="register")
api.add_resource(UserLogoutResource, "/api/logout", endpoint="logout")
api.add_resource(
    CheckTokenValidResource, "/api/check_token_valid", endpoint="check_token_valid"
)


api.add_resource(SubjectResources, "/api/subjects", endpoint="subjects")
api.add_resource(TestPostResource, "/api/test", endpoint="test")
api.add_resource(ChapterResources, "/api/chapters", endpoint="chapters")
api.add_resource(QuizResources, "/api/quizzes", endpoint="quizzes")
api.add_resource(QuestionResources, "/api/questions", endpoint="questions")



api.add_resource(UserDashboardResource, "/api/dashboard", endpoint="dashboard")
api.add_resource(ScoresResource, "/api/scores", endpoint="scores")
api.add_resource(TakeQuizResource, "/api/fetchQuestions", endpoint="fetchQuestions")
api.add_resource(TakeResponseResource, "/api/takeResponse", endpoint="takeResponse")
api.add_resource(ReturnUsersScoreBoard, "/api/scoreboard", endpoint="scoreboard")



api.add_resource(
    UserPreferencesResource, "/api/user/preferences", endpoint="user_preferences"
)


api.add_resource(
    AdminDashboardResource, "/api/admin/dashboard", endpoint="admin_dashboard"
)
api.add_resource(ExportUserStatsResource, "/api/admin/export", endpoint="admin_export")
api.add_resource(
    AdminUsersResource, "/api/admin/users", endpoint="admin_users_list"
)  
