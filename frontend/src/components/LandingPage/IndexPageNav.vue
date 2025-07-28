<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <div class="container-fluid">
      <a class="navbar-brand" href="/">
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
          <template v-if="isTokenValidating">
            <li class="nav-item">
              <span class="nav-link">
                <i class="fas fa-spinner fa-spin"></i> Validating...
              </span>
            </li>
          </template>
          <template v-else-if="isAuth && userRole === 'admin'">
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
            <!-- <li class="nav-item">
              <router-link
                to="/summary"
                class="nav-link"
                :class="{ active: isActive('/summary') }"
              >
                Summary
              </router-link>
            </li> -->
            <li class="nav-item">
              <router-link
                to="/admin/dashboard"
                class="nav-link"
                :class="{ active: isActive('/admin/dashboard') }"
              >
                Dashboard
              </router-link>
            </li>
            <li class="nav-item">
              <router-link
                to="/admin/users"
                class="nav-link"
                :class="{ active: isActive('/admin/users') }"
              >
                Users
              </router-link>
            </li>
            <li class="nav-item">
              <router-link
                to="/admin/export"
                class="nav-link"
                :class="{ active: isActive('/admin/export') }"
              >
                Export
              </router-link>
            </li>
            <li class="nav-item danger-bg">
              <a href="" class="nav-link" @click.prevent="logout_user">
                Logout
              </a>
            </li>
          </template>

          <!-- Navbar for user role -->
          <template v-else-if="isAuth && userRole === 'user'">
            <li class="nav-item">
              <router-link
                to="/dashboard"
                class="nav-link"
                :class="{ active: isActive('/dashboard') }"
              >
                Dashboard
              </router-link>
            </li>
            <li class="nav-item">
              <router-link
                to="/scores"
                class="nav-link"
                :class="{ active: isActive('/scores') }"
              >
                My Scores
              </router-link>
            </li>
            <li class="nav-item">
              <router-link
                to="/mystats"
                class="nav-link"
                :class="{ active: isActive('/mystats') }"
              >
                My Stats
              </router-link>
            </li>
            <li class="nav-item">
              <router-link
                to="/mypreferences"
                class="nav-link"
                :class="{ active: isActive('/mypreferences') }"
              >
                My Preferences
              </router-link>
            </li>
            <li class="nav-item danger-bg">
              <a href="" class="nav-link" @click.prevent="logout_user">
                Logout
              </a>
            </li>
          </template>

          <!-- Navbar for unauthenticated users -->
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
import { ref, onMounted, watch } from "vue";
import {
  logout,
  validateToken,
  isAuthenticated,
  getUserrole,
} from "@/stores/appState";
import { useRouter, useRoute } from "vue-router";

export default {
  name: "IndexPageNav",
  setup() {
    const router = useRouter();
    const route = useRoute();

    const isAuth = ref(false);
    const userRole = ref("");
    const isTokenValidating = ref(false);

    const checkAuthStatus = async () => {
      try {
        isTokenValidating.value = true;

        const isValidToken = await validateToken();
        if (isValidToken) {
          isAuth.value = await isAuthenticated();
          userRole.value = await getUserrole();
        } else {
          isAuth.value = false;
          userRole.value = "";
        }
      } catch (error) {
        console.error("Error validating token:", error);
        isAuth.value = false;
        userRole.value = "";
      } finally {
        isTokenValidating.value = false;
      }
    };

    onMounted(async () => {
      await checkAuthStatus();
    });

    watch(
      () => route.path,
      async () => {
        await checkAuthStatus(); // Validate token on route change
      }
    );

    const logout_user = async () => {
      try {
        await logout();
        isAuth.value = false;
        userRole.value = "";
        router.push("/login");
      } catch (error) {
        console.error("Logout failed:", error);
        isAuth.value = false;
        userRole.value = "";
        router.push("/login");
      }
    };

    const isActive = (path) => route.path === path;

    return {
      isAuth,
      userRole,
      isTokenValidating,
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
</style>
