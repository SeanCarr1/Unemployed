import { mount } from '@vue/test-utils'
import ApplicationForm from '@/components/ApplicationForm.vue'
import { describe, it, expect, beforeEach, vi } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useApplicationsStore } from '@/stores/applications'
import { nextTick } from 'vue'

beforeEach(() => {
  setActivePinia(createPinia())
})

describe('ApplicationForm.vue', () => {
  it('renders application form fields', () => {
    const wrapper = mount(ApplicationForm)
    expect(wrapper.text()).toContain('Apply')
  })


  it('submits application and shows success', async () => {
    const store = useApplicationsStore()
    vi.spyOn(store, 'create').mockResolvedValue({
      id: 1,
      job: 1,
      seeker: 1,
      resume: 'resume.pdf',
      cover_letter: 'I am interested.',
      status: 'pending',
      applied_at: new Date().toISOString()
    })
    const wrapper = mount(ApplicationForm, {
      global: { plugins: [createPinia()] }
    })
    // Fill form fields (adjust selectors as needed)
    await wrapper.find('input[name="position"]').setValue('Developer')
    await wrapper.find('textarea[name="coverLetter"]').setValue('I am interested.')
    await wrapper.find('form').trigger('submit.prevent')
    await nextTick()
    expect(wrapper.text()).toContain('Application submitted successfully')
  })


  it('shows error on duplicate application', async () => {
    const store = useApplicationsStore()
    vi.spyOn(store, 'create').mockRejectedValue({ response: { data: { error: 'Duplicate application' } } })
    const wrapper = mount(ApplicationForm, {
      global: { plugins: [createPinia()] }
    })
    await wrapper.find('input[name="position"]').setValue('Developer')
    await wrapper.find('textarea[name="coverLetter"]').setValue('I am interested.')
    await wrapper.find('form').trigger('submit.prevent')
    await nextTick()
    expect(wrapper.text()).toContain('Duplicate application')
  })


  it('shows forbidden error for employer', async () => {
    const store = useApplicationsStore()
    vi.spyOn(store, 'create').mockRejectedValue({ response: { status: 403, data: { error: 'Forbidden' } } })
    const wrapper = mount(ApplicationForm, {
      global: { plugins: [createPinia()] }
    })
    // Simulate employer role (adjust as needed)
    // If your component uses a user/auth store or prop, mock it here
    await wrapper.find('input[name="position"]').setValue('Developer')
    await wrapper.find('textarea[name="coverLetter"]').setValue('I am interested.')
    await wrapper.find('form').trigger('submit.prevent')
    await nextTick()
    expect(wrapper.text()).toContain('Forbidden')
  })


  it('shows validation errors for invalid data', async () => {
    const store = useApplicationsStore()
    vi.spyOn(store, 'create').mockRejectedValue({ response: { status: 400, data: { error: 'Validation error' } } })
    const wrapper = mount(ApplicationForm, {
      global: { plugins: [createPinia()] }
    })
    // Leave required fields empty
    await wrapper.find('form').trigger('submit.prevent')
    await nextTick()
    expect(wrapper.text()).toContain('Validation error')
  })
})
