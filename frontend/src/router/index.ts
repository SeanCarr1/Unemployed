import { createRouter, createWebHistory } from 'vue-router' // used to setup routing in a vue js app
import { useAuth } from '../composables/useAuth'  // custom composable for my authentication
import LoginForm from '../components/LoginForm.vue' // a login form vue component

// Lazy-loaded (optional)
const Dashboard = () => import('../components/Dashboard.vue') // loads the dashboard component only when needed

const routes = [
  { path: '/', redirect: '/dashboard'},
  { path: '/login', component: LoginForm, meta: { public: true } },
  { path: '/dashboard', component: Dashboard, meta: { requiresAuth: true } },
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

// global route guard
router.beforeEach(async (to, from, next) => {
    const { token, fetchUser, user } = useAuth()

    if (!user.value && token.value) {
        await fetchUser()
    }

    const isAuthenticated = !!user.value

    if (to.meta.requiresAuth && !isAuthenticated) {
        next('/login')
    } else if (to.path == '/login' && isAuthenticated) {
        next('/dashboard')
    } else {
        next()
    }
})

export default router