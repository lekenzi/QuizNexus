<template>
  <div class="container mt-4">
    <h1 class="text-primary mb-4">User Management</h1>

    <div v-if="loading" class="text-center my-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p class="mt-2">Loading users...</p>
    </div>

    <div v-else-if="error" class="alert alert-danger">
      {{ error }}
    </div>

    <div v-else>
      <div class="card mb-4">
        <div
          class="card-header bg-light d-flex justify-content-between align-items-center"
        >
          <h5 class="mb-0">Users List</h5>
          <div>
            <select
              v-model="perPage"
              class="form-select form-select-sm"
              @change="changePage(1)"
            >
              <option :value="10">10 per page</option>
              <option :value="25">25 per page</option>
              <option :value="50">50 per page</option>
            </select>
          </div>
        </div>
        <div class="card-body p-0">
          <div class="table-responsive">
            <table class="table table-hover mb-0">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Username</th>
                  <th>Full Name</th>
                  <th>Role</th>
                  <th>Quizzes Taken</th>
                  <th>Average Score</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="user in users" :key="user.id">
                  <td>{{ user.id }}</td>
                  <td>{{ user.username }}</td>
                  <td>{{ user.full_name }}</td>
                  <td>
                    <span :class="getRoleBadgeClass(user.role)">
                      {{ user.role }}
                    </span>
                  </td>
                  <td>{{ user.stats.quizzes_taken }}</td>
                  <td>{{ user.stats.average_score.toFixed(1) }}%</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
        <div class="card-footer">
          <nav aria-label="User pagination">
            <ul class="pagination justify-content-center mb-0">
              <li class="page-item" :class="{ disabled: currentPage === 1 }">
                <a
                  class="page-link"
                  href="#"
                  @click.prevent="changePage(currentPage - 1)"
                >
                  Previous
                </a>
              </li>
              <li
                v-for="pageNum in pageNumbers"
                :key="pageNum"
                class="page-item"
                :class="{ active: pageNum === currentPage }"
              >
                <a
                  class="page-link"
                  href="#"
                  @click.prevent="changePage(pageNum)"
                >
                  {{ pageNum }}
                </a>
              </li>
              <li
                class="page-item"
                :class="{ disabled: currentPage === totalPages }"
              >
                <a
                  class="page-link"
                  href="#"
                  @click.prevent="changePage(currentPage + 1)"
                >
                  Next
                </a>
              </li>
            </ul>
          </nav>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { fetchAdminUsers } from "@/stores/appState";

export default {
  name: "AdminUsersComponent",
  data() {
    return {
      users: [],
      loading: true,
      error: null,
      currentPage: 1,
      perPage: 10,
      totalUsers: 0,
      totalPages: 0,
    };
  },
  computed: {
    pageNumbers() {
      const pages = [];

      // Show a limited number of page links
      const maxVisiblePages = 5;
      let startPage = Math.max(
        1,
        this.currentPage - Math.floor(maxVisiblePages / 2)
      );
      let endPage = Math.min(this.totalPages, startPage + maxVisiblePages - 1);

      if (endPage - startPage + 1 < maxVisiblePages) {
        startPage = Math.max(1, endPage - maxVisiblePages + 1);
      }

      for (let i = startPage; i <= endPage; i++) {
        pages.push(i);
      }

      return pages;
    },
  },
  mounted() {
    this.fetchUsers();
  },
  methods: {
    async fetchUsers() {
      this.loading = true;
      this.error = null;

      try {
        const response = await fetchAdminUsers(this.currentPage, this.perPage);
        this.users = response.users;
        this.totalUsers = response.pagination.total;
        this.totalPages = response.pagination.pages;
      } catch (error) {
        this.error = "Failed to load users. Please try again later.";
        console.error("Fetch users error:", error);
      } finally {
        this.loading = false;
      }
    },
    changePage(page) {
      if (page < 1 || page > this.totalPages) return;
      this.currentPage = page;
      this.fetchUsers();
    },
    getRoleBadgeClass(role) {
      const classes = {
        admin: "badge bg-danger",
        user: "badge bg-primary",
      };
      return classes[role] || "badge bg-secondary";
    },
  },
};
</script>
