<template>
  <div
    class="container d-flex align-items-center justify-content-center min-vh-10 mt-5"
  >
    <div class="card shadow p-4" style="max-width: 400px; width: 100%">
      <h2 class="text-center mb-4">Login</h2>
      <form @submit.prevent="handleLogin">
        <div class="mb-3">
          <label for="username" class="form-label">Username</label>
          <input
            type="text"
            class="form-control"
            id="username"
            v-model="username"
            required
            placeholder="Username"
          />
        </div>
        <div class="mb-3">
          <label for="password" class="form-label">Password</label>
          <input
            type="password"
            class="form-control"
            id="password"
            v-model="password"
            required
            placeholder="Password"
          />
        </div>
        <button type="submit" class="btn btn-primary w-100" :disabled="loading">
          {{ loading ? "Logging in..." : "Login" }}
        </button>
      </form>
      <div v-if="error" class="alert alert-danger mt-3">
        {{ error }}
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import {
  getBaseUrl,
  setToken,
  setUser,
  setIsAuthenticated,
} from "@/stores/appState";

export default {
  name: "LoginComponent",
  data() {
    return {
      username: "",
      password: "",
      loading: false,
      error: null,
    };
  },
  methods: {
    async handleLogin() {
      this.loading = true;
      this.error = null;

      try {
        const response = await axios.post(getBaseUrl() + "/login", {
          username: this.username,
          password: this.password,
        });

        console.log("Login successful:", response.data);

        // Extract the token and user from response
        const { access_token, user } = response.data;

        // Check if we have both token and user
        if (access_token && user) {
          // Update store using proper helper functions
          setToken(access_token); // This will also handle localStorage
          setUser(user);
          setIsAuthenticated(true);

          this.$router.push({ name: "home" });
        } else {
          throw new Error("Invalid response format - missing token or user");
        }
      } catch (error) {
        console.error("Login failed:", error);

        // Clear any partial state
        setToken("");
        setUser({ id: null, username: "", role: "" });
        setIsAuthenticated(false);

        // Show error to user
        this.error =
          error.response?.data?.message ||
          "Login failed. Please check your credentials.";
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>
