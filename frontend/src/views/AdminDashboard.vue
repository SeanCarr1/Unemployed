<script setup lang="ts">
import { ref, onMounted } from 'vue';
import api from '@/api/api';
import { useAuthStore } from '@/stores/auth';

interface User {
  id: number;
  email: string;
  username: string;
  role: string;
  date_joined: string;
}

const users = ref<User[]>([]);
const loading = ref(false);
const error = ref('');
const auth = useAuthStore();

const fetchUsers = async () => {
  loading.value = true;
  error.value = '';
  try {
    const res = await api.get<User[]>('/users/');
    users.value = res.data;
  } catch (err: any) {
    error.value = 'Failed to fetch users';
  } finally {
    loading.value = false;
  }
};

const promoteUser = async (userId: number) => {
  // Placeholder: call backend to promote user
  alert(`Promote user ${userId}`);
};
const demoteUser = async (userId: number) => {
  // Placeholder: call backend to demote user
  alert(`Demote user ${userId}`);
};
const deactivateUser = async (userId: number) => {
  // Placeholder: call backend to deactivate user
  alert(`Deactivate user ${userId}`);
};

onMounted(() => {
  fetchUsers();
});
</script>

<template>
  <div>
    <h1>Admin Dashboard</h1>
    <div v-if="loading.value">Loading users...</div>
    <div v-if="error.value" style="color: red;">{{ error }}</div>
    <table v-if="users.value.length">
      <thead>
        <tr>
          <th>ID</th>
          <th>Email</th>
          <th>Username</th>
          <th>Role</th>
          <th>Date Joined</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in users.value" :key="user.id">
          <td>{{ user.id }}</td>
          <td>{{ user.email }}</td>
          <td>{{ user.username }}</td>
          <td>{{ user.role }}</td>
          <td>{{ user.date_joined }}</td>
          <td>
            <button @click="promoteUser(user.id)">Promote</button>
            <button @click="demoteUser(user.id)">Demote</button>
            <button @click="deactivateUser(user.id)">Deactivate</button>
          </td>
        </tr>
      </tbody>
    </table>
    <div v-else-if="!loading.value && !error.value">No users found.</div>
  </div>
</template>
