<template>here your scores are displayed</template>
<script>
import axios from "axios";
export default {
  name: "ScoresView",
  data() {
    return {
      scores: [],
    };
  },
  created() {
    // this.fetchScores();
  },
  methods: {
    async fetchScores() {
      try {
        // Replace with your API endpoint to fetch scores
        const response = await axios.get("/api/scores");
        this.scores = response.data;
      } catch (error) {
        console.error("Error fetching scores:", error);
      }
    },
  },
};
</script>
