<template>
  <div class="subjects-grid container">
    <div class="d-flex justify-content-center my-4">
      <AddButtonComponent
        class="add-button"
        subject="Add Subject"
        @add="showModal = true"
        @refresh-subjects="fetchSubjects"
      />
    </div>

    <div class="row">
      <div v-for="subject in subjects" :key="subject.id">
        <TableComponent :subject="subject" />
      </div>
    </div>
  </div>
</template>

<script>
import TableComponent from "@/components/fragments/TableComponent.vue";
import AddButtonComponent from "@/components/fragments/AddButtonComponent.vue";
import { make_getrequest } from "@/stores/appState";
export default {
  name: "HomeViewComponent",
  data() {
    return {
      subjects: [],
      showModal: false,
    };
  },
  methods: {
    async fetchSubjects() {
      try {
        const response = await make_getrequest("/subjects");
        // Map backend fields to expected frontend fields
        this.subjects = (response.subjects || []).map((s) => ({
          name: s.subject_name,
          description: s.subject_description,
          id: s.subject_id,
        }));
      } catch (error) {
        console.error("Failed to fetch subjects:", error);
      }
    },
  },
  components: {
    TableComponent,
    AddButtonComponent,
  },
  mounted() {
    this.fetchSubjects();
  },
};
</script>

<style scoped>
.subjects-grid {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.subject-card {
  margin: 10px 0;
}
</style>
