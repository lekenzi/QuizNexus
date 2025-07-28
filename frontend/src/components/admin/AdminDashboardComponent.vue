<template>
  <div class="container mt-4">
    <h1 class="text-primary mb-4">Admin Dashboard</h1>

    <div v-if="loading" class="text-center my-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p class="mt-2">Loading dashboard statistics...</p>
    </div>

    <div v-else-if="error" class="alert alert-danger">
      {{ error }}
    </div>

    <div v-else class="row">
      <div class="col-md-4 mb-4">
        <div class="card bg-primary text-white h-100">
          <div class="card-body text-center">
            <h5 class="card-title">Total Users</h5>
            <h2 class="display-4">{{ stats.total_users }}</h2>
            <p class="card-text">
              <span class="badge bg-light text-dark">
                {{ stats.new_users_30d }} new in last 30 days
              </span>
            </p>
          </div>
        </div>
      </div>

      <div class="col-md-4 mb-4">
        <div class="card bg-success text-white h-100">
          <div class="card-body text-center">
            <h5 class="card-title">Total Quizzes</h5>
            <h2 class="display-4">{{ stats.total_quizzes }}</h2>
            <p class="card-text">
              <span class="badge bg-light text-dark">
                {{ stats.recent_quizzes_7d }} new in last 7 days
              </span>
            </p>
          </div>
        </div>
      </div>

      <div class="col-md-4 mb-4">
        <div class="card bg-info text-white h-100">
          <div class="card-body text-center">
            <h5 class="card-title">Quiz Attempts</h5>
            <h2 class="display-4">{{ stats.total_attempts }}</h2>
            <p class="card-text">
              <span class="badge bg-light text-dark">
                {{ stats.average_score }}% average score
              </span>
            </p>
          </div>
        </div>
      </div>

      <div class="col-12 mt-4">
        <div class="card">
          <div class="card-header bg-light">
            <h5 class="mb-0">Quick Actions</h5>
          </div>
          <div class="card-body">
            <div class="row">
              <div class="col-md-4">
                <router-link
                  to="/admin/users"
                  class="btn btn-outline-primary w-100 mb-2"
                >
                  <i class="fas fa-users me-2"></i> Manage Users
                </router-link>
              </div>
              <div class="col-md-4">
                <router-link
                  to="/admin/export"
                  class="btn btn-outline-success w-100 mb-2"
                >
                  <i class="fas fa-file-export me-2"></i> Export Data
                </router-link>
              </div>
              <div class="col-md-4">
                <router-link
                  to="/quizzes"
                  class="btn btn-outline-info w-100 mb-2"
                >
                  <i class="fas fa-question-circle me-2"></i> Manage Quizzes
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { fetchAdminDashboardStats } from "@/stores/appState";

export default {
  name: "AdminDashboardComponent",
  data() {
    return {
      stats: {
        total_users: 0,
        total_quizzes: 0,
        total_attempts: 0,
        new_users_30d: 0,
        recent_quizzes_7d: 0,
        average_score: 0,
      },
      loading: true,
      error: null,
    };
  },
  mounted() {
    this.fetchDashboardStats();
  },
  methods: {
    async fetchDashboardStats() {
      this.loading = true;
      this.error = null;

      try {
        const stats = await fetchAdminDashboardStats();
        this.stats = stats;
      } catch (error) {
        this.error =
          "Failed to load dashboard statistics. Please try again later.";
        console.error("Dashboard stats error:", error);
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped>
.card {
  transition: transform 0.3s ease;
}
.card:hover {
  transform: translateY(-5px);
}
</style>
