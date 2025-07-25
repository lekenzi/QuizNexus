import { createRouter, createWebHistory } from "vue-router";
import LoginComponent from "@/components/LandingPage/LoginComponent.vue";
import HomeViewComponent from "@/components/admin/HomeViewComponent.vue";
import RegisterComponent from "@/components/LandingPage/RegisterComponent.vue";
import LandingPageComponent from "@/components/LandingPage/LandingPageComponent.vue";
import QuizesViewComponent from "@/components/admin/QuizesViewComponent.vue";
import SummaryViewComponent from "@/components/summary/SummaryViewComponent.vue";
import QuizSubDisplay from "@/components/fragments/QuizSubDisplay.vue";
import { validateToken, getUserrole } from "@/stores/appState";
import UserDashBoardView from "@/components/users/UserDashBoardView.vue";
import UnauthorisedComponent from "@/components/unauthorised/UnauthorisedComponent.vue";
import ScoresView from "@/components/users/ScoresView.vue";
import QuizPage from "@/components/users/QuizPage.vue";
import DisplayQuestion from "@/components/users/userdashboardfragments/DisplayQuestion.vue";

const routes = [
  {
    path: "/login",
    name: "login",
    component: LoginComponent,
  },
  {
    path: "/",
    name: "index",
    component: LandingPageComponent,
  },
  {
    path: "/register",
    name: "register",
    component: RegisterComponent,
  },
  {
    path: "/home",
    name: "home",
    component: HomeViewComponent,
    meta: {
      requiresAuth: true,
      requiresRole: "admin",
    },
  },
  {
    path: "/quizzes",
    name: "quizzes",
    component: QuizesViewComponent,
    meta: {
      requiresAuth: true,
      requiresRole: "admin",
    },
    redirect: { name: "all_quizzes" },
    children: [
      {
        path: "",
        name: "all_quizzes",
        component: QuizSubDisplay,
        props: () => ({
          subject_id: null,
        }),
      },
      {
        path: "subject/:subject_id",
        name: "quizzes_by_subject",
        component: QuizSubDisplay,
        props: (route) => ({
          subject_id: parseInt(route.params.subject_id),
        }),
      },
    ],
  },
  {
    name: "summary",
    path: "/summary",
    component: SummaryViewComponent,
    meta: {
      requiresAuth: true,
      requiresRole: "admin",
    },
  },
  {
    path: "/unauthorized",
    name: "unauthorized",
    component: () => UnauthorisedComponent,
  },
  {
    path: "/:pathMatch(.*)*",
    name: "notfound",
    redirect: { name: "unauth" },
  },
  // all the routes below are for for the users
  {
    path: "/dashboard",
    name: "user_dashboard",
    component: UserDashBoardView,
    meta: {
      requiresAuth: true,
      requiresRole: "user",
    },
  },
  {
    path: "/scores",
    name: "user_scores",
    component: ScoresView,
    meta: {
      requiresAuth: true,
      requiresRole: "user",
    },
  },
  // this route breaks out of the main flow of the app as it is used to display the quizs
  {
    path: "/quizzes/:quiz_id",
    name: "quiz_page",
    component: QuizPage,
    props: (route) => ({
      quiz_id: parseInt(route.params.quiz_id),
    }),
    children: [
      {
        path: "question/:questionIndex",
        name: "quiz_question",
        component: DisplayQuestion,
        props: (route) => {
          const quiz = route.params.quiz;
          const questionIndex = parseInt(route.params.questionIndex);
          return {
            question: quiz?.questions?.[questionIndex] || null,
          };
        },
      },
    ],
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

router.beforeEach(async (to, from, next) => {
  try {
    if (to.meta.requiresAuth) {
      const token = localStorage.getItem("token");

      if (!token) {
        return next({ name: "login" });
      }

      const isValid = await validateToken();

      if (!isValid) {
        return next({ name: "login" });
      }

      // Check for role-based access
      const userRole = await getUserrole();
      console.log("User role:", userRole);
      if (to.meta.requiresRole && to.meta.requiresRole !== userRole) {
        return next({ name: "unauthorized" });
      }
    } else if (
      (to.name === "login" || to.name === "register" || to.name === "index") &&
      localStorage.getItem("token")
    ) {
      const isValid = await validateToken();

      if (isValid) {
        return next({ name: "home" });
      }
    }
  } catch (error) {
    console.error("Token validation failed:", error);
    if (to.meta.requiresAuth) {
      return next({ name: "login" });
    }
  }

  next();
});

export default router;
