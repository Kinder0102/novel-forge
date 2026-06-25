







import { defineStore } from 'pinia'

interface TaskLogEntry {
  id?: number
  expanded?: boolean
  url?: string
  method?: string
  requestData?: unknown
  responseData?: unknown
  timestamp?: string
  status?: number
  error?: boolean
}

interface LlmLogItem {
  id: number | string
  expanded?: boolean
}

export const useTaskLogStore = defineStore('taskLog', {
  state: () => ({
    _id: 0,
    taskLogs: [] as TaskLogEntry[],
    llmLogs: [] as LlmLogItem[],
  }),

  getters: {
    llmLogCount: (state) => state.llmLogs.length,
  },

  actions: {
    addTaskLog(entry: TaskLogEntry) {
      this.taskLogs.unshift({ id: ++this._id, expanded: false, ...entry })
      if (this.taskLogs.length > 50) this.taskLogs.pop()
    },

    clearTaskLogs() {
      this.taskLogs.splice(0, this.taskLogs.length)
    },

    replaceLlmLogs(logs: LlmLogItem[]) {
      const expandedMap: Record<string, boolean> = {}
      for (const item of this.llmLogs) {
        if (item.expanded) expandedMap[String(item.id)] = true
      }
      this.llmLogs.splice(0, this.llmLogs.length)
      for (const log of logs) {
        this.llmLogs.push({ ...log, expanded: expandedMap[String(log.id)] || false })
      }
    },

    clearLlmLogsStore() {
      this.llmLogs.splice(0, this.llmLogs.length)
    },
  },
})
