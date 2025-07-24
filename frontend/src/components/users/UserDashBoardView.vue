<template>
  <div>
    <h5>user dashboard</h5>
    <UpComingQuizTable :quizzes="allQuizzes" />
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
