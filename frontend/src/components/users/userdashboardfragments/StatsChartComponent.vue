<template>
  <div class="stats-chart-container">
    <div class="row mb-4">
      <div class="col-lg-3 col-md-6 mb-3">
        <div class="stats-card card border-0 shadow-lg h-100 quizzes-card">
          <div class="card-body text-center p-4">
            <div class="icon-container mb-3">
              <i class="fas fa-clipboard-list fa-2x text-white"></i>
            </div>
            <h5 class="card-title text-white fw-semibold mb-1">
              Total Quizzes
            </h5>
            <h3 class="text-white fw-bold mb-2">
              {{ stats.total_quizzes_taken || 0 }}
            </h3>
            <small class="text-white-50">
              <i class="fas fa-calendar me-1"></i>
              {{ stats.recent_activity_30d || 0 }} in last 30 days
            </small>
          </div>
        </div>
      </div>

      <div class="col-lg-3 col-md-6 mb-3">
        <div class="stats-card card border-0 shadow-lg h-100 average-card">
          <div class="card-body text-center p-4">
            <div class="icon-container mb-3">
              <i class="fas fa-chart-line fa-2x text-white"></i>
            </div>
            <h5 class="card-title text-white fw-semibold mb-1">
              Average Score
            </h5>
            <h3 class="text-white fw-bold mb-2">
              {{ stats.average_score || 0 }}%
            </h3>
            <small class="text-white-50">
              <i class="fas fa-trophy me-1"></i>
              Top {{ stats.percentile_rank || 0 }}% of users
            </small>
          </div>
        </div>
      </div>

      <div class="col-lg-3 col-md-6 mb-3">
        <div class="stats-card card border-0 shadow-lg h-100 accuracy-card">
          <div class="card-body text-center p-4">
            <div class="icon-container mb-3">
              <i class="fas fa-bullseye fa-2x text-white"></i>
            </div>
            <h5 class="card-title text-white fw-semibold mb-1">Accuracy</h5>
            <h3 class="text-white fw-bold mb-2">
              {{ stats.accuracy_percentage || 0 }}%
            </h3>
            <small class="text-white-50">
              <i class="fas fa-check me-1"></i>
              {{ stats.total_correct_answers || 0 }}/{{
                stats.total_questions_attempted || 0
              }}
              correct
            </small>
          </div>
        </div>
      </div>

      <div class="col-lg-3 col-md-6 mb-3">
        <div class="stats-card card border-0 shadow-lg h-100 best-card">
          <div class="card-body text-center p-4">
            <div class="icon-container mb-3">
              <i class="fas fa-star fa-2x text-white"></i>
            </div>
            <h5 class="card-title text-white fw-semibold mb-1">Best Score</h5>
            <h3 class="text-white fw-bold mb-2">
              {{ stats.best_score || 0 }}%
            </h3>
            <small class="text-white-50">
              <i class="fas fa-trend-up me-1"></i>
              {{ getTrendIcon(stats.performance_trend) }}
              {{ formatTrend(stats.performance_trend) }}
            </small>
          </div>
        </div>
      </div>
    </div>

    <div
      class="row mb-4"
      v-if="stats.achievements && stats.achievements.length > 0"
    >
      <div class="col-12">
        <div class="card border-0 shadow-lg">
          <div class="card-header bg-gradient-warning text-white border-0 py-3">
            <h5 class="mb-0 fw-semibold">
              <i class="fas fa-trophy me-2"></i>Your Achievements
            </h5>
          </div>
          <div class="card-body p-4">
            <div class="row">
              <div
                v-for="achievement in stats.achievements"
                :key="achievement.type"
                class="col-lg-4 col-md-6 mb-3"
              >
                <div class="achievement-badge">
                  <div class="achievement-icon">{{ achievement.icon }}</div>
                  <h6 class="fw-bold mb-1">{{ achievement.title }}</h6>
                  <small class="text-muted">{{
                    achievement.description
                  }}</small>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="row">
      <div
        class="col-md-12 mb-4"
        v-if="stats.subject_breakdown && stats.subject_breakdown.length > 0"
      >
        <div class="card border-0 shadow-lg">
          <div class="card-header bg-gradient-primary text-white border-0 py-3">
            <h5 class="mb-0 fw-semibold">
              <i class="fas fa-chart-bar me-2"></i>Subject Performance Overview
            </h5>
          </div>
          <div class="card-body p-4">
            <canvas id="subjectChart"></canvas>
          </div>
        </div>
      </div>
    </div>

    <div
      class="row"
      v-if="stats.subject_breakdown && stats.subject_breakdown.length > 0"
    >
      <div class="col-12">
        <div class="card border-0 shadow-lg">
          <div class="card-header bg-gradient-info text-white border-0 py-3">
            <h5 class="mb-0 fw-semibold">
              <i class="fas fa-list me-2"></i>Subject Breakdown
            </h5>
          </div>
          <div class="card-body p-4">
            <div class="row">
              <div
                v-for="subject in stats.subject_breakdown"
                :key="subject.subject_id"
                class="col-lg-4 col-md-6 mb-3"
              >
                <div class="subject-detail-card">
                  <h6 class="fw-bold text-primary mb-2">
                    {{ subject.subject_name }}
                  </h6>
                  <div class="subject-stats">
                    <div class="stat-item">
                      <span class="stat-label">Quizzes:</span>
                      <span class="stat-value">{{
                        subject.quizzes_taken
                      }}</span>
                    </div>
                    <div class="stat-item">
                      <span class="stat-label">Average:</span>
                      <span class="stat-value text-success"
                        >{{ subject.average_score }}%</span
                      >
                    </div>
                    <div class="stat-item">
                      <span class="stat-label">Best:</span>
                      <span class="stat-value text-info"
                        >{{ subject.best_score }}%</span
                      >
                    </div>
                    <div class="stat-item">
                      <span class="stat-label">Worst:</span>
                      <span class="stat-value text-warning"
                        >{{ subject.worst_score }}%</span
                      >
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="row mt-4" v-if="stats.activity_summary">
      <div class="col-12">
        <div class="card border-0 shadow-lg">
          <div class="card-header bg-gradient-success text-white border-0 py-3">
            <h5 class="mb-0 fw-semibold">
              <i class="fas fa-activity me-2"></i>Activity Summary
            </h5>
          </div>
          <div class="card-body p-4">
            <div class="row text-center">
              <div class="col-md-3 col-6 mb-3">
                <div class="summary-stat">
                  <i class="fas fa-bookmark text-primary fa-2x mb-2"></i>
                  <h5 class="fw-bold text-primary">
                    {{ stats.activity_summary.subjects_attempted }}
                  </h5>
                  <p class="text-muted mb-0">Subjects Attempted</p>
                </div>
              </div>
              <div class="col-md-3 col-6 mb-3">
                <div class="summary-stat">
                  <i class="fas fa-fire text-danger fa-2x mb-2"></i>
                  <h5 class="fw-bold text-danger">
                    {{ stats.activity_summary.most_active_subject }}
                  </h5>
                  <p class="text-muted mb-0">Most Active Subject</p>
                </div>
              </div>
              <div class="col-md-3 col-6 mb-3">
                <div class="summary-stat">
                  <i class="fas fa-crown text-warning fa-2x mb-2"></i>
                  <h5 class="fw-bold text-warning">
                    {{ stats.activity_summary.best_subject }}
                  </h5>
                  <p class="text-muted mb-0">Best Subject</p>
                </div>
              </div>
              <div class="col-md-3 col-6 mb-3">
                <div class="summary-stat">
                  <i class="fas fa-percentage text-success fa-2x mb-2"></i>
                  <h5 class="fw-bold text-success">
                    {{ stats.activity_summary.best_subject_average }}%
                  </h5>
                  <p class="text-muted mb-0">Best Subject Average</p>
                </div>
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

