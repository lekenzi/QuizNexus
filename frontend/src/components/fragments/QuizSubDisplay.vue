<template>
  <div class="quiz-sub-display">
    <div class="content-header">
      <h2 v-if="subject_id === null">All Quizzes</h2>
      <h2 v-else>Quizzes for Subject {{ subject_id }}</h2>
      <p class="text-muted">{{ filteredQuizzes.length }} quiz(s) found</p>
    </div>

    <div class="search-container mb-3">
      <input
        type="text"
        class="form-control"
        placeholder="Search by quiz title, chapter, or subject..."
        v-model="searchQuery"
      />
    </div>

    <div v-if="loading" class="loading-state">
      <div class="spinner-border" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p>Loading quizzes...</p>
    </div>

    <div
      v-else-if="filteredQuizzes.length === 0 && !loading"
      class="no-quizzes"
    >
      <div class="text-center">
        <i class="fas fa-clipboard-list fa-3x text-muted mb-3"></i>
        <h4 v-if="searchQuery.trim()">No Matching Quizzes Found</h4>
        <h4 v-else>No Quizzes Found</h4>
        <p class="text-muted" v-if="searchQuery.trim()">
          No quizzes match your search query "{{ searchQuery }}".
        </p>
        <p class="text-muted" v-else>
          There are no quizzes available for this selection.
        </p>
      </div>
    </div>

    <div v-else class="quiz-grid">
      <QuizTableComponent
        v-for="quiz in filteredQuizzes"
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
      searchQuery: "",
    };
  },
  components: {
    QuizTableComponent,
  },
  computed: {
    filteredQuizzes() {
      if (!this.searchQuery.trim()) {
        return this.quizzes;
      }

      const searchTerm = this.searchQuery.toLowerCase();

      return this.quizzes.filter((quiz) => {
        // Search in quiz title
        const titleMatch =
          quiz.quiz_title && quiz.quiz_title.toLowerCase().includes(searchTerm);

        // Search in chapter name
        const chapterMatch =
          quiz.chapter_name &&
          quiz.chapter_name.toLowerCase().includes(searchTerm);

        // Search in subject name
        const subjectMatch =
          quiz.subject_name &&
          quiz.subject_name.toLowerCase().includes(searchTerm);

        // Return true if any of the fields match
        return titleMatch || chapterMatch || subjectMatch;
      });
    },
  },
  watch: {
    $route: {
      immediate: true,
      handler() {
        this.fetchQuizzes();
      },
    },

    subject_id: {
      immediate: true,
      handler() {
        this.fetchQuizzes();
      },
    },
  },
  methods: {
    async fetchQuizzes() {
      this.loading = true;

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

      try {
        const response = await make_getrequest(endpoint);
        this.quizzes = response.quizzes || [];
      } catch (error) {
        console.error("Error fetching quizzes:", error);
        this.quizzes = [];
      } finally {
        this.loading = false;
      }
    },
  },
  mounted() {},
};
</script>

<style scoped>
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

.search-container {
  max-width: 400px;
}

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
