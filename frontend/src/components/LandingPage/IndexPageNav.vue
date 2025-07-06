<template>
  <nav class="navbar">
    <div class="navbar-brand">
      <img
        src="./../../../public/img/icon-no-bg.png"
        width="70"
        height="70"
        alt="Brand Logo"
      />
    </div>
    <div class="navbar-links">
      <router-link to="/" class="nav-link">Home</router-link>
      <router-link to="/login" class="nav-link">Login</router-link>
      <router-link to="/register" class="nav-link">Register</router-link>
    </div>
  </nav>
</template>

<script>
export default {
  name: "IndexPageNav",
};
</script>

<style scoped>
.navbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #f8f9fa;
  padding: 0.5rem 1rem;
  border-bottom: 1px solid #e5e5e5;
}

.navbar-brand img {
  display: block;
}

.navbar-links {
  display: flex;
  gap: 1rem;
}

.nav-link {
  color: #343a40;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s;
}

.nav-link:hover {
  color: #007bff;
}
</style>
