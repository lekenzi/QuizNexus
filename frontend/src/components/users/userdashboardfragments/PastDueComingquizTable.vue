<template>
  <div
    class="past-due-quiz-container d-flex flex-column align-items-center p-4 bg-light rounded shadow-sm"
  >
    <h5 class="mb-4 text-danger font-weight-bold">Past Due Quizzes</h5>
    <table class="table table-bordered table-hover table-striped">
      <thead class="thead-dark">
        <tr>
          <th scope="col">Quiz Title</th>
          <th scope="col">Date</th>
          <th scope="col">Time</th>
          <th scope="col">Duration</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="quiz in quizzes" :key="quiz.id">
          <td class="font-weight-bold text-secondary">{{ quiz.title }}</td>
          <td class="text-muted">{{ formatDateOnly(quiz.date_of_quiz) }}</td>
          <td class="text-muted">{{ formatTimeOnly(quiz.time_of_day) }}</td>
          <td>{{ quiz.duration }} minutes</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  name: "PastDueComingquizTable",
  props: {
    quizzes: {
      type: Array,
      required: true,
      default: () => [],
    },
  },
  methods: {
    formatDateOnly(dateString) {
      if (!dateString) return "N/A";
      // Extract just the date part from ISO string
      const date = new Date(dateString);
      if (isNaN(date)) return dateString;
      return date.toLocaleDateString();
    },

    formatTimeOnly(timeString) {
      if (!timeString) return "N/A";

      // If it's a full ISO string, extract just the time
      if (timeString.includes("T")) {
        const timePart = timeString.split("T")[1];
        return timePart.split(".")[0]; // Remove milliseconds if present
      }

      // If it's already just a time string
      return timeString.split(".")[0]; // Remove any milliseconds
    },
  },
};
</script>

<style scoped>
.past-due-quiz-container {
  display: flex;
  flex-direction: column;
  margin: 0 auto;
}
</style>
