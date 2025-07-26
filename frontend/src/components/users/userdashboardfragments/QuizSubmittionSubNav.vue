<template>
  <div class="d-flex flex-row" style="height: 100vh; overflow: hidden">
    <div
      class="d-flex flex-column bg-white p-3 overflow-auto"
      style="width: 380px; flex-shrink: 0"
    >
      <p class="mb-3"><strong>Quiz ID:</strong> {{ quiz_id }}</p>
      <button
        type="button"
        class="btn btn-success mb-3"
        @click="triggerSocketToStartQuiz"
      >
        <strong>START QUIZ</strong>
      </button>
      <QuestionGridBlock :quiz_id="quiz_id" class="mb-3" />
      <button class="btn btn-danger" @click="triggerSocketToEndQuiz">
        End Quiz
      </button>
    </div>
    <div class="flex-grow-1 bg-light p-3">
      <slot></slot>
    </div>
  </div>
</template>

<script>
import { useRouter } from "vue-router";
import QuestionGridBlock from "./QuestionGridBlock.vue";
export default {
  name: "QuizSubmissionSubNav",
  props: {
    quiz_id: {
      type: Number,
      required: true,
    },
  },
  components: {
    QuestionGridBlock,
  },
  setup(props) {
    const router = useRouter();

    const navigateToQuestion = (index) => {
      const question = props.quiz?.questions?.[index];
      if (!question) {
        console.error("Question not found at index:", index);
        return;
      }
      router.push({
        name: "quiz_question",
        params: {
          quiz_id: props.quiz_id,
          questionIndex: index,
          quiz: props.quiz, // Pass the quiz object as a route parameter
        },
      });
    };

    return {
      navigateToQuestion,
    };
  },
  methods: {
    triggerSocketToStartQuiz() {
      console.log("Starting quiz with ID:", this.quiz_id);
      this.$emit("start-quiz", this.quiz_id);
    },
    triggerSocketToEndQuiz() {
      console.log("Ending quiz with ID:", this.quiz_id);
      this.$emit("end-quiz", this.quiz_id);
    },
  },
  beforeUnmount() {
    this.triggerSocketToEndQuiz();
    console.log(
      "QuizSubmissionSubNav component is being unmounted, ending quiz."
    );
  },
};
</script>

<style scoped>
.d-flex {
  overflow-y: auto;
}
</style>
