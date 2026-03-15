
<template>
  <div class="space-y-24 py-8 sm:py-12">
    <section class="relative overflow-hidden rounded-3xl border bg-gradient-to-br from-white via-emerald-50/30 to-neutral-100 p-8 sm:p-12">
      <div class="pointer-events-none absolute -left-24 top-0 h-60 w-60 rounded-full bg-emerald-300/20 blur-3xl" />
      <div class="pointer-events-none absolute -right-20 bottom-0 h-52 w-52 rounded-full bg-neutral-900/10 blur-3xl" />

      <div class="relative space-y-8 text-center">
        <Badge variant="secondary" class="px-4 py-1 text-xs uppercase tracking-[0.16em]">
          Built for seekers and employers
        </Badge>

        <h1 class="text-5xl font-bold tracking-tight sm:text-6xl lg:text-7xl">
          Build your next team.
          <br>
          Find your next role.
        </h1>

        <p class="mx-auto max-w-3xl text-base text-muted-foreground sm:text-lg">
          A focused hiring platform for people who value clarity over noise. Discover real opportunities,
          move faster, and connect with teams that are actually hiring.
        </p>

        <div class="flex flex-wrap items-center justify-center gap-3">
          <Button as-child size="lg" class="min-w-44">
            <RouterLink :to="primaryHeroCta.to">{{ primaryHeroCta.label }}</RouterLink>
          </Button>
          <Button as-child size="lg" variant="outline" class="min-w-44">
            <RouterLink :to="secondaryHeroCta.to">{{ secondaryHeroCta.label }}</RouterLink>
          </Button>
        </div>
      </div>
    </section>

    <section class="space-y-6">
      <div class="max-w-2xl space-y-2">
        <h2 class="text-3xl font-semibold tracking-tight">Why people choose Unemployed</h2>
        <p class="text-muted-foreground">Designed to keep hiring momentum high and friction low.</p>
      </div>

      <div class="grid gap-4 md:grid-cols-3">
        <Card v-for="item in valueProps" :key="item.title" class="transition-shadow hover:shadow-md">
          <CardHeader>
            <CardTitle class="text-lg">{{ item.title }}</CardTitle>
            <CardDescription>{{ item.description }}</CardDescription>
          </CardHeader>
        </Card>
      </div>
    </section>

    <section class="space-y-6">
      <div class="flex flex-wrap items-end justify-between gap-3">
        <div>
          <h2 class="text-3xl font-semibold tracking-tight">Featured Jobs</h2>
          <p class="text-muted-foreground">Fresh openings pulled directly from live listings.</p>
        </div>
        <Button as-child variant="ghost" class="px-1">
          <RouterLink to="/jobs">View all jobs</RouterLink>
        </Button>
      </div>

      <div v-if="loading" class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        <Card v-for="i in 3" :key="`skeleton-${i}`">
          <CardHeader class="space-y-3">
            <Skeleton class="h-5 w-3/4" />
            <Skeleton class="h-4 w-1/2" />
          </CardHeader>
          <CardContent class="space-y-2">
            <Skeleton class="h-4 w-full" />
            <Skeleton class="h-4 w-10/12" />
          </CardContent>
          <CardFooter class="justify-between">
            <Skeleton class="h-4 w-24" />
            <Skeleton class="h-8 w-20" />
          </CardFooter>
        </Card>
      </div>

      <Alert v-else-if="error" variant="destructive">
        <AlertTitle>Could not load featured jobs</AlertTitle>
        <AlertDescription class="mt-2 flex flex-wrap items-center gap-3">
          <span>{{ error }}</span>
          <Button variant="outline" size="sm" @click="fetchJobs">Retry</Button>
        </AlertDescription>
      </Alert>

      <Alert v-else-if="featuredJobs.length === 0">
        <AlertTitle>No openings available yet</AlertTitle>
        <AlertDescription>Check back soon or create an account to post the first role.</AlertDescription>
      </Alert>

      <div v-else class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        <Card
          v-for="job in featuredJobs"
          :key="job.id"
          class="transition-shadow duration-200 hover:shadow-md"
        >
          <CardHeader class="gap-2">
            <div class="flex items-center justify-between gap-2">
              <CardTitle class="line-clamp-1 text-lg">{{ job.title }}</CardTitle>
              <Badge variant="outline">{{ formatType(job.job_type) }}</Badge>
            </div>
            <CardDescription>
              {{ companyLabel(job.employer_email) }} • {{ job.location }}
            </CardDescription>
          </CardHeader>
          <CardContent>
            <p class="line-clamp-3 text-sm text-muted-foreground">{{ job.description }}</p>
          </CardContent>
          <CardFooter class="items-center justify-between gap-2">
            <span class="text-sm font-medium">{{ salaryLabel(job.salary_min, job.salary_max) }}</span>
            <Button as-child variant="link" class="px-0">
              <RouterLink :to="`/jobs/${job.id}`">View details</RouterLink>
            </Button>
          </CardFooter>
        </Card>
      </div>
    </section>

    <section class="space-y-6">
      <h2 class="text-3xl font-semibold tracking-tight">How it works</h2>
      <div class="grid gap-4 md:grid-cols-3">
        <Card v-for="step in steps" :key="step.title">
          <CardHeader>
            <Badge variant="secondary" class="w-fit">Step {{ step.order }}</Badge>
            <CardTitle>{{ step.title }}</CardTitle>
            <CardDescription>{{ step.description }}</CardDescription>
          </CardHeader>
        </Card>
      </div>
    </section>

    <section class="rounded-3xl border bg-card p-6 sm:p-8">
      <div class="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <Card v-for="stat in stats" :key="stat.label" class="border-none bg-muted/40 shadow-none">
          <CardHeader>
            <CardTitle class="text-3xl tracking-tight">{{ stat.value }}</CardTitle>
            <CardDescription>{{ stat.label }}</CardDescription>
          </CardHeader>
        </Card>
      </div>
    </section>

    <section class="space-y-6">
      <h2 class="text-3xl font-semibold tracking-tight">What users say</h2>
      <div class="grid gap-4 md:grid-cols-3">
        <Card v-for="item in testimonials" :key="item.name" class="transition-shadow hover:shadow-md">
          <CardHeader class="gap-4">
            <div class="flex items-center gap-3">
              <Avatar class="size-10">
                <AvatarImage :src="item.image" :alt="item.name" />
                <AvatarFallback>{{ item.initials }}</AvatarFallback>
              </Avatar>
              <div>
                <CardTitle class="text-base">{{ item.name }}</CardTitle>
                <CardDescription>{{ item.role }}</CardDescription>
              </div>
            </div>
            <p class="text-sm text-muted-foreground">"{{ item.quote }}"</p>
          </CardHeader>
        </Card>
      </div>
    </section>

    <section class="space-y-5">
      <h2 class="text-3xl font-semibold tracking-tight">Frequently asked questions</h2>
      <Card>
        <CardContent class="pt-2">
          <Accordion type="single" collapsible>
            <AccordionItem v-for="item in faqs" :key="item.value" :value="item.value">
              <AccordionTrigger>{{ item.question }}</AccordionTrigger>
              <AccordionContent>{{ item.answer }}</AccordionContent>
            </AccordionItem>
          </Accordion>
        </CardContent>
      </Card>
    </section>

    <section class="rounded-3xl border bg-gradient-to-r from-neutral-900 to-neutral-800 p-8 text-white sm:p-10">
      <div class="flex flex-col gap-6 sm:flex-row sm:items-end sm:justify-between">
        <div class="max-w-2xl space-y-2">
          <h2 class="text-3xl font-semibold tracking-tight">{{ finalCta.title }}</h2>
          <p class="text-sm text-white/75 sm:text-base">{{ finalCta.description }}</p>
        </div>
        <div class="flex flex-wrap gap-3">
          <Button as-child size="lg" variant="secondary">
            <RouterLink :to="finalCta.primaryTo">{{ finalCta.primaryLabel }}</RouterLink>
          </Button>
          <Button as-child size="lg" variant="outline" class="border-white/25 bg-transparent text-white hover:bg-white/10 hover:text-white">
            <RouterLink :to="finalCta.secondaryTo">{{ finalCta.secondaryLabel }}</RouterLink>
          </Button>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { RouterLink } from 'vue-router'

