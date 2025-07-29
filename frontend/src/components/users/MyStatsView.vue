<template>
  <div class="stats-view container mt-5 p-4 bg-light rounded shadow">
    <h1 class="title text-center text-primary mb-3">
      My Performance Statistics
    </h1>

    <div v-if="loading" class="text-center my-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p class="mt-2">Loading your statistics...</p>
    </div>

    <div v-else-if="error" class="alert alert-danger" role="alert">
      {{ error }}
    </div>

    <div v-else-if="!stats.total_quizzes_taken" class="text-center my-5">
      <div class="alert alert-info" role="alert">
        <h4 class="alert-heading">No Quiz Activity Found</h4>
        <p>
          You haven't taken any quizzes yet. Start taking quizzes to see your
          statistics here!
        </p>
      </div>
    </div>

    <template v-else>
      <!-- Performance Overview Cards -->
      <div class="row mb-4">
        <div class="col-md-3">
          <div class="card text-white bg-primary h-100">
            <div class="card-body text-center">
              <h5 class="card-title">Total Quizzes</h5>
              <p class="card-text display-4">{{ stats.total_quizzes_taken }}</p>
              <p class="small mt-2">
                {{ stats.recent_activity_30d }} in last 30 days
              </p>
            </div>
          </div>
        </div>
        <div class="col-md-3">
          <div class="card text-white bg-success h-100">
            <div class="card-body text-center">
              <h5 class="card-title">Average Score</h5>
              <p class="card-text display-4">{{ stats.average_score }}%</p>
              <div class="small mt-2">
                <span :class="getTrendClass()">
                  <i :class="getTrendIcon()"></i>
                  {{ getTrendText() }}
                </span>
              </div>
            </div>
          </div>
        </div>
        <div class="col-md-3">
          <div class="card text-white bg-info h-100">
            <div class="card-body text-center">
              <h5 class="card-title">Subjects Covered</h5>
              <p class="card-text display-4">
                {{ stats.activity_summary.subjects_attempted }}
              </p>
              <p class="small mt-2">
                Best: {{ stats.activity_summary.best_subject }}
              </p>
            </div>
          </div>
        </div>
        <div class="col-md-3">
          <div class="card text-white bg-warning h-100">
            <div class="card-body text-center">
              <h5 class="card-title">Accuracy Rate</h5>
              <p class="card-text display-4">
                {{ stats.accuracy_percentage }}%
              </p>
              <p class="small mt-2">
                {{ stats.total_correct_answers }} /
                {{ stats.total_questions_attempted }} correct
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- Percentile Rank -->
      <div class="row mb-4">
        <div class="col-12">
          <div class="card">
            <div class="card-header bg-dark text-white">
              <h5 class="m-0">Your Ranking</h5>
            </div>
            <div class="card-body">
              <div class="progress mb-3" style="height: 25px">
                <div
                  class="progress-bar bg-success"
                  role="progressbar"
                  :style="`width: ${stats.percentile_rank}%`"
                  :aria-valuenow="stats.percentile_rank"
                  aria-valuemin="0"
                  aria-valuemax="100"
                >
                  {{ stats.percentile_rank }}%
                </div>
              </div>
              <p class="text-center mb-0">
                Your performance is better than {{ stats.percentile_rank }}% of
                all users
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- Achievements Section -->
      <div
        class="row mb-4"
        v-if="stats.achievements && stats.achievements.length > 0"
      >
        <div class="col-12">
          <div class="card">
            <div class="card-header bg-purple text-white">
              <h5 class="m-0">Your Achievements</h5>
            </div>
            <div class="card-body">
              <div
                class="achievements-container d-flex flex-wrap justify-content-center"
              >
                <div
                  v-for="(achievement, index) in stats.achievements"
                  :key="index"
                  class="achievement-badge m-2 p-3"
                >
                  <div class="achievement-icon">{{ achievement.icon }}</div>
                  <h5 class="achievement-title">{{ achievement.title }}</h5>
                  <p class="achievement-desc">{{ achievement.description }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Statistics Charts -->
      <div class="stats-chart-container">
        <div class="row">
          <div class="col-md-12 mb-4">
            <div class="card">
              <div class="card-header bg-primary text-white">
                <h5 class="m-0">Subject Performance Overview</h5>
              </div>
              <div class="card-body">
                <canvas id="subjectChart"></canvas>
              </div>
            </div>
          </div>
        </div>

        <div class="row" v-if="selectedSubject">
          <div class="col-md-12 mb-4">
            <div class="card">
              <div
                class="card-header bg-success text-white d-flex justify-content-between align-items-center"
              >
                <h5 class="m-0">
                  Chapter Performance for {{ selectedSubject }}
                </h5>
                <button
                  class="btn btn-sm btn-light"
                  @click="selectedSubject = null"
                >
                  Back to All Subjects
                </button>
              </div>
              <div class="card-body">
                <canvas id="chapterChart"></canvas>
              </div>
            </div>
          </div>
        </div>

        <div class="row" v-else>
          <div class="col-md-12">
            <div class="card">
              <div class="card-header bg-info text-white">
                <h5 class="m-0">Subject Breakdown</h5>
              </div>
              <div class="card-body">
                <div class="subject-selector">
                  <div
                    v-for="subject in Object.keys(subjectData)"
                    :key="subject"
                    class="subject-item"
                  >
                    <button
                      class="btn btn-outline-primary mb-2"
                      @click="showChapterChart(subject)"
                    >
                      {{ subject }} Details
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script>
import Chart from "chart.js/auto";
import { make_getrequest } from "@/stores/appState";

export default {
  name: "MyStatsView",
  data() {
    return {
      scores: [],
      subjectChart: null,
      chapterChart: null,
      selectedSubject: null,
      subjectData: {},
      chapterData: {},
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
    };
  },
  computed: {
    averageScore() {
      return this.stats.average_score;
    },
    uniqueSubjectsCount() {
      return this.stats.activity_summary.subjects_attempted;
    },
  },
  mounted() {
    this.fetchStats();
  },
  methods: {
    async fetchStats() {
      this.loading = true;
      this.error = null;

      try {
        const response = await make_getrequest("/my_quiz_stats");
        if (!response || !response.stats) {
          this.error = "Failed to load statistics data";
          console.error("Invalid response format:", response);
          return;
        }

        this.stats = response.stats;
        this.scores = this.stats.subject_breakdown.flatMap((subject) =>
          Array(subject.quizzes_taken)
            .fill()
            .map(() => ({
              subject_name: subject.subject_name,
              score: subject.average_score,
            }))
        );

        this.processData();

        this.$nextTick(() => {
          this.initializeCharts();
        });
      } catch (error) {
        this.error = "An error occurred while fetching your statistics";
        console.error("Error fetching stats:", error);
      } finally {
        this.loading = false;
      }
    },

    initializeCharts() {
      if (
        !this.error &&
        this.stats.subject_breakdown &&
        this.stats.subject_breakdown.length > 0
      ) {
        this.createSubjectChart();
      }
    },

    getTrendClass() {
      const trendMap = {
        improving: "text-success",
        declining: "text-danger",
        stable: "text-muted",
      };
      return trendMap[this.stats.performance_trend] || "text-muted";
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

    processData() {
      this.subjectData = {};
      this.chapterData = {};

      this.stats.subject_breakdown.forEach((subject) => {
        const subjectName = subject.subject_name;

        this.subjectData[subjectName] = {
          totalScore: subject.average_score * subject.quizzes_taken,
          count: subject.quizzes_taken,
          averageScore: subject.average_score,
        };

        this.chapterData[subjectName] = {
          Overall: {
            totalScore: subject.average_score * subject.quizzes_taken,
            count: subject.quizzes_taken,
            averageScore: subject.average_score,
          },
        };
      });
    },
    createSubjectChart() {
      const chartElement = document.getElementById("subjectChart");
      if (!chartElement) {
        console.warn("Subject chart element not found in DOM");
        return;
      }

      const ctx = chartElement.getContext("2d");
      if (!ctx) {
        console.warn("Could not get 2d context from chart element");
        return;
      }

      if (this.subjectChart) {
        this.subjectChart.destroy();
      }

      const subjects = Object.keys(this.subjectData);
      if (subjects.length === 0) {
        console.warn("No subject data available for chart");
        return;
      }

      const averageScores = subjects.map(
        (subject) => this.subjectData[subject].averageScore
      );
      const totalQuizzes = subjects.map(
        (subject) => this.subjectData[subject].count
      );

      this.subjectChart = new Chart(ctx, {
        type: "bar",
        data: {
          labels: subjects,
          datasets: [
            {
              label: "Average Score",
              data: averageScores,
              backgroundColor: "rgba(54, 162, 235, 0.7)",
              borderColor: "rgba(54, 162, 235, 1)",
              borderWidth: 1,
              yAxisID: "y",
            },
            {
              label: "Number of Quizzes",
              data: totalQuizzes,
              backgroundColor: "rgba(255, 99, 132, 0.7)",
              borderColor: "rgba(255, 99, 132, 1)",
              borderWidth: 1,
              yAxisID: "y1",
            },
          ],
        },
        options: {
          responsive: true,
          scales: {
            y: {
              type: "linear",
              position: "left",
              title: {
                display: true,
                text: "Average Score",
              },
              min: 0,
              max: 100,
            },
            y1: {
              type: "linear",
              position: "right",
              title: {
                display: true,
                text: "Quiz Count",
              },
              grid: {
                drawOnChartArea: false,
              },
            },
          },
          onClick: (e, activeElements) => {
            if (activeElements.length > 0) {
              const index = activeElements[0].index;
              const subject = subjects[index];
              this.showChapterChart(subject);
            }
          },
        },
      });
    },
    createChapterChart(subject) {
      const chartElement = document.getElementById("chapterChart");
      if (!chartElement) {
        console.warn("Chapter chart element not found in DOM");
        return;
      }

      const ctx = chartElement.getContext("2d");
      if (!ctx) {
        console.warn("Could not get 2d context from chart element");
        return;
      }

      if (this.chapterChart) {
        this.chapterChart.destroy();
      }

      const chapters = Object.keys(this.chapterData[subject] || {});
      const averageScores = chapters.map(
        (chapter) => this.chapterData[subject][chapter].averageScore
      );
      const quizCounts = chapters.map(
        (chapter) => this.chapterData[subject][chapter].count
      );

      this.chapterChart = new Chart(ctx, {
        type: "bar",
        data: {
          labels: chapters,
          datasets: [
            {
              label: "Average Score",
              data: averageScores,
              backgroundColor: "rgba(75, 192, 192, 0.7)",
              borderColor: "rgba(75, 192, 192, 1)",
              borderWidth: 1,
              yAxisID: "y",
            },
            {
              label: "Number of Quizzes",
              data: quizCounts,
              backgroundColor: "rgba(153, 102, 255, 0.7)",
              borderColor: "rgba(153, 102, 255, 1)",
              borderWidth: 1,
              yAxisID: "y1",
            },
          ],
        },
        options: {
          responsive: true,
          scales: {
            y: {
              type: "linear",
              position: "left",
              title: {
                display: true,
                text: "Average Score",
              },
              min: 0,
              max: 100,
            },
            y1: {
              type: "linear",
              position: "right",
              title: {
                display: true,
                text: "Quiz Count",
              },
              grid: {
                drawOnChartArea: false,
              },
            },
          },
        },
      });
    },
    showChapterChart(subject) {
      this.selectedSubject = subject;
      this.$nextTick(() => {
        this.createChapterChart(subject);
      });
    },
  },
  beforeUnmount() {
    if (this.subjectChart) {
      this.subjectChart.destroy();
    }
    if (this.chapterChart) {
      this.chapterChart.destroy();
    }
  },
};
</script>

<style scoped>
.stats-view {
  max-width: 1000px;
}
.stats-chart-container {
  margin-top: 20px;
}
.subject-selector {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  justify-content: center;
}
.subject-item {
  margin-bottom: 5px;
}
.display-4 {
  font-size: 2.5rem;
}
.bg-purple {
  background-color: #6f42c1;
}
.achievement-badge {
  background-color: #f8f9fa;
  border-radius: 10px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  text-align: center;
  min-width: 180px;
  max-width: 200px;
}
.achievement-icon {
  font-size: 2.5rem;
  margin-bottom: 10px;
}
.achievement-title {
  font-size: 1rem;
  font-weight: bold;
  margin-bottom: 5px;
}
.achievement-desc {
  font-size: 0.8rem;
  color: #6c757d;
}
</style>
