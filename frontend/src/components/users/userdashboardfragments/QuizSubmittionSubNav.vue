<template>
  <div class="d-flex flex-row" style="height: 100vh; overflow: hidden">
    <div
      class="d-flex flex-column bg-white p-3 overflow-auto"
      style="width: 380px; flex-shrink: 0"
    >
      <p class="mb-3"><strong>Quiz ID:</strong> {{ quiz_id }}</p>
      <div v-if="quizEndedMessage">
        <strong class="text-success">{{ quizEndedMessage }}</strong>
      </div>
      <div v-else>
        <div
          v-if="countdown.minutes >= 0 && countdown.seconds >= 0"
          class="mb-3"
        >
          <strong>
            Quiz starts in: {{ countdown.minutes }}:{{
              countdown.seconds.toString().padStart(2, "0")
            }}
          </strong>
        </div>
        <QuestionGridBlock :quiz_id="quiz_id" class="mb-3" />
        <button class="btn btn-danger" @click="triggerSocketToEndQuiz">
          End Quiz
        </button>
      </div>
    </div>
    <div class="flex-grow-1 bg-light p-3">
      <slot></slot>
    </div>
  </div>
</template>

<script>
import { useRouter } from "vue-router";
import QuestionGridBlock from "./QuestionGridBlock.vue";
import { io } from "socket.io-client";

export default {
  name: "QuizSubmissionSubNav",
  props: {
    quiz_id: {
      type: Number,
      required: true,
    },
    quiz_start_time: {
      type: String, // Expecting ISO 8601 format (e.g., "2023-10-01T10:00:00Z")
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
  data() {
    return {
      socket: null,
      countdown: { minutes: -1, seconds: -1 }, // Countdown timer state
      quizEndedMessage: "", // State to store the quiz ended message
      countdownInterval: null, // Interval for updating the countdown
    };
  },
  created() {
    const token = localStorage.getItem("token"); // Retrieve JWT token from local storage
    if (!token) {
      console.error("JWT token not found in local storage.");
      return;
    }

    this.socket = io("http://localhost:5000", {
      auth: {
        token: token, // Send the JWT token as part of the socket authentication
      },
    });

    this.socket.on("connect", () => {
      console.log("Socket connected:", this.socket.id);

      // Automatically join the quiz room
      this.socket.emit("join_quiz", { quiz_id: this.quiz_id });
    });

    // Listen for quiz ended event
    this.socket.on("quiz_ended", (data) => {
      this.quizEndedMessage = "You have completed your test"; // Set the message
      console.log(`Quiz ${data.quiz_id} has ended`);
    });

    // Start the countdown timer
    this.startCountdown();
  },
  methods: {
    startCountdown() {
      const quizStartTime = new Date(this.quiz_start_time).getTime();
      this.countdownInterval = setInterval(() => {
        const now = new Date().getTime();
        const timeDifference = quizStartTime - now;

        if (timeDifference <= 0) {
          clearInterval(this.countdownInterval);
          this.countdown = { minutes: 0, seconds: 0 };
          console.log("Quiz has started!");
        } else {
          const minutes = Math.floor(timeDifference / (1000 * 60));
          const seconds = Math.floor((timeDifference % (1000 * 60)) / 1000);
          this.countdown = { minutes, seconds };
        }
      }, 1000);
    },
    triggerSocketToEndQuiz() {
      if (this.socket) {
        this.socket.emit("endquiz");
      } else {
        console.error("Socket is not initialized.");
      }
    },
  },
  beforeUnmount() {
    if (this.socket) {
      this.socket.disconnect();
    }
    if (this.countdownInterval) {
      clearInterval(this.countdownInterval);
    }
    this.triggerSocketToEndQuiz();
  },
};
</script>

<style scoped>
.d-flex {
  overflow-y: auto;
}
</style>
