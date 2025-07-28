<template>
  <div>
    <!-- Delete Button -->
    <button class="btn btn-danger" @click="openModal">Delete</button>

    <!-- Modal -->
    <div
      v-if="showModal"
      class="modal fade show d-block"
      tabindex="-1"
      style="background: rgba(0, 0, 0, 0.75)"
    >
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title text-danger">
              <i class="fas fa-exclamation-triangle me-2"></i>Delete Quiz
            </h5>
            <button
              type="button"
              class="btn-close"
              @click="closeModal"
              :disabled="isDeleting"
            ></button>
          </div>
          <div class="modal-body">
            <div class="alert alert-warning">
              <strong>Warning:</strong> This action cannot be undone!
            </div>
            <p>
              Are you sure you want to delete the quiz
              <strong>"{{ quiz.quiz_title }}"</strong>?
            </p>
            <div class="quiz-info bg-light p-3 rounded">
              <p class="mb-1">
                <strong>Subject:</strong> {{ quiz.subject_name }}
              </p>
              <p class="mb-1">
                <strong>Chapter:</strong> {{ quiz.chapter_name }}
              </p>
              <p class="mb-0">
                <strong>Questions:</strong> {{ quiz.number_of_questions }}
              </p>
            </div>

            <div v-if="deleteError" class="alert alert-danger mt-3">
              {{ deleteError }}
            </div>
          </div>
          <div class="modal-footer">
            <button
              type="button"
              class="btn btn-secondary"
              @click="closeModal"
              :disabled="isDeleting"
            >
              Cancel
            </button>
            <button
              type="button"
              class="btn btn-danger"
              @click="confirmDelete"
              :disabled="isDeleting"
            >
              <span
                v-if="isDeleting"
                class="spinner-border spinner-border-sm me-2"
                role="status"
              ></span>
              {{ isDeleting ? "Deleting..." : "Delete Quiz" }}
            </button>
          </div>
        </div>
      </div>
    </div>
    <div v-if="showModal" class="modal-backdrop fade show"></div>
  </div>
</template>

<script>
import { make_deleterequest } from "@/stores/appState";

export default {
  name: "DeleteQuizModal",
  props: {
    quiz: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      showModal: false,
      isDeleting: false,
      deleteError: null,
    };
  },
  methods: {
    openModal() {
      this.showModal = true;
    },

    closeModal() {
      if (!this.isDeleting) {
        this.showModal = false;
        this.deleteError = null;
      }
    },

    async confirmDelete() {
      this.isDeleting = true;
      this.deleteError = null;

      try {
        console.log("Attempting to delete quiz:", this.quiz.id);
        const response = await make_deleterequest("/quizzes", {
          quiz_id: this.quiz.quiz_id,
        });
        console.log("Delete response:", response);
        if (response) {
          this.$emit("quiz-deleted", {
            quiz: this.quiz,
            message: response.message || "Quiz deleted successfully",
          });
          this.closeModal();
        }
      } catch (error) {
        console.error("Failed to delete quiz:", error);
        this.deleteError = "Failed to delete quiz. Please try again.";
      } finally {
        this.isDeleting = false;
      }
    },
  },
  watch: {
    showModal(newValue) {
      if (!newValue) {
        this.deleteError = null;
      }
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

.quiz-info {
  border-left: 4px solid #007bff;
}
</style>
