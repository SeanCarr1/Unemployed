import { mount } from '@vue/test-utils'
import ApplicationList from '@/components/ApplicationList.vue'
import { describe, it, expect, beforeEach, vi } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
// import and mock your applications store as needed

beforeEach(() => {
  setActivePinia(createPinia())
})

describe('ApplicationList.vue', () => {
  it('renders application list title', () => {
    const wrapper = mount(ApplicationList)
    expect(wrapper.text()).toContain('Applications')
  })

  it('shows loading indicator', () => {
    // TODO: mock loading state in store and assert UI
  })

  it('shows error message', () => {
    // TODO: mock error state in store and assert UI
  })

  it('renders applications from store', () => {
    // TODO: mock applications in store and assert they are rendered
  })

  it('shows empty state if no applications', () => {
    // TODO: mock empty applications and assert UI
  })
})
