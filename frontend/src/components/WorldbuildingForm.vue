<template>
  
  <div v-if="!editingId" class="bg-white rounded-xl shadow-sm border border-gray-200 p-6 mb-6">
    <div class="flex items-center gap-3">
      <div class="w-10 h-10 rounded-lg bg-indigo-100 flex items-center justify-center flex-shrink-0">
        <font-awesome-icon icon="fa-solid fa-wand-magic-sparkles" class="text-indigo-600" />
      </div>
      <div class="flex-1">
        <p class="text-sm font-semibold text-gray-900 mb-0.5">{{ t('worldbuilding.aiGenerate') }}</p>
        <p class="text-xs text-gray-400">{{ t('worldbuilding.aiGenerateDesc') }}</p>
      </div>
    </div>
    <div class="flex gap-3 mt-4">
      <input v-model="aiTheme" type="text"
        class="flex-1 border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-sm"
        :placeholder="t('worldbuilding.aiPlaceholder')" @keydown.enter.prevent="aiGenerate" />
      <button @click="aiGenerate" :disabled="store.loading || !aiTheme"
        class="bg-indigo-600 hover:bg-indigo-700 disabled:bg-indigo-300 text-white rounded-lg px-5 py-2 font-medium transition-colors text-sm flex-shrink-0">
        <font-awesome-icon v-if="store.loading" icon="fa-solid fa-spinner" spin class="mr-1.5" />{{ t('worldbuilding.generate') }}
      </button>
    </div>
  </div>

  
  <Form v-if="editingId" ref="editPanel" :validation-schema="validationSchema" :initial-values="initialForm" @submit="updateForm"
    class="bg-white rounded-xl shadow-sm border border-gray-200 p-6 mb-6">
    <div class="flex items-center justify-between mb-4">
      <span class="text-lg font-semibold text-gray-900">
        <font-awesome-icon icon="fa-solid fa-edit" class="mr-2 text-indigo-600" />{{ t('worldbuilding.editTitle') }}
      </span>
      <button type="button" @click="cancelEdit" class="text-gray-400 hover:text-gray-600 transition-colors">
        <font-awesome-icon icon="fa-solid fa-times" class="text-lg" />
      </button>
    </div>
    <div class="space-y-4">
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">{{ t('worldbuilding.name') }} <span class="text-red-500">*</span></label>
        <Field name="title" v-slot="{ field, errorMessage }">
          <input v-bind="field" type="text" :placeholder="t('worldbuilding.namePlaceholder')"
            class="w-full border rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
            :class="errorMessage ? 'border-red-400' : 'border-gray-300'" />
        </Field>
        <ErrorMessage name="title" class="text-red-500 text-xs mt-1" />
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">{{ t('worldbuilding.genre') }}</label>
        <Field name="genre" v-slot="{ field }">
          <input v-bind="field" type="text" :placeholder="t('worldbuilding.genrePlaceholder')"
            class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500" />
        </Field>
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">{{ t('worldbuilding.description') }}</label>
        <Field name="description" v-slot="{ field }">
          <textarea v-bind="field" rows="3" :placeholder="t('worldbuilding.descriptionPlaceholder')"
            class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"></textarea>
        </Field>
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">{{ t('worldbuilding.setting') }}</label>
        <Field name="setting" v-slot="{ field }">
          <textarea v-bind="field" rows="3" :placeholder="t('worldbuilding.settingPlaceholder')"
            class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"></textarea>
        </Field>
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">{{ t('worldbuilding.rules') }}</label>
        <Field name="rules" v-slot="{ field }">
          <textarea v-bind="field" rows="3" :placeholder="t('worldbuilding.rulesPlaceholder')"
            class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"></textarea>
        </Field>
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">
          {{ t('common.aiContent') }}
          <button
            type="button"
            @click="regenSummary"
            :disabled="summaryLoading"
            class="ml-2 text-xs text-indigo-500 hover:text-indigo-700 disabled:text-indigo-300 transition-colors align-middle"
            :title="t('common.regenerateSummary')"
          >
            <font-awesome-icon
              :icon="summaryLoading ? 'fa-solid fa-spinner' : 'fa-solid fa-arrows-rotate'"
              :spin="summaryLoading"
            />
          </button>
        </label>
        <Field name="summary" v-slot="{ field }">
          <textarea v-bind="field" rows="3" :placeholder="t('common.aiContentPlaceholder')"
            class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"></textarea>
        </Field>
      </div>
      <div class="flex gap-3">
        <button type="submit" :disabled="store.loading"
          class="bg-indigo-600 hover:bg-indigo-700 disabled:bg-indigo-300 text-white rounded-lg px-4 py-2 font-medium transition-colors text-sm">{{ t('common.save') }}</button>
        <button type="button" @click="cancelEdit"
          class="bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-lg px-4 py-2 font-medium transition-colors text-sm">{{ t('common.cancel') }}</button>
      </div>
    </div>
  </Form>
</template><script setup lang="ts">
import { ref, nextTick } from 'vue'
import { useI18n } from 'vue-i18n'
import { Form, Field, ErrorMessage } from 'vee-validate'
import { toFormValidator } from '@vee-validate/zod'
import { useWorldbuildingStore } from '../stores/worldbuilding'
import { createWorldbuildingSchema } from '../utils/validation'
import * as api from '../api'
import { extractErrorMessage } from '../utils/error'

const props = defineProps({ novelId: { type: Number, required: true } })

const { t } = useI18n()
const store = useWorldbuildingStore()
const validationSchema = toFormValidator(createWorldbuildingSchema())
const editingId = ref<number | null>(null)
const aiTheme = ref('')
const editPanel = ref<any>(null)
const initialForm = ref({})
const summaryLoading = ref(false)

function emptySnapshot() {
  return { title: '', genre: '', description: '', setting: '', rules: '', summary: '' }
}

async function updateForm(values) {
  await store.update(editingId.value, values)
  cancelEdit()
}

async function aiGenerate() {
  if (!aiTheme.value.trim() || store.loading) return
  store.loading = true
  store.error = null
  try {
    await api.generateWorldbuilding(props.novelId, aiTheme.value)
    await store.fetchAll(props.novelId)
    aiTheme.value = ''
  } catch (e) {
    store.error = extractErrorMessage(e)
  } finally {
    store.loading = false
  }
}

function startEdit(wb) {
  editingId.value = wb.id
  initialForm.value = {
    title: wb.title || '',
    genre: wb.genre || '',
    description: wb.description || '',
    setting: wb.setting || '',
    rules: wb.rules || '',
    summary: wb.summary || ''
  }
  nextTick(() => { editPanel.value?.$el?.scrollIntoView({ behavior: 'smooth', block: 'start' }) })
}

async function regenSummary() {
  if (summaryLoading.value || !editingId.value) return
  summaryLoading.value = true
  try {
    const result = await store.regenerateSummary(editingId.value)
    editPanel.value?.resetForm({ values: { ...editPanel.value?.values, summary: result.summary || '' } })
  } finally {
    summaryLoading.value = false
  }
}

function cancelEdit() {
  editingId.value = null
  initialForm.value = emptySnapshot()
}

defineExpose({ startEdit })
</script>