export default {
  name: "StatsChartComponent",
  props: {
    stats: {
      type: Object,
      required: true,
      default: () => ({}),
    },
  },
  data() {
    return {
      subjectChart: null,
    };
  },
  mounted() {
    if (
      this.stats.subject_breakdown &&
      this.stats.subject_breakdown.length > 0
    ) {
      this.$nextTick(() => {
        this.createSubjectChart();
      });
    }
  },
  watch: {
    stats: {
      handler() {
        this.updateCharts();
      },
      deep: true,
    },
  },
  methods: {
    createSubjectChart() {
      const canvas = document.getElementById("subjectChart");
      if (!canvas) return;

      const ctx = canvas.getContext("2d");

      const subjects = this.stats.subject_breakdown.map((s) => s.subject_name);
      const averageScores = this.stats.subject_breakdown.map(
        (s) => s.average_score
      );
      const quizCounts = this.stats.subject_breakdown.map(
        (s) => s.quizzes_taken
      );

      this.subjectChart = new Chart(ctx, {
        type: "bar",
        data: {
          labels: subjects,
          datasets: [
            {
              label: "Average Score (%)",
              data: averageScores,
              backgroundColor: "rgba(102, 126, 234, 0.8)",
              borderColor: "rgba(102, 126, 234, 1)",
              borderWidth: 2,
              yAxisID: "y",
              borderRadius: 8,
            },
            {
              label: "Quizzes Taken",
              data: quizCounts,
              backgroundColor: "rgba(40, 167, 69, 0.8)",
              borderColor: "rgba(40, 167, 69, 1)",
              borderWidth: 2,
              yAxisID: "y1",
              borderRadius: 8,
            },
          ],
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              position: "top",
              labels: {
                usePointStyle: true,
                padding: 20,
                font: {
                  size: 14,
                  weight: "bold",
                },
              },
            },
          },
          scales: {
            x: {
              grid: {
                display: false,
              },
              ticks: {
                font: {
                  size: 12,
                  weight: "bold",
                },
              },
            },
            y: {
              type: "linear",
              position: "left",
              title: {
                display: true,
                text: "Average Score (%)",
                font: {
                  size: 14,
                  weight: "bold",
                },
              },
              min: 0,
              max: 100,
              grid: {
                color: "rgba(0,0,0,0.1)",
              },
            },
            y1: {
              type: "linear",
              position: "right",
              title: {
                display: true,
                text: "Quiz Count",
                font: {
                  size: 14,
                  weight: "bold",
                },
              },
              grid: {
                drawOnChartArea: false,
              },
            },
          },
        },
      });
    },

    updateCharts() {
      if (this.subjectChart) {
        this.subjectChart.destroy();
      }
      if (
        this.stats.subject_breakdown &&
        this.stats.subject_breakdown.length > 0
      ) {
        this.$nextTick(() => {
          this.createSubjectChart();
        });
      }
    },

    getTrendIcon(trend) {
      switch (trend) {
        case "improving":
          return "📈";
        case "declining":
          return "📉";
        default:
          return "➡️";
      }
    },

    formatTrend(trend) {
      switch (trend) {
        case "improving":
          return "Improving";
        case "declining":
          return "Declining";
        case "stable":
          return "Stable";
        default:
          return "No Data";
      }
    },
  },
  beforeUnmount() {
    if (this.subjectChart) {
      this.subjectChart.destroy();
    }
  },
};
</script>

