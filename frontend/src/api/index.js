import axios from 'axios'

const apiClient = axios.create({
  baseURL: '/api'
})

// worldbuilding
export const getWorldbuildings = () => apiClient.get('/worldbuilding/')
export const getWorldbuilding = (id) => apiClient.get(`/worldbuilding/${id}`)
export const createWorldbuilding = (data) => apiClient.post('/worldbuilding/', data)
export const updateWorldbuilding = (id, data) => apiClient.put(`/worldbuilding/${id}`, data)
export const deleteWorldbuilding = (id) => apiClient.delete(`/worldbuilding/${id}`)
export const generateWorldbuilding = (id, theme) => apiClient.post(`/worldbuilding/${id}/generate`, { theme })

// character
export const getCharacters = (worldbuildingId) => apiClient.get('/character/', { params: { worldbuilding_id: worldbuildingId } })
export const createCharacter = (data) => apiClient.post('/character/', data)
export const updateCharacter = (id, data) => apiClient.put(`/character/${id}`, data)
export const deleteCharacter = (id) => apiClient.delete(`/character/${id}`)
export const generateCharacters = (data) => apiClient.post('/character/generate', data)

// outline
export const getOutlines = (worldbuildingId) => apiClient.get('/outline/', { params: { worldbuilding_id: worldbuildingId } })
export const getOutline = (id) => apiClient.get(`/outline/${id}`)
export const createOutline = (data) => apiClient.post('/outline/', data)
export const updateOutline = (id, data) => apiClient.put(`/outline/${id}`, data)
export const deleteOutline = (id) => apiClient.delete(`/outline/${id}`)
export const generateOutline = (data) => apiClient.post('/outline/generate', data)

// scene
export const getScenes = (outlineId, chapterIndex) => apiClient.get('/scene/', { params: { outline_id: outlineId, chapter_index: chapterIndex } })
export const createScene = (data) => apiClient.post('/scene/', data)
export const updateScene = (id, data) => apiClient.put(`/scene/${id}`, data)
export const deleteScene = (id) => apiClient.delete(`/scene/${id}`)
export const generateScenes = (data) => apiClient.post('/scene/generate', data)
export const generateSceneContent = (id) => apiClient.put(`/scene/${id}/content`)

// chapter
export const getChapters = (outlineId) => apiClient.get('/chapter/', { params: { outline_id: outlineId } })
export const createChapter = (data) => apiClient.post('/chapter/', data)
export const updateChapter = (id, data) => apiClient.put(`/chapter/${id}`, data)
export const deleteChapter = (id) => apiClient.delete(`/chapter/${id}`)
export const generateChapter = (data) => apiClient.post('/chapter/generate', data)
export const exportChapters = (outlineId) => apiClient.get(`/chapter/export/${outlineId}`, { responseType: 'text' })

// settings
export const getModuleConfigs = () => apiClient.get('/settings/modules')
export const getModuleConfig = (moduleName) => apiClient.get(`/settings/modules/${moduleName}`)
export const updateModuleConfig = (moduleName, data) => apiClient.put(`/settings/modules/${moduleName}`, data)
export const deleteModuleConfig = (moduleName) => apiClient.delete(`/settings/modules/${moduleName}`)
