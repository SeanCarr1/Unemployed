import { defineStore } from 'pinia'

interface Toast {
  id: number
  message: string
  type: 'success' | 'error'
}

export const useToastStore = defineStore('toast', {
  state: () => ({
    toasts: [] as Toast[],
    nextId: 1,
  }),
  actions: {
    success(message: string) {
      this.add(message, 'success')
    },
    error(message: string) {
      this.add(message, 'error')
    },
    add(message: string, type: 'success' | 'error') {
      const id = this.nextId++
      this.toasts.push({ id, message, type })
      setTimeout(() => this.remove(id), 5000)
    },
    remove(id: number) {
      this.toasts = this.toasts.filter((t) => t.id !== id)
    },
  },
})
