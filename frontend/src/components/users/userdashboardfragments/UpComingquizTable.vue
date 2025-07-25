<template>
  <div
    class="upcoming-quiz-container d-flex flex-column align-items-center p-4 bg-light rounded shadow-sm"
  >
    <h5 class="mb-4 text-primary font-weight-bold">Upcoming Quizzes</h5>
    <table class="table table-bordered table-hover table-striped">
      <thead class="thead-dark">
        <tr>
          <th scope="col">Quiz Title</th>
          <th scope="col">Due Date</th>
          <th scope="col">Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="quiz in quizzes?.data || []" :key="quiz.id">
          <td class="font-weight-bold text-secondary">{{ quiz.title }}</td>
          <td class="text-muted">{{ formatDate(quiz.date_of_quiz) }}</td>
          <td>
            <button
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
      type: Object,
      required: true,
      default: () => ({ data: [] }),
    },
  },
  methods: {
    formatDate(date) {
      const options = { year: "numeric", month: "long", day: "numeric" };
      return new Date(date).toLocaleDateString(undefined, options);
    },
    handleAction(quizId) {
      console.log(`Action triggered for quiz ID: ${quizId}`);
      this.$router.push({ name: "quiz_page", params: { quiz_id: quizId } });
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
