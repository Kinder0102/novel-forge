import { defineStore } from 'pinia'
import * as api from '../api'

export const useCharacterStore = defineStore('character', {
  state: () => ({
    characters: [],
    current: null,
    loading: false,
    error: null
  }),
  actions: {
    async fetchAll(worldbuildingId) {
      this.loading = true
      this.error = null
      try {
        const res = await api.getCharacters(worldbuildingId)
        this.characters = res.data
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
        const res = await api.createCharacter(data)
        this.characters.push(res.data)
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
        const res = await api.updateCharacter(id, data)
        const idx = this.characters.findIndex(c => c.id === id)
        if (idx !== -1) this.characters[idx] = res.data
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
        await api.deleteCharacter(id)
        this.characters = this.characters.filter(c => c.id !== id)
      } catch (e) {
        this.error = e.response?.data?.detail || e.message
      } finally {
        this.loading = false
      }
    },
    async generateCharacters(data) {
      this.loading = true
      this.error = null
      try {
        const res = await api.generateCharacters(data)
        if (res.data && typeof res.data === 'object' && !Array.isArray(res.data)) {
          this.characters.push(res.data)
        }
        return res.data
      } catch (e) {
        this.error = e.response?.data?.detail || e.message
      } finally {
        this.loading = false
      }
    }
  }
})
