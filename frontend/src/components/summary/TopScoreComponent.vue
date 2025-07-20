<template>
  <!-- add the chart js component and then get this imported into the main summary component -->
  <canvas id="topScoreChart"></canvas>
</template>

<script>
import { onMounted } from "vue";
import Chart from "chart.js/auto";

export default {
  name: "TopScoreComponent",
  setup() {
    onMounted(() => {
      const ctx = document.getElementById("topScoreChart").getContext("2d");
      new Chart(ctx, {
        type: "bar",
        data: {
          labels: ["Subject 1", "Subject 2", "Subject 3"],
          datasets: [
            {
              label: "Highest Scores",
              data: [95, 85, 90],
              backgroundColor: "rgba(75, 192, 192, 0.2)",
              borderColor: "rgba(75, 192, 192, 1)",
              borderWidth: 1,
            },
          ],
        },
        options: {
          scales: {
            y: {
              beginAtZero: true,
            },
          },
        },
      });
    });
  },
};
</script>

<style scoped>
#topScoreChart {
  background-color: white;
}
</style>
