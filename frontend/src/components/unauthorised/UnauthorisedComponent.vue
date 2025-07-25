<template>
  <div class="container text-center mt-5">
    <div class="alert alert-danger" role="alert">
      <h1 class="display-4">403 - Unauthorized</h1>
      <p class="lead">{{ message }}</p>
      <hr />
      <p>
        If you believe this is a mistake, please contact the administrator.
        Role: {{ role }}
      </p>
      <div>
        <a
          v-if="role === 'user'"
          href="/dashboard"
          class="btn btn-primary mt-3"
        >
          Go to Dashboard
        </a>
        <a
          v-else-if="role === 'admin'"
          href="/home"
          class="btn btn-primary mt-3"
        >
          Go to Home
        </a>
        <a v-else href="/login" class="btn btn-primary mt-3"> Login </a>
      </div>
    </div>
  </div>
</template>

<script>
import { getUserrole } from "@/stores/appState";
export default {
  name: "UnauthorisedComponent",
  data() {
    return {
      role: "",
      message: "You are not authorised to view this page.",
    };
  },
  mounted() {
    const user = this.getUser();
    if (user.role === "admin") {
      this.$router.push({ name: "home" });
    } else if (user.role === "user") {
      this.$router.push({ name: "user_dashboard" });
    }
  },
  methods: {
    async getUser() {
      const role = await getUserrole();
      this.role = role;
      return { role };
    },
  },
};
</script>

<style scoped>
.container {
  max-width: 600px;
}
</style>
