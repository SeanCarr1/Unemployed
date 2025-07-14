import { createRouter, createWebHistory } from 'vue-router' // used to setup routing in a vue js app
import { useAuthStore } from '@/stores/auth'


// Lazy-loaded (optional)
const Dashboard = () => import('../components/Dashboard.vue') // loads the dashboard component only when needed

// Views
import LoginForm from '../components/LoginForm.vue'
import JobForm from '@/components/JobForm.vue'
import JobList from '@/components/JobList.vue'
import JobEdit from '@/components/JobEdit.vue'
import RegisterForm from '@/components/RegisterForm.vue'



const routes = [
    { path: '/', redirect: '/dashboard'},
    { path: '/register', component: RegisterForm, meta: { public: true } },
    { path: '/login', component: LoginForm, meta: { public: true } },
    { 
        path: '/dashboard', 
        component: Dashboard,
        children: [
            { path: '', component: JobList },
            { path: 'jobs', component: JobList },
            { path: 'jobs/new', component: JobForm },
            { path: 'jobs/:id/edit', component: JobEdit },
        ],
        meta: { requiresAuth: true }
    },
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

// global route guard
router.beforeEach(async (to, from, next) => {
    const auth = useAuthStore()

    if (!auth.use && auth.token) {
        await auth.fetchUser()
    }

    const isAuthenticated = auth.isAuthenticated

    if (to.meta.requiresAuth && !isAuthenticated) {
        next('/login')
    } else if (to.path == '/login' && isAuthenticated) {
        next('/dashboard')
    } else {
        next()
    }
})

export default router