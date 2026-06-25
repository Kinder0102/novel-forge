<template>
  <div class="task-panel-root">
    <button
      class="task-fab"
      :class="{ active: open }"
      @click="togglePanel"
      :title="open ? t('taskPanel.collapse') : t('taskPanel.title')"
    >
      <font-awesome-icon :icon="['fas', 'code']" class="text-lg" />
      <span
        v-if="taskLogStore.llmLogs.length && !open"
        class="task-badge"
      >{{ taskLogStore.llmLogs.length > 99 ? '99+' : taskLogStore.llmLogs.length }}</span>
    </button>

    <Transition name="panel">
      <div v-if="open" class="task-panel">
        <div class="flex items-center justify-between px-4 py-3 border-b border-gray-700 shrink-0">
          <h3 class="text-sm font-semibold text-gray-200">{{ t('taskPanel.title') }}</h3>
          <div class="flex items-center gap-2">
            <span v-if="polling" class="text-[10px] text-gray-500">● {{ t('taskPanel.listening') }}</span>
            <button
              v-if="taskLogStore.llmLogs.length"
              @click="handleClear"
              class="text-xs text-gray-400 hover:text-red-400 transition-colors"
              :title="t('taskPanel.clear')"
            >
              {{ t('taskPanel.clear') }}
            </button>
            <button
              @click="open = false"
              class="text-gray-400 hover:text-gray-200 transition-colors"
            >
              <font-awesome-icon :icon="['fas', 'times']" />
            </button>
          </div>
        </div>

        <div class="flex-1 overflow-y-auto">
          <div v-if="!taskLogStore.llmLogs.length" class="p-4 text-center text-gray-500 text-sm">
            {{ t('taskPanel.noLogs') }}
          </div>
          <div
            v-for="log in taskLogStore.llmLogs"
            :key="log.id"
            class="border-b border-gray-700/50"
          >
            <button
              class="w-full flex items-center gap-3 px-4 py-3 hover:bg-gray-700/30 transition-colors text-left"
              @click="log.expanded = !log.expanded"
            >
              <span
                class="shrink-0 w-2 h-2 rounded-full"
                :class="log.error ? 'bg-red-500' : 'bg-emerald-500'"
              ></span>
              <span class="text-xs text-gray-400 shrink-0 w-24 uppercase tracking-wider">{{ log.module }}</span>
              <span class="text-xs font-mono text-gray-300 truncate flex-1">{{ log.model }}</span>
              <span class="text-[10px] text-gray-500 shrink-0">{{ fmtDuration(log.duration_ms) }}</span>
              <font-awesome-icon
                :icon="['fas', 'chevron-down']"
                class="text-gray-500 text-xs transition-transform"
                :class="{ 'rotate-180': log.expanded }"
              />
            </button>

            <div v-if="log.expanded" class="px-4 pb-3 space-y-2">
              <div class="grid grid-cols-2 gap-2 text-xs">
                <div>
                  <div class="text-gray-500 mb-1 font-medium">{{ t('taskPanel.module') }}</div>
                  <div class="text-gray-300">{{ log.module }}</div>
                </div>
                <div>
                  <div class="text-gray-500 mb-1 font-medium">{{ t('taskPanel.duration') }}</div>
                  <div class="text-gray-300">{{ fmtDuration(log.duration_ms) }}</div>
                </div>
              </div>
              <div class="text-xs">
                <div class="text-gray-500 mb-1 font-medium">{{ t('taskPanel.llmUrl') }}</div>
                <pre class="p-2 rounded text-xs overflow-x-auto whitespace-pre-wrap break-all font-mono bg-gray-800 text-gray-300">{{ log.llm_url }}</pre>
              </div>
              <div class="text-xs">
                <div class="text-gray-500 mb-1 font-medium">{{ t('taskPanel.model') }}</div>
                <pre class="p-2 rounded text-xs overflow-x-auto whitespace-pre-wrap break-all font-mono bg-gray-800 text-gray-300">{{ log.model }}</pre>
              </div>
              <div class="text-xs">
                <div class="text-gray-500 mb-1 font-medium">{{ t('taskPanel.prompt') }}</div>
                <pre class="p-2 rounded text-xs overflow-x-auto whitespace-pre-wrap break-all font-mono bg-gray-800 text-gray-300">{{ fmtJson(log.request) }}</pre>
              </div>
              <div class="text-xs">
                <div class="text-gray-500 mb-1 font-medium">{{ t('taskPanel.response') }}</div>
                <pre
                  class="p-2 rounded text-xs overflow-x-auto whitespace-pre-wrap break-all font-mono"
                  :class="log.error ? 'bg-red-900/30 text-red-300' : 'bg-gray-800 text-gray-300'"
                >{{ log.error ? log.error : log.response }}</pre>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template><script setup lang="ts">
import { ref, onUnmounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useTaskLogStore } from '../stores/taskLog'
import { getLlmLogs, clearLlmLogs } from '../api'

const { t } = useI18n()
const taskLogStore = useTaskLogStore()
const open = ref(false)
const polling = ref(false)
let timer: ReturnType<typeof setInterval> | null = null
const POLL_INTERVAL = 2000

async function fetchLogs() {
  try {
    const res = await getLlmLogs()
    taskLogStore.replaceLlmLogs(res.data)
  } catch {
    
  }
}

function startPolling() {
  if (timer) return
  polling.value = true
  fetchLogs()
  timer = setInterval(fetchLogs, POLL_INTERVAL)
}

function stopPolling() {
  if (timer) {
    clearInterval(timer)
    timer = null
  }
  polling.value = false
}

function togglePanel() {
  open.value = !open.value
  if (open.value) {
    startPolling()
  } else {
    stopPolling()
  }
}

async function handleClear() {
  try {
    await clearLlmLogs()
  } catch {
    
  }
  taskLogStore.clearLlmLogsStore()
}

onUnmounted(() => {
  stopPolling()
})

function fmtDuration(ms) {
  if (ms == null) return ''
  if (ms < 1000) return `${ms}ms`
  return `${(ms / 1000).toFixed(1)}s`
}

function fmtJson(obj) {
  if (!obj) return ''
  try {
    return JSON.stringify(obj, null, 2)
  } catch {
    return String(obj)
  }
}
</script><style scoped>
.task-panel-root {
  position: fixed;
  bottom: 24px;
  right: 24px;
  z-index: 9999;
}

.task-fab {
  position: absolute;
  bottom: 0;
  right: 0;
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: #1e293b;
  border: 1px solid #334155;
  color: #94a3b8;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4);
  transition: all 0.2s;
}
.task-fab:hover {
  background: #334155;
  color: #e2e8f0;
  transform: scale(1.05);
}
.task-fab.active {
  background: #4338ca;
  border-color: #6366f1;
  color: #e0e7ff;
}

.task-badge {
  position: absolute;
  top: -4px;
  right: -4px;
  min-width: 20px;
  height: 20px;
  border-radius: 10px;
  background: #ef4444;
  color: #fff;
  font-size: 10px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 5px;
  border: 2px solid #0f172a;
}

.task-panel {
  position: absolute;
  bottom: 60px;
  right: 0;
  width: 420px;
  max-height: 560px;
  background: #0f172a;
  border: 1px solid #334155;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.panel-enter-active,
.panel-leave-active {
  transition: all 0.25s ease;
}
.panel-enter-from,
.panel-leave-to {
  opacity: 0;
  transform: translateY(12px) scale(0.96);
}
</style>