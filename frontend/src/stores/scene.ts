import { createCrudStore } from './crudStoreFactory'
import { extractErrorMessage } from '../utils/error'
import * as api from '../api'
import type { SceneData } from '../types'

export type Scene = SceneData & {
  status: string
  content?: string
}

export interface GenerateScenesRequest {
  novel_id?: number
  chapter_title_id: number
  chapter_title?: string
  previous_summary?: string
  context?: string
  description?: string
}

export const useSceneStore = createCrudStore<Scene>({
  storeId: 'scene',
  itemsKey: 'scenes',
  apiModule: api,
  extraActions: {
    async generateScenes(data: GenerateScenesRequest) {
      this.loading = true
      this.error = null
      try {
        const res = await api.generateScenes(data)
        if (Array.isArray(res.data)) {
          
          
          this.scenes = [...this.scenes, ...res.data]
        }
        return res.data
      } catch (e: unknown) {
        this.error = extractErrorMessage(e)
      } finally {
        this.loading = false
      }
    },
    async loadAllForOutlines(outlineIds: number[]) {
      this.loading = true
      this.error = null
      try {
        const results = await Promise.allSettled(outlineIds.map((id) => api.getScenesByOutline(id)))
        this.scenes = results
          .filter((r): r is PromiseFulfilledResult<{ data: Scene[] }> => r.status === 'fulfilled')
          .flatMap((r) => r.value.data || [])
      } catch (e: unknown) {
        this.error = extractErrorMessage(e)
      } finally {
        this.loading = false
      }
    },
    async regenerateSummary(sceneId: number) {
      const res = await api.regenerateSceneSummary(sceneId)
      const idx = this.scenes.findIndex((s) => s.id === sceneId)
      if (idx !== -1) this.scenes[idx] = res.data
      return res.data
    },
  },
})
