<template>
  <div class="quizzes-view-container d-flex flex-row w-100">
    <div class="sidebar-container">
      <QuizzesSideNavBar
        :quizzes="quizzes"
        @navigate="loadComponent"
        @refresh-cards="fetchQuizzes"
      />
    </div>
    <div class="main-content">
      <router-view />
    </div>
  </div>
</template>

<script>
// import QuizTableComponent from "@/components/fragments/QuizTableComponent.vue";
import { make_getrequest } from "@/stores/appState";
import QuizzesSideNavBar from "../LandingPage/QuizzesSideNavBar.vue";

export default {
  name: "QuizesViewComponent",
  data() {
    return {
      quizzes: [],
      showModal: false,
      currentComponent: "QuizTableComponent", // Default component to load
    };
  },
  methods: {
    async fetchQuizzes() {
      try {
        const response = await make_getrequest("/quizzes");

        // Store subjects with their chapters and quizzes
        this.quizzes = response.quizzes || [];
      } catch (error) {
        console.error("Failed to fetch quizzes:", error);
      }
    },
    loadComponent(componentName) {
      this.currentComponent = componentName;
    },
  },
  components: {
    // QuizTableComponent,
    QuizzesSideNavBar,
  },
  mounted() {
    this.fetchQuizzes();
  },
};
</script>

<style scoped>
.quizzes-view-container {
  height: 100vh;
  display: flex;
  overflow: hidden;
}

.sidebar-container {
  width: 400px;
  height: 100vh;
  background-color: #f8f9fa;
  border-right: 1px solid #ddd;
  overflow-y: auto;
  flex-shrink: 0;
  position: sticky;
  top: 0;
}

.main-content {
  flex: 1;
  height: 100vh;
  overflow-y: auto;
  padding: 1em;
}
</style>
