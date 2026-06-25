import { defineStore } from 'pinia'
import * as api from '../api'

export const useSceneStore = defineStore('scene', {
  state: () => ({
    scenes: [],
    current: null,
    loading: false,
    error: null
  }),
  actions: {
    async fetchAll(outlineId, chapterIndex) {
      this.loading = true
      this.error = null
      try {
        const res = await api.getScenes(outlineId, chapterIndex)
        this.scenes = res.data
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
        const res = await api.createScene(data)
        this.scenes.push(res.data)
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
        const res = await api.updateScene(id, data)
        const idx = this.scenes.findIndex(s => s.id === id)
        if (idx !== -1) this.scenes[idx] = res.data
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
        await api.deleteScene(id)
        this.scenes = this.scenes.filter(s => s.id !== id)
      } catch (e) {
        this.error = e.response?.data?.detail || e.message
      } finally {
        this.loading = false
      }
    },
    async generateScenes(data) {
      this.loading = true
      this.error = null
      try {
        const res = await api.generateScenes(data)
        if (Array.isArray(res.data)) {
          this.scenes.push(...res.data)
        }
        return res.data
      } catch (e) {
        this.error = e.response?.data?.detail || e.message
      } finally {
        this.loading = false
      }
    },
    async generateContent(id) {
      this.loading = true
      this.error = null
      try {
        const res = await api.generateSceneContent(id)
        const idx = this.scenes.findIndex(s => s.id === id)
        if (idx !== -1) this.scenes[idx] = res.data
        return res.data
      } catch (e) {
        this.error = e.response?.data?.detail || e.message
      } finally {
        this.loading = false
      }
    }
  }
})
