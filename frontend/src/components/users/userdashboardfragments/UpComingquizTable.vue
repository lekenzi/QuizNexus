<template>
  <div
    class="upcoming-quiz-container d-flex flex-column align-items-center p-4 bg-light rounded shadow-sm"
  >
    <h5 class="mb-4 text-primary font-weight-bold">Upcoming Quizzes</h5>
    <table class="table table-bordered table-hover table-striped">
      <thead class="thead-dark">
        <tr>
          <th scope="col">Quiz Title</th>
          <th scope="col">Date</th>
          <th scope="col">Time</th>
          <th scope="col">Duration</th>
          <th scope="col">Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="quiz in quizzes" :key="quiz.id">
          <td class="font-weight-bold text-secondary">{{ quiz.title }}</td>
          <td class="text-muted">{{ formatDateOnly(quiz.date_of_quiz) }}</td>
          <td class="text-muted">{{ formatTimeOnly(quiz.time_of_day) }}</td>
          <td>{{ quiz.duration }} minutes</td>
          <td>
            <button
              v-if="
                canTakeQuiz(quiz.date_of_quiz, quiz.time_of_day, quiz.duration)
              "
              class="btn btn-success btn-sm"
              @click="handleAction(quiz.id)"
            >
              Take Quiz
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  name: "UpComingQuizTable",
  props: {
    quizzes: {
      type: Array,
      required: true,
      default: () => [],
    },
  },
  methods: {
    canTakeQuiz(date, time, duration) {
      if (!date || !time || !duration) return false;
      // Extract date part (YYYY-MM-DD)
      const datePart = date.split("T")[0];
      // Remove microseconds from time if present (e.g., "20:00:00.000001" -> "20:00:00")
      const timePart = time.split(".")[0];
      // Combine to ISO string
      const isoString = `${datePart}T${timePart}`;
      const quizStartTime = new Date(isoString).getTime();
      const quizEndTime = quizStartTime + duration * 60 * 1000;
      const now = new Date().getTime();
      return now >= quizStartTime && now <= quizEndTime; // Return true if the current time is within the quiz time range
    },
    handleAction(quizId) {
      this.$router.push({ name: "quiz_page", params: { quiz_id: quizId } });
    },
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
.upcoming-quiz-container {
  display: flex;
  flex-direction: column;
  margin: 0 auto;
}
</style>
<style scoped>
.upcoming-quiz-container {
  display: flex;
  flex-direction: column;
  margin: 0 auto;
}
</style>
