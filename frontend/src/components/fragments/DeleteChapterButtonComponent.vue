<template>
  <div>
    <button class="btn btn-danger" @click="showDeleteModal = true">
      Delete Chapter
    </button>

    <div
      v-if="showDeleteModal"
      class="modal fade show d-block"
      tabindex="-1"
      style="background: rgba(0, 0, 0, 0.5)"
    >
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              Confirm Delete Chapter (Chapter {{ chapter_id }})
            </h5>
            <button
              type="button"
              class="btn-close"
              @click="showDeleteModal = false"
            ></button>
          </div>
          <div class="modal-body">
            <p>Are you sure you want to delete this chapter?</p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-danger" @click="handleDelete">
              Delete Confirm
            </button>
            <button
              type="button"
              class="btn btn-secondary"
              @click="showDeleteModal = false"
            >
              Cancel
            </button>
          </div>
        </div>
      </div>
    </div>
    <div v-if="showDeleteModal" class="modal-backdrop fade show"></div>
  </div>
</template>

<script>
import { make_deleterequest } from "@/stores/appState";

export default {
  name: "DeleteChapterButtonComponent",
  props: {
    chapter_id: {
      type: Number,
      required: true,
    },
  },
  data() {
    return {
      showDeleteModal: false,
    };
  },
  methods: {
    async handleDelete() {
      try {
        await make_deleterequest(`/chapters`, {
          id: this.chapter_id,
        });
        this.$emit("chapter-deleted", this.chapter_id);
        this.showDeleteModal = false;
        this.$emit("refresh-chapters");
      } catch (error) {
        console.error("API call failed:", error);
      }
    },
  },
};
</script>
