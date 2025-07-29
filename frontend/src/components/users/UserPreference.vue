<template>
  <div class="container mt-5 bg-white p-4 rounded">
    <h1 class="text-primary mb-4">User Preferences</h1>

    <div v-if="loading" class="text-center my-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p class="mt-2">Loading preferences...</p>
    </div>

    <div v-else-if="error" class="alert alert-danger rounded">
      {{ error }}
    </div>

    <div v-else class="row">
      <div class="col-md-8">
        <div class="card rounded">
          <div class="card-header bg-primary text-white rounded-top">
            <h5 class="mb-0"><i class="fas fa-cog me-2"></i>My Preferences</h5>
          </div>
          <div class="card-body">
            <form @submit.prevent="updatePreferences">
              <div class="mb-4">
                <h6 class="text-secondary mb-3">Notification Settings</h6>

                <div class="form-check mb-3">
                  <input
                    class="form-check-input"
                    type="checkbox"
                    id="emailReminders"
                    v-model="form.email_reminders"
                  />
                  <label class="form-check-label" for="emailReminders">
                    <strong>Email Reminders</strong>
                    <br />
                    <small class="text-muted">
                      Receive email notifications about upcoming quizzes
                    </small>
                  </label>
                </div>

                <div class="form-check mb-3">
                  <input
                    class="form-check-input"
                    type="checkbox"
                    id="monthlyReport"
                    v-model="form.monthly_report"
                  />
                  <label class="form-check-label" for="monthlyReport">
                    <strong>Monthly Performance Report</strong>
                    <br />
                    <small class="text-muted">
                      Get a monthly summary of your quiz performance
                    </small>
                  </label>
                </div>

                <div class="mb-3">
                  <label for="reminderTime" class="form-label">
                    <strong>Daily Reminder Time</strong>
                  </label>
                  <input
                    type="time"
                    class="form-control rounded"
                    id="reminderTime"
                    v-model="form.reminder_time"
                    :disabled="!form.email_reminders"
                  />
                  <small class="form-text text-muted">
                    Choose when you'd like to receive daily quiz reminders
                  </small>
                </div>
              </div>

              <div v-if="updateError" class="alert alert-danger rounded">
                <i class="fas fa-exclamation-triangle me-2"></i>
                {{ updateError }}
              </div>

              <div v-if="updateSuccess" class="alert alert-success rounded">
                <i class="fas fa-check-circle me-2"></i>
                {{ updateSuccess }}
              </div>

              <div class="d-flex justify-content-end">
                <button
                  type="button"
                  class="btn btn-secondary me-2 rounded"
                  @click="resetForm"
                  :disabled="isUpdating"
                >
                  Reset
                </button>
                <button
                  type="submit"
                  class="btn btn-primary rounded"
                  :disabled="isUpdating"
                >
                  <span
                    v-if="isUpdating"
                    class="spinner-border spinner-border-sm me-2"
                    role="status"
                  ></span>
                  {{ isUpdating ? "Updating..." : "Save Preferences" }}
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>

      <div class="col-md-4">
        <div class="card mb-4 rounded">
          <div class="card-header bg-info text-white rounded-top">
            <h6 class="mb-0">
              <i class="fas fa-info-circle me-2"></i>Account Summary
            </h6>
          </div>
          <div class="card-body">
            <div class="mb-3">
              <strong>Last Visit:</strong>
              <br />
              <span class="text-muted">
                {{ formatDateTime(preferences.last_visit) }}
              </span>
            </div>

            <div class="mb-3">
              <strong>Email Notifications:</strong>
              <br />
              <span
                :class="
                  preferences.email_reminders ? 'text-success' : 'text-danger'
                "
              >
                <i
                  :class="
                    preferences.email_reminders
                      ? 'fas fa-check'
                      : 'fas fa-times'
                  "
                ></i>
                {{ preferences.email_reminders ? "Enabled" : "Disabled" }}
              </span>
            </div>

            <div class="mb-3">
              <strong>Monthly Reports:</strong>
              <br />
              <span
                :class="
                  preferences.monthly_report ? 'text-success' : 'text-danger'
                "
              >
                <i
                  :class="
                    preferences.monthly_report ? 'fas fa-check' : 'fas fa-times'
                  "
                ></i>
                {{ preferences.monthly_report ? "Enabled" : "Disabled" }}
              </span>
            </div>

            <div v-if="preferences.reminder_time">
              <strong>Reminder Time:</strong>
              <br />
              <span class="text-primary">
                <i class="fas fa-clock me-1"></i>
                {{ formatTime(preferences.reminder_time) }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { make_getrequest, make_postrequest } from "@/stores/appState";

export default {
  name: "UserPreference",
  data() {
    return {
      preferences: {
        notifications_enabled: false,
        reminder_time: null,
        email_reminders: true,
        monthly_report: true,
        last_visit: null,
      },
      form: {
        reminder_time: "",
        email_reminders: true,
        monthly_report: true,
      },
      loading: true,
      error: null,
      isUpdating: false,
      updateError: null,
      updateSuccess: null,
    };
  },
  mounted() {
    this.fetchPreferences();
  },
  methods: {
    async fetchPreferences() {
      this.loading = true;
      this.error = null;

      try {
        const response = await make_getrequest("/user/preferences");
        this.preferences = response.preferences;
        this.initializeForm();
      } catch (error) {
        console.error("Error fetching preferences:", error);
        this.error = "Failed to load preferences. Please try again later.";
      } finally {
        this.loading = false;
      }
    },

    initializeForm() {
      this.form = {
        reminder_time: this.preferences.reminder_time || "18:00",
        email_reminders: this.preferences.email_reminders,
        monthly_report: this.preferences.monthly_report,
      };
    },

    async updatePreferences() {
      this.isUpdating = true;
      this.updateError = null;
      this.updateSuccess = null;

      try {
        const payload = {
          reminder_time: this.form.reminder_time,
          email_reminders: this.form.email_reminders,
          monthly_report: this.form.monthly_report,
        };

        const response = await make_postrequest("/user/preferences", payload);

        this.updateSuccess =
          response.message || "Preferences updated successfully";

        // Update local preferences
        this.preferences.reminder_time = this.form.reminder_time;
        this.preferences.email_reminders = this.form.email_reminders;
        this.preferences.monthly_report = this.form.monthly_report;

        // Clear success message after 3 seconds
        setTimeout(() => {
          this.updateSuccess = null;
        }, 3000);
      } catch (error) {
        console.error("Error updating preferences:", error);
        this.updateError = "Failed to update preferences. Please try again.";
      } finally {
        this.isUpdating = false;
      }
    },

    resetForm() {
      this.initializeForm();
      this.updateError = null;
      this.updateSuccess = null;
    },

    formatDateTime(dateString) {
      if (!dateString) return "Never";

      try {
        const date = new Date(dateString);
        return date.toLocaleString();
      } catch (error) {
        return "Invalid date";
      }
    },

    formatTime(timeString) {
      if (!timeString) return "Not set";

      try {
        // Handle both "HH:MM" and "HH:MM:SS" formats
        const timeParts = timeString.split(":");
        const hours = parseInt(timeParts[0]);
        const minutes = timeParts[1];

        const period = hours >= 12 ? "PM" : "AM";
        const displayHours = hours > 12 ? hours - 12 : hours === 0 ? 12 : hours;

        return `${displayHours}:${minutes} ${period}`;
      } catch (error) {
        return timeString;
      }
    },
  },
};
</script>

<style scoped>
.form-check-input:checked {
  background-color: #0d6efd;
  border-color: #0d6efd;
}

.form-check-label {
  cursor: pointer;
}

.alert {
  border: none;
  border-radius: 8px;
}

.btn {
  border-radius: 6px;
}

.text-success {
  color: #198754 !important;
}

.text-danger {
  color: #dc3545 !important;
}

.spinner-border-sm {
  width: 1rem;
  height: 1rem;
}
</style>
