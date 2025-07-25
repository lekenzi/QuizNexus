<template>
  <div>
    <div class="d-flex flex-row" style="height: 100vh">
      <div
        class="d-flex flex-column align-items-stretch flex-shrink-0 bg-white"
        style="width: 380px; height: 100%; overflow-y: auto"
      >
        <p>{{ quiz_id }}</p>
        <div
          v-if="quiz.questions && quiz.questions.length > 0"
          class="list-group list-group-flush border-bottom scrollarea"
        >
          <div
            v-for="(question, index) in quiz.questions"
            :key="index"
            class="list-group-item list-group-item-action py-3 lh-tight"
            @click="navigateToQuestion(index)"
          >
            <div
              class="d-flex w-100 align-items-center justify-content-between"
            >
              <strong class="mb-1">Question {{ index + 1 }}</strong>
              <small>Marks: {{ question.marks }}</small>
            </div>
            <div class="col-10 mb-1 small">
              {{ question.question }}
            </div>
            <ul>
              <li
                v-for="(option, optIndex) in question.options"
                :key="optIndex"
              >
                {{ option }}
              </li>
            </ul>
          </div>
        </div>
        <div v-else>
          <p>No questions available for this quiz.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useRouter } from "vue-router";

export default {
  name: "QuizSubmissionSubNav",
  props: {
    quiz_id: {
      type: Number,
      required: true,
    },
    quiz: {
      type: Object,
      required: true, // Ensure the quiz object is passed as a prop
    },
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
};
</script>
