import { createRouter, createWebHistory } from "vue-router";
import LandingPage from "@/views/LandingPage.vue";
const routes = [
  {
    path: "/login",
    name: "login",
    component: () => import("@/views/LoginPageView.vue"),
  },
  {
    path: "/",
    name: "home-alias",
    component: LandingPage,
  },
  {
    path: "/register",
    name: "register",
    component: () => import("@/views/RegisterPageView.vue"),
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
