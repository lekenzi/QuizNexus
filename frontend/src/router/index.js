import { createRouter, createWebHistory } from "vue-router";
import LoginComponent from "@/components/LandingPage/LoginComponent.vue";
import HomeViewComponent from "@/components/admin/HomeViewComponent.vue";
import RegisterComponent from "@/components/LandingPage/RegisterComponent.vue";
import LandingPageComponent from "@/components/LandingPage/LandingPageComponent.vue";
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
    props: (route) => ({
      returnStore: route.query.returnStore || null,
    }),
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

router.beforeEach((to, _, next) => {
  const isAuthenticated = localStorage.getItem("token") !== null;

  if (to.name !== "login" && to.name !== "register" && !isAuthenticated) {
    next({ name: "login" });
  } else {
    next();
  }
});

// router.beforeEach((to, from, next) => {
//   if (to.matched.length === 0) {
//     next({ name: "index" });
//   } else {
//     next();
//   }
// });

export default router;
