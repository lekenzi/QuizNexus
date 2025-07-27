<template>
  <div>
    <button class="btn btn-danger" @click="showModal = true">
      Delete {{ subject.name }}
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
            <h5 class="modal-title">Confirm Delete</h5>
            <button
              type="button"
              class="btn-close"
              @click="showModal = false"
            ></button>
          </div>
          <div class="modal-body">
            <p>
              Are you sure you want to delete the subject "{{ subject.name }}"?
            </p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-danger" @click="handleDelete">
              Delete Confirm
            </button>
            <button
              type="button"
              class="btn btn-secondary"
              @click="showModal = false"
            >
              Cancel
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
  name: "DeleteSubjectButtonComponent",
  props: {
    subject: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      showModal: false,
    };
  },
  methods: {
    async handleDelete() {
      try {
        await make_deleterequest(`/subjects`, {
          name: this.subject.name,
        });
        this.$emit("refresh-subjects", this.subject.id);
        this.showModal = false;
      } catch (error) {
        console.error("Failed to delete subject:", error);
      }
    },
  },
};
</script>
