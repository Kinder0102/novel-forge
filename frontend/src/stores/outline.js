import { defineStore } from 'pinia'
import * as api from '../api'

export const useOutlineStore = defineStore('outline', {
  state: () => ({
    outlines: [],
    current: null,
    loading: false,
    error: null
  }),
  actions: {
    async fetchAll(worldbuildingId) {
      this.loading = true
      this.error = null
      try {
        const res = await api.getOutlines(worldbuildingId)
        this.outlines = res.data
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
        const res = await api.getOutline(id)
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
        const res = await api.createOutline(data)
        this.outlines.push(res.data)
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
        const res = await api.updateOutline(id, data)
        const idx = this.outlines.findIndex(o => o.id === id)
        if (idx !== -1) this.outlines[idx] = res.data
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
        await api.deleteOutline(id)
        this.outlines = this.outlines.filter(o => o.id !== id)
      } catch (e) {
        this.error = e.response?.data?.detail || e.message
      } finally {
        this.loading = false
      }
    },
    async generateOutline(data) {
      this.loading = true
      this.error = null
      try {
        const res = await api.generateOutline(data)
        this.outlines.push(res.data)
        return res.data
      } catch (e) {
        this.error = e.response?.data?.detail || e.message
      } finally {
        this.loading = false
      }
    }
  }
})