import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from '@/components/ui/accordion'
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert'
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card'
import { Skeleton } from '@/components/ui/skeleton'
import type { Job } from '@/api/jobsApi'
import { useAuthStore } from '@/stores/auth'
import { useJobsStore } from '@/stores/jobs'

interface ValueProp {
  title: string
  description: string
}

interface Step {
  order: number
  title: string
  description: string
}

interface Stat {
  value: string
  label: string
}

interface Testimonial {
  name: string
  role: string
  quote: string
  initials: string
  image: string
}

interface Faq {
  value: string
  question: string
  answer: string
}

const jobsStore = useJobsStore()
const authStore = useAuthStore()

const loading = computed(() => jobsStore.loading)
const error = computed(() => jobsStore.error)
const featuredJobs = computed(() => jobsStore.items.slice(0, 3))

const valueProps: ValueProp[] = [
  {
    title: 'Only relevant jobs',
    description: 'No cluttered feeds or recycled posts. We surface openings that are active and clear.'
  },
  {
    title: 'Faster employer workflow',
    description: 'Post roles, review applications, and move candidates forward with less admin overhead.'
  },
  {
    title: 'Transparent expectations',
    description: 'Clear role types, salary ranges, and location details so both sides can decide quickly.'
  }
]

const steps: Step[] = [
  {
    order: 1,
    title: 'Discover opportunities',
    description: 'Search open jobs by title, type, and location to find roles that fit your goals.'
  },
  {
    order: 2,
    title: 'Apply with confidence',
    description: 'Submit focused applications and track your status from your profile dashboard.'
  },
  {
    order: 3,
    title: 'Hire or get hired',
    description: 'Employers review strong candidates quickly while seekers keep momentum high.'
  }
]

