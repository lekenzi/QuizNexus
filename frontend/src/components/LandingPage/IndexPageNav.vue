<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <div class="container-fluid">
      <a class="navbar-brand" href="#">
        <img
          src="./../../../public/img/icon-no-bg.png"
          width="70"
          height="70"
          alt="Brand Logo"
        />
      </a>
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarNav"
        aria-controls="navbarNav"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav ms-auto">
          <template v-if="isAuthenticated">
            <li class="nav-item">
              <router-link
                to="/home"
                class="nav-link"
                :class="{ active: isActive('/home') }"
              >
                Home
              </router-link>
            </li>
            <li class="nav-item">
              <router-link
                to="/quizzes"
                class="nav-link"
                :class="{ active: isActive('/quizzes') }"
              >
                Quizzes
              </router-link>
            </li>
            <li class="nav-item">
              <router-link
                to="/summary"
                class="nav-link"
                :class="{ active: isActive('/summary') }"
              >
                Summary
              </router-link>
            </li>
            <!-- <li class="nav-item">
              <router-link
                to="/profile"
                class="nav-link"
                :class="{ active: isActive('/profile') }"
              >
                Profile
              </router-link>
            </li> -->
            <li class="nav-item danger-bg">
              <a href="" class="nav-link" @click.prevent="logout_user">
                Logout
              </a>
            </li>
          </template>
          <template v-else>
            <li class="nav-item">
              <router-link
                to="/"
                class="nav-link"
                :class="{ active: isActive('/') }"
              >
                Home
              </router-link>
            </li>
            <li class="nav-item">
              <router-link
                to="/login"
                class="nav-link"
                :class="{ active: isActive('/login') }"
              >
                Login
              </router-link>
            </li>
            <li class="nav-item">
              <router-link
                to="/register"
                class="nav-link"
                :class="{ active: isActive('/register') }"
              >
                Register
              </router-link>
            </li>
          </template>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
import { logout, isAuthenticated } from "@/stores/appState";
import { useRouter, useRoute } from "vue-router";
import { computed } from "vue";

export default {
  name: "IndexPageNav",
  setup() {
    const router = useRouter();
    const route = useRoute();

    // Create a computed property that reactively tracks authentication state
    const isAuth = computed(() => isAuthenticated());

    const logout_user = async () => {
      try {
        await logout();
        router.push("/login");
      } catch (error) {
        console.error("Logout failed:", error);
        router.push("/login");
      }
    };

    const isActive = (path) => route.path === path;

    return {
      isAuthenticated: isAuth,
      logout_user,
      isActive,
    };
  },
};
</script>

<style scoped>
.navbar {
  box-shadow: rgba(0, 0, 0, 0.15) 0px 15px 25px,
    rgba(0, 0, 0, 0.05) 0px 5px 10px;
}
.nav-link.active {
  font-weight: bold;
  color: #007bff !important;
}
body {
  padding-top: 200px;
}
</style>
