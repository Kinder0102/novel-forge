<template>
  <div>
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900">{{ t('settings.title') }}</h1>
      <p class="text-gray-500 mt-1">{{ t('settings.subtitle') }}</p>
    </div>

    
    <div class="flex flex-wrap gap-2 mb-6">
      <button
        v-for="mod in moduleList"
        :key="mod.value"
        @click="activeModule = mod.value"
        class="px-4 py-2 rounded-lg text-sm font-medium transition-colors"
        :class="activeModule === mod.value ? 'bg-violet-600 text-white' : 'bg-white text-gray-600 border border-gray-200 hover:border-gray-300'"
      >
        {{ mod.label }}
        <span v-if="hasCustomConfig(mod.value) && activeModule !== mod.value" class="ml-1.5 text-xs opacity-70">
          ({{ t('settings.custom') }})
        </span>
      </button>
    </div>

    
    <div v-if="store.loading" class="flex justify-center py-8">
      <font-awesome-icon icon="fa-solid fa-spinner" spin class="text-violet-600" />
    </div>

    <div v-else class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
      <div class="flex items-center justify-between mb-4">
        <h2 class="text-lg font-semibold text-gray-900">
          {{ currentModuleLabel }}
          <span v-if="hasCustomConfig(activeModule)" class="ml-2 text-xs text-green-600 font-normal">
            {{ t('settings.custom') }}
          </span>
          <span v-else class="ml-2 text-xs text-gray-400 font-normal">
            {{ t('settings.usingDefault') }}
          </span>
        </h2>
        <div class="flex space-x-2">
          <button
            v-if="hasCustomConfig(activeModule)"
            @click="clearModule"
            class="text-xs text-red-500 hover:text-red-700"
          >
            {{ t('settings.clearSettings') }}
          </button>
          <button
            @click="saveModule"
            :disabled="store.loading"
            class="bg-violet-600 hover:bg-violet-700 disabled:bg-violet-300 text-white rounded-lg px-4 py-2 text-sm font-medium transition-colors"
          >
            {{ saveSuccess ? t('common.saved') : t('settings.saveSettings') }}
          </button>
        </div>
      </div>

      <div v-if="form" class="space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">{{ t('settings.apiKey') }}</label>
          <input
            v-model="form.api_key"
            type="password"
            class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-violet-500 focus:border-violet-500"
            :placeholder="t('common.placeholder_optional')"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">{{ t('settings.baseUrl') }}</label>
          <input
            v-model="form.base_url"
            class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-violet-500 focus:border-violet-500"
            :placeholder="t('settings.baseUrlPlaceholder')"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">{{ t('settings.model') }}</label>
          <input
            v-model="form.model"
            class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-violet-500 focus:border-violet-500"
            :placeholder="t('settings.modelPlaceholder')"
          />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">{{ t('settings.systemPrompt') }}</label>
          <textarea
            v-model="form.system_prompt"
            rows="3"
            class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-violet-500 focus:border-violet-500"
            :placeholder="t('settings.systemPromptPlaceholder')"
          ></textarea>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            {{ t('settings.userPromptTemplate') }}
            <span class="text-gray-400 font-normal">{{ t('settings.userPromptTemplateHint') }}</span>
          </label>
          <textarea
            v-model="form.user_prompt_template"
            rows="3"
            class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-violet-500 focus:border-violet-500"
            :placeholder="t('settings.userPromptTemplatePlaceholder')"
          ></textarea>
        </div>
      </div>
    </div>
  </div>
</template><script setup lang="ts">
import { ref, computed, reactive, watch, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useSettingsStore } from '../stores/settings'

const { t } = useI18n()
const store = useSettingsStore()

const moduleList = [
  { value: 'default', label: t('settings.modules.default') },
  { value: 'worldbuilding', label: t('settings.modules.worldbuilding') },
  { value: 'character', label: t('settings.modules.character') },
  { value: 'outline', label: t('settings.modules.outline') },
  { value: 'scene', label: t('settings.modules.scene') },
  { value: 'chapter', label: t('settings.modules.chapter') },
  { value: 'compact', label: t('settings.modules.compact') },
]

const activeModule = ref('default')
const form = reactive<any>({
  api_key: '',
  base_url: '',
  model: '',
  system_prompt: '',
  user_prompt_template: '',
})
const saveSuccess = ref(false)

const currentModuleLabel = computed(() => {
  const m = moduleList.find(m => m.value === activeModule.value)
  return m?.label || ''
})

function hasCustomConfig(moduleName: string): boolean {
  return store.modules.some(m => m.module_name === moduleName && m.id != null)
}

function loadModule(moduleName: string) {
  const config = store.modules.find(m => m.module_name === moduleName)
  form.api_key = config?.api_key || ''
  form.base_url = config?.base_url || ''
  form.model = config?.model || ''
  form.system_prompt = config?.system_prompt || ''
  form.user_prompt_template = config?.user_prompt_template || ''
}

watch(activeModule, loadModule)

async function saveModule() {
  saveSuccess.value = false
  const data: any = {}
  if (form.api_key) data.api_key = form.api_key
  if (form.base_url) data.base_url = form.base_url
  if (form.model) data.model = form.model
  if (form.system_prompt) data.system_prompt = form.system_prompt
  if (form.user_prompt_template) data.user_prompt_template = form.user_prompt_template

  const ok = await store.updateModule(activeModule.value, data)
  if (ok) {
    saveSuccess.value = true
    setTimeout(() => { saveSuccess.value = false }, 2000)
  }
}

async function clearModule() {
  await store.deleteModule(activeModule.value)
  loadModule(activeModule.value)
}

onMounted(async () => {
  await store.fetchAll()
  loadModule(activeModule.value)
})
</script>