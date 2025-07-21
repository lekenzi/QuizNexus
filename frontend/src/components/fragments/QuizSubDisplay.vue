<template>
  <div class="quiz-sub-display">
    <div class="content-header">
      <h2 v-if="subject_id === null">All Quizzes</h2>
      <h2 v-else>Quizzes for Subject {{ subject_id }}</h2>
      <p class="text-muted">{{ quizzes.length }} quiz(s) found</p>
    </div>

    <div v-if="loading" class="loading-state">
      <div class="spinner-border" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p>Loading quizzes...</p>
    </div>

    <div v-else-if="quizzes.length === 0" class="no-quizzes">
      <div class="text-center">
        <i class="fas fa-clipboard-list fa-3x text-muted mb-3"></i>
        <h4>No Quizzes Found</h4>
        <p class="text-muted">
          There are no quizzes available for this selection.
        </p>
      </div>
    </div>

    <div v-else class="quiz-grid">
      <QuizTableComponent
        v-for="quiz in quizzes"
        :key="`${quiz.quiz_id}-${$route.fullPath}`"
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
      type: [Number, String],
      default: null,
      validator: (value) => value === null || !isNaN(Number(value)),
    },
  },
  data() {
    return {
      quizzes: [],
      loading: false,
    };
  },
  components: {
    QuizTableComponent,
  },
  watch: {
    // Watch for route changes
    $route: {
      immediate: true,
      handler(newRoute) {
        console.log("Route changed:", newRoute.fullPath);
        this.fetchQuizzes();
      },
    },
    // Watch for prop changes
    subject_id: {
      immediate: true,
      handler(newSubjectId) {
        console.log("Subject ID changed:", newSubjectId);
        this.fetchQuizzes();
      },
    },
  },
  methods: {
    async fetchQuizzes() {
      this.loading = true;

      // Get subject_id from route params if not provided as prop
      const subjectId =
        this.subject_id !== null
          ? this.subject_id
          : this.$route.params.subject_id
          ? parseInt(this.$route.params.subject_id)
          : null;

      let endpoint = "/quizzes";
      if (subjectId !== null && !isNaN(subjectId)) {
        endpoint += `?subject_id=${subjectId}`;
      }

      console.log(`Fetching quizzes from: ${endpoint}`);

      try {
        const response = await make_getrequest(endpoint);
        this.quizzes = response.quizzes || [];
        console.log("Quizzes fetched successfully:", {
          endpoint,
          subjectId,
          count: this.quizzes.length,
          quizzes: this.quizzes,
        });
      } catch (error) {
        console.error("Error fetching quizzes:", error);
        this.quizzes = [];
      } finally {
        this.loading = false;
      }
    },
  },
  mounted() {
    console.log(
      "QuizSubDisplay component mounted with subject_id:",
      this.subject_id
    );
    console.log("Current route:", this.$route);
  },
};
</script>
<!-- 
<style scoped>
/* Example of simpler, cleaner CSS */
.quiz-sub-display {
  padding: 1rem;
  background-color: #ffffff;
  min-height: 100vh;
  padding-bottom: 100px;
}

.content-header {
  margin-bottom: 1rem;
  border-bottom: 1px solid #ccc;
}

.content-header h2 {
  font-size: 1.5rem;
  color: #333;
}

.loading-state {
  text-align: center;
  padding: 2rem;
}

.no-quizzes {
  text-align: center;
  color: #666;
  padding: 2rem;
}

.quiz-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}

.quiz-grid > * {
  flex: 1 1 calc(33.333% - 1rem);
  box-sizing: border-box;
}
</style> -->

<style scoped>
/* Example of simpler, cleaner CSS */
.quiz-sub-display {
  width: 100%;
  padding: 1rem;
  background-color: #ffffff;
  min-height: 100vh;
  padding-bottom: 100px;
}

.content-header {
  margin-bottom: 1rem;
  border-bottom: 1px solid #ccc;
}

.content-header h2 {
  font-size: 1.5rem;
  color: #333;
}

/* Combine loading-state and no-quizzes styles */
.loading-state,
.no-quizzes {
  width: 100%;
  text-align: center;
  color: #666;
  padding: 2rem;
}

.quiz-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}

.quiz-grid > * {
  flex: 1 1 calc(33.333% - 1rem);
  box-sizing: border-box;
}
</style>
