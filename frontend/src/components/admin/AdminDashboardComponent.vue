<template>
  <div class="container-fluid mt-4 bg-light rounded shadow-sm">
    <div class="row">
      <div class="col-12">
        <div
          class="d-flex flex-column justify-content-between align-items-center mb-4"
        >
          <h1 class="text-primary mb-0">
            <i class="fas fa-chart-line me-2"></i>Admin Dashboard
          </h1>
          <button
            @click="refreshStats"
            class="btn btn-primary"
            :disabled="loading"
          >
            <i class="fas fa-sync-alt me-1" :class="{ 'fa-spin': loading }"></i>
            Refresh
          </button>
        </div>
      </div>
    </div>

    <div v-if="loading" class="text-center my-5">
      <div
        class="spinner-border text-primary"
        role="status"
        style="width: 3rem; height: 3rem"
      >
        <span class="visually-hidden">Loading...</span>
      </div>
      <p class="mt-3 text-muted">
        Loading comprehensive dashboard statistics...
      </p>
    </div>

    <div v-else-if="error" class="alert alert-danger mx-3">
      <i class="fas fa-exclamation-triangle me-2"></i>
      {{ error }}
    </div>

    <div v-else>
      <div class="row mb-4">
        <div class="col-lg-3 col-md-6 mb-3">
          <div class="card bg-gradient-primary text-white h-100 shadow-sm">
            <div class="card-body">
              <div class="d-flex justify-content-between">
                <div>
                  <h6 class="card-title text-white-50">Total Users</h6>
                  <h2 class="mb-0">{{ stats.overview?.total_users || 0 }}</h2>
                  <small class="text-white-75">
                    <i class="fas fa-arrow-up me-1"></i>
                    {{ stats.overview?.new_users_30d || 0 }} new this month
                  </small>
                </div>
                <div class="align-self-center">
                  <i class="fas fa-users fa-2x text-white-50"></i>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="col-lg-3 col-md-6 mb-3">
          <div class="card bg-gradient-success text-white h-100 shadow-sm">
            <div class="card-body">
              <div class="d-flex justify-content-between">
                <div>
                  <h6 class="card-title text-white-50">Total Quizzes</h6>
                  <h2 class="mb-0">{{ stats.overview?.total_quizzes || 0 }}</h2>
                  <small class="text-white-75">
                    <i class="fas fa-plus me-1"></i>
                    {{ stats.overview?.recent_quizzes_7d || 0 }} added this week
                  </small>
                </div>
                <div class="align-self-center">
                  <i class="fas fa-clipboard-list fa-2x text-white-50"></i>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="col-lg-3 col-md-6 mb-3">
          <div class="card bg-gradient-info text-white h-100 shadow-sm">
            <div class="card-body">
              <div class="d-flex justify-content-between">
                <div>
                  <h6 class="card-title text-white-50">Quiz Attempts</h6>
                  <h2 class="mb-0">
                    {{ stats.overview?.total_attempts || 0 }}
                  </h2>
                  <small class="text-white-75">
                    <i class="fas fa-chart-line me-1"></i>
                    {{ stats.performance?.average_score || 0 }}% avg score
                  </small>
                </div>
                <div class="align-self-center">
                  <i class="fas fa-pen-alt fa-2x text-white-50"></i>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="col-lg-3 col-md-6 mb-3">
          <div class="card bg-gradient-warning text-white h-100 shadow-sm">
            <div class="card-body">
              <div class="d-flex justify-content-between">
                <div>
                  <h6 class="card-title text-white-50">Active Users</h6>
                  <h2 class="mb-0">
                    {{ stats.performance?.active_users_30d || 0 }}
                  </h2>
                  <small class="text-white-75">
                    <i class="fas fa-percentage me-1"></i>
                    {{ stats.performance?.engagement_rate || 0 }}% engagement
                  </small>
                </div>
                <div class="align-self-center">
                  <i class="fas fa-user-check fa-2x text-white-50"></i>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="row mb-4">
        <div class="col-lg-8 mb-3">
          <div class="card shadow-sm">
            <div class="card-header bg-white">
              <h5 class="card-title mb-0">
                <i class="fas fa-chart-bar me-2 text-primary"></i>
                Subject Performance Overview
              </h5>
            </div>
            <div class="card-body">
              <div
                v-if="stats.subject_breakdown?.length"
                class="table-responsive"
              >
                <table class="table table-hover">
                  <thead class="table-light">
                    <tr>
                      <th>Subject</th>
                      <th>Total Quizzes</th>
                      <th>Total Attempts</th>
                      <th>Average Score</th>
                      <th>Performance</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr
                      v-for="subject in stats.subject_breakdown"
                      :key="subject.subject_name"
                    >
                      <td class="fw-medium">{{ subject.subject_name }}</td>
                      <td>{{ subject.total_quizzes }}</td>
                      <td>{{ subject.total_attempts }}</td>
                      <td>{{ subject.average_score }}%</td>
                      <td>
                        <div class="progress" style="height: 8px">
                          <div
                            class="progress-bar"
                            :class="getPerformanceColor(subject.average_score)"
                            :style="{ width: subject.average_score + '%' }"
                          ></div>
                        </div>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <div v-else class="text-center py-4 text-muted">
                <i class="fas fa-chart-bar fa-3x mb-3"></i>
                <p>No subject data available yet</p>
              </div>
            </div>
          </div>
        </div>

        <div class="col-lg-4 mb-3">
          <div class="card shadow-sm h-100">
            <div class="card-header bg-white">
              <h5 class="card-title mb-0">
                <i class="fas fa-cogs me-2 text-success"></i>
                System Metrics
              </h5>
            </div>
            <div class="card-body">
              <div class="mb-3">
                <div
                  class="d-flex justify-content-between align-items-center mb-1"
                >
                  <span class="text-muted">Subjects</span>
                  <span class="fw-bold">{{
                    stats.overview?.total_subjects || 0
                  }}</span>
                </div>
                <div
                  class="d-flex justify-content-between align-items-center mb-1"
                >
                  <span class="text-muted">Chapters</span>
                  <span class="fw-bold">{{
                    stats.overview?.total_chapters || 0
                  }}</span>
                </div>
                <div
                  class="d-flex justify-content-between align-items-center mb-1"
                >
                  <span class="text-muted">Questions</span>
                  <span class="fw-bold">{{
                    stats.overview?.total_questions || 0
                  }}</span>
                </div>
                <div
                  class="d-flex justify-content-between align-items-center mb-3"
                >
                  <span class="text-muted">Avg Q's per Quiz</span>
                  <span class="fw-bold">{{
                    stats.performance?.avg_questions_per_quiz || 0
                  }}</span>
                </div>
              </div>

              <div class="border-top pt-3">
                <h6 class="text-muted mb-2">Score Distribution</h6>
                <div
                  class="d-flex justify-content-between align-items-center mb-1"
                >
                  <span class="text-muted">Highest Score</span>
                  <span class="badge bg-success"
                    >{{ stats.performance?.highest_score || 0 }}%</span
                  >
                </div>
                <div
                  class="d-flex justify-content-between align-items-center mb-1"
                >
                  <span class="text-muted">Average Score</span>
                  <span class="badge bg-primary"
                    >{{ stats.performance?.average_score || 0 }}%</span
                  >
                </div>
                <div class="d-flex justify-content-between align-items-center">
                  <span class="text-muted">Lowest Score</span>
                  <span class="badge bg-warning"
                    >{{ stats.performance?.lowest_score || 0 }}%</span
                  >
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="row mb-4">
        <div class="col-lg-6 mb-3">
          <div class="card shadow-sm h-100">
            <div class="card-header bg-white">
              <h5 class="card-title mb-0">
                <i class="fas fa-trophy me-2 text-warning"></i>
                Top Performers
              </h5>
            </div>
            <div class="card-body">
              <div
                v-if="stats.top_performers?.length"
                class="list-group list-group-flush"
              >
                <div
                  v-for="(user, index) in stats.top_performers.slice(0, 5)"
                  :key="user.username"
                  class="list-group-item d-flex justify-content-between align-items-center px-0"
                >
                  <div class="d-flex align-items-center">
                    <span class="badge me-3" :class="getRankBadgeClass(index)">
                      {{ index + 1 }}
                    </span>
                    <div>
                      <div class="fw-medium">
                        {{ user.full_name || user.username }}
                      </div>
                      <small class="text-muted"
                        >{{ user.total_attempts }} attempts</small
                      >
                    </div>
                  </div>
                  <span class="badge bg-success"
                    >{{ user.average_score }}%</span
                  >
                </div>
              </div>
              <div v-else class="text-center py-4 text-muted">
                <i class="fas fa-trophy fa-3x mb-3"></i>
                <p>No user performance data yet</p>
              </div>
            </div>
          </div>
        </div>

        <div class="col-lg-6 mb-3">
          <div class="card shadow-sm h-100">
            <div class="card-header bg-white">
              <h5 class="card-title mb-0">
                <i class="fas fa-fire me-2 text-danger"></i>
                Popular Quizzes
              </h5>
            </div>
            <div class="card-body">
              <div
                v-if="stats.popular_quizzes?.length"
                class="list-group list-group-flush"
              >
                <div
                  v-for="quiz in stats.popular_quizzes.slice(0, 5)"
                  :key="quiz.quiz_title"
                  class="list-group-item px-0"
                >
                  <div class="d-flex justify-content-between align-items-start">
                    <div class="flex-grow-1">
                      <div class="fw-medium">{{ quiz.quiz_title }}</div>
                      <small class="text-muted"
                        >{{ quiz.subject_name }} •
                        {{ quiz.chapter_name }}</small
                      >
                    </div>
                    <div class="text-end">
                      <div class="badge bg-info">
                        {{ quiz.total_attempts }} attempts
                      </div>
                      <div class="small text-muted mt-1">
                        {{ quiz.average_score }}% avg
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <div v-else class="text-center py-4 text-muted">
                <i class="fas fa-fire fa-3x mb-3"></i>
                <p>No quiz engagement data yet</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="row">
        <div class="col-12">
          <div class="card shadow-sm">
            <div class="card-header bg-white">
              <h5 class="card-title mb-0">
                <i class="fas fa-chart-line me-2 text-info"></i>
                Activity Trends (Last 6 Months)
              </h5>
            </div>
            <div class="card-body">
              <div v-if="stats.monthly_trends?.length" class="table-responsive">
                <table class="table table-sm">
                  <thead class="table-light">
                    <tr>
                      <th>Month</th>
                      <th>New Users</th>
                      <th>Quiz Attempts</th>
                      <th>Growth</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr
                      v-for="(trend, index) in stats.monthly_trends"
                      :key="trend.month"
                    >
                      <td class="fw-medium">{{ formatMonth(trend.month) }}</td>
                      <td>{{ trend.new_users }}</td>
                      <td>{{ trend.quiz_attempts }}</td>
                      <td>
                        <span
                          v-if="index > 0"
                          class="badge"
                          :class="
                            getGrowthBadgeClass(
                              trend.quiz_attempts,
                              stats.monthly_trends[index - 1].quiz_attempts
                            )
                          "
                        >
                          {{
                            getGrowthPercentage(
                              trend.quiz_attempts,
                              stats.monthly_trends[index - 1].quiz_attempts
                            )
                          }}
                        </span>
                        <span v-else class="text-muted">-</span>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <div v-else class="text-center py-4 text-muted">
                <i class="fas fa-chart-line fa-3x mb-3"></i>
                <p>No trend data available yet</p>
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
        overview: {},
        performance: {},
        subject_breakdown: [],
        top_performers: [],
        popular_quizzes: [],
        monthly_trends: [],
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

    async refreshStats() {
      await this.fetchDashboardStats();
    },

    getPerformanceColor(score) {
      if (score >= 80) return "bg-success";
      if (score >= 60) return "bg-warning";
      return "bg-danger";
    },

    getRankBadgeClass(index) {
      switch (index) {
        case 0:
          return "bg-warning text-dark";
        case 1:
          return "bg-secondary";
        case 2:
          return "bg-warning text-dark";
        default:
          return "bg-primary";
      }
    },

    formatMonth(monthStr) {
      const date = new Date(monthStr + "-01");
      return date.toLocaleDateString("en-US", {
        month: "long",
        year: "numeric",
      });
    },

    getGrowthPercentage(current, previous) {
      if (previous === 0) return current > 0 ? "+100%" : "0%";
      const growth = (((current - previous) / previous) * 100).toFixed(1);
      return growth > 0 ? `+${growth}%` : `${growth}%`;
    },

    getGrowthBadgeClass(current, previous) {
      if (current > previous) return "bg-success";
      if (current < previous) return "bg-danger";
      return "bg-secondary";
    },
  },
};
</script>

<style scoped>
.bg-gradient-primary {
  background: linear-gradient(45deg, #007bff, #0056b3);
}

.bg-gradient-success {
  background: linear-gradient(45deg, #28a745, #1e7e34);
}

.bg-gradient-info {
  background: linear-gradient(45deg, #17a2b8, #117a8b);
}

.bg-gradient-warning {
  background: linear-gradient(45deg, #ffc107, #d39e00);
}

.card {
  border: none;
  transition: transform 0.2s ease-in-out;
}

.card:hover {
  transform: translateY(-2px);
}

.progress {
  background-color: #e9ecef;
}

.list-group-item {
  border-left: none;
  border-right: none;
}

.list-group-item:first-child {
  border-top: none;
}

.list-group-item:last-child {
  border-bottom: none;
}

.text-white-50 {
  color: rgba(255, 255, 255, 0.5) !important;
}

.text-white-75 {
  color: rgba(255, 255, 255, 0.75) !important;
}
</style>
