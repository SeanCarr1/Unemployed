<script setup lang="ts">
</script>

<template>
  <div>
    <!-- 🔹 Simple Navbar -->
    <div style="padding: 1rem; background-color: #eee;">
      <strong>Navigation:</strong>
      <ul style="list-style: none; display: flex; gap: 1rem; padding: 0;">
        <li><router-link to="/dashboard">Home</router-link></li>
        <li><router-link to="/jobs">All Jobs</router-link></li>
        <li><router-link to="/jobs/new">New Job</router-link></li>
        <li><router-link to="/logout">Logout</router-link></li>
      </ul>
    </div>

    <!-- 🔹 Page Content -->
    <div style="padding: 1rem;">
      <router-view />
    </div>
  </div>
</template>
