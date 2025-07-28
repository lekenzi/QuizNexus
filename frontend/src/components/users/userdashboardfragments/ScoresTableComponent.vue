<template>
  <div>
    <table class="table table-striped table-bordered">
      <thead class="thead-light">
        <tr>
          <th>ID</th>
          <th>Quiz Title</th>
          <th>Subject</th>
          <th>Chapter</th>
          <th>Score</th>
          <th>Date</th>
          <th>Time</th>
        </tr>
      </thead>
      <tbody v-if="scores.length > 0">
        <tr v-for="score in scores" :key="score.id">
          <td>{{ score.id }}</td>
          <td>{{ score.quiz_title || "N/A" }}</td>
          <td>{{ score.subject_name || "N/A" }}</td>
          <td>{{ score.chapter_name || "N/A" }}</td>
          <td>{{ score.score }}</td>
          <td>{{ formatDate(score.timestamp) }}</td>
          <td>{{ formatTime(score.timestamp) }}</td>
        </tr>
      </tbody>
      <tbody v-else>
        <tr>
          <td colspan="7" class="text-center text-muted">
            No scores available
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  name: "ScoresTableComponent", // Corrected component name
  props: {
    scores: {
      type: Array,
      default: () => [],
    },
  },
  methods: {
    formatDate(isoString) {
      if (!isoString) return "N/A";
      const date = new Date(isoString);
      if (isNaN(date)) return isoString;
      return date.toLocaleDateString();
    },
    formatTime(isoString) {
      if (!isoString) return "N/A";
      const date = new Date(isoString);
      if (isNaN(date)) return "";
      return date.toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
      });
    },
  },
};
</script>

<style scoped>
.table {
  background-color: white;
}
</style>
