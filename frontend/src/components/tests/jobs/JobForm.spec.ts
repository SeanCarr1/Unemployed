
import { mount } from '@vue/test-utils'
import JobForm from '@/components/JobForm.vue'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { useJobsStore } from '@/stores/jobs'
import { setActivePinia, createPinia } from 'pinia'

beforeEach(() => {
  setActivePinia(createPinia())
})

describe('JobForm.vue', () => {
  it('renders create job form', () => {
    const wrapper = mount(JobForm)
    expect(wrapper.text()).toContain('Create Job')
  })

  it('shows error message from store', () => {
    const store = useJobsStore()
    store.error = 'Test error'
    const wrapper = mount(JobForm)
    expect(wrapper.text()).toContain('Test error')
  })

  it('shows loading indicator', () => {
    const store = useJobsStore()
    store.loading = true
    const wrapper = mount(JobForm)
    expect(wrapper.text()).toContain('Loading')
  })

  it('calls createJob on submit', async () => {
    const store = useJobsStore()
    const spy = vi.spyOn(store, 'createJob').mockResolvedValue({})
    const wrapper = mount(JobForm)
    await wrapper.find('form').trigger('submit.prevent')
    expect(spy).toHaveBeenCalled()
  })
})
