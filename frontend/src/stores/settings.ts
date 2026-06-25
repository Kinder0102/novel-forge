














import { defineStore } from 'pinia'
import axios from 'axios'
import { extractErrorMessage } from '../utils/error'
import { getModuleConfigs, updateModuleConfig, deleteModuleConfig } from '../api'
import type { ModuleConfigData } from '../types'

export const useSettingsStore = defineStore('settings', {
  state: () => ({
    modules: [] as ModuleConfigData[],
    loading: false,
    error: null as string | null,
  }),
  actions: {
    async fetchAll() {
      this.loading = true
      this.error = null
      try {
        const res = await getModuleConfigs()
        this.modules = res.data
      } catch (e: unknown) {
        this.error = extractErrorMessage(e)
      } finally {
        this.loading = false
      }
    },
    async updateModule(moduleName: string, data: Partial<ModuleConfigData>) {
      this.loading = true
      this.error = null
      try {
        const res = await updateModuleConfig(moduleName, data)
        const idx = this.modules.findIndex((m) => m.module_name === moduleName)
        if (idx >= 0) this.modules[idx] = res.data
        else this.modules.push(res.data)
        return true
      } catch (e: unknown) {
        this.error = extractErrorMessage(e)
        return false
      } finally {
        this.loading = false
      }
    },
    async deleteModule(moduleName: string) {
      this.loading = true
      this.error = null
      try {
        await deleteModuleConfig(moduleName)
        this.modules = this.modules.filter((m) => m.module_name !== moduleName)
        return true
      } catch (e: unknown) {
        this.error = extractErrorMessage(e)
        return false
      } finally {
        this.loading = false
      }
    },
  },
})
