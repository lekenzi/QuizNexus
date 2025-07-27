<template>
  <div>
    <button class="btn btn-primary" @click="showModal = true">
      Add New Quiz
    </button>

    <div
      v-if="showModal"
      class="modal fade show d-block"
      tabindex="-1"
      style="background: rgba(0, 0, 0, 0.75)"
    >
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Add {{ subject }}</h5>
            <button
              type="button"
              class="btn-close"
              @click="showModal = false"
            ></button>
          </div>
          <form @submit.prevent="handleSubmit">
            <div class="modal-body">
              <div class="mb-3">
                <label for="quiztitle" class="form-label">Title</label>
                <input
                  type="text"
                  class="form-control"
                  id="quiztitle"
                  v-model="form.quiztitle"
                  required
                />
              </div>
              <div class="mb-3">
                <label for="remarks" class="form-label">Remarks</label>
                <textarea
                  class="form-control"
                  id="remarks"
                  v-model="form.remarks"
                  rows="3"
                ></textarea>
              </div>
              <div class="mb-3">
                <label for="timeduration" class="form-label"
                  >Time Duration</label
                >
                <select
                  class="form-control"
                  id="timeduration"
                  v-model="form.timeduration"
                  required
                >
                  <option value="" disabled>Select duration</option>
                  <option value="1">1 hour</option>
                  <option value="2">2 hours</option>
                  <option value="3">3 hours</option>
                </select>
              </div>
              <div class="mb-3">
                <label for="date" class="form-label">Date of Quiz</label>
                <input
                  type="date"
                  class="form-control"
                  id="date"
                  v-model="form.date"
                  required
                />
              </div>
              <div class="mb-3">
                <label for="time_of_day" class="form-label">Time of Day</label>
                <select
                  class="form-control"
                  id="time_of_day"
                  v-model="form.time_of_day"
                  required
                >
                  <option value="" disabled>Select time</option>
                  <option v-for="hour in hours" :key="hour" :value="hour">
                    {{ hour }}:00
                  </option>
                </select>
              </div>
              <div class="mb-3">
                <label for="subject" class="form-label">Subject</label>
                <select
                  class="form-control"
                  id="subject"
                  v-model="form.subject"
                  @change="onSubjectChange"
                  required
                >
                  <option value="" disabled>Select subject</option>
                  <option
                    v-for="subject in subjects"
                    :key="subject.subject_id"
                    :value="subject.subject_id"
                  >
                    {{ subject.subject_name }}
                  </option>
                </select>
                <div class="form-text">
                  Select a subject to load its chapters. ({{ subjects.length }}
                  subjects loaded)
                </div>
              </div>
              <div class="mb-3">
                <label for="chapter" class="form-label">Chapter</label>
                <select
                  class="form-control"
                  id="chapter"
                  v-model="form.chapter"
                  :disabled="!form.subject || chapters.length === 0"
                  required
                >
                  <option value="" disabled>
                    {{
                      !form.subject
                        ? "Select a subject first"
                        : chapters.length === 0
                        ? "Loading chapters..."
                        : "Select chapter"
                    }}
                  </option>
                  <option
                    v-for="chapter in chapters"
                    :key="chapter.id"
                    :value="chapter.id"
                  >
                    {{ chapter.name }}
                  </option>
                </select>
                <div class="form-text">
                  {{ chapters.length }} chapters loaded
                </div>
              </div>
            </div>
            <div class="modal-footer">
              <button
                type="button"
                class="btn btn-secondary"
                @click="closeModal"
              >
                Close
              </button>
              <button type="submit" class="btn btn-primary">
                Save changes
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
    <div v-if="showModal" class="modal-backdrop fade show"></div>
  </div>
</template>
<script>
import { make_postrequest, make_getrequest } from "@/stores/appState";

export default {
  name: "AddQuizesComponentForm",
  props: {
    subject: {
      type: String,
      required: false,
    },
  },
  data() {
    return {
      showModal: false,
      form: {
        quiztitle: "",
        remarks: "",
        timeduration: "",
        date: "",
        subject: "",
        chapter: "",
        time_of_day: "",
      },
      subjects: [],
      chapters: [],
      hours: Array.from({ length: 24 }, (_, i) => i), // Generate hours 0-23
      loading: {
        subjects: false,
        chapters: false,
      },
    };
  },
  watch: {
    "form.subject"(newSubjectId) {
      if (newSubjectId) {
        this.fetchChapters(newSubjectId);
      } else {
        this.chapters = [];
        this.form.chapter = "";
      }
    },
  },
  mounted() {
    this.fetchSubjects();
  },
  methods: {
    async fetchSubjects() {
      this.loading.subjects = true;
      try {
        const response = await make_getrequest("/subjects");

        if (response.subjects && Array.isArray(response.subjects)) {
          this.subjects = response.subjects;
        } else {
          console.error("Unexpected response structure:", response);
          this.subjects = [];
          return;
        }

        if (this.subjects.length === 0) {
          console.warn("No subjects found in the response");
        }
      } catch (error) {
        console.error("Failed to fetch subjects:", error);
        console.error("Error details:", error.response || error.message);
        this.subjects = [];
      } finally {
        this.loading.subjects = false;
      }
    },

    async fetchChapters(subjectId) {
      this.loading.chapters = true;
      try {
        const response = await make_getrequest(
          `/chapters?subject_id=${subjectId}`
        );

        if (
          response.data &&
          response.data.chapters &&
          Array.isArray(response.data.chapters)
        ) {
          this.chapters = response.data.chapters;
        } else {
          console.error("Unexpected chapters response structure:", response);
          this.chapters = [];
        }

        this.form.chapter = "";
      } catch (error) {
        console.error("Failed to fetch chapters:", error);
        console.error("Error details:", error.response || error.message);
        this.chapters = [];
        this.form.chapter = "";
      } finally {
        this.loading.chapters = false;
      }
    },

    onSubjectChange() {
      this.form.chapter = "";
    },

    closeModal() {
      this.showModal = false;
      this.resetForm();
    },

    resetForm() {
      this.form = {
        quiztitle: "",
        remarks: "",
        timeduration: "",
        date: "",
        subject: "",
        chapter: "",
        time_of_day: "",
      };
      this.chapters = [];
    },

    async handleSubmit() {
      try {
        const payload = {
          title: this.form.quiztitle,
          remarks: this.form.remarks,
          timeduration: this.form.timeduration,
          date: this.form.date,
          subject_id: this.form.subject,
          chapter_id: this.form.chapter,
          time_of_day: this.form.time_of_day,
        };

        const response = await make_postrequest("/quizzes", payload);

        this.$emit("add", response);
        this.closeModal();
        this.$emit("refresh-quizzes");
      } catch (error) {
        console.error("API call failed:", error);
        console.error("Error details:", error.response || error.message);
      }
    },
  },
};
</script>
