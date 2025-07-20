import { createRouter, createWebHistory } from "vue-router";
import LoginComponent from "@/components/LandingPage/LoginComponent.vue";
import HomeViewComponent from "@/components/admin/HomeViewComponent.vue";
import RegisterComponent from "@/components/LandingPage/RegisterComponent.vue";
import LandingPageComponent from "@/components/LandingPage/LandingPageComponent.vue";
import QuizesViewComponent from "@/components/admin/QuizesViewComponent.vue";
import SummaryViewComponent from "@/components/summary/SummaryViewComponent.vue";
import QuizSubDisplay from "@/components/fragments/QuizSubDisplay.vue";
import { validateToken } from "@/stores/appState";
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
    meta: { requiresAuth: true },
  },
  {
    path: "/quizzes",
    name: "quizzes",
    component: QuizesViewComponent,
    meta: { requiresAuth: true },
    children: [
      {
        path: "all_quizzes",
        name: "all_quizzes",
        index: true,
        component: QuizSubDisplay,
        props: () => ({
          filter: "all",
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
      // {
      //   path: "quiz/:quiz_id",
      //   name: "quiz_detail",
      //   component: QuizDetailComponent, // Create this component for individual quiz
      //   props: (route) => ({
      //     quiz_id: parseInt(route.params.quiz_id),
      //   }),
      // },
    ],
  },
  {
    name: "summary",
    path: "/summary",
    component: SummaryViewComponent,
    meta: { requiresAuth: true },
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

router.beforeEach(async (to, from, next) => {
  if (to.meta.requiresAuth) {
    const token = localStorage.getItem("token");

    if (!token) {
      next({ name: "login" });
      return;
    }

    try {
      const isValid = await validateToken();

      if (isValid) {
        next();
      } else {
        next({ name: "login" });
      }
    } catch (error) {
      console.error("Token validation failed:", error);

      next({ name: "login" });
    }
  } else if (
    (to.name === "login" || to.name === "register" || to.name === "index") &&
    localStorage.getItem("token")
  ) {
    try {
      const isValid = await validateToken();

      if (isValid) {
        next({ name: "home" });
        return;
      }
    } catch (error) {
      console.error("Token validation failed:", error);
    }
    // next({ name: "home" }); // Uncomment this line if you want to redirect logged-in users from login/register/index to home
  } else {
    next();
  }
});

export default router;
