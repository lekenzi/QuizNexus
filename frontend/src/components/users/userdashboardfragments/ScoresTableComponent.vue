<template>
  <div>
    <table class="table table-striped table-bordered">
      <thead class="thead-light">
        <tr>
          <th>ID</th>
          <th>Quiz ID</th>
          <th>Quiz Title</th>
          <th>Subject Name</th>
          <th>Chapter Name</th>
          <th>Score</th>
          <th>Timestamp</th>
        </tr>
      </thead>
      <tbody v-if="scores.length > 0">
        <tr v-for="score in scores" :key="score.id">
          <td>{{ score.id }}</td>
          <td>{{ score.quiz_id }}</td>
          <td>{{ score.quiz_title || "N/A" }}</td>
          <td>{{ score.subject_name || "N/A" }}</td>
          <td>{{ score.chapter_name || "N/A" }}</td>
          <td>{{ score.score }}</td>
          <td>{{ score.timestamp }}</td>
        </tr>
      </tbody>
      <tbody v-else>
        <tr>
          <td colspan="7" class="text-center text-muted">No data available</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  name: "ScoresView",
  data() {
    return {
      userdetails: {},
    };
  },
  props: {
    scores: {
      type: Array,
      default: () => [],
    },
  },
};
</script>

<style scoped>
/* No custom styles needed as Bootstrap is used */
</style>
