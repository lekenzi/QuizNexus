<template>
  <div class="stats-view container mt-5 p-4 bg-light rounded shadow">
    <h1 class="title text-center text-primary mb-3">
      My Performance Statistics
    </h1>

    <!-- Stats Summary -->
    <div class="row mb-4">
      <div class="col-md-4">
        <div class="card text-white bg-primary">
          <div class="card-body text-center">
            <h5 class="card-title">Total Quizzes</h5>
            <p class="card-text display-4">{{ scores.length }}</p>
          </div>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card text-white bg-success">
          <div class="card-body text-center">
            <h5 class="card-title">Average Score</h5>
            <p class="card-text display-4">{{ averageScore }}%</p>
          </div>
        </div>
      </div>
      <div class="col-md-4">
        <div class="card text-white bg-info">
          <div class="card-body text-center">
            <h5 class="card-title">Subjects Covered</h5>
            <p class="card-text display-4">{{ uniqueSubjectsCount }}</p>
          </div>
        </div>
      </div>
    </div>

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
              <h5 class="m-0">Chapter Performance for {{ selectedSubject }}</h5>
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
    };
  },
  computed: {
    averageScore() {
      if (this.scores.length === 0) return 0;
      const sum = this.scores.reduce((acc, score) => acc + score.score, 0);
      return (sum / this.scores.length).toFixed(1);
    },
    uniqueSubjectsCount() {
      if (this.scores.length === 0) return 0;
      const subjects = new Set(
        this.scores.map((score) => score.subject_name).filter(Boolean)
      );
      return subjects.size;
    },
  },
  mounted() {
    this.fetchScores();
  },
  methods: {
    async fetchScores() {
      try {
        const response = await make_getrequest("/scoreboard");
        if (!response || !response.scores) {
          console.error("Invalid response format:", response);
          return;
        }

        this.scores = response.scores;

        this.processData();
        this.createSubjectChart();
      } catch (error) {
        console.error("Error fetching scores:", error);
      }
    },
    processData() {
      // Reset data
      this.subjectData = {};
      this.chapterData = {};

      // Process scores to get subject and chapter data
      this.scores.forEach((score) => {
        const subjectName = score.subject_name || "Unknown Subject";
        const chapterName = score.chapter_name || "Unknown Chapter";
        const scoreValue = score.score;

        // Process subject data
        if (!this.subjectData[subjectName]) {
          this.subjectData[subjectName] = {
            totalScore: 0,
            count: 0,
            averageScore: 0,
          };
        }
        this.subjectData[subjectName].totalScore += scoreValue;
        this.subjectData[subjectName].count += 1;
        this.subjectData[subjectName].averageScore =
          this.subjectData[subjectName].totalScore /
          this.subjectData[subjectName].count;

        // Process chapter data
        if (!this.chapterData[subjectName]) {
          this.chapterData[subjectName] = {};
        }
        if (!this.chapterData[subjectName][chapterName]) {
          this.chapterData[subjectName][chapterName] = {
            totalScore: 0,
            count: 0,
            averageScore: 0,
          };
        }
        this.chapterData[subjectName][chapterName].totalScore += scoreValue;
        this.chapterData[subjectName][chapterName].count += 1;
        this.chapterData[subjectName][chapterName].averageScore =
          this.chapterData[subjectName][chapterName].totalScore /
          this.chapterData[subjectName][chapterName].count;
      });
    },
    createSubjectChart() {
      const ctx = document.getElementById("subjectChart").getContext("2d");

      const subjects = Object.keys(this.subjectData);
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
      if (this.chapterChart) {
        this.chapterChart.destroy();
      }

      const ctx = document.getElementById("chapterChart").getContext("2d");

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
</style>
