<template>
  <div class="container">
    <h1>Summary</h1>
    <TopScoreComponent />
  </div>
</template>

<script>
import TopScoreComponent from "./TopScoreComponent.vue";
export default {
  name: "SummaryViewComponent",
  components: {
    TopScoreComponent,
  },
};
</script>
