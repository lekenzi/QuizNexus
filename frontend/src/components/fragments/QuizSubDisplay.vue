<!-- <template>
  <div class="quiz-sub-display">
    <p>this is all quizzes for subject id {{ subject_id }}</p>
    <div class="quiz-grid">
      <QuizTableComponent
        v-for="quiz in quizzes"
        :key="quiz.quiz_id"
        :quizzes="quiz"
      />
    </div>
  </div>
</template>

<script>
import { make_getrequest } from "@/stores/appState";
import QuizTableComponent from "./QuizTableComponent.vue";

export default {
  name: "QuizSubDisplay",
  props: {
    subject_id: {
      type: [Number],
      default: 99999,
      validator: (value) => !isNaN(value),
    },
  },
  data() {
    return {
      quizzes: [],
    };
  },
  methods: {
    async fetchQuizzes() {
      try {
        const response = await make_getrequest(
          `/quizzes?subject_id=${this.subject_id}`
        );
        this.quizzes = response.quizzes || [];
      } catch (error) {
        console.error("Error fetching quizzes:", error);
      }
    },
  },
  mounted() {
    console.log(`Component mounted with subject_id: ${this.subject_id}`);
    if (this.$attrs.filter) {
      console.log(`Filter attribute received: ${this.$attrs.filter}`);
    }
    this.fetchQuizzes();
  },
  components: {
    QuizTableComponent,
  },
};
</script>

<style scoped>
.quiz-sub-display {
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
}

.quiz-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.quiz-grid > * {
  flex: 1 1 calc(33.333% - 20px); /* Adjust the percentage for the number of columns */
  box-sizing: border-box;
}

.sidebar-nav ul {
  list-style-type: none;
  padding: 0;
}

.sidebar-nav li {
  margin: 10px 0;
  background-color: #f0f0f0;
  border-right: 1px solid #ddd;
  height: 100vh;
}
</style> -->

<template>
  <div class="quiz-sub-display">
    <p>this is all quizzes for subject id {{ subject_id }}</p>
    <div class="quiz-grid">
      <QuizTableComponent
        v-for="quiz in quizzes"
        :key="quiz.quiz_id"
        :quizzes="quiz"
      />
    </div>
  </div>
</template>

<script>
import { make_getrequest } from "@/stores/appState";
import QuizTableComponent from "./QuizTableComponent.vue";

export default {
  name: "QuizSubDisplay",
  props: {
    subject_id: {
      type: [Number],
      default: 99999,
      validator: (value) => !isNaN(value),
    },
  },
  data() {
    return {
      quizzes: [],
    };
  },
  methods: {
    async fetchQuizzes() {
      try {
        const response = await make_getrequest(
          `/quizzes?subject_id=${this.subject_id}`
        );
        this.quizzes = response.quizzes || [];
      } catch (error) {
        console.error("Error fetching quizzes:", error);
      }
    },
  },
  mounted() {
    console.log(`Component mounted with subject_id: ${this.subject_id}`);
    if (this.$attrs.filter) {
      console.log(`Filter attribute received: ${this.$attrs.filter}`);
    }
    this.fetchQuizzes();
  },
  components: {
    QuizTableComponent,
  },
};
</script>

<style scoped>
.quiz-sub-display {
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  height: 100%;
  overflow-y: auto;
  box-sizing: border-box;
}

.quiz-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  min-height: min-content;
}

.quiz-grid > * {
  flex: 1 1 calc(33.333% - 20px); /* Adjust the percentage for the number of columns */
  box-sizing: border-box;
  min-height: fit-content;
}

.sidebar-nav ul {
  list-style-type: none;
  padding: 0;
}

.sidebar-nav li {
  margin: 10px 0;
  background-color: #f0f0f0;
  border-right: 1px solid #ddd;
  height: 100vh;
}
</style>
