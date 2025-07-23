<template>
  <div>
    <button class="btn btn-primary" @click="showModal = true">
      Add Questions for Quiz {{ quiz_id }}
    </button>

    <div
      v-if="showModal"
      class="modal d-flex justify-content-center align-items-center"
    >
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title bg-success text-white p-2">
              Add Question to {{ quiz_title }} in chapter {{ chapter_name }}
            </h5>
            <button
              type="button"
              class="btn-close"
              @click="showModal = false"
            ></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="submitForm">
              <div class="mb-3">
                <label for="question" class="form-label">Question:</label>
                <input
                  type="text"
                  id="question"
                  class="form-control"
                  v-model="form.question"
                  required
                />
              </div>
              <div class="mb-3">
                <label for="option1" class="form-label">Option 1:</label>
                <input
                  type="text"
                  id="option1"
                  class="form-control"
                  v-model="form.option1"
                  required
                />
              </div>
              <div class="mb-3">
                <label for="option2" class="form-label">Option 2:</label>
                <input
                  type="text"
                  id="option2"
                  class="form-control"
                  v-model="form.option2"
                  required
                />
              </div>
              <div class="mb-3">
                <label for="option3" class="form-label">Option 3:</label>
                <input
                  type="text"
                  id="option3"
                  class="form-control"
                  v-model="form.option3"
                  required
                />
              </div>
              <div class="mb-3">
                <label for="option4" class="form-label">Option 4:</label>
                <input
                  type="text"
                  id="option4"
                  class="form-control"
                  v-model="form.option4"
                  required
                />
              </div>
              <div class="mb-3">
                <label for="answer" class="form-label">Answer:</label>
                <input
                  type="text"
                  id="answer"
                  class="form-control"
                  v-model="form.answer"
                  required
                />
              </div>
              <div class="mb-3">
                <label for="marks" class="form-label">Marks:</label>
                <input
                  type="number"
                  id="marks"
                  class="form-control"
                  v-model="form.marks"
                />
              </div>
              <button type="submit" class="btn btn-success">Submit</button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { make_postrequest } from "@/stores/appState";
export default {
  name: "AddQuestionsToQuizzesModal",
  props: {
    quiz_id: {
      type: Number,
      required: true,
    },
    subject_id: {
      type: Number,
      required: true,
    },
    chapter_id: {
      type: Number,
      required: true,
    },
    chapter_name: {
      type: String,
      required: true,
    },
    quiz_title: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      showModal: false,
      form: {
        question: "",
        option1: "",
        option2: "",
        option3: "",
        option4: "",
        answer: "",
        marks: 1,
      },
    };
  },
  methods: {
    async submitForm() {
      try {
        const payload = {
          ...this.form,
          quiz_id: this.quiz_id,
          chapter_id: this.chapter_id,
          subject_id: this.subject_id,
        };
        const response = await make_postrequest("/questions", payload);
        if (response.status === 201) {
          console.log("Question added successfully:", response.data);
          alert("Question added successfully!");
          this.showModal = false;
          this.resetForm();
        } else {
          console.error("Failed to add question:", response.data);
          alert("Failed to add question.");
        }
      } catch (error) {
        console.error("Error adding question:", error);
        alert("Failed to add question.");
      }
    },
  },
  resetForm() {
    this.form = {
      question: "",
      option1: "",
      option2: "",
      option3: "",
      option4: "",
      answer: "",
      marks: 1,
    };
  },
};
</script>

<style>
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
