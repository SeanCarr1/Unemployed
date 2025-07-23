import { mount } from '@vue/test-utils'
import ApplicationForm from '@/components/ApplicationForm.vue'
import { describe, it, expect, beforeEach, vi } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
// import and mock your applications store as needed

beforeEach(() => {
  setActivePinia(createPinia())
})

describe('ApplicationForm.vue', () => {
  it('renders application form fields', () => {
    const wrapper = mount(ApplicationForm)
    expect(wrapper.text()).toContain('Apply')
  })

  it('submits application and shows success', async () => {
    // TODO: mock store action, fill form, submit, assert success UI
  })

  it('shows error on duplicate application', async () => {
    // TODO: mock store/API error, submit, assert error UI
  })

  it('shows forbidden error for employer', async () => {
    // TODO: mock employer role, submit, assert forbidden UI
  })

  it('shows validation errors for invalid data', async () => {
    // TODO: submit invalid form, assert validation errors
  })
})
