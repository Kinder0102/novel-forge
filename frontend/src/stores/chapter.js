import { defineStore } from 'pinia'
import * as api from '../api'

export const useChapterStore = defineStore('chapter', {
  state: () => ({
    chapters: [],
    current: null,
    loading: false,
    error: null
  }),
  actions: {
    async fetchAll(outlineId) {
      this.loading = true
      this.error = null
      try {
        const res = await api.getChapters(outlineId)
        this.chapters = res.data
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
        const res = await api.createChapter(data)
        this.chapters.push(res.data)
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
        const res = await api.updateChapter(id, data)
        const idx = this.chapters.findIndex(c => c.id === id)
        if (idx !== -1) this.chapters[idx] = res.data
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
        await api.deleteChapter(id)
        this.chapters = this.chapters.filter(c => c.id !== id)
      } catch (e) {
        this.error = e.response?.data?.detail || e.message
      } finally {
        this.loading = false
      }
    },
    async generateChapter(data) {
      this.loading = true
      this.error = null
      try {
        const res = await api.generateChapter(data)
        this.chapters.push(res.data)
        return res.data
      } catch (e) {
        this.error = e.response?.data?.detail || e.message
      } finally {
        this.loading = false
      }
    },
    async exportChapters(outlineId) {
      this.loading = true
      this.error = null
      try {
        const res = await api.exportChapters(outlineId)
        return res.data
      } catch (e) {
        this.error = e.response?.data?.detail || e.message
      } finally {
        this.loading = false
      }
    }
  }
})
