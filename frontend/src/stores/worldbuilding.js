import { defineStore } from 'pinia'
import * as api from '../api'

export const useWorldbuildingStore = defineStore('worldbuilding', {
  state: () => ({
    worldbuildings: [],
    current: null,
    loading: false,
    error: null
  }),
  actions: {
    async fetchAll() {
      this.loading = true
      this.error = null
      try {
        const res = await api.getWorldbuildings()
        this.worldbuildings = res.data
      } catch (e) {
        this.error = e.response?.data?.detail || e.message
      } finally {
        this.loading = false
      }
    },
    async fetchOne(id) {
      this.loading = true
      this.error = null
      try {
        const res = await api.getWorldbuilding(id)
        this.current = res.data
      } catch (e) {
        this.error = e.response?.data?.detail || e.message
      } finally {
        this.loading = false
      }
    },
    async create(data) {
      this.loading = true
      this.error = null
      try {
        const res = await api.createWorldbuilding(data)
        this.worldbuildings.push(res.data)
        return res.data
      } catch (e) {
        this.error = e.response?.data?.detail || e.message
      } finally {
        this.loading = false
      }
    },
    async update(id, data) {
      this.loading = true
      this.error = null
      try {
        const res = await api.updateWorldbuilding(id, data)
        const idx = this.worldbuildings.findIndex(w => w.id === id)
        if (idx !== -1) this.worldbuildings[idx] = res.data
        return res.data
      } catch (e) {
        this.error = e.response?.data?.detail || e.message
      } finally {
        this.loading = false
      }
    },
    async remove(id) {
      this.loading = true
      this.error = null
      try {
        await api.deleteWorldbuilding(id)
        this.worldbuildings = this.worldbuildings.filter(w => w.id !== id)
      } catch (e) {
        this.error = e.response?.data?.detail || e.message
      } finally {
        this.loading = false
      }
    },
    async generateWorldbuilding(id, theme) {
      this.loading = true
      this.error = null
      try {
        const res = await api.generateWorldbuilding(id, theme)
        const idx = this.worldbuildings.findIndex(w => w.id === id)
        if (idx !== -1) this.worldbuildings[idx] = res.data
        return res.data
      } catch (e) {
        this.error = e.response?.data?.detail || e.message
      } finally {
        this.loading = false
      }
    }
  }
})
