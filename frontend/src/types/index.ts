
export interface ApiResponse<T = unknown> {
  data: T
}

export interface NovelData {
  id: number
  title: string
  description?: string
  writing_style?: string
  status?: string
  created_at?: string
  updated_at?: string
}

export interface WorldbuildingData {
  id: number
  novel_id?: number
  title: string
  genre: string
  description: string
  setting: string
  rules: string
  summary?: string
  created_at?: string
  updated_at?: string
}

export interface CharacterData {
  id: number
  worldbuilding_id: number
  novel_id?: number
  name: string
  role: string
  personality: string
  background: string
  appearance: string
  created_at?: string
  updated_at?: string
}

export interface OutlineData {
  id: number
  novel_id?: number
  worldbuilding_id: number
  title: string
  description: string
  summary: string
  chapters?: ChapterTitleData[]
  created_at?: string
  updated_at?: string
}

export interface ChapterTitleData {
  id: number
  outline_id: number
  idx: number
  title: string
}

export interface SceneData {
  id: number
  chapter_title_id: number
  scene_number: number
  title: string
  description: string
  summary: string
  content?: string
  status: string
  created_at?: string
  updated_at?: string
}

export interface ChapterContentData {
  id: number
  chapter_title_id: number
  content: string
  description: string
  summary: string
  status: string
  created_at?: string
  updated_at?: string
}

export interface ModuleConfigData {
  id?: number
  module_name: string
  api_key?: string
  base_url?: string
  model?: string
  system_prompt?: string
  user_prompt_template?: string
  updated_at?: string
}

export interface LlmCallLogData {
  id: number
  module: string
  model: string
  llm_url: string
  status: string
  request?: unknown
  response?: string
  prompt_tokens?: number
  completion_tokens?: number
  total_tokens?: number
  duration_ms?: number
  error?: string
  created_at: string
  updated_at: string
}
