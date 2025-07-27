<template>
  <div class="scores-view container mt-5 p-4 bg-light rounded shadow">
    <h1 class="title text-center text-primary mb-3">User Dashboard</h1>
    <p class="description text-center text-secondary mb-4">
      Welcome to your dashboard! Here are your quizzes:
    </p>
    <div class="card-body">
      <h3 class="text-primary">Upcoming Quizzes</h3>
      <UpComingQuizTable :quizzes="upcomingQuizzes" />
      <h3 class="text-danger mt-5">Past Due Quizzes</h3>
      <PastDueComingquizTable :quizzes="pastQuizzes" />
    </div>
  </div>
</template>

<script>
import { make_getrequest } from "@/stores/appState";
import UpComingQuizTable from "@/components/users/userdashboardfragments/UpComingquizTable.vue";
import PastDueComingquizTable from "@/components/users/userdashboardfragments/PastDueComingquizTable.vue";

export default {
  name: "UserDashBoardView",
  data() {
    return {
      upcomingQuizzes: [],
      pastQuizzes: [],
    };
  },
  mounted() {
    this.fetchAllQuizzes();
  },
  methods: {
    async fetchAllQuizzes() {
      try {
        const response = await make_getrequest("/dashboard");
        this.upcomingQuizzes =
          response.upcoming_quizzes.map((quiz) => ({
            ...quiz,
            time_of_day: quiz.time_of_day || "00:00",
          })) || [];
        this.pastQuizzes =
          response.past_quizzes.map((quiz) => ({
            ...quiz,
            time_of_day: quiz.time_of_day || "00:00",
          })) || [];
      } catch (error) {
        console.error("Error fetching quizzes:", error);
      }
    },
  },
  components: {
    UpComingQuizTable,
    PastDueComingquizTable,
  },
};
</script>
