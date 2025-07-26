<template>
  <div class="quiz-component height-100 d-flex flex-row w-100">
    <QuizSubmittionSubNav
      :quiz_id="quiz_id"
      @select-question="handleQuestionSelect"
    />
    <div class="content flex-grow-1 p-3 overflow-auto">
      <DisplayQuestion :questions="questions" />
    </div>
  </div>
</template>

<script>
import QuizSubmittionSubNav from "./userdashboardfragments/QuizSubmittionSubNav.vue";
import DisplayQuestion from "./userdashboardfragments/DisplayQuestion.vue";
import { make_getrequest } from "@/stores/appState";

export default {
  name: "QuizPage",
  props: {
    quiz_id: {
      type: Number,
      required: true,
    },
  },
  data() {
    return {
      questions: [],
    };
  },
  methods: {
    async fetchquestionsForQuiz() {
      const response = await make_getrequest("/fetchQuestions", {
        quiz_id: this.quiz_id,
      });
      console.log("fetch questions response", response.data);
      this.questions = response.data;
    },
    handleQuestionSelect(selectedQuestion) {
      console.log("Selected question:", selectedQuestion);
    },
  },
  components: {
    QuizSubmittionSubNav,
    DisplayQuestion,
  },
  mounted() {
    this.fetchquestionsForQuiz();
  },
};
</script>

<style scoped>
.quiz-component {
  display: flex;
  flex-direction: row;
  width: 100%;
  height: 100vh;
  overflow: hidden;
}
.content {
  overflow-y: auto;
}
</style>
