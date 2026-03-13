import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const JobList = () => import('@/views/jobs/JobList.vue')
const JobDetail = () => import('@/views/jobs/JobDetail.vue')
const JobCreate = () => import('@/views/jobs/JobCreate.vue')
const JobEdit = () => import('@/views/jobs/JobEdit.vue')

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'Home',
      component: () => import('@/views/home/Home.vue'),
    },
    {
      path: '/jobs',
      name: 'JobsList',
      component: JobList,
    },
    {
      path: '/jobs/new',
      name: 'JobCreate',
      component: JobCreate,
      meta: { requiresAuth: true, role: 'employer' },
    },
    {
      path: '/jobs/:id/edit',
      name: 'JobEdit',
      component: JobEdit,
      meta: { requiresAuth: true, role: 'employer' },
    },
    {
      path: '/jobs/:id',
      name: 'JobDetail',
      component: JobDetail,
    },
    {
      path: '/login',
      name: 'Login',
      component: () => import('@/views/users/Login.vue'),
      meta: { guestOnly: true },
    },
    {
      path: '/register',
      name: 'Register',
      component: () => import('@/views/users/Register.vue'),
      meta: { guestOnly: true },
    },
    {
      path: '/profile',
      name: 'Profile',
      component: () => import('@/views/users/Profile.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/employer/dashboard',
      name: 'EmployerDashboard',
      component: () => import('@/views/employer/EmployerDashboard.vue'),
      meta: { requiresAuth: true, role: 'employer' },
    },
  ],
})

router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()

  // Fetch user profile if token exists but user not loaded
  if (!authStore.user && authStore.accessToken) {
    try {
      await authStore.fetchUser()
    } catch (e) {
      authStore.logout()
    }
  }

  const isAuthenticated = authStore.isAuthenticated

  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login')
  } else if (to.path === '/login' && isAuthenticated) {
    next('/employer/dashboard')
  } else if (to.meta.guestOnly && isAuthenticated) {
    next('/')
  } else if (to.meta.role && authStore.user?.role !== to.meta.role) {
    next('/')
  } else {
    next()
  }
})

export default router
