import { createRouter, createWebHistory } from "vue-router";
import LoginComponent from "@/components/LandingPage/LoginComponent.vue";
import HomeViewComponent from "@/components/admin/HomeViewComponent.vue";
import RegisterComponent from "@/components/LandingPage/RegisterComponent.vue";
import LandingPageComponent from "@/components/LandingPage/LandingPageComponent.vue";
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
  } else {
    next();
  }
});

export default router;
