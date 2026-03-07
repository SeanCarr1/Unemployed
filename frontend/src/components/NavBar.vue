<template>
	<nav class="navbar">
		<ul>
			<li><router-link to="/">Home</router-link></li>
			<li><router-link to="/jobs">Jobs</router-link></li>
			<li><router-link to="/dashboard">Dashboard</router-link></li>
			<li><router-link to="/login">Login</router-link></li>
			<li><router-link to="/register">Register</router-link></li>
		</ul>
	</nav>
</template>

<script setup lang="ts">
// Basic navigation bar component
</script>

<style scoped>
.navbar {
	background: #f8f9fa;
	padding: 1rem;
}
ul {
	list-style: none;
	display: flex;
	gap: 1rem;
	margin: 0;
	padding: 0;
}
li {
	font-weight: 500;
}
a {
	text-decoration: none;
	color: #333;
}
a.router-link-active {
	color: #007bff;
}
</style>
