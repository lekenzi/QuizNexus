<template>
  <div>
    <!-- Edit Button -->
    <button class="btn btn-warning" @click="openModal">Edit</button>

    <!-- Modal -->
    <div
      v-if="showModal"
      class="modal fade show d-block"
      tabindex="-1"
      style="background: rgba(0, 0, 0, 0.75)"
    >
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              <i class="fas fa-edit me-2"></i>Edit Quiz
            </h5>
            <button
              type="button"
              class="btn-close"
              @click="closeModal"
              :disabled="isUpdating"
            ></button>
          </div>
          <form @submit.prevent="updateQuiz">
            <div class="modal-body">
              <div class="mb-3">
                <label for="quizTitle" class="form-label">Quiz Title</label>
                <input
                  type="text"
                  class="form-control"
                  id="quizTitle"
                  v-model="form.title"
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

              <div class="row">
                <div class="col-md-6">
                  <div class="mb-3">
                    <label for="duration" class="form-label"
                      >Duration (minutes)</label
                    >
                    <input
                      type="number"
                      class="form-control"
                      id="duration"
                      v-model="form.time_duration"
                      min="1"
                      required
                    />
                  </div>
                </div>
                <div class="col-md-6">
                  <div class="mb-3">
                    <label for="date" class="form-label">Date</label>
                    <input
                      type="date"
                      class="form-control"
                      id="date"
                      v-model="form.date"
                      required
                    />
                  </div>
                </div>
              </div>

              <div class="mb-3">
                <label for="timeOfDay" class="form-label">Time</label>
                <input
                  type="time"
                  class="form-control"
                  id="timeOfDay"
                  v-model="form.time_of_day"
                  required
                />
              </div>

              <div class="row">
                <div class="col-md-6">
                  <div class="mb-3">
                    <label for="subject" class="form-label">Subject</label>
                    <select
                      class="form-control"
                      id="subject"
                      v-model="form.subject_id"
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
                  </div>
                </div>
                <div class="col-md-6">
                  <div class="mb-3">
                    <label for="chapter" class="form-label">Chapter</label>
                    <select
                      class="form-control"
                      id="chapter"
                      v-model="form.chapter_id"
                      :disabled="!form.subject_id || chapters.length === 0"
                      required
                    >
                      <option value="" disabled>
                        {{
                          !form.subject_id
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
                  </div>
                </div>
              </div>

              <div v-if="updateError" class="alert alert-danger">
                {{ updateError }}
              </div>

              <div v-if="updateSuccess" class="alert alert-success">
                {{ updateSuccess }}
              </div>
            </div>
            <div class="modal-footer">
              <button
                type="button"
                class="btn btn-secondary"
                @click="closeModal"
                :disabled="isUpdating"
              >
                Cancel
              </button>
              <button
                type="submit"
                class="btn btn-primary"
                :disabled="isUpdating"
              >
                <span
                  v-if="isUpdating"
                  class="spinner-border spinner-border-sm me-2"
                  role="status"
                ></span>
                {{ isUpdating ? "Updating..." : "Update Quiz" }}
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
import { make_getrequest } from "@/stores/appState";

export default {
  name: "EditQuizModal",
  props: {
    quiz: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      showModal: false,
      form: {
        id: null,
        title: "",
        remarks: "",
        time_duration: 0,
        date: "",
        time_of_day: "",
        subject_id: "",
        chapter_id: "",
      },
      subjects: [],
      chapters: [],
      isUpdating: false,
      updateError: null,
      updateSuccess: null,
    };
  },
  watch: {
    showModal(newValue) {
      if (newValue) {
        this.initializeForm();
        this.fetchSubjects();
      } else {
        this.resetMessages();
      }
    },
    "form.subject_id"(newSubjectId) {
      if (newSubjectId) {
        this.fetchChapters(newSubjectId);
      } else {
        this.chapters = [];
        this.form.chapter_id = "";
      }
    },
  },
  methods: {
    openModal() {
      this.showModal = true;
    },

    closeModal() {
      if (!this.isUpdating) {
        this.showModal = false;
        this.resetMessages();
      }
    },

    initializeForm() {
      this.form = {
        id: this.quiz.quiz_id,
        title: this.quiz.quiz_title || "",
        remarks: this.quiz.remarks || "",
        time_duration: this.quiz.time_duration || 0,
        date: this.formatDateForInput(this.quiz.date_of_quiz),
        time_of_day: this.formatTimeForInput(this.quiz.time_of_day),
        subject_id: this.quiz.subject_id || "",
        chapter_id: this.quiz.chapter_id || "",
      };
    },

    formatDateForInput(dateString) {
      if (!dateString) return "";
      return dateString.split("T")[0];
    },

    formatTimeForInput(timeString) {
      if (!timeString) return "";
      return timeString.split(":").slice(0, 2).join(":");
    },

    async fetchSubjects() {
      try {
        const response = await make_getrequest("/subjects");
        this.subjects = response.subjects || [];

        if (this.form.subject_id) {
          await this.fetchChapters(this.form.subject_id);
        }
      } catch (error) {
        console.error("Failed to fetch subjects:", error);
      }
    },

    async fetchChapters(subjectId) {
      try {
        const response = await make_getrequest(
          `/chapters?subject_id=${subjectId}`
        );
        this.chapters = response.data?.chapters || [];
      } catch (error) {
        console.error("Failed to fetch chapters:", error);
        this.chapters = [];
      }
    },

    onSubjectChange() {
      this.form.chapter_id = "";
    },

    async updateQuiz() {
      this.isUpdating = true;
      this.updateError = null;
      this.updateSuccess = null;

      try {
        const payload = {
          id: this.form.id,
          title: this.form.title,
          remarks: this.form.remarks,
          time_duration: parseInt(this.form.time_duration),
          date: this.form.date,
          time_of_day: this.form.time_of_day + ":00",
          subject_id: this.form.subject_id,
          chapter_id: this.form.chapter_id,
        };

        const token = localStorage.getItem("token");
        const response = await fetch(
          `${
            this.$store?.state?.BASEURL || "http://localhost:5000/api"
          }/quizzes`,
          {
            method: "PATCH",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify(payload),
          }
        );

        if (!response.ok) {
          throw new Error("Update failed");
        }

        const result = await response.json();
        this.updateSuccess = result.message || "Quiz updated successfully";

        this.$emit("quiz-updated", {
          quiz: { ...this.quiz, ...payload },
          message: this.updateSuccess,
        });

        setTimeout(() => {
          this.closeModal();
        }, 1500);
      } catch (error) {
        console.error("Failed to update quiz:", error);
        this.updateError = "Failed to update quiz. Please try again.";
      } finally {
        this.isUpdating = false;
      }
    },

    resetMessages() {
      this.updateError = null;
      this.updateSuccess = null;
    },
  },
};
</script>

<style scoped>
.modal-content {
  border: none;
  border-radius: 8px;
}

.modal-header {
  border-bottom: 1px solid #dee2e6;
}

.modal-footer {
  border-top: 1px solid #dee2e6;
}
</style>
