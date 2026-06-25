<template>
  <div class="max-w-4xl mx-auto px-4 py-8">
    <!-- Header -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900 flex items-center space-x-3">
        <font-awesome-icon icon="fa-solid fa-gear" class="text-indigo-600" />
        <span>LLM API 設定</span>
      </h1>
      <p class="mt-2 text-gray-500">每個功能模組可獨立配置 API，留空則使用 DEFAULT 預設值</p>
    </div>

    <!-- Loading -->
    <div v-if="store.loading && store.modules.length === 0" class="flex justify-center py-12">
      <font-awesome-icon icon="fa-solid fa-spinner" class="animate-spin text-3xl text-indigo-500" />
    </div>

    <!-- Error -->
    <div v-if="store.error && store.modules.length === 0" class="bg-red-50 border border-red-200 text-red-700 rounded-lg p-4 mb-6">
      {{ store.error }}
    </div>

    <!-- Module Cards -->
    <div v-for="mod in moduleList" :key="mod.module_name" class="my-4 bg-white border border-gray-200 rounded-xl shadow-sm p-6">
      <!-- Module Header -->
      <div class="flex items-center justify-between mb-5">
        <div class="flex items-center space-x-3">
          <font-awesome-icon :icon="mod.icon" class="text-xl text-indigo-500" />
          <h2 class="font-semibold text-lg text-gray-900">{{ mod.label }}</h2>
          <span
            class="text-xs px-2 py-0.5 rounded-full font-medium"
            :class="badgeClass(mod)"
          >{{ badgeText(mod) }}</span>
        </div>
        <button
          v-if="mod.module_name !== 'default'"
          @click="handleDelete(mod.module_name)"
          :disabled="deletingModule === mod.module_name"
          class="flex items-center space-x-1 text-sm bg-gray-200 hover:bg-gray-300 text-gray-700 px-3 py-1.5 rounded-lg transition-colors disabled:opacity-50"
        >
          <font-awesome-icon icon="fa-solid fa-undo" class="text-xs" />
          <span>清除設定</span>
        </button>
      </div>

      <!-- Fields -->
      <div class="space-y-4">
        <!-- API Key -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">API Key</label>
          <div class="relative">
            <input
              :type="showPassword[mod.module_name] ? 'text' : 'password'"
              v-model="formData[mod.module_name].api_key"
              placeholder="留空使用預設值"
              class="border border-gray-300 rounded-lg px-3 py-2 w-full pr-10 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
            />
            <button
              @click="togglePassword(mod.module_name)"
              class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
            >
              <font-awesome-icon :icon="showPassword[mod.module_name] ? 'fa-solid fa-eye-slash' : 'fa-solid fa-eye'" />
            </button>
          </div>
        </div>

        <!-- Base URL -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Base URL</label>
          <input
            type="text"
            v-model="formData[mod.module_name].base_url"
            placeholder="留空使用預設值"
            class="border border-gray-300 rounded-lg px-3 py-2 w-full focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
          />
        </div>

        <!-- Model -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Model</label>
          <input
            type="text"
            v-model="formData[mod.module_name].model"
            placeholder="留空使用預設值"
            class="border border-gray-300 rounded-lg px-3 py-2 w-full focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
          />
        </div>
      </div>

      <!-- Save Button -->
      <div class="mt-5 flex items-center space-x-3">
        <button
          @click="handleSave(mod.module_name)"
          :disabled="savingModule === mod.module_name"
          class="flex items-center space-x-2 bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-lg transition-colors disabled:opacity-50"
        >
          <font-awesome-icon v-if="savingModule === mod.module_name" icon="fa-solid fa-spinner" class="animate-spin" />
          <span>儲存設定</span>
        </button>

        <!-- Success/Error feedback -->
        <span v-if="feedback[mod.module_name] === 'success'" class="text-green-600 text-sm font-medium">
          <font-awesome-icon icon="fa-solid fa-check" class="mr-1" />已儲存
        </span>
        <span v-if="feedback[mod.module_name] === 'error'" class="text-red-600 text-sm font-medium">
          <font-awesome-icon icon="fa-solid fa-times" class="mr-1" />儲存失敗
        </span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useSettingsStore } from '../stores/settings'

const store = useSettingsStore()

const moduleList = [
  { module_name: 'default', label: '全域預設 (DEFAULT)', icon: 'fa-solid fa-shield-halved' },
  { module_name: 'worldbuilding', label: '世界觀規劃器 (Worldbuilding)', icon: 'fa-solid fa-globe' },
  { module_name: 'character', label: '角色管理器 (Character)', icon: 'fa-solid fa-users' },
  { module_name: 'outline', label: '故事大綱生成器 (Outline)', icon: 'fa-solid fa-list-ol' },
  { module_name: 'scene', label: 'Story Planner (Scene)', icon: 'fa-solid fa-clapperboard' },
  { module_name: 'chapter', label: '章節生成器 (Chapter)', icon: 'fa-solid fa-book' }
]

// Initialize reactive state synchronously (before template renders)
const showPassword = reactive({})
const formData = reactive({})
const feedback = reactive({})
moduleList.forEach(m => {
  showPassword[m.module_name] = false
  formData[m.module_name] = { api_key: '', base_url: '', model: '' }
  feedback[m.module_name] = null
})

const savingModule = ref(null)
const deletingModule = ref(null)

function initForms() {
  moduleList.forEach(m => {
    const existing = store.modules.find(mod => mod.module_name === m.module_name)
    if (existing) {
      formData[m.module_name] = {
        api_key: existing.api_key || '',
        base_url: existing.base_url || '',
        model: existing.model || ''
      }
    }
  })
}

function badgeClass(mod) {
  if (mod.module_name === 'default') return 'bg-blue-100 text-blue-700'
  const existing = store.modules.find(m => m.module_name === mod.module_name)
  return existing?.api_key ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-500'
}

function badgeText(mod) {
  if (mod.module_name === 'default') return '全域預設'
  const existing = store.modules.find(m => m.module_name === mod.module_name)
  return existing?.api_key ? '已自訂' : '使用 DEFAULT'
}

function togglePassword(name) {
  showPassword[name] = !showPassword[name]
}

async function handleSave(moduleName) {
  savingModule.value = moduleName
  feedback[moduleName] = null
  const data = { ...formData[moduleName] }
  const ok = await store.updateModule(moduleName, data)
  if (ok) {
    feedback[moduleName] = 'success'
    setTimeout(() => { feedback[moduleName] = null }, 2000)
  } else {
    feedback[moduleName] = 'error'
  }
  savingModule.value = null
}

async function handleDelete(moduleName) {
  deletingModule.value = moduleName
  const ok = await store.deleteModule(moduleName)
  if (ok) {
    formData[moduleName] = { api_key: '', base_url: '', model: '' }
    feedback[moduleName] = 'success'
    setTimeout(() => { feedback[moduleName] = null }, 2000)
  } else {
    feedback[moduleName] = 'error'
  }
  deletingModule.value = null
}

onMounted(async () => {
  await store.fetchAll()
  initForms()
})
</script>
