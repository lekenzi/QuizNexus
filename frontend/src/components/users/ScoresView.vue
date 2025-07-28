<template>
  <div class="scores-view container mt-5 p-4 bg-light rounded shadow">
    <h1 class="title text-center text-primary mb-3">Your Scores</h1>

    <div class="mb-4 text-center">
      <router-link to="/mystats" class="btn btn-primary">
        View Performance Charts
      </router-link>
    </div>

    <p class="description text-center text-secondary mb-4">
      Below are your scores displayed in a table format:
    </p>
    <ScoresTableComponent :scores="scores" />
  </div>
</template>

<script>
import { make_getrequest } from "@/stores/appState";
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
        const response = await make_getrequest("/scoreboard");
        if (!response || !response.scores) {
          console.error("Invalid response format:", response);
          return;
        }
        // API returns { scores: [...] }
        this.scores = response.scores;
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
