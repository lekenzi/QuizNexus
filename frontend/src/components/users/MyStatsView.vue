<template>
  <div class="stats-view container-fluid mt-4 bg-light min-vh-100">
    <div class="row">
      <div class="col-12">
        <div
          class="d-flex flex-column justify-content-between align-items-center mb-4"
        >
          <h1 class="text-primary mb-0">
            <i class="fas fa-chart-line me-2"></i>My Performance Analytics
          </h1>
          <button
            @click="fetchStats"
            class="btn btn-outline-primary"
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
      <p class="mt-3 text-muted">Loading your performance analytics...</p>
    </div>

    <div v-else-if="error" class="alert alert-danger mx-3">
      <i class="fas fa-exclamation-triangle me-2"></i>
      {{ error }}
      <button @click="fetchStats" class="btn btn-sm btn-outline-danger ms-2">
        Try Again
      </button>
    </div>

    <div v-else-if="!stats.total_quizzes_taken" class="text-center my-5">
      <div class="card shadow-sm mx-auto" style="max-width: 500px">
        <div class="card-body p-5">
          <i class="fas fa-chart-pie fa-5x text-muted mb-4"></i>
          <h4 class="text-muted mb-3">No Quiz Activity Found</h4>
          <p class="text-muted mb-4">
            You haven't taken any quizzes yet. Start taking quizzes to see your
            detailed performance analytics!
          </p>
          <router-link to="/dashboard" class="btn btn-primary">
            <i class="fas fa-play me-2"></i>Start Taking Quizzes
          </router-link>
        </div>
      </div>
    </div>

    <div v-else>
      <div class="row mb-4">
        <div class="col-lg-3 col-md-6 mb-3">
          <div class="card bg-gradient-primary text-white h-100 shadow-sm">
            <div class="card-body">
              <div class="d-flex justify-content-between">
                <div>
                  <h6 class="card-title text-white-50">Total Quizzes</h6>
                  <h2 class="mb-0">{{ stats.total_quizzes_taken }}</h2>
                  <small class="text-white-75">
                    <i class="fas fa-calendar me-1"></i>
                    {{ stats.recent_activity_30d }} in last 30 days
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
          <div class="card bg-gradient-success text-white h-100 shadow-sm">
            <div class="card-body">
              <div class="d-flex justify-content-between">
                <div>
                  <h6 class="card-title text-white-50">Average Score</h6>
                  <h2 class="mb-0">{{ stats.average_score }}%</h2>
                  <small class="text-white-75" :class="getTrendClass()">
                    <i :class="getTrendIcon() + ' me-1'"></i>
                    {{ getTrendText() }}
                  </small>
                </div>
                <div class="align-self-center">
                  <i class="fas fa-trophy fa-2x text-white-50"></i>
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
                  <h6 class="card-title text-white-50">Accuracy Rate</h6>
                  <h2 class="mb-0">{{ stats.accuracy_percentage }}%</h2>
                  <small class="text-white-75">
                    <i class="fas fa-bullseye me-1"></i>
                    {{ stats.total_correct_answers }}/{{
                      stats.total_questions_attempted
                    }}
                    correct
                  </small>
                </div>
                <div class="align-self-center">
                  <i class="fas fa-chart-pie fa-2x text-white-50"></i>
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
                  <h6 class="card-title text-white-50">Subjects Covered</h6>
                  <h2 class="mb-0">
                    {{ stats.activity_summary.subjects_attempted }}
                  </h2>
                  <small class="text-white-75">
                    <i class="fas fa-star me-1"></i>
                    Best: {{ stats.activity_summary.best_subject || "None" }}
                  </small>
                </div>
                <div class="align-self-center">
                  <i class="fas fa-books fa-2x text-white-50"></i>
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
                <i class="fas fa-medal me-2 text-warning"></i>
                Your Performance Ranking
              </h5>
            </div>
            <div class="card-body">
              <div class="row align-items-center">
                <div class="col-md-8">
                  <div class="mb-3">
                    <div class="d-flex justify-content-between mb-2">
                      <span class="text-muted">Performance Percentile</span>
                      <span class="fw-bold">{{ stats.percentile_rank }}%</span>
                    </div>
                    <div class="progress" style="height: 20px">
                      <div
                        class="progress-bar bg-gradient-success"
                        role="progressbar"
                        :style="`width: ${stats.percentile_rank}%`"
                        :aria-valuenow="stats.percentile_rank"
                        aria-valuemin="0"
                        aria-valuemax="100"
                      >
                        <small class="fw-bold"
                          >{{ stats.percentile_rank }}%</small
                        >
                      </div>
                    </div>
                  </div>
                  <p class="text-muted mb-0">
                    Your performance is better than
                    <strong>{{ stats.percentile_rank }}%</strong> of all users
                  </p>
                </div>
                <div class="col-md-4 text-center">
                  <canvas ref="rankingChart" width="150" height="150"></canvas>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="col-lg-4 mb-3">
          <div class="card shadow-sm h-100">
            <div class="card-header bg-white">
              <h5 class="card-title mb-0">
                <i class="fas fa-chart-bar me-2 text-info"></i>
                Score Summary
              </h5>
            </div>
            <div class="card-body">
              <div class="row g-3">
                <div class="col-6 text-center">
                  <div class="h4 text-success mb-1">
                    {{ stats.best_score }}%
                  </div>
                  <div class="small text-muted">Best Score</div>
                </div>
                <div class="col-6 text-center">
                  <div class="h4 text-primary mb-1">
                    {{ stats.average_score }}%
                  </div>
                  <div class="small text-muted">Average</div>
                </div>
                <div class="col-6 text-center">
                  <div class="h4 text-warning mb-1">
                    {{ stats.worst_score }}%
                  </div>
                  <div class="small text-muted">Lowest</div>
                </div>
                <div class="col-6 text-center">
                  <div class="h4 text-info mb-1">{{ stats.total_points }}</div>
                  <div class="small text-muted">Total Points</div>
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
                Subject Performance Analysis
              </h5>
            </div>
            <div class="card-body" style="height: 400px">
              <canvas ref="subjectChart" :key="chartKey"></canvas>
            </div>
          </div>
        </div>

        <div class="col-lg-4 mb-3">
          <div class="card shadow-sm">
            <div class="card-header bg-white">
              <h5 class="card-title mb-0">
                <i class="fas fa-spider me-2 text-success"></i>
                Performance Radar
              </h5>
            </div>
            <div class="card-body" style="height: 400px">
              <canvas ref="performanceRadar" :key="chartKey"></canvas>
            </div>
          </div>
        </div>
      </div>

      <div class="row mb-4">
        <div class="col-lg-6 mb-3">
          <div class="card shadow-sm">
            <div class="card-header bg-white">
              <h5 class="card-title mb-0">
                <i class="fas fa-chart-pie me-2 text-info"></i>
                Score Distribution by Subject
              </h5>
            </div>
            <div class="card-body" style="height: 350px">
              <canvas ref="scoreDistributionChart" :key="chartKey"></canvas>
            </div>
          </div>
        </div>

        <div class="col-lg-6 mb-3">
          <div class="card shadow-sm">
            <div class="card-header bg-white">
              <h5 class="card-title mb-0">
                <i class="fas fa-chart-line me-2 text-warning"></i>
                Subject Quiz Activity
              </h5>
            </div>
            <div class="card-body" style="height: 350px">
              <canvas ref="activityChart" :key="chartKey"></canvas>
            </div>
          </div>
        </div>
      </div>

      <div
        class="row mb-4"
        v-if="stats.achievements && stats.achievements.length > 0"
      >
        <div class="col-12">
          <div class="card shadow-sm">
            <div class="card-header bg-gradient-purple text-white">
              <h5 class="card-title mb-0">
                <i class="fas fa-trophy me-2"></i>
                Your Achievements
              </h5>
            </div>
            <div class="card-body">
              <div class="row">
                <div
                  v-for="(achievement, index) in stats.achievements"
                  :key="index"
                  class="col-lg-3 col-md-4 col-sm-6 mb-3"
                >
                  <div class="achievement-card h-100">
                    <div class="achievement-icon">{{ achievement.icon }}</div>
                    <h6 class="achievement-title">{{ achievement.title }}</h6>
                    <p class="achievement-desc">
                      {{ achievement.description }}
                    </p>
                  </div>
                </div>
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
                <i class="fas fa-table me-2 text-secondary"></i>
                Detailed Subject Breakdown
              </h5>
            </div>
            <div class="card-body">
              <div class="table-responsive">
                <table class="table table-hover">
                  <thead class="table-light">
                    <tr>
                      <th>Subject</th>
                      <th>Quizzes Taken</th>
                      <th>Average Score</th>
                      <th>Best Score</th>
                      <th>Worst Score</th>
                      <th>Performance</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr
                      v-for="subject in stats.subject_breakdown"
                      :key="subject.subject_name"
                    >
                      <td class="fw-medium">{{ subject.subject_name }}</td>
                      <td>{{ subject.quizzes_taken }}</td>
                      <td>{{ subject.average_score }}%</td>
                      <td>
                        <span class="badge bg-success"
                          >{{ subject.best_score }}%</span
                        >
                      </td>
                      <td>
                        <span class="badge bg-warning"
                          >{{ subject.worst_score }}%</span
                        >
                      </td>
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
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Chart from "chart.js/auto";
import { make_getrequest } from "@/stores/appState";

