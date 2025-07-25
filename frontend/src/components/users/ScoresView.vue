<template>
  <div class="scores-view container mt-5 p-4 bg-light rounded shadow">
    <h1 class="title text-center text-primary mb-3">Your Scores</h1>
    <p class="description text-center text-secondary mb-4">
      Below are your scores displayed in a table format:
    </p>
    <ScoresTableComponent :scores="scores" />
  </div>
</template>

<script>
import make_getrequest from "@/stores/appState";
import ScoresTableComponent from "./userdashboardfragments/ScoresTableComponent.vue";

export default {
  name: "ScoresView",
  data() {
    return {
      scores: [],
    };
  },
  created() {
    this.fetchScores();
  },
  components: {
    ScoresTableComponent,
  },
  methods: {
    async fetchScores() {
      try {
        const response = await make_getrequest("/scores");
        if (!response || !response.data) {
          console.error("Invalid response format:", response);
          return;
        }
        this.scores = response.data;
      } catch (error) {
        console.error("Error fetching scores:", error);
      }
    },
  },
};
</script>

<style scoped>
.scores-view {
  max-width: 800px;
}
</style>
