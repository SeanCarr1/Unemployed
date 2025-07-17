
import { mount } from '@vue/test-utils'
import JobEdit from '../components/JobEdit.vue'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { useJobsStore } from '../stores/jobs'
import { setActivePinia, createPinia } from 'pinia'

vi.mock('vue-router', () => ({
  useRoute: () => ({ params: { pk: 1 } }),
  useRouter: () => ({ push: vi.fn() })
}))

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
    const spy = vi.spyOn(store, 'updateJob').mockResolvedValue({})
    const wrapper = mount(JobEdit)
    await wrapper.find('form').trigger('submit.prevent')
    expect(spy).toHaveBeenCalled()
  })
})
