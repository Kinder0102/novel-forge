import { defineStore } from 'pinia'
import { getModuleConfigs, updateModuleConfig, deleteModuleConfig } from '../api'

export const useSettingsStore = defineStore('settings', {
  state: () => ({
    modules: [],
    loading: false,
    error: null
  }),
  actions: {
    async fetchAll() {
      this.loading = true
      this.error = null
      try {
        const res = await getModuleConfigs()
        this.modules = res.data
      } catch (e) {
        this.error = e.response?.data?.detail || e.message
      } finally {
        this.loading = false
      }
    },
    async updateModule(moduleName, data) {
      this.loading = true
      this.error = null
      try {
        const res = await updateModuleConfig(moduleName, data)
        const idx = this.modules.findIndex(m => m.module_name === moduleName)
        if (idx >= 0) this.modules[idx] = res.data
        else this.modules.push(res.data)
        return true
      } catch (e) {
        this.error = e.response?.data?.detail || e.message
        return false
      } finally {
        this.loading = false
      }
    },
    async deleteModule(moduleName) {
      this.loading = true
      this.error = null
      try {
        await deleteModuleConfig(moduleName)
        const idx = this.modules.findIndex(m => m.module_name === moduleName)
        if (idx >= 0) this.modules[idx] = { ...this.modules[idx], api_key: null, base_url: null, model: null }
        return true
      } catch (e) {
        this.error = e.response?.data?.detail || e.message
        return false
      } finally {
        this.loading = false
      }
    }
  }
})
