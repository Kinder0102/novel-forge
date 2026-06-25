import axios from 'axios'
import { useTaskLogStore } from '../stores/taskLog'
import type {
  NovelData,
  WorldbuildingData,
  CharacterData,
  OutlineData,
  ChapterTitleData,
  SceneData,
  ChapterContentData,
  ModuleConfigData,
  LlmCallLogData,
} from '../types'

export type { NovelData, WorldbuildingData, CharacterData, OutlineData, ChapterTitleData, SceneData, ChapterContentData, ModuleConfigData, LlmCallLogData }

const base = import.meta.env.VITE_API_BASE_URL as string | undefined
const baseURL = base ? `${base.replace(/\/$/, '')}/api` : '/api'

const apiClient = axios.create({ baseURL })


const pendingLLM = new Map<string, { url: string; method: string; data: unknown; timestamp: string }>()

function isLLMEndpoint(url: string): boolean {
  const patterns = [
    /\/worldbuilding\/\d+\/generate$/,
    /\/character\/generate$/,
    /\/outline\/generate$/,
    /\/scene\/bulk-generate$/,
    /\/chapter\/generate$/,
    /\/chapter\/\d+\/summary$/,
    /\/worldbuilding\/\d+\/summary$/,
    /\/character\/\d+\/summary$/,
    /\/outline\/\d+\/summary$/,
    /\/scene\/\d+\/summary$/,
  ]
  return patterns.some((p) => p.test(url))
}

apiClient.interceptors.request.use((config) => {
  if (config.url && isLLMEndpoint(config.url)) {
    const id = Date.now() + '_' + Math.random().toString(36).slice(2, 8)
    pendingLLM.set(id, {
      url: config.url,
      method: config.method?.toUpperCase() ?? 'GET',
      data: { ...config.data },
      timestamp: new Date().toISOString(),
    })
    ;(config as Record<string, unknown>).__llmId = id
  }
  return config
})

apiClient.interceptors.response.use(
  (response) => {
    const id = (response.config as Record<string, unknown>)?.__llmId as string | undefined
    if (id && pendingLLM.has(id)) {
      const req = pendingLLM.get(id)!
      useTaskLogStore().addTaskLog({
        url: req.url,
        method: req.method,
        requestData: req.data,
        responseData: response.data,
        timestamp: req.timestamp,
        status: response.status,
      })
      pendingLLM.delete(id)
    }
    return response
  },
  (error) => {
    const id = (error.config as Record<string, unknown>)?.__llmId as string | undefined
    if (id && pendingLLM.has(id)) {
      const req = pendingLLM.get(id)!
      useTaskLogStore().addTaskLog({
        url: req.url,
        method: req.method,
        requestData: req.data,
        responseData: error.response?.data || { error: error.message },
        timestamp: req.timestamp,
        status: error.response?.status || 0,
        error: true,
      })
      pendingLLM.delete(id)
    }
    
    const status = error.response?.status
    if (status && status >= 500) {
      console.error('[Global Error] Server Error', status, error.response?.data)
    } else if (status === 401) {
      console.error('[Global Error] Unauthorized', error.response?.data)
    }
    return Promise.reject(error)
  },
)


export const getNovels = () => apiClient.get<NovelData[]>('/novels/')
export const getNovel = (id: number) => apiClient.get<NovelData>(`/novels/${id}`)
export const createNovel = (data: Partial<NovelData>) => apiClient.post<NovelData>('/novels/', data)
export const updateNovel = (id: number, data: Partial<NovelData>) => apiClient.put<NovelData>(`/novels/${id}`, data)
export const deleteNovel = (id: number) => apiClient.delete(`/novels/${id}`)

export const getWorldbuildings = (novelId?: number) => {
  const params: Record<string, number> = {}
  if (novelId) params.novel_id = novelId
  return apiClient.get<WorldbuildingData[]>('/worldbuilding/', { params })
}
export const getWorldbuilding = (id: number) => apiClient.get<WorldbuildingData>(`/worldbuilding/${id}`)
export const updateWorldbuilding = (id: number, data: Partial<WorldbuildingData>) =>
  apiClient.put<WorldbuildingData>(`/worldbuilding/${id}`, data)
export const deleteWorldbuilding = (id: number) => apiClient.delete(`/worldbuilding/${id}`)
export const generateWorldbuilding = (novelId: number, theme: string) =>
  apiClient.post<WorldbuildingData>(`/worldbuilding/generate`, { novel_id: novelId, theme })


export const getCharacters = ({ worldbuildingId, novelId }: { worldbuildingId?: number; novelId?: number } = {}) => {
  const params: Record<string, number> = {}
  if (novelId) params.novel_id = novelId
  else if (worldbuildingId) params.worldbuilding_id = worldbuildingId
  return apiClient.get<CharacterData[]>('/character/', { params })
}
export const createCharacter = (data: Partial<CharacterData>) =>
  apiClient.post<CharacterData>('/character/', data)
