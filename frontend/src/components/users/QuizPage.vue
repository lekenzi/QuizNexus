<template>
  <div class="d-flex flex-row flex-shrink-0 w-100">
    <QuizSubmittionSubNav
      :quiz_id="quiz_id"
      :quiz="quiz"
      @select-question="handleQuestionSelect"
    />
    <div class="content flex-grow-1 p-3">
      <DisplayQuestion v-if="selectedQuestion" :question="selectedQuestion" />
    </div>
  </div>
</template>

<script>
import QuizSubmittionSubNav from "./userdashboardfragments/QuizSubmittionSubNav.vue";
import DisplayQuestion from "./userdashboardfragments/DisplayQuestion.vue";
import { ref } from "vue";

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
      quiz: {
        quiz_id: 1,
        number_of_questions: 5,
        time_duration: 30,
        questions: [
          {
            id: 1,
            question: "What is the capital of France?",
            options: ["Paris", "London", "Berlin", "Madrid"],
            answer: "Paris",
            marks: 5,
          },
          {
            id: 2,
            question: "What is 2 + 2?",
            options: ["3", "4", "5", "6"],
            answer: "4",
            marks: 2,
          },
        ],
      },
      selectedQuestion: null,
    };
  },
  components: {
    QuizSubmittionSubNav,
    DisplayQuestion,
  },
  setup() {
    const selectedQuestion = ref(null);

    const handleQuestionSelect = (question) => {
      selectedQuestion.value = question;
    };

    return {
      handleQuestionSelect,
    };
  },
};
</script>
