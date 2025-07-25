<template>
  <div class="scores-view container mt-5 p-4 bg-light rounded shadow">
    <h1 class="title text-center text-primary mb-3">User Dashboard</h1>
    <p class="description text-center text-secondary mb-4">
      Welcome to your dashboard! Here are your upcoming quizzes:
    </p>
    <div class="card-body">
      <UpComingQuizTable :quizzes="allQuizzes" />
    </div>
  </div>
</template>

<script>
import { make_getrequest } from "@/stores/appState";
import UpComingQuizTable from "@/components/users/userdashboardfragments/UpComingquizTable.vue";
export default {
  name: "UserDashBoardView",
  data() {
    return {
      allQuizzes: [],
    };
  },
  mounted() {
    this.fetchAllQuizzes();
  },
  methods: {
    async fetchAllQuizzes() {
      try {
        const response = await make_getrequest("/dashboard");
        this.allQuizzes = response;
      } catch (error) {
        console.error("Error fetching quizzes:", error);
      }
    },
  },
  components: {
    UpComingQuizTable,
  },
};
</script>
