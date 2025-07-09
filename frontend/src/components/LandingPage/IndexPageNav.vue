<template>
  <nav class="navbar">
    <div class="navbar-brand">
      <img
        src="./../../../public/img/icon-no-bg.png"
        width="70"
        height="70"
        alt="Brand Logo"
      />
    </div>
    <div class="navbar-links">
      <template v-if="isAuthenticated">
        <router-link to="/home" class="nav-link">Home</router-link>
        <router-link to="/quizzes" class="nav-link">Quizzes</router-link>
        <router-link to="/summary" class="nav-link">Summary</router-link>
        <router-link to="/profile" class="nav-link">Profile</router-link>
        <a href="" class="nav-link" @click.prevent="logout_user">Logout</a>
      </template>
      <template v-else>
        <router-link to="/" class="nav-link">Home</router-link>
        <router-link to="/login" class="nav-link">Login</router-link>
        <router-link to="/register" class="nav-link">Register</router-link>
      </template>
    </div>
  </nav>
</template>

<script>
import { logout, isAuthenticated } from "@/stores/appState";
import { useRouter } from "vue-router";
import { computed } from "vue";

export default {
  name: "IndexPageNav",
  setup() {
    const router = useRouter();

    // Create a computed property that reactively tracks authentication state
    const isAuth = computed(() => isAuthenticated());

    const logout_user = async () => {
      try {
        await logout();
        router.push("/login");
        console.log("User logged out successfully.");
      } catch (error) {
        console.error("Logout failed:", error);
        router.push("/login");
      }
    };

    return {
      isAuthenticated: isAuth,
      logout_user,
    };
  },
};
</script>

<style scoped>
.navbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #f8f9fa;
  padding: 0.5rem 1rem;
  border-bottom: 1px solid #e5e5e5;
}

.navbar-brand img {
  display: block;
}

.navbar-links {
  display: flex;
  gap: 1rem;
}

.nav-link {
  color: #343a40;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s;
}

.nav-link:hover {
  color: #007bff;
}
</style>
