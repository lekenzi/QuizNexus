<template>
  <div class="container my-5">
    <div class="card shadow mb-4">
      <div class="card-body">
        <h2 class="card-title text-center mb-4">{{ subject.name }}</h2>
        <table class="table table-hover align-middle">
          <thead class="table-light">
            <tr>
              <th>Chapter Name</th>
              <th>Number of Questions</th>
              <th colspan="2">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="chapter in chapters" :key="chapter.id">
              <td>{{ chapter.name }}</td>
              <td>{{ chapter.questions ?? 0 }}</td>
              <td>
                <button class="btn btn-success btn-sm me-2">Edit</button>
              </td>
              <td>
                <button class="btn btn-danger btn-sm">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
        <AddChapterButtonComponent :subject="subject" :key="subject.id" />
      </div>
    </div>
  </div>
</template>

<script>
import AddChapterButtonComponent from "@/components/fragments/AddChapterButtonComponent.vue";
import { make_getrequest } from "@/stores/appState";
export default {
  name: "TableComponent",
  props: {
    subject: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      chapters: [],
    };
  },
  components: {
    AddChapterButtonComponent,
  },
  methods: {
    async fetchChapters() {
      try {
        const response = await make_getrequest("/chapters", {
          subject_id: this.subject.id,
        });
        // Expecting response.data.chapters to be an array
        const chaptersArray = response?.data?.chapters || [];
        this.chapters = chaptersArray.map((chap) => ({
          id: chap.id,
          name: chap.name,
          questions: 0, // Default or fetch actual question count if available
        }));
        console.log("Chapters fetched successfully:", this.chapters);
      } catch (error) {
        console.error("Failed to fetch chapters:", error);
      }
    },
  },
  mounted() {
    this.fetchChapters();
  },
};
</script>
<style scoped>
.container {
  max-width: 800px;
  margin: 0 auto;
}
.card {
  margin-bottom: 20px;
}
</style>
