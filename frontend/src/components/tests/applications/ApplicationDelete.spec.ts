import { mount } from '@vue/test-utils'
import ApplicationDelete from '@/components/ApplicationDelete.vue'
import { describe, it, expect, beforeEach, vi } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
// import and mock your applications store as needed

beforeEach(() => {
  setActivePinia(createPinia())
})

describe('ApplicationDelete.vue', () => {
  it('renders delete button', () => {
    // TODO: assert delete button is rendered
  })

  it('deletes application and shows success', async () => {
    // TODO: mock store action, click delete, assert success UI
  })

  it('shows error on forbidden/unauthorized delete', async () => {
    // TODO: mock forbidden error, click delete, assert error UI
  })
})
