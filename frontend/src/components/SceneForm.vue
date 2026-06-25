<template>
  
  <div v-if="!editingId" class="bg-white rounded-xl shadow-sm border border-gray-200 p-6 mb-6">
    <div class="flex items-center gap-3">
      <div class="w-10 h-10 rounded-lg bg-rose-100 flex items-center justify-center flex-shrink-0">
        <font-awesome-icon icon="fa-solid fa-wand-magic-sparkles" class="text-rose-600" />
      </div>
      <div class="flex-1">
        <p class="text-sm font-semibold text-gray-900 mb-0.5">{{ t('scene.aiSplit') }}</p>
        <p class="text-xs text-gray-400">{{ t('scene.aiSplitDesc') }}</p>
      </div>
    </div>
    <div class="space-y-3 mt-4">
      <textarea v-model="description" rows="2"
        class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-rose-500 focus:border-rose-500"
        :placeholder="t('scene.aiPlaceholder')"></textarea>
      <button @click="aiGenerateScenes" :disabled="store.loading"
        class="cursor-pointer bg-rose-600 hover:bg-rose-700 disabled:bg-rose-300 text-white rounded-lg px-5 py-2 font-medium transition-colors text-sm">
        <font-awesome-icon v-if="store.loading" icon="fa-solid fa-spinner" spin class="mr-1.5" />{{ t('scene.aiSplitBtn') }}
      </button>
    </div>
  </div>

  
  <Form v-if="editingId" :key="editingId" ref="editPanel" :validation-schema="validationSchema" :initial-values="initialForm" @submit="updateForm"
    class="bg-white rounded-xl shadow-sm border border-gray-200 p-6 mb-6">
    <div class="flex items-center justify-between mb-4">
      <span class="text-lg font-semibold text-gray-900">
        <font-awesome-icon icon="fa-solid fa-edit" class="mr-2 text-rose-600" />{{ t('scene.editTitle') }}
      </span>
      <button type="button" @click="cancelEdit" class="text-gray-400 hover:text-gray-600 transition-colors">
        <font-awesome-icon icon="fa-solid fa-times" class="text-lg" />
      </button>
    </div>
    <div class="space-y-4">
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">{{ t('scene.sceneNumber') }}</label>
        <Field name="scene_number" v-slot="{ field, errorMessage }">
          <input v-bind="field" type="number" step="any" min="0.01"
            class="w-full border rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-rose-500 focus:border-rose-500"
            :class="errorMessage ? 'border-red-400' : 'border-gray-300'" />
        </Field>
        <ErrorMessage name="scene_number" class="text-red-500 text-xs mt-1" />
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">{{ t('scene.sceneTitle') }} <span class="text-red-500">*</span></label>
        <Field name="title" v-slot="{ field, errorMessage }">
          <input v-bind="field" type="text" :placeholder="t('scene.sceneTitlePlaceholder')"
            class="w-full border rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-rose-500 focus:border-rose-500"
            :class="errorMessage ? 'border-red-400' : 'border-gray-300'" />
        </Field>
        <ErrorMessage name="title" class="text-red-500 text-xs mt-1" />
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">{{ t('scene.description') }}</label>
        <Field name="description" v-slot="{ field }">
          <textarea v-bind="field" rows="3" :placeholder="t('scene.descriptionPlaceholder')"
            class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-rose-500 focus:border-rose-500"></textarea>
        </Field>
      </div>
      <div>
        <div class="flex items-center gap-2 mb-1">
          <label class="block text-sm font-medium text-gray-700">{{ t('common.aiContent') }}</label>
          <button type="button" @click="regenSummary" :disabled="regenLoading"
            class="p-1 rounded text-gray-400 hover:text-rose-600 hover:bg-rose-50 transition-colors"
            :title="t('common.regenerateSummary')">
            <font-awesome-icon
              :icon="regenLoading ? 'fa-solid fa-spinner' : 'fa-solid fa-arrows-rotate'"
              :spin="regenLoading"
              class="text-xs"/>
          </button>
        </div>
        <Field name="summary" v-slot="{ field }">
          <textarea v-bind="field" rows="3" :placeholder="t('common.aiContentPlaceholder')"
            class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-rose-500 focus:border-rose-500"></textarea>
        </Field>
      </div>
      <div class="flex gap-3">
        <button type="submit" :disabled="store.loading"
          class="bg-rose-600 hover:bg-rose-700 disabled:bg-rose-300 text-white rounded-lg px-4 py-2 font-medium transition-colors text-sm">{{ t('common.save') }}</button>
        <button type="button" @click="cancelEdit"
          class="bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-lg px-4 py-2 font-medium transition-colors text-sm">{{ t('common.cancel') }}</button>
      </div>
    </div>
  </Form>
</template><script setup lang="ts">
import { ref, nextTick, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { Form, Field, ErrorMessage } from 'vee-validate'
import { toFormValidator } from '@vee-validate/zod'
import { useSceneStore } from '../stores/scene'
import { useOutlineStore } from '../stores/outline'
import { useChapterStore } from '../stores/chapter'
import { createSceneSchema } from '../utils/validation'

const props = defineProps({
  novelId: { type: Number, required: true },
  chapterTitleId: { type: Number, required: true }
})

const { t } = useI18n()
const store = useSceneStore()
const outlineStore = useOutlineStore()
const chapterStore = useChapterStore()
const validationSchema = toFormValidator(createSceneSchema())
const editingId = ref<number | null>(null)
const nextSceneNumber = ref(1)
const description = ref('')
const editPanel = ref<any>(null)
const regenLoading = ref(false)
const initialForm = ref({})

const chapterTitle = computed(() => {
  const chapters = outlineStore.current?.chapter_titles || []
  return chapters.find((c: any) => c.id === props.chapterTitleId)
})

function emptySnapshot() {
  return { scene_number: nextSceneNumber.value++, title: '', description: '', summary: '' }
}

async function updateForm(values) {
  await store.update(editingId.value, {
    scene_number: Number(values.scene_number),
    title: values.title,
    description: values.description || '',
    summary: values.summary || ''
  })
  cancelEdit()
}

function startEdit(scene) {
  editingId.value = scene.id
  initialForm.value = {
    scene_number: scene.scene_number || 1,
    title: scene.title || '',
    description: scene.description || '',
    summary: scene.summary || ''
  }
  nextTick(() => { editPanel.value?.$el?.scrollIntoView({ behavior: 'smooth', block: 'start' }) })
}

function cancelEdit() {
  editingId.value = null
  initialForm.value = emptySnapshot()
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

async function aiGenerateScenes() {
  const ch = chapterTitle.value
  if (!ch) return
  const outline = outlineStore.current

  let prevCh
  const chapterTitles = [...(outlineStore.current?.chapter_titles || [])].sort((a, b) => a.idx - b.idx)
  const currentPos = chapterTitles.findIndex(ct => ct.id === ch.id)
  if (currentPos > 0) {
    prevCh = chapterTitles[currentPos - 1]
  }

  await store.generateScenes({
    novel_id: props.novelId,
    worldbuilding_id: outline.id,
    chapter_title_id: props.chapterTitleId,
    chapter_id: prevCh?.id,
    description: description.value
  })
  description.value = ''
}

defineExpose({ startEdit })
</script>