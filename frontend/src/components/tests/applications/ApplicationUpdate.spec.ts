import { mount } from '@vue/test-utils'
import ApplicationUpdate from '@/components/ApplicationUpdate.vue'
import { describe, it, expect, beforeEach, vi } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
// import and mock your applications store as needed

beforeEach(() => {
  setActivePinia(createPinia())
})

describe('ApplicationUpdate.vue', () => {
  it('renders update form for application', () => {
    // TODO: mock application and assert form fields
  })

  it('submits update and shows success', async () => {
    // TODO: mock store action, submit, assert success UI
  })

  it('shows error on invalid update', async () => {
    // TODO: mock error, submit, assert error UI
  })

  it('shows forbidden error for seeker', async () => {
    // TODO: mock seeker role, submit, assert forbidden UI
  })
})
