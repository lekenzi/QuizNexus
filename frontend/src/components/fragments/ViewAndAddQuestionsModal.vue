<template>
  <div>
    <!-- Trigger Button -->
    <button
      class="btn btn-primary"
      @click="toggleModal"
      :disabled="!quiz.quiz_id"
    >
      <i class="fas fa-eye me-2"></i>
      View & Add Questions
    </button>

    <!-- Modal -->
    <div
      v-if="showModal"
      class="modal fade show d-block"
      tabindex="-1"
      style="background: rgba(0, 0, 0, 0.5)"
      @click="closeModalOnBackdrop"
    >
      <div class="modal-dialog modal-xl">
        <div class="modal-content">
          <!-- Modal Header -->
          <div class="modal-header">
            <h5 class="modal-title">
              <i class="fas fa-question-circle me-2"></i>
              Questions for "{{ quiz.quiz_title || "Quiz" }}"
            </h5>
            <button
              type="button"
              class="btn-close"
              @click="closeModal"
            ></button>
          </div>

          <!-- Modal Body -->
          <div class="modal-body">
            <!-- Quiz Info Card -->
            <div class="card mb-4 bg-light">
              <div class="card-body">
                <div class="row">
                  <div class="col-md-6">
                    <p class="mb-1">
                      <strong>Subject:</strong> {{ getSubjectName() }}
                    </p>
                    <p class="mb-0">
                      <strong>Chapter:</strong> {{ quiz.chapter_name || "N/A" }}
                    </p>
                  </div>
                  <div class="col-md-6 text-md-end">
                    <span class="badge bg-primary fs-6">
                      {{ questions.length }} Question{{
                        questions.length !== 1 ? "s" : ""
                      }}
                    </span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Add Question Section -->
            <div class="mb-4">
              <div
                class="d-flex justify-content-between align-items-center mb-3"
              >
                <h6 class="mb-0">Add New Question</h6>
                <button
                  class="btn btn-success btn-sm"
                  @click="toggleAddQuestionForm"
                  v-if="!showAddQuestionForm"
                >
                  <i class="fas fa-plus me-1"></i>
                  Add Question
                </button>
              </div>

              <!-- Add Question Form -->
              <div
                v-if="showAddQuestionForm"
                class="border rounded p-3 bg-light"
              >
                <AddQuestionsToQuizzesModal
                  :quiz_id="quiz.quiz_id"
                  :subject_id="quiz.subject_id"
                  :chapter_id="quiz.chapter_id"
                  :chapter_name="quiz.chapter_name"
                  :quiz_title="quiz.quiz_title"
                  @question-added="handleQuestionAdded"
                  @cancel="toggleAddQuestionForm"
                />
              </div>
            </div>

            <!-- Questions List -->
            <div class="questions-section">
              <div
                class="d-flex justify-content-between align-items-center mb-3"
              >
                <h6 class="mb-0">Existing Questions</h6>
                <button
                  class="btn btn-outline-secondary btn-sm"
                  @click="refreshQuestions"
                  :disabled="loading"
                >
                  <i
                    class="fas fa-sync-alt me-1"
                    :class="{ 'fa-spin': loading }"
                  ></i>
                  Refresh
                </button>
              </div>

              <!-- Loading State -->
              <div v-if="loading" class="text-center py-4">
                <div class="spinner-border text-primary" role="status">
                  <span class="visually-hidden">Loading questions...</span>
                </div>
                <p class="mt-2 text-muted">Loading questions...</p>
              </div>

              <!-- Error State -->
              <div v-else-if="error" class="alert alert-danger" role="alert">
                <i class="fas fa-exclamation-triangle me-2"></i>
                {{ error }}
                <button
                  class="btn btn-sm btn-outline-danger ms-2"
                  @click="refreshQuestions"
                >
                  Try Again
                </button>
              </div>

              <!-- Empty State -->
              <div v-else-if="questions.length === 0" class="text-center py-5">
                <i class="fas fa-question-circle fa-3x text-muted mb-3"></i>
                <h6 class="text-muted">No questions found</h6>
                <p class="text-muted mb-3">
                  This quiz doesn't have any questions yet.
                </p>
                <button
                  class="btn btn-primary"
                  @click="toggleAddQuestionForm"
                  v-if="!showAddQuestionForm"
                >
                  Add First Question
                </button>
              </div>

              <!-- Questions List -->
              <div v-else class="questions-list">
                <div
                  v-for="(question, index) in questions"
                  :key="question.id"
                  class="card mb-3"
                >
                  <div
                    class="card-header d-flex justify-content-between align-items-start"
                  >
                    <div class="flex-grow-1">
                      <h6 class="card-title mb-1">
                        <span class="badge bg-secondary me-2"
                          >Q{{ index + 1 }}</span
                        >
                        {{ question.question_text }}
                      </h6>
                      <small class="text-muted">
                        Type: {{ question.question_type || "Multiple Choice" }}
                        <span v-if="question.difficulty" class="ms-2">
                          • Difficulty: {{ question.difficulty }}
                        </span>
                      </small>
                    </div>
                    <div class="btn-group btn-group-sm">
                      <button
                        class="btn btn-outline-primary"
                        @click="editQuestion(question)"
                        title="Edit Question"
                      >
                        <i class="fas fa-edit"></i>
                      </button>
                      <button
                        class="btn btn-outline-danger"
                        @click="deleteQuestion(question.id)"
                        title="Delete Question"
                      >
                        <i class="fas fa-trash"></i>
                      </button>
                    </div>
                  </div>

                  <div class="card-body">
                    <div class="row">
                      <div class="col-12">
                        <h6 class="mb-2">Options:</h6>
                        <div class="list-group list-group-flush">
                          <div
                            v-for="option in question.options"
                            :key="option.id"
                            class="list-group-item d-flex align-items-center"
                            :class="{
                              'list-group-item-success': option.is_correct,
                            }"
                          >
                            <i
                              class="fas me-2"
                              :class="
                                option.is_correct
                                  ? 'fa-check-circle text-success'
                                  : 'fa-circle text-muted'
                              "
                            ></i>
                            <span>{{ option.text }}</span>
                            <span
                              v-if="option.is_correct"
                              class="badge bg-success ms-auto"
                            >
                              Correct
                            </span>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Modal Footer -->
          <div class="modal-footer">
            <div class="me-auto">
              <small class="text-muted">
                Last updated:
                {{ lastUpdated ? formatDate(lastUpdated) : "Never" }}
              </small>
            </div>
            <button type="button" class="btn btn-secondary" @click="closeModal">
              Close
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal Backdrop -->
    <div v-if="showModal" class="modal-backdrop fade show"></div>
  </div>
