<template>
  <div class="container" style="overflow-y: auto">
    <div class="card" style="height: 100vh; overflow-y: auto">
      <div class="card-header bg-primary text-white">
        <h2>Quiz Details</h2>
      </div>
      <div class="card-body overflow-scroll" style="max-height: 100vh">
        <p><strong>Quiz ID:</strong> {{ questions.quiz_id }}</p>
        <p>
          <strong>Number of Questions:</strong>
          {{ questions.number_of_questions }}
        </p>
        <p>
          <strong>Time Duration:</strong> {{ questions.time_duration }} minutes
        </p>
        <hr />
        <h4>Questions</h4>
        <div
          v-for="(question, index) in questions.questions"
          :key="question.id"
          class="mb-4"
        >
          <div class="card">
            <div class="card-body">
              <h5 class="card-title">Question {{ index + 1 }}:</h5>
              <p class="card-text">{{ question.question }}</p>
              <form>
                <ul class="list-group">
                  <li
                    v-for="(option, idx) in question.options"
                    :key="idx"
                    class="list-group-item"
                  >
                    <label class="form-check-label">
                      <input
                        type="radio"
                        :name="'question-' + question.id"
                        :value="option"
                        class="form-check-input me-2"
                        @change="
                          handleOptionSelect(
                            question.id,
                            questions.user_id,
                            option
                          )
                        "
                      />
                      {{ idx + 1 }}. {{ option }}
                    </label>
                  </li>
                </ul>
              </form>
              <p><strong>Marks:</strong> {{ question.marks }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import { getUser, make_postrequest } from "@/stores/appState";

export default {
  name: "DisplayQuestion",
  props: {
    questions: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      user_id: getUser().id,
    };
  },
  methods: {
    async handleOptionSelect(question_id, user_id, selectedOption) {
      console.log("Question ID:", question_id);
      console.log("User ID:", this.user_id);
      console.log("Selected Option:", selectedOption);

      try {
        // Ensure the payload matches the server's expected format
        const payload = {
          quiz_id: this.questions.quiz_id,
          question_id: question_id,
          user_id: this.user_id,
          selected_option: selectedOption,
        };

        console.log("Payload being sent:", payload);

        const response = await make_postrequest("/takeResponse", payload);
        console.log("Response recorded successfully:", response);
      } catch (error) {
        console.error(
          "Error recording response:",
          error.response?.data || error.message
        );
      }
    },
  },
};
</script>
