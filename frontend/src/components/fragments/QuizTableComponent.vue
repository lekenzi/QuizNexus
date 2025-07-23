<template>
  <div
    class="quiz-card-component shadow-sm m-4"
    v-if="Object.keys(quizzes).length"
    style="width: 400px; padding: 20px"
  >
    <div class="card-header bg-primary text-white">
      <h2 class="mb-0">{{ quizzes.subject_name }}</h2>
    </div>
    <div class="card-body">
      <div class="quiz-details">
        <p><strong>Chapter:</strong> {{ quizzes.chapter_name }}</p>
        <p><strong>Quiz Title:</strong> {{ quizzes.quiz_title }}</p>
        <p>
          <strong>Number of Questions:</strong>
          {{ quizzes.number_of_questions }}
        </p>
      </div>
    </div>
    <div class="d-flex justify-content-between align-items-center mt-3">
      <ViewAndAddQuestionsModal :quiz="quizzes" />
      <button class="btn btn-danger" @click="$emit('delete-quiz', quizzes)">
        <i class="fas fa-trash-alt"></i> Delete Quiz
      </button>
    </div>
  </div>
</template>

<script>
import ViewAndAddQuestionsModal from "@/components/fragments/ViewAndAddQuestionsModal.vue";
export default {
  name: "QuizTableComponent",
  props: {
    quizzes: {
      type: Object,
      default: () => ({}),
    },
  },
  components: {
    ViewAndAddQuestionsModal,
  },
};
</script>

<style scoped>
.quiz-card-component {
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
</style>
