
import { mount } from '@vue/test-utils'
import JobEdit from '@/components/JobEdit.vue'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { useJobsStore } from '@/stores/jobs'
import { setActivePinia, createPinia } from 'pinia'

vi.mock('vue-router', async (importOriginal) => {
  const actual = await importOriginal() as Record<string, unknown>;
  return {
    ...actual,
    useRoute: () => ({ params: { pk: 1 } }),
    useRouter: () => ({ push: vi.fn() })
  }
})

beforeEach(() => {
  setActivePinia(createPinia())
})

describe('JobEdit.vue', () => {
  it('renders edit job form', () => {
    const wrapper = mount(JobEdit)
    expect(wrapper.text()).toContain('Edit Job')
  })

  it('shows error message from store', () => {
    const store = useJobsStore()
    store.error = 'Test error'
    const wrapper = mount(JobEdit)
    expect(wrapper.text()).toContain('Test error')
  })

  it('shows loading indicator', () => {
    const store = useJobsStore()
    store.loading = true
    const wrapper = mount(JobEdit)
    expect(wrapper.text()).toContain('Loading')
  })

  it('calls updateJob on submit', async () => {
    const store = useJobsStore()
    // Mock a valid Job object for updateJob
    const mockJob = {
      id: 1,
      title: 'Test Job',
      description: 'Test Description',
      location: 'Test Location',
      salary_min: 500,
      salary_max: 1500,
      job_type: 'full-time',
      employer_email: 'employer@example.com',
      posted_at: '2025-07-18T00:00:00Z',
    };
    const spy = vi.spyOn(store, 'updateJob').mockResolvedValue(mockJob)
    const wrapper = mount(JobEdit)
    await wrapper.find('form').trigger('submit.prevent')
    expect(spy).toHaveBeenCalled()
  })
})
