<!-- <template>
  <div
    class="sidebar_nav d-flex flex-column align-items-stretch flex-shrink-0 bg-light shadow-sm rounded"
    style="width: 400px; overflow: scroll; scrollbar-width: none"
  >
    <div class="p-4 text-black">
      <h5 class="fw-bold mb-0">Subjects</h5>
    </div>

    <div class="p-3">
      <AddQuizesComponentForm
        :subjects="subjects"
        @refresh-quizzes="makeAnotherEmitCall"
        class="mb-3"
      />
    </div>

    <div class="p-3">
      <input
        type="text"
        class="form-control"
        placeholder="Search subjects..."
        aria-label="Search"
      />
    </div>

    <div class="list-group list-group-flush border-top">
      <router-link
        :to="{ name: 'all_quizzes' }"
        class="list-group-item list-group-item-action"
        :class="{ active: isAllSubjectsActive }"
      >
        <div class="d-flex w-100 align-items-center justify-content-between">
          <strong>All Subjects</strong>
        </div>
      </router-link>
      <router-link
        v-for="subject in subjects"
        :key="subject.subject_id"
        :to="{
          name: 'quizzes_by_subject',
          params: { subject_id: subject.subject_id },
        }"
        class="list-group-item list-group-item-action"
        :class="{ active: isSubjectActive(subject.subject_id) }"
      >
        {{ subject.subject_name }}
      </router-link>
    </div>
  </div>
</template>

<script>
import { make_getrequest } from "@/stores/appState";
import AddQuizesComponentForm from "../fragments/AddQuizesComponentForm.vue";

export default {
  name: "QuizzesSideNavBar",
  props: {
    quizzes: {
      type: Array,
      default: () => [],
    },
  },
  components: {
    AddQuizesComponentForm,
  },
  computed: {
    isAllSubjectsActive() {
      return this.$route.name === "all_quizzes";
    },
  },
  methods: {
    makeAnotherEmitCall() {
      this.$emit("refresh-cards");
    },
    getAllSubjects() {
      make_getrequest("/subjects")
        .then((response) => {
          this.subjects = response.subjects || [];
        })
        .catch((error) => {
          console.error("Failed to fetch subjects:", error);
        });
    },
    isSubjectActive(subjectId) {
      return (
        this.$route.name === "quizzes_by_subject" &&
        parseInt(this.$route.params.subject_id) === subjectId
      );
    },
  },
  data() {
    return {
      subjects: [],
    };
  },
  mounted() {
    this.getAllSubjects();
  },
  watch: {
    $route: {
      immediate: true,
      handler() {
        this.getAllSubjects();
        this.$emit("refresh-quizzes");
      },
    },
  },
};
</script>

<style scoped>
.sidebar-nav {
  padding: 1em;
  box-shadow: rgba(0, 0, 0, 0.15) 1.95px 1.95px 2.6px;
}
</style> -->

<template>
  <div
    class="sidebar_nav d-flex flex-column align-items-stretch flex-shrink-0 bg-light shadow-sm rounded"
    style="width: 400px; overflow: scroll; scrollbar-width: none"
  >
    <div class="p-4 text-black">
      <h5 class="fw-bold mb-0">Subjects</h5>
    </div>

    <div class="p-3">
      <AddQuizesComponentForm
        :subjects="subjects"
        @refresh-quizzes="makeAnotherEmitCall"
        class="mb-3"
      />
    </div>

    <div class="p-3">
      <input
        type="text"
        class="form-control"
        placeholder="Search subjects..."
        aria-label="Search"
        v-model="searchQuery"
      />
    </div>

    <div class="list-group list-group-flush border-top">
      <router-link
        :to="{ name: 'all_quizzes' }"
        class="list-group-item list-group-item-action"
        :class="{ active: isAllSubjectsActive }"
        v-show="showAllSubjects"
      >
        <div class="d-flex w-100 align-items-center justify-content-between">
          <strong>All Subjects</strong>
        </div>
      </router-link>
      <router-link
        v-for="subject in filteredSubjects"
        :key="subject.subject_id"
        :to="{
          name: 'quizzes_by_subject',
          params: { subject_id: subject.subject_id },
        }"
        class="list-group-item list-group-item-action"
        :class="{ active: isSubjectActive(subject.subject_id) }"
      >
        {{ subject.subject_name }}
      </router-link>
    </div>
  </div>
</template>

<script>
import { make_getrequest } from "@/stores/appState";
import AddQuizesComponentForm from "../fragments/AddQuizesComponentForm.vue";

export default {
  name: "QuizzesSideNavBar",
  props: {
    quizzes: {
      type: Array,
      default: () => [],
    },
  },
  components: {
    AddQuizesComponentForm,
  },
  computed: {
    isAllSubjectsActive() {
      return this.$route.name === "all_quizzes";
    },
    filteredSubjects() {
      if (!this.searchQuery.trim()) {
        return this.subjects;
      }
      return this.subjects.filter((subject) =>
        subject.subject_name
          .toLowerCase()
          .includes(this.searchQuery.toLowerCase())
      );
    },
    showAllSubjects() {
      if (!this.searchQuery.trim()) {
        return true;
      }
      return "All Subjects"
        .toLowerCase()
        .includes(this.searchQuery.toLowerCase());
    },
  },
  methods: {
    makeAnotherEmitCall() {
      this.$emit("refresh-cards");
    },
    getAllSubjects() {
      make_getrequest("/subjects")
        .then((response) => {
          this.subjects = response.subjects || [];
        })
        .catch((error) => {
          console.error("Failed to fetch subjects:", error);
        });
    },
    isSubjectActive(subjectId) {
      return (
        this.$route.name === "quizzes_by_subject" &&
        parseInt(this.$route.params.subject_id) === subjectId
      );
    },
  },
  data() {
    return {
      subjects: [],
      searchQuery: "",
    };
  },
  mounted() {
    this.getAllSubjects();
  },
  watch: {
    $route: {
      immediate: true,
      handler() {
        this.getAllSubjects();
        this.$emit("refresh-quizzes");
      },
    },
  },
};
</script>

<style scoped>
.sidebar-nav {
  padding: 1em;
  box-shadow: rgba(0, 0, 0, 0.15) 1.95px 1.95px 2.6px;
}
</style>
