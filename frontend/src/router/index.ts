import { createRouter, createWebHistory } from 'vue-router' // used to setup routing in a vue js app
import { useAuthStore } from '@/stores/auth'


// Lazy-loaded (optional)
const Dashboard = () => import('../components/Dashboard.vue') // loads the dashboard component only when needed

// Views
import LoginForm from '../components/LoginForm.vue'
import JobForm from '@/components/jobs/JobForm.vue'
import JobList from '@/components/jobs/JobList.vue'
import JobEdit from '@/components/jobs/JobEdit.vue'
import RegisterForm from '@/components/RegisterForm.vue'
import JobDetail from '@/components/jobs/JobDetail.vue'




const routes = [
    { path: '/', redirect: '/jobs' },
    { path: '/register', component: RegisterForm, meta: { public: true } },
    { path: '/login', component: LoginForm, meta: { public: true } },
    {
        path: '/dashboard',
        component: Dashboard,
        meta: { requiresAuth: true }
    },
    {
        path: '/jobs',
        component: () => import('@/components/jobs/Jobs.vue'),
        meta: { requiresAuth: true },
        children: [
            { path: '', component: JobList },
            { path: 'new', component: JobForm },
            { path: ':id/edit', component: JobEdit },
            { path: ':id', component: JobDetail },
            
        ]
    },
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

// global route guard
router.beforeEach(async (to, from, next) => {
    const auth = useAuthStore()

    if (!auth.user && auth.token) {
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