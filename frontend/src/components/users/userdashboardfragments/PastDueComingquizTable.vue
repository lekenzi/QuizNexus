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
          <td class="text-muted">{{ quiz.date_of_quiz }}</td>
          <td class="text-muted">{{ quiz.time_of_day }}</td>
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
};
</script>

<style scoped>
.past-due-quiz-container {
  display: flex;
  flex-direction: column;
  margin: 0 auto;
}
</style>
