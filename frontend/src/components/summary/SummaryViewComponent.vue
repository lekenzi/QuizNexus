<template>
  <!-- this page will give you a sumarry of all the application stats -->

  <!-- need to make 2 components one is highest score subject-wise and other is subject wise quize attempts -->
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
