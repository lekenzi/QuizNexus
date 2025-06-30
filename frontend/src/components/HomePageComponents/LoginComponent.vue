<template>
  <div
    class="container d-flex align-items-center justify-content-center min-vh-100"
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
        <button type="submit" class="btn btn-primary w-100">Login</button>
      </form>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import store, { getBaseUrl } from "@/stores/appState";
export default {
  name: "LoginComponent",
  data() {
    return {
      username: "",
      password: "",
    };
  },
  methods: {
    handleLogin() {
      axios
        .post(getBaseUrl() + "/api/login", {
          username: this.username,
          password: this.password,
        })
        .then((response) => {
          console.log("Login successful:", response.data);

          store.commit("setUser", response.data.user);
          store.commit("setIsAuthenticated", true);

          localStorage.setItem("token", response.data.access_token);

          this.$router.push({ name: "home-alias" });
        })
        .catch((error) => {
          console.error("Login failed:", error);
        });
    },
  },
};
</script>