const stats: Stat[] = [
  { value: '1.2k+', label: 'Monthly active candidates' },
  { value: '320+', label: 'Employers hiring this quarter' },
  { value: '4.7/5', label: 'Average application experience rating' },
  { value: '< 48h', label: 'Median first employer response time' }
]

const testimonials: Testimonial[] = [
  {
    name: 'Mia R.',
    role: 'Frontend Engineer',
    quote: 'The flow is clean and direct. I got interviews faster because every listing felt intentional.',
    initials: 'MR',
    image: 'https://picsum.photos/seed/mia-avatar/120/120'
  },
  {
    name: 'Daniel K.',
    role: 'Hiring Manager',
    quote: 'We posted in minutes and screened applicants without the usual dashboard bloat.',
    initials: 'DK',
    image: 'https://picsum.photos/seed/daniel-avatar/120/120'
  },
  {
    name: 'Lena T.',
    role: 'Product Designer',
    quote: 'Salary and role details were upfront, so I only applied where there was a real fit.',
    initials: 'LT',
    image: 'https://picsum.photos/seed/lena-avatar/120/120'
  }
]

const faqs: Faq[] = [
  {
    value: 'faq-1',
    question: 'Do I need to pay to create an account?',
    answer: 'No. Creating an account is free for both job seekers and employers during MVP.'
  },
  {
    value: 'faq-2',
    question: 'Who can post jobs?',
    answer: 'Employers can create and manage their own listings once registered with an employer role.'
  },
  {
    value: 'faq-3',
    question: 'Can I track my applications?',
    answer: 'Yes. Seekers can view application status updates directly from their profile dashboard.'
  },
  {
    value: 'faq-4',
    question: 'What job types are currently supported?',
    answer: 'Current supported types are full-time, contract, and remote roles.'
  }
]

const primaryHeroCta = computed(() => {
  if (authStore.isEmployer) {
    return {
      label: 'Go to Dashboard',
      to: '/employer/dashboard'
    }
  }

  return {
    label: 'Browse Jobs',
    to: '/jobs'
  }
})

const secondaryHeroCta = computed(() => {
  if (authStore.isAuthenticated) {
    return {
      label: 'View Profile',
      to: '/profile'
    }
  }

  return {
    label: 'Create Account',
    to: '/register'
  }
})

const finalCta = computed(() => {
  if (authStore.isEmployer) {
    return {
      title: 'Ready to fill your next role?',
      description: 'Manage listings and review applicants from one focused dashboard.',
      primaryLabel: 'Open Dashboard',
      primaryTo: '/employer/dashboard',
      secondaryLabel: 'Browse Candidate-Facing Jobs',
      secondaryTo: '/jobs'
    }
  }

  if (authStore.isAuthenticated) {
    return {
      title: 'Your next opportunity is waiting.',
      description: 'Keep applying to quality roles and track progress in your profile.',
      primaryLabel: 'Explore Jobs',
      primaryTo: '/jobs',
      secondaryLabel: 'Open Profile',
      secondaryTo: '/profile'
    }
  }

  return {
    title: 'Start your hiring journey today.',
    description: 'Create an account in minutes and connect with roles or candidates that fit.',
    primaryLabel: 'Create Account',
    primaryTo: '/register',
    secondaryLabel: 'Browse Jobs',
    secondaryTo: '/jobs'
  }
})

const salaryLabel = (min: number, max: number): string => {
  return `$${Number(min).toLocaleString()} - $${Number(max).toLocaleString()}`
}

const companyLabel = (email?: string): string => {
  return email ?? 'Company'
}

const formatType = (value: Job['job_type']): string => {
  return value.replace('-', ' ').replace(/\b\w/g, (char) => char.toUpperCase())
}

const fetchJobs = async (): Promise<void> => {
  await jobsStore.fetchAll()
}

onMounted(fetchJobs)
</script>