<style scoped>
.stats-chart-container {
  margin-top: 20px;
}

.stats-card {
  transition: all 0.3s ease;
  border-radius: 20px !important;
  overflow: hidden;
  position: relative;
}

.stats-card:hover {
  transform: translateY(-5px) scale(1.02);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15) !important;
}

.quizzes-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.average-card {
  background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
}

.accuracy-card {
  background: linear-gradient(135deg, #17a2b8 0%, #6f42c1 100%);
}

.best-card {
  background: linear-gradient(135deg, #ffc107 0%, #ff8c00 100%);
}

.icon-container {
  padding: 15px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.2);
  display: inline-block;
  backdrop-filter: blur(10px);
}

.bg-gradient-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
}

.bg-gradient-info {
  background: linear-gradient(135deg, #17a2b8 0%, #6f42c1 100%) !important;
}

.bg-gradient-success {
  background: linear-gradient(135deg, #28a745 0%, #20c997 100%) !important;
}

.bg-gradient-warning {
  background: linear-gradient(135deg, #ffc107 0%, #ff8c00 100%) !important;
}

.achievement-badge {
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  padding: 1.5rem;
  border-radius: 15px;
  text-align: center;
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.achievement-badge:hover {
  transform: translateY(-3px);
  border-color: #667eea;
  box-shadow: 0 10px 25px rgba(102, 126, 234, 0.15);
}

.achievement-icon {
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

.subject-detail-card {
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  padding: 1.5rem;
  border-radius: 15px;
  transition: all 0.3s ease;
  border: 1px solid #dee2e6;
}

.subject-detail-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  border-color: #667eea;
}

.subject-stats {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.stat-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.stat-label {
  font-weight: 500;
  color: #6c757d;
}

.stat-value {
  font-weight: bold;
}

.summary-stat {
  padding: 1rem;
  border-radius: 15px;
  background: rgba(102, 126, 234, 0.05);
  transition: all 0.3s ease;
}

.summary-stat:hover {
  background: rgba(102, 126, 234, 0.1);
  transform: translateY(-3px);
}

.card {
  border-radius: 20px !important;
}

@media (max-width: 768px) {
  .stats-card .icon-container {
    padding: 10px;
  }

  .stats-card .icon-container i {
    font-size: 1.5rem !important;
  }

  .stats-card h3 {
    font-size: 1.5rem;
  }
}
</style>