</template>

<script>
import AddQuestionsToQuizzesModal from "@/components/fragments/AddQuestionsToQuizzesModal.vue";
import { make_getrequest } from "@/stores/appState";

export default {
  name: "ViewAndAddQuestionsModal",
  components: {
    AddQuestionsToQuizzesModal,
  },
  props: {
    quiz: {
      type: Object,
      required: true,
      validator(value) {
        return value && typeof value === "object" && value.quiz_id;
      },
    },
  },
  data() {
    return {
      showModal: false,
      showAddQuestionForm: false,
      questions: [],
      loading: false,
      error: null,
      lastUpdated: null,
    };
  },
  methods: {
    toggleModal() {
      this.showModal = !this.showModal;
      if (this.showModal) {
        this.fetchQuestions();
      } else {
        this.showAddQuestionForm = false;
      }
    },

    closeModal() {
      this.showModal = false;
      this.showAddQuestionForm = false;
    },

    closeModalOnBackdrop(event) {
      if (event.target === event.currentTarget) {
        this.closeModal();
      }
    },

    toggleAddQuestionForm() {
      this.showAddQuestionForm = !this.showAddQuestionForm;
    },

    async fetchQuestions() {
      if (!this.quiz.quiz_id) {
        this.error = "Invalid quiz ID";
        return;
      }

      this.loading = true;
      this.error = null;

      try {
        const response = await make_getrequest(
          `/quizzes/${this.quiz.quiz_id}/questions`
        );
        this.questions = response.questions || [];
        this.lastUpdated = new Date();
      } catch (error) {
        console.error("Failed to fetch questions:", error);
        this.error = "Failed to load questions. Please try again.";
        this.questions = [];
      } finally {
        this.loading = false;
      }
    },

    refreshQuestions() {
      this.fetchQuestions();
    },

    handleQuestionAdded(newQuestion) {
      // Add the new question to the list
      this.questions.push(newQuestion);
      this.showAddQuestionForm = false;
      this.lastUpdated = new Date();

      // Optionally refresh the entire list
      // this.refreshQuestions();
    },

    editQuestion(question) {
      // Emit event to parent or handle edit logic
      this.$emit("edit-question", question);
      console.log("Edit question:", question);
    },

    async deleteQuestion(questionId) {
      if (!confirm("Are you sure you want to delete this question?")) {
        return;
      }

      try {
        // await make_deleterequest(`/questions/${questionId}`);
        this.questions = this.questions.filter((q) => q.id !== questionId);
        this.lastUpdated = new Date();
        console.log("Question deleted:", questionId);
      } catch (error) {
        console.error("Failed to delete question:", error);
        alert("Failed to delete question. Please try again.");
      }
    },

    getSubjectName() {
      // You might want to fetch subject name based on subject_id
      return this.quiz.subject_name || `Subject ID: ${this.quiz.subject_id}`;
    },

    formatDate(date) {
      return new Intl.DateTimeFormat("en-US", {
        year: "numeric",
        month: "short",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
      }).format(date);
    },
  },

  mounted() {
    console.log("Quiz Data:", this.quiz);
  },

  // Cleanup when component is destroyed
  beforeUnmount() {
    // Remove any event listeners or cleanup
  },
};
</script>

<style scoped>
.questions-list {
  max-height: 400px;
  overflow-y: auto;
}

.list-group-item-success {
  background-color: #d1e7dd;
  border-color: #badbcc;
}

.modal-xl {
  max-width: 90%;
}
</style>
