
import { mount } from '@vue/test-utils'
import JobList from '@/components/jobs/JobList.vue'
import { describe, it, expect, beforeEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'

beforeEach(() => {
  setActivePinia(createPinia())
})

describe('JobList.vue', () => {
  it('renders job list title', () => {
    const wrapper = mount(JobList)
    expect(wrapper.text()).toContain('Job Listings')
  })
})
