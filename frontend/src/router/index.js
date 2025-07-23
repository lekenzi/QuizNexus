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
      roleComponents: {
        admin: HomeViewComponent,
        user: UserDashBoardView,
      },
    },
  },
  {
    path: "/quizzes",
    name: "quizzes",
    component: QuizesViewComponent,
    meta: {
      requiresAuth: true,
      roleComponents: { admin: QuizesViewComponent },
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
        meta: {
          roleComponents: {
            admin: QuizSubDisplay,
          },
        },
      },
      {
        path: "subject/:subject_id",
        name: "quizzes_by_subject",
        component: QuizSubDisplay,
        props: (route) => ({
          subject_id: parseInt(route.params.subject_id),
        }),
        meta: {
          roleComponents: {
            admin: QuizSubDisplay,
          },
        },
      },
    ],
  },
  {
    name: "summary",
    path: "/summary",
    component: SummaryViewComponent,
    meta: {
      requiresAuth: true,
      roleComponents: { admin: SummaryViewComponent },
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
    redirect: { name: "index" },
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

      if (!isValid) {
        next({ name: "login" });
        return;
      }

      if (to.meta.requiredRole) {
        const userRole = await getUserrole();
        console.log("User role:", userRole);

        if (userRole !== to.meta.requiredRole) {
          next({ name: "unauthorized" });
          return;
        }
      }

      if (to.meta.roleComponents) {
        const userRole = await getUserrole();

        if (!to.meta.roleComponents[userRole]) {
          next({ name: "unauthorized" });
          return;
        }
      }

      next();
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
  }

  next();
});

export default router;