export default {
  name: "MyStatsView",
  data() {
    return {
      stats: {
        total_quizzes_taken: 0,
        average_score: 0,
        best_score: 0,
        worst_score: 0,
        total_points: 0,
        total_correct_answers: 0,
        total_questions_attempted: 0,
        accuracy_percentage: 0,
        percentile_rank: 0,
        recent_activity_30d: 0,
        performance_trend: "stable",
        subject_breakdown: [],
        achievements: [],
        activity_summary: {
          most_active_subject: "",
          subjects_attempted: 0,
          best_subject: "",
          best_subject_average: 0,
        },
      },
      loading: true,
      error: null,
      charts: {
        subjectChart: null,
        performanceRadar: null,
        scoreDistributionChart: null,
        activityChart: null,
        rankingChart: null,
      },
      chartKey: 0,
    };
  },
  mounted() {
    this.fetchStats();
  },
  beforeUnmount() {
    this.destroyCharts();
  },
  methods: {
    async fetchStats() {
      this.loading = true;
      this.error = null;

      try {
        console.log("Fetching user stats...");
        const response = await make_getrequest("/my_quiz_stats");

        if (!response || !response.stats) {
          this.error = "Failed to load statistics data";
          console.error("Invalid response format:", response);
          return;
        }

        this.stats = response.stats;
        console.log("User stats loaded:", this.stats);

        // Wait for next tick to ensure DOM elements are rendered
        await this.$nextTick();

        // Force re-render of charts
        this.chartKey++;

        // Initialize charts after a small delay
        setTimeout(() => {
          this.initializeCharts();
        }, 100);
      } catch (error) {
        this.error = "An error occurred while fetching your statistics";
        console.error("Error fetching stats:", error);
      } finally {
        this.loading = false;
      }
    },

    destroyCharts() {
      Object.values(this.charts).forEach((chart) => {
        if (chart) {
          chart.destroy();
        }
      });
      this.charts = {
        subjectChart: null,
        performanceRadar: null,
        scoreDistributionChart: null,
        activityChart: null,
        rankingChart: null,
      };
    },

    initializeCharts() {
      try {
        this.createSubjectChart();
        this.createPerformanceRadar();
        this.createScoreDistributionChart();
        this.createActivityChart();
        this.createRankingChart();
      } catch (error) {
        console.error("Error initializing charts:", error);
      }
    },

    createSubjectChart() {
      const ctx = this.$refs.subjectChart?.getContext("2d");
      if (!ctx) return;

      const data = this.stats.subject_breakdown || [];

      if (data.length === 0) {
        this.charts.subjectChart = new Chart(ctx, {
          type: "bar",
          data: {
            labels: ["No Data"],
            datasets: [
              {
                label: "No Data Available",
                data: [0],
                backgroundColor: "rgba(200, 200, 200, 0.6)",
              },
            ],
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
          },
        });
        return;
      }

      this.charts.subjectChart = new Chart(ctx, {
        type: "bar",
        data: {
          labels: data.map((s) => s.subject_name),
          datasets: [
            {
              label: "Average Score (%)",
              data: data.map((s) => s.average_score),
              backgroundColor: "rgba(54, 162, 235, 0.6)",
              borderColor: "rgba(54, 162, 235, 1)",
              borderWidth: 1,
              yAxisID: "y",
            },
            {
              label: "Quizzes Taken",
              data: data.map((s) => s.quizzes_taken),
              type: "line",
              backgroundColor: "rgba(255, 99, 132, 0.6)",
              borderColor: "rgba(255, 99, 132, 1)",
              borderWidth: 2,
              yAxisID: "y1",
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            y: {
              type: "linear",
              display: true,
              position: "left",
              title: { display: true, text: "Average Score (%)" },
              min: 0,
              max: 100,
            },
            y1: {
              type: "linear",
              display: true,
              position: "right",
              title: { display: true, text: "Quizzes Taken" },
              grid: { drawOnChartArea: false },
            },
          },
          plugins: {
            legend: { display: true, position: "top" },
          },
        },
      });
    },

    createPerformanceRadar() {
      const ctx = this.$refs.performanceRadar?.getContext("2d");
      if (!ctx) return;

      const performanceData = [
        this.stats.accuracy_percentage || 0,
        this.stats.average_score || 0,
        this.stats.percentile_rank || 0,
        Math.min((this.stats.recent_activity_30d || 0) * 10, 100),
        Math.min(
          (this.stats.activity_summary.subjects_attempted || 0) * 20,
          100
        ),
      ];

      this.charts.performanceRadar = new Chart(ctx, {
        type: "radar",
        data: {
          labels: [
            "Accuracy",
            "Avg Score",
            "Ranking",
            "Activity",
            "Subject Coverage",
          ],
          datasets: [
            {
              label: "Your Performance",
              data: performanceData,
              backgroundColor: "rgba(75, 192, 192, 0.2)",
              borderColor: "rgba(75, 192, 192, 1)",
              pointBackgroundColor: "rgba(75, 192, 192, 1)",
              pointBorderColor: "#fff",
              pointHoverBackgroundColor: "#fff",
              pointHoverBorderColor: "rgba(75, 192, 192, 1)",
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            r: {
              beginAtZero: true,
              max: 100,
            },
          },
          plugins: {
            legend: { display: false },
          },
        },
      });
    },

    createScoreDistributionChart() {
      const ctx = this.$refs.scoreDistributionChart?.getContext("2d");
      if (!ctx) return;

      const data = this.stats.subject_breakdown || [];
      const colors = [
        "#FF6384",
        "#36A2EB",
        "#FFCE56",
        "#4BC0C0",
        "#9966FF",
        "#FF9F40",
        "#FF6384",
        "#C9CBCF",
      ];

      this.charts.scoreDistributionChart = new Chart(ctx, {
        type: "doughnut",
        data: {
          labels: data.map((s) => s.subject_name),
          datasets: [
            {
              data: data.map((s) => s.quizzes_taken),
              backgroundColor: colors.slice(0, data.length),
              borderWidth: 2,
              borderColor: "#fff",
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              display: true,
              position: "bottom",
              labels: { padding: 10, usePointStyle: true },
            },
            tooltip: {
              callbacks: {
                label: (context) => {
                  const total = context.dataset.data.reduce((a, b) => a + b, 0);
                  const percentage = ((context.parsed / total) * 100).toFixed(
                    1
                  );
                  return `${context.label}: ${context.parsed} quizzes (${percentage}%)`;
                },
              },
            },
          },
        },
      });
    },

    createActivityChart() {
      const ctx = this.$refs.activityChart?.getContext("2d");
      if (!ctx) return;

      const data = this.stats.subject_breakdown || [];

      this.charts.activityChart = new Chart(ctx, {
        type: "polarArea",
        data: {
          labels: data.map((s) => s.subject_name),
          datasets: [
            {
              data: data.map((s) => s.average_score),
              backgroundColor: [
                "rgba(255, 99, 132, 0.6)",
                "rgba(54, 162, 235, 0.6)",
                "rgba(255, 205, 86, 0.6)",
                "rgba(75, 192, 192, 0.6)",
                "rgba(153, 102, 255, 0.6)",
                "rgba(255, 159, 64, 0.6)",
              ],
              borderWidth: 2,
              borderColor: "#fff",
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              display: true,
              position: "bottom",
            },
          },
          scales: {
            r: {
              beginAtZero: true,
              max: 100,
            },
          },
        },
      });
    },

    createRankingChart() {
      const ctx = this.$refs.rankingChart?.getContext("2d");
      if (!ctx) return;

      const percentile = this.stats.percentile_rank || 0;

      this.charts.rankingChart = new Chart(ctx, {
        type: "doughnut",
        data: {
          datasets: [
            {
              data: [percentile, 100 - percentile],
              backgroundColor: ["#28a745", "#e9ecef"],
              borderWidth: 0,
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: true,
          cutout: "70%",
          plugins: {
            legend: { display: false },
            tooltip: { enabled: false },
          },
        },
        plugins: [
          {
            afterDraw: (chart) => {
              const { ctx, chartArea } = chart;
              ctx.save();
              ctx.font = "bold 16px Arial";
              ctx.fillStyle = "#28a745";
              ctx.textAlign = "center";
              ctx.textBaseline = "middle";
              const centerX = (chartArea.left + chartArea.right) / 2;
              const centerY = (chartArea.top + chartArea.bottom) / 2;
              ctx.fillText(`${percentile}%`, centerX, centerY);
              ctx.restore();
            },
          },
        ],
      });
    },

    getTrendClass() {
      const trendMap = {
        improving: "text-success",
        declining: "text-danger",
        stable: "text-light",
      };
      return trendMap[this.stats.performance_trend] || "text-light";
    },

    getTrendIcon() {
      const iconMap = {
        improving: "fas fa-arrow-up",
        declining: "fas fa-arrow-down",
        stable: "fas fa-equals",
      };
      return iconMap[this.stats.performance_trend] || "fas fa-equals";
    },

    getTrendText() {
      const textMap = {
        improving: "Improving",
        declining: "Declining",
        stable: "Stable",
        no_data: "Not enough data",
      };
      return textMap[this.stats.performance_trend] || "Stable";
    },

    getPerformanceColor(score) {
      if (score >= 80) return "bg-success";
      if (score >= 60) return "bg-warning";
      return "bg-danger";
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

.bg-gradient-purple {
  background: linear-gradient(45deg, #6f42c1, #5a2d91);
}

.card {
  border: none;
  transition: transform 0.2s ease-in-out;
}

.card:hover {
  transform: translateY(-2px);
}

.achievement-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 15px;
  padding: 20px;
  text-align: center;
  color: white;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}

.achievement-card:hover {
  transform: translateY(-5px);
}

.achievement-icon {
  font-size: 2.5rem;
  margin-bottom: 10px;
  display: block;
}

.achievement-title {
  font-size: 1rem;
  font-weight: bold;
  margin-bottom: 8px;
  color: #fff;
}

.achievement-desc {
  font-size: 0.85rem;
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 0;
}

.text-white-50 {
  color: rgba(255, 255, 255, 0.5) !important;
}

.text-white-75 {
  color: rgba(255, 255, 255, 0.75) !important;
}

.progress {
  background-color: #e9ecef;
}

.progress-bar {
  transition: width 0.6s ease;
}

.table th {
  border-top: none;
  font-weight: 600;
  color: #495057;
}

.table td {
  vertical-align: middle;
}
</style>
