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
                <PatchChapterButtonComponent
                  :chapter="chapter"
                  @chapter-updated="fetchChapters"
                />
              </td>
              <td>
                <DeleteChapterButtonComponent
                  :chapter_id="chapter.id"
                  @chapter-deleted="fetchChapters"
                />
              </td>
            </tr>
          </tbody>
        </table>
        <div class="d-flex justify-content-between flex-row mt-4">
          <AddChapterButtonComponent
            :subject="subject"
            :key="subject.id"
            @refresh-chapters="fetchChapters"
          />
          <DeleteSubjectButtonComponent
            :subject="subject"
            @refresh-subjects="fetchSubjects"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import AddChapterButtonComponent from "@/components/fragments/AddChapterButtonComponent.vue";
import DeleteSubjectButtonComponent from "@/components/fragments/DeleteSubjectButtonComponent.vue";
import DeleteChapterButtonComponent from "@/components/fragments/DeleteChapterButtonComponent.vue";
import PatchChapterButtonComponent from "@/components/fragments/PatchChapterButtonComponent.vue";
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
    DeleteSubjectButtonComponent,
    DeleteChapterButtonComponent,
    PatchChapterButtonComponent,
  },
  methods: {
    async fetchChapters() {
      try {
        const response = await make_getrequest("/chapters", {
          subject_id: this.subject.id,
        });

        const chaptersArray = response?.data?.chapters || [];
        this.chapters = chaptersArray.map((chap) => ({
          id: chap.id,
          name: chap.name,
          description: chap.description,
          questions: 0,
        }));
      } catch (error) {
        console.error("Failed to fetch chapters:", error);
      }
    },
    fetchSubjects() {
      this.$emit("refresh-subjects");
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
