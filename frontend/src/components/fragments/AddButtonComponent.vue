<template>
  <div>
    <button class="btn btn-primary" @click="showModal = true">
      Add {{ subject }}
    </button>

    <div
      v-if="showModal"
      class="modal fade show d-block"
      tabindex="-1"
      style="background: rgba(0, 0, 0, 0.5)"
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
                <label class="form-label">Name:</label>
                <input v-model="form.name" class="form-control" required />
              </div>
              <div class="mb-3">
                <label class="form-label">Description:</label>
                <input
                  v-model="form.description"
                  class="form-control"
                  required
                />
              </div>
            </div>
            <div class="modal-footer">
              <button type="submit" class="btn btn-success">Submit</button>
              <button
                type="button"
                class="btn btn-secondary"
                @click="showModal = false"
              >
                Cancel
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
import { make_postrequest } from "@/stores/appState";
export default {
  props: {
    subject: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      showModal: false,
      form: {
        name: "",
        description: "",
      },
    };
  },
  methods: {
    async handleSubmit() {
      try {
        const response = await make_postrequest("/subjects", {
          name: this.form.name,
          description: this.form.description,
        });
        this.$emit("add", response);
        this.showModal = false;
        this.form.name = "";
        this.form.description = "";
        this.$emit("refresh-subjects");
      } catch (error) {
        console.error("API call failed:", error);
      }
    },
  },
};
</script>
