<template>
  <div>
    <button class="btn btn-success" @click="showModal = true">
      Edit Chapter
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
            <h5 class="modal-title">Edit Chapter</h5>
            <button
              type="button"
              class="btn-close"
              @click="showModal = false"
            ></button>
          </div>
          <form @submit.prevent="handleSubmit">
            <div class="modal-body">
              <div class="mb-3">
                <label class="form-label">Chapter Name:</label>
                <input
                  v-model="form.chapterName"
                  class="form-control"
                  placeholder="Chapter Name"
                  id="chapter-name-input"
                  name="chapterName"
                  required
                />
                <label class="form-label mt-2">Description</label>
                <textarea
                  v-model="form.description"
                  class="form-control"
                  placeholder="Chapter Description"
                  id="chapter-description-input"
                  name="description"
                  required
                ></textarea>
              </div>
            </div>
            <div class="modal-footer">
              <button type="submit" class="btn btn-success">Save</button>
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
import { make_patchrequest } from "@/stores/appState";

export default {
  name: "PatchChapterButtonComponent",
  props: {
    chapter: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      showModal: false,
      form: {
        chapterName: this.chapter.name || "",
        description: this.chapter.description || "",
      },
    };
  },
  methods: {
    async handleSubmit() {
      if (!this.form.chapterName.trim() || !this.form.description.trim())
        return;

      try {
        const response = await make_patchrequest(
          `/chapters/${this.chapter.id}`,
          {
            chapter_id: this.chapter.id,
            chapter_name: this.form.chapterName,
            chapter_description: this.form.description,
          }
        );
        this.$emit("chapter-updated", response);
        this.showModal = false;
      } catch (error) {
        console.error("API call failed:", error);
      }
    },
  },
};
</script>