export const updateCharacter = (id: number, data: Partial<CharacterData>) =>
  apiClient.put<CharacterData>(`/character/${id}`, data)
export const deleteCharacter = (id: number) => apiClient.delete(`/character/${id}`)
export const generateCharacters = (data: Record<string, unknown>) =>
  apiClient.post('/character/generate', data)


export const getOutlines = ({ worldbuildingId, novelId }: { worldbuildingId?: number; novelId?: number } = {}) => {
  const params: Record<string, number> = {}
  if (novelId) params.novel_id = novelId
  else if (worldbuildingId) params.worldbuilding_id = worldbuildingId
  return apiClient.get<OutlineData[]>('/outline/', { params })
}
export const getOutline = (id: number) => apiClient.get<OutlineData>(`/outline/${id}`)
export const createOutline = (data: Partial<OutlineData>) =>
  apiClient.post<OutlineData>('/outline/', data)
export const updateOutline = (id: number, data: Partial<OutlineData>) =>
  apiClient.put<OutlineData>(`/outline/${id}`, data)
export const deleteOutline = (id: number) => apiClient.delete(`/outline/${id}`)
export const generateOutline = (data: Record<string, unknown>) =>
  apiClient.post<OutlineData>('/outline/generate', data)


export const getChapterTitles = (outlineId: number) =>
  apiClient.get<ChapterTitleData[]>('/chapter-title/', { params: { outline_id: outlineId } })
export const createChapterTitle = (data: Partial<ChapterTitleData>) =>
  apiClient.post<ChapterTitleData>('/chapter-title/', data)
export const updateChapterTitle = (id: number, data: Partial<ChapterTitleData>) =>
  apiClient.put<ChapterTitleData>(`/chapter-title/${id}`, data)
export const deleteChapterTitle = (id: number) => apiClient.delete(`/chapter-title/${id}`)
export const reorderChapterTitles = (data: { outline_id: number; moved_id: number; prev_id: number | null; next_id: number | null }) =>
  apiClient.post('/chapter-title/reorder', data)


export const getScenes = (chapterTitleId: number) =>
  apiClient.get<SceneData[]>('/scene/', { params: { chapter_title_id: chapterTitleId } })
export const getScenesByOutline = (outlineId: number) =>
  apiClient.get<SceneData[]>('/scene/', { params: { outline_id: outlineId } })
export const getScene = (id: number) => apiClient.get<SceneData>(`/scene/${id}`)
export const createScene = (data: Partial<SceneData>) =>
  apiClient.post<SceneData>('/scene/', data)
export const updateScene = (id: number, data: Partial<SceneData>) =>
  apiClient.put<SceneData>(`/scene/${id}`, data)
export const deleteScene = (id: number) => apiClient.delete(`/scene/${id}`)
export const generateScenes = (data: Record<string, unknown>) =>
  apiClient.post<SceneData[]>('/scene/bulk-generate', data)


export const getChapters = (outlineId: number) =>
  apiClient.get<ChapterContentData[]>('/chapter/', { params: { outline_id: outlineId } })
export const getChapter = (id: number) => apiClient.get<ChapterContentData>(`/chapter/${id}`)
export const createChapter = (data: Partial<ChapterContentData>) =>
  apiClient.post<ChapterContentData>('/chapter/', data)
export const updateChapter = (id: number, data: Partial<ChapterContentData>) =>
  apiClient.put<ChapterContentData>(`/chapter/${id}`, data)
export const deleteChapter = (id: number) => apiClient.delete(`/chapter/${id}`)
export const generateChapter = (data: Record<string, unknown>) =>
  apiClient.post<ChapterContentData>('/chapter/generate', data)
export const regenerateSummary = (chapId: number) =>
  apiClient.post<ChapterContentData>(`/chapter/${chapId}/summary`)

export const regenerateWorldbuildingSummary = (id: number) =>
  apiClient.post<WorldbuildingData>(`/worldbuilding/${id}/summary`)

export const regenerateCharacterSummary = (id: number) =>
  apiClient.post<CharacterData>(`/character/${id}/summary`)

export const regenerateOutlineSummary = (id: number) =>
  apiClient.post<OutlineData>(`/outline/${id}/summary`)

export const regenerateSceneSummary = (id: number) =>
  apiClient.post<SceneData>(`/scene/${id}/summary`)


export const getModuleConfigs = () => apiClient.get<ModuleConfigData[]>('/settings/modules')
export const getModuleConfig = (moduleName: string) =>
  apiClient.get<ModuleConfigData>(`/settings/modules/${moduleName}`)
export const updateModuleConfig = (moduleName: string, data: Partial<ModuleConfigData>) =>
  apiClient.put<ModuleConfigData>(`/settings/modules/${moduleName}`, data)
export const deleteModuleConfig = (moduleName: string) =>
  apiClient.delete(`/settings/modules/${moduleName}`)


export const getLlmLogs = () => apiClient.get<LlmCallLogData[]>('/llm-logs')
export const clearLlmLogs = () => apiClient.delete('/llm-logs')
