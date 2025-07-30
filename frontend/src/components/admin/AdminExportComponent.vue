<template>
  <div class="container mt-4 bg-light rounded shadow-sm">
    <h1 class="text-primary mb-4">Data Export</h1>

    <div class="row">
      <div class="col-md-6">
        <div class="card mb-4">
          <div class="card-header bg-primary text-white">
            <h5 class="mb-0">Generate New Export</h5>
          </div>
          <div class="card-body">
            <p>
              Generate a CSV file containing statistics for all users. This
              process runs in the background and may take a few minutes.
            </p>
            <button
              class="btn btn-primary"
              @click="triggerExport"
              :disabled="isExporting"
            >
              <span
                v-if="isExporting"
                class="spinner-border spinner-border-sm me-2"
                role="status"
                aria-hidden="true"
              ></span>
              {{
                isExporting ? "Generating..." : "Generate User Statistics CSV"
              }}
            </button>

            <div v-if="exportMessage" class="alert alert-success mt-3">
              {{ exportMessage }}
            </div>

            <div v-if="exportError" class="alert alert-danger mt-3">
              {{ exportError }}
            </div>
          </div>
        </div>
      </div>

      <div class="col-md-6">
        <div class="card">
          <div
            class="card-header bg-success text-white d-flex justify-content-between align-items-center"
          >
            <h5 class="mb-0">Available Exports</h5>
            <button class="btn btn-sm btn-light" @click="refreshExports">
              <i class="fas fa-sync"></i> Refresh
            </button>
          </div>
          <div class="card-body p-0">
            <div v-if="loadingExports" class="text-center p-4">
              <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
              </div>
              <p class="mt-2">Loading exports...</p>
            </div>

            <div v-else-if="exportsError" class="alert alert-danger m-3">
              {{ exportsError }}
            </div>

            <div
              v-else-if="exports.length === 0"
              class="p-4 text-center text-muted"
            >
              <p>No exports available yet.</p>
            </div>

            <table v-else class="table table-hover mb-0">
              <thead>
                <tr>
                  <th>Filename</th>
                  <th>Created</th>
                  <th>Size</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="export_file in exports" :key="export_file.filename">
                  <td>{{ export_file.filename }}</td>
                  <td>{{ formatDate(export_file.created) }}</td>
                  <td>{{ formatFileSize(export_file.size) }}</td>
                  <td>
                    <button
                      @click="downloadFile(export_file.filename)"
                      class="btn btn-sm btn-primary"
                      :disabled="isDownloading === export_file.filename"
                    >
                      <span
                        v-if="isDownloading === export_file.filename"
                        class="spinner-border spinner-border-sm me-1"
                        role="status"
                      ></span>
                      <i v-else class="fas fa-download me-1"></i> Download
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {
  triggerUserStatsExport,
  fetchExportsList,
  downloadExportFile,
} from "@/stores/appState";

export default {
  name: "AdminExportComponent",
  data() {
    return {
      exports: [],
      isExporting: false,
      loadingExports: true,
      exportMessage: "",
      exportError: null,
      exportsError: null,
      isDownloading: null,
    };
  },
  mounted() {
    this.fetchExports();
  },
  methods: {
    async triggerExport() {
      this.isExporting = true;
      this.exportMessage = "";
      this.exportError = null;

      try {
        const response = await triggerUserStatsExport();
        this.exportMessage = response.message;

        // Set a timeout to refresh the exports list after a delay
        setTimeout(() => {
          this.fetchExports();
        }, 5000);
      } catch (error) {
        this.exportError = "Failed to start export. Please try again.";
        console.error("Export error:", error);
      } finally {
        this.isExporting = false;
      }
    },

    async fetchExports() {
      this.loadingExports = true;
      this.exportsError = null;

      try {
        this.exports = await fetchExportsList();
      } catch (error) {
        this.exportsError = "Failed to load exports list.";
        console.error("Fetch exports error:", error);
      } finally {
        this.loadingExports = false;
      }
    },

    async downloadFile(filename) {
      this.isDownloading = filename;
      try {
        await downloadExportFile(filename);
      } catch (error) {
        this.$bvToast?.toast
          ? this.$bvToast.toast("Download failed. Please try again.", {
              title: "Error",
              variant: "danger",
              toaster: "b-toaster-top-center",
            })
          : alert("Download failed. Please try again.");
      } finally {
        this.isDownloading = null;
      }
    },

    refreshExports() {
      this.fetchExports();
    },

    formatDate(dateString) {
      const date = new Date(dateString);
      return date.toLocaleString();
    },

    formatFileSize(bytes) {
      if (bytes < 1024) return bytes + " B";
      const kb = bytes / 1024;
      if (kb < 1024) return kb.toFixed(2) + " KB";
      const mb = kb / 1024;
      return mb.toFixed(2) + " MB";
    },
  },
};
</script>
