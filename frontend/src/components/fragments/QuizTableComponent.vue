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
    <AddQuestionsToQuizzesModal
      :quiz_id="quizzes.quiz_id"
      :subject_id="quizzes.subject_id"
      :chapter_id="quizzes.chapter_id"
      :chapter_name="quizzes.chapter_name"
      :quiz_title="quizzes.quiz_title"
    />
  </div>
</template>

<script>
import AddQuestionsToQuizzesModal from "@/components/fragments/AddQuestionsToQuizzesModal.vue";
export default {
  name: "QuizTableComponent",
  props: {
    quizzes: {
      type: Object,
      default: () => ({}),
    },
  },
  mounted() {
    console.log("Quizzes in QuizTableComponent:", this.quizzes);
  },
  components: {
    AddQuestionsToQuizzesModal,
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
