<template>
  
  <div v-if="!editingId" class="bg-white rounded-xl shadow-sm border border-gray-200 p-6 mb-6">
    <div class="flex items-center gap-3">
      <div class="w-10 h-10 rounded-lg bg-emerald-100 flex items-center justify-center flex-shrink-0">
        <font-awesome-icon icon="fa-solid fa-wand-magic-sparkles" class="text-emerald-600" />
      </div>
      <div class="flex-1">
        <p class="text-sm font-semibold text-gray-900 mb-0.5">{{ t('character.aiGenerate') }}</p>
        <p class="text-xs text-gray-400">{{ t('character.aiGenerateDesc') }}</p>
      </div>
    </div>
    <div class="space-y-3 mt-4">
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">{{ t('character.selectWorldbuilding') }} <span class="text-red-500">*</span></label>
        <select v-model="selectedWorldbuildingId"
          class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500">
          <option :value="null" disabled>{{ t('character.selectWorldbuildingPlaceholder') }}</option>
          <option v-for="wb in worldbuildingList" :key="wb.id" :value="wb.id">
            {{ wb.title }}
          </option>
        </select>
      </div>
      <textarea v-model="aiDescription" rows="2"
        class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500"
        :placeholder="t('character.aiPlaceholder')"></textarea>
      <button @click="aiGenerate" :disabled="store.loading || !selectedWorldbuildingId"
        class="bg-emerald-600 hover:bg-emerald-700 disabled:bg-emerald-300 text-white rounded-lg px-5 py-2 font-medium transition-colors text-sm">
        <font-awesome-icon v-if="store.loading" icon="fa-solid fa-spinner" spin class="mr-1.5" />
        {{ t('character.generateCharacter') }}
      </button>
    </div>
  </div>

  
  <Form v-if="editingId" ref="editPanel" :validation-schema="validationSchema" :initial-values="initialForm" @submit="updateForm"
    class="bg-white rounded-xl shadow-sm border border-gray-200 p-6 mb-6">
    <div class="flex items-center justify-between mb-4">
      <span class="text-lg font-semibold text-gray-900">
        <font-awesome-icon icon="fa-solid fa-edit" class="mr-2 text-emerald-600" />{{ t('character.editTitle') }}
      </span>
      <button type="button" @click="cancelEdit" class="text-gray-400 hover:text-gray-600 transition-colors">
        <font-awesome-icon icon="fa-solid fa-times" class="text-lg" />
      </button>
    </div>
    <div class="space-y-4">
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">{{ t('character.name') }} <span class="text-red-500">*</span></label>
        <Field name="name" v-slot="{ field, errorMessage }">
          <input v-bind="field" type="text" :placeholder="t('character.namePlaceholder')"
            class="w-full border rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500"
            :class="errorMessage ? 'border-red-400' : 'border-gray-300'" />
        </Field>
        <ErrorMessage name="name" class="text-red-500 text-xs mt-1" />
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">{{ t('character.role') }}</label>
        <Field name="role" v-slot="{ field }">
          <input v-bind="field" type="text" :placeholder="t('character.rolePlaceholder')"
            class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500" />
        </Field>
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">{{ t('character.personality') }}</label>
        <Field name="personality" v-slot="{ field }">
          <textarea v-bind="field" rows="2" :placeholder="t('character.personalityPlaceholder')"
            class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500"></textarea>
        </Field>
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">{{ t('character.background') }}</label>
        <Field name="background" v-slot="{ field }">
          <textarea v-bind="field" rows="3" :placeholder="t('character.backgroundPlaceholder')"
            class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500"></textarea>
        </Field>
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">{{ t('character.appearance') }}</label>
        <Field name="appearance" v-slot="{ field }">
          <textarea v-bind="field" rows="2" :placeholder="t('character.appearancePlaceholder')"
            class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500"></textarea>
        </Field>
      </div>

      <div>
        <div class="flex items-center gap-2 mb-1">
          <label class="block text-sm font-medium text-gray-700">{{ t('common.aiContent') }}</label>
          <button type="button" @click="regenSummary" :disabled="regenLoading"
            class="p-1 rounded text-gray-400 hover:text-emerald-600 hover:bg-emerald-50 transition-colors"
            :title="t('common.regenerateSummary')">
            <font-awesome-icon
              :icon="regenLoading ? 'fa-solid fa-spinner' : 'fa-solid fa-arrows-rotate'"
              :spin="regenLoading"
              class="text-xs"/>
          </button>
        </div>
        <Field name="summary" v-slot="{ field }">
          <textarea v-bind="field" rows="2" :placeholder="t('common.aiContentPlaceholder')"
            class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500"></textarea>
        </Field>
      </div>

      <div class="flex gap-3">
        <button type="submit" :disabled="store.loading"
          class="bg-emerald-600 hover:bg-emerald-700 disabled:bg-emerald-300 text-white rounded-lg px-4 py-2 font-medium transition-colors text-sm">{{ t('common.save') }}</button>
        <button type="button" @click="cancelEdit"
          class="bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-lg px-4 py-2 font-medium transition-colors text-sm">{{ t('common.cancel') }}</button>
      </div>
    </div>
  </Form>
</template><script setup lang="ts">
import { ref, reactive, nextTick, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { Form, Field, ErrorMessage } from 'vee-validate'
import { toFormValidator } from '@vee-validate/zod'
import { useCharacterStore } from '../stores/character'
import { getWorldbuildings } from '../api'
import { createCharacterSchema } from '../utils/validation'

const props = defineProps({ novelId: { type: Number, required: true } })

const { t } = useI18n()
const store = useCharacterStore()
const validationSchema = toFormValidator(createCharacterSchema())
const editingId = ref<number | null>(null)
const aiDescription = ref('')
const selectedWorldbuildingId = ref<number | null>(null)
const worldbuildingList = ref([])
const editPanel = ref<any>(null)
const initialForm = ref({})
const regenLoading = ref(false)

onMounted(async () => {
  try {
    const res = await getWorldbuildings(props.novelId)
    worldbuildingList.value = res.data || []
  } catch (e) {
    console.error('Failed to load worldbuilding list', e)
  }
})

function emptySnapshot() {
  return { name: '', role: '', personality: '', background: '', appearance: '', summary: '' }
}

async function updateForm(values) {
  await store.update(editingId.value, values)
  cancelEdit()
}

async function aiGenerate() {
  const payload = { novel_id: props.novelId, worldbuilding_id: selectedWorldbuildingId.value }
  if (aiDescription.value.trim()) payload.description = aiDescription.value.trim()
  await store.generateCharacters(payload)
}

function startEdit(ch) {
  editingId.value = ch.id
  initialForm.value = {
    name: ch.name || '',
    role: ch.role || '',
    personality: ch.personality || '',
    background: ch.background || '',
    appearance: ch.appearance || '',
    summary: ch.summary || ''
  }
  nextTick(() => { editPanel.value?.$el?.scrollIntoView({ behavior: 'smooth', block: 'start' }) })
}

async function regenSummary() {
  if (!editingId.value) return
  regenLoading.value = true
  try {
    const result = await store.regenerateSummary(editingId.value)
    editPanel.value?.resetForm({ values: { ...editPanel.value?.values, summary: result.summary || '' } })
  } catch {
  } finally {
    regenLoading.value = false
  }
}

function cancelEdit() {
  editingId.value = null
  initialForm.value = emptySnapshot()
}

defineExpose({ startEdit })
</script>