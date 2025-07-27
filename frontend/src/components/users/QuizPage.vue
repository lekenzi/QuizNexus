<template>
  <div class="quiz-component height-100 d-flex flex-row w-100">
    <QuizSubmittionSubNav
      :quiz_id="quiz_id"
      :questions="Array.isArray(questions.questions) ? questions.questions : []"
      :answeredQuestions="answeredQuestions"
      :countdown="countdown"
      :quizStarted="quizStarted"
      :quizEndedMessage="quizEndedMessage"
      :quizTitle="questions.quiz_title || 'Quiz'"
      :quizDuration="quizDuration"
      :subjectName="questions.subject_name || 'Subject'"
      :chapterName="questions.chapter_name || 'Chapter'"
      @end-quiz="autoSubmitQuiz"
    />
    <div class="content flex-grow-1 p-3 overflow-auto">
      <div v-if="quizStarted && !quizEnded">
        <div class="countdown mb-3">
          <strong
            >Time left: {{ countdown.minutes }}m
            {{ countdown.seconds }}s</strong
          >
        </div>
        <DisplayQuestion :questions="questions" @answered="markAnswered" />
      </div>
      <div v-else-if="!quizStarted && quizStartTime">
        <div class="countdown mb-3">
          <strong
            >Quiz starts in: {{ countdown.minutes }}m
            {{ countdown.seconds }}s</strong
          >
        </div>
      </div>
      <div v-else-if="quizEnded">
        <div class="alert alert-success">
          {{
            quizEndedMessage ||
            "Quiz time is over! Your responses have been submitted."
          }}
        </div>
      </div>
      <div v-else>
        <div class="alert alert-warning">Loading quiz details...</div>
      </div>
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
      questions: {},
      quizStartTime: "",
      rawStartTime: "",
      quizDuration: 0,
      answeredQuestions: {},
      countdown: { minutes: 0, seconds: 0 },
      quizStarted: false,
      quizEnded: false,
      quizEndedMessage: "",
      countdownInterval: null,
      debugMode: true,
    };
  },
  methods: {
    async fetchquestionsForQuiz() {
      try {
        const response = await make_getrequest("/fetchQuestions", {
          quiz_id: this.quiz_id,
        });

        this.questions = response.data || {};

        this.rawStartTime = response.data?.time_of_day || "";

        const quizStartDate = this.constructQuizStartDate(
          response.data?.time_of_day
        );
        this.quizStartTime = quizStartDate ? quizStartDate.toISOString() : "";

        this.quizDuration = response.data?.time_duration || 0;

        if (this.quizStartTime && this.quizDuration) {
          this.startCountdown();
        } else {
          this.quizEndedMessage =
            "Invalid quiz configuration. Please contact support.";
          this.quizEnded = true;
        }
      } catch (error) {
        console.error("Failed to fetch quiz questions:", error);
        this.quizEndedMessage = "Failed to load quiz details.";
        this.quizEnded = true;
      }
    },

    constructQuizStartDate(timeOfDay) {
      if (!timeOfDay) return null;

      const [hours, minutes, seconds] = timeOfDay.split(":").map(Number);

      if (
        isNaN(hours) ||
        isNaN(minutes) ||
        (seconds !== undefined && isNaN(seconds))
      ) {
        console.error("Invalid time format:", timeOfDay);
        return null;
      }

      const today = new Date();
      today.setHours(hours, minutes, seconds || 0, 0);

      return today;
    },

    handleQuestionSelect(selectedQuestion) {
      selectedQuestion;
    },

    markAnswered(questionId) {
      this.$set(this.answeredQuestions, questionId, true);
    },

    startCountdown() {
      if (!this.quizStartTime) {
        console.error("Cannot start countdown: Missing quiz start time");
        return;
      }

      const startTime = new Date(this.quizStartTime).getTime();
      const durationMs = this.quizDuration * 60 * 1000;
      const endTime = startTime + durationMs;

      const updateTimer = () => {
        const now = new Date().getTime();

        if (now >= startTime && now < endTime) {
          this.quizStarted = true;
          const diff = endTime - now;
          this.countdown = {
            minutes: Math.floor(diff / (1000 * 60)),
            seconds: Math.floor((diff / 1000) % 60),
          };
        } else if (now < startTime) {
          this.quizStarted = false;
          const diff = startTime - now;
          this.countdown = {
            minutes: Math.floor(diff / (1000 * 60)),
            seconds: Math.floor((diff / 1000) % 60),
          };
        } else {
          this.countdown = { minutes: 0, seconds: 0 };
          this.autoSubmitQuiz(
            "Quiz time is over! Your responses have been submitted."
          );
        }
      };

      updateTimer();
      this.countdownInterval = setInterval(updateTimer, 1000);
    },

    autoSubmitQuiz(message = "Quiz submitted successfully.") {
      if (this.quizEnded) return;

      this.quizEnded = true;
      this.quizEndedMessage = message;
      if (this.countdownInterval) {
        clearInterval(this.countdownInterval);
        this.countdownInterval = null;
      }
    },
  },
  components: {
    QuizSubmittionSubNav,
    DisplayQuestion,
  },
  mounted() {
    this.fetchquestionsForQuiz();
  },
  beforeUnmount() {
    if (this.countdownInterval) {
      clearInterval(this.countdownInterval);
    }
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
.countdown {
  font-size: 1.2em;
}
</style>
