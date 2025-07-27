<template>
  <div class="d-flex flex-row" style="height: 100vh; overflow: hidden">
    <div
      class="d-flex flex-column bg-white p-3 overflow-auto"
      style="width: 380px; flex-shrink: 0"
    >
      <!-- Quiz Details Card -->
      <div class="card mb-3 border-0 bg-light">
        <div class="card-body">
          <h5 class="card-title text-primary">
            <i class="fas fa-clipboard-list me-2"></i>Quiz Details
          </h5>
          <div class="quiz-info">
            <p class="mb-2"><strong>Quiz ID:</strong> {{ quiz_id }}</p>
            <p class="mb-2"><strong>Title:</strong> {{ quizTitle }}</p>
            <p class="mb-2">
              <strong>Duration:</strong> {{ quizDuration }} minutes
            </p>
            <p class="mb-2">
              <strong>Questions:</strong> {{ questions.length }}
            </p>
            <p class="mb-2"><strong>Subject:</strong> {{ subjectName }}</p>
            <p class="mb-2"><strong>Chapter:</strong> {{ chapterName }}</p>
          </div>
        </div>
      </div>

      <div v-if="quizEndedMessage" class="alert alert-success">
        <i class="fas fa-check-circle me-2"></i>{{ quizEndedMessage }}
      </div>
      <div v-else>
        <!-- Timer Section -->
        <div class="card mb-3 border-0">
          <div class="card-body">
            <!-- Quiz hasn't started yet -->
            <div v-if="!quizStarted" class="text-center">
              <div class="countdown-circle">
                {{ countdown.minutes }}:{{
                  countdown.seconds.toString().padStart(2, "0")
                }}
              </div>
              <p class="text-info mt-2">Quiz starts in</p>
            </div>
            <!-- Quiz is running -->
            <div v-else class="text-center">
              <div class="countdown-circle running">
                {{ countdown.minutes }}:{{
                  countdown.seconds.toString().padStart(2, "0")
                }}
              </div>
              <p class="text-warning mt-2">Time remaining</p>
            </div>
          </div>
        </div>

        <!-- Progress Section -->
        <div class="card mb-3 border-0" v-if="quizStarted">
          <div class="card-body">
            <h6 class="card-subtitle mb-2 text-muted">Your Progress</h6>
            <div class="progress mb-2">
              <div
                class="progress-bar bg-success"
                role="progressbar"
                :style="{ width: progressPercentage + '%' }"
                :aria-valuenow="progressPercentage"
                aria-valuemin="0"
                aria-valuemax="100"
              >
                {{ progressPercentage }}%
              </div>
            </div>
            <small
              >{{ answeredCount }} of {{ questions.length }} questions
              answered</small
            >
          </div>
        </div>

        <!-- Question grid - only show when quiz has started -->
        <div v-if="quizStarted" class="card mb-3 border-0">
          <div class="card-body">
            <h6 class="card-subtitle mb-2 text-muted">Questions</h6>
            <div class="question-grid">
              <div
                v-for="(question, idx) in questions"
                :key="question.id"
                class="question-block"
                :class="{ answered: answeredQuestions[question.id] }"
              >
                {{ idx + 1 }}
              </div>
            </div>
          </div>
        </div>

        <!-- End quiz button - only show when quiz is active -->
        <button
          class="btn btn-danger w-100"
          @click="endQuiz"
          v-if="quizStarted && !quizEndedMessage"
        >
          <i class="fas fa-stop-circle me-2"></i>Submit Quiz
        </button>
      </div>
    </div>
    <div class="flex-grow-1 bg-light p-3">
      <slot></slot>
    </div>
  </div>
</template>

<script>
export default {
  name: "QuizSubmissionSubNav",
  props: {
    quiz_id: { type: Number, required: true },
    questions: { type: Array, required: true, default: () => [] },
    answeredQuestions: { type: Object, required: true, default: () => ({}) },
    countdown: {
      type: Object,
      required: true,
      default: () => ({ minutes: 0, seconds: 0 }),
    },
    quizStarted: { type: Boolean, required: true },
    quizEndedMessage: { type: String, required: false },
    quizTitle: { type: String, default: "Quiz" },
    quizDuration: { type: Number, default: 0 },
    subjectName: { type: String, default: "General" },
    chapterName: { type: String, default: "Not specified" },
  },
  computed: {
    answeredCount() {
      return Object.keys(this.answeredQuestions).length;
    },
    progressPercentage() {
      if (!this.questions.length) return 0;
      return Math.round((this.answeredCount / this.questions.length) * 100);
    },
  },
  methods: {
    endQuiz() {
      this.$emit("end-quiz", "Quiz submitted by user.");
    },
  },
};
</script>

<style scoped>
.d-flex {
  overflow-y: auto;
}

.quiz-info p {
  font-size: 0.9rem;
  color: #444;
}

.countdown-circle {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  background: #f8f9fa;
  border: 4px solid #17a2b8;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  font-weight: bold;
  color: #17a2b8;
  margin: 0 auto;
}

.countdown-circle.running {
  border-color: #ffc107;
  color: #ffc107;
}

.question-grid {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.question-block {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: #eee;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  border: 2px solid #ccc;
  cursor: pointer;
  font-size: 0.8em;
}

.question-block.answered {
  background: #28a745;
  color: #fff;
  border-color: #28a745;
}
</style>
