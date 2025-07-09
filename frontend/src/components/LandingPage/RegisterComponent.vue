<template>
  <div
    class="container d-flex align-items-center justify-content-center min-vh-10 mt-5"
  >
    <div class="card shadow p-4" style="max-width: 400px; width: 100%">
      <h2 class="text-center mb-4">Register New User</h2>
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
          <label for="fullname" class="form-label">Full name</label>
          <input
            type="text"
            class="form-control"
            id="fullname"
            v-model="fullname"
            required
            placeholder="Full name"
          />
        </div>
        <div class="mb-3">
          <label for="dateOfBirth" class="form-label">Date of Birth</label>
          <input
            type="date"
            class="form-control"
            id="dateOfBirth"
            v-model="dateOfBirth"
            required
            format="YYYY-MM-DD"
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
            placeholder=" Enter password"
          />
        </div>
        <div class="mb-3">
          <label for="confirmPassword" class="form-label"
            >Re-enter Password</label
          >
          <input
            type="password"
            class="form-control"
            id="confirmPassword"
            v-model="confirmPassword"
            required
            placeholder="Re-enter password"
          />
        </div>
        <button type="submit" class="btn btn-primary w-100">Register</button>
      </form>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import { getBaseUrl } from "@/stores/appState";
// check if the password and confirm password match
export default {
  name: "RegisterComponent",
  data() {
    return {
      username: "",
      password: "",
      confirmPassword: "",
      fullname: "",
      dateOfBirth: "",
    };
  },
  methods: {
    handleLogin() {
      if (this.password !== this.confirmPassword) {
        alert("Passwords do not match!");
        // make the input fields red
        document.getElementById("password").style.borderColor = "red";
        document.getElementById("confirmPassword").style.borderColor = "red";
        return;
      }
      // console.log("Registration data:", {
      //   username: this.username,
      //   password: this.password,
      //   confirmPassword: this.confirmPassword,
      //   fullname: this.fullname,
      //   dateOfBirth: this.dateOfBirth,
      // });

      axios
        .post(getBaseUrl() + "/register", {
          username: this.username,
          password: this.password,
          full_name: this.fullname,
          date_of_birth: this.dateOfBirth,
        })
        .then((response) => {
          console.log("Registration successful:", response.data);
          alert("Registration successful! You can now log in.");
          this.$router.push("/");
        })
        .catch((error) => {
          console.error("Registration failed:", error);
          alert("Registration failed. Please try again.");
        });
    },
  },
};
</script>
