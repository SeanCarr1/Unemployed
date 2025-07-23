// crudFactory.ts
// Factory function for generic Pinia CRUD stores
import { ref } from 'vue'

export function useCrudStore<T, CreatePayload = Partial<T>, UpdatePayload = Partial<T>>(api: {
  list: () => Promise<T[]>,
  get: (id: number) => Promise<T>,
  create: (payload: CreatePayload) => Promise<T>,
  update: (id: number, payload: UpdatePayload) => Promise<T>,
  remove: (id: number) => Promise<void>
}) {
  const items = ref<T[]>([])
  const selected = ref<T | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function fetchAll() {
    loading.value = true
    error.value = null
    try {
      items.value = await api.list()
    } catch (err: any) {
      error.value = err.detail || err.message || 'Failed to fetch items'
    } finally {
      loading.value = false
    }
  }

  async function fetchOne(id: number) {
    loading.value = true
    error.value = null
    try {
      selected.value = await api.get(id)
    } catch (err: any) {
      error.value = err.detail || err.message || 'Failed to fetch item'
    } finally {
      loading.value = false
    }
  }

  async function create(payload: CreatePayload) {
    loading.value = true
    error.value = null
    try {
      const item = await api.create(payload)
      items.value.push(item)
      return item
    } catch (err: any) {
      error.value = err.detail || err.message || 'Failed to create item'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function update(id: number, payload: UpdatePayload) {
    loading.value = true
    error.value = null
    try {
      const item = await api.update(id, payload)
      const idx = items.value.findIndex(i => (i as any).id === id)
      if (idx !== -1) items.value[idx] = item
      if (selected.value && (selected.value as any).id === id) selected.value = item
      return item
    } catch (err: any) {
      error.value = err.detail || err.message || 'Failed to update item'
      throw err
    } finally {
      loading.value = false
    }
  }

  async function remove(id: number) {
    loading.value = true
    error.value = null
    try {
      await api.remove(id)
      items.value = items.value.filter(i => (i as any).id !== id)
      if (selected.value && (selected.value as any).id === id) selected.value = null
    } catch (err: any) {
      error.value = err.detail || err.message || 'Failed to delete item'
      throw err
    } finally {
      loading.value = false
    }
  }

  function clearError() {
    error.value = null
  }

  return {
    items,
    selected,
    loading,
    error,
    fetchAll,
    fetchOne,
    create,
    update,
    remove,
    clearError
  }
}
