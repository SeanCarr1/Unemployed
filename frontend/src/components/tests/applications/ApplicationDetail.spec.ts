import { mount } from '@vue/test-utils'
import ApplicationDetail from '@/components/ApplicationDetail.vue'
import { describe, it, expect, beforeEach, vi } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
// import and mock your applications store as needed

beforeEach(() => {
  setActivePinia(createPinia())
})

describe('ApplicationDetail.vue', () => {
  it('renders application details', () => {
    // TODO: mock application in store/props and assert details are shown
  })

  it('shows loading indicator', () => {
    // TODO: mock loading state and assert UI
  })

  it('shows error message', () => {
    // TODO: mock error state and assert UI
  })
})
