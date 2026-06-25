<template>
  
  <div v-if="!editingId" class="bg-white rounded-xl shadow-sm border border-gray-200 p-6 mb-6">
    <div class="flex items-center gap-3">
      <div class="w-10 h-10 rounded-lg bg-amber-100 flex items-center justify-center flex-shrink-0">
        <font-awesome-icon icon="fa-solid fa-wand-magic-sparkles" class="text-amber-600" />
      </div>
      <div class="flex-1">
        <p class="text-sm font-semibold text-gray-900 mb-0.5">{{ t('outline.aiGenerate') }}</p>
        <p class="text-xs text-gray-400">{{ t('outline.aiGenerateDesc') }}</p>
      </div>
    </div>
    <div class="space-y-3 mt-4">
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">{{ t('outline.selectWorldbuilding') }} <span class="text-red-500">*</span></label>
        <select v-model="selectedWorldbuildingId"
          class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-amber-500">
          <option :value="null" disabled>{{ t('outline.selectWorldbuildingPlaceholder') }}</option>
          <option v-for="wb in worldbuildingList" :key="wb.id" :value="wb.id">
            {{ wb.title }}
          </option>
        </select>
      </div>
      <textarea v-model="description" rows="2"
        class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-amber-500"
        :placeholder="t('outline.aiPlaceholder')"></textarea>

      <div v-if="characters.length > 0">
        <label class="block text-xs font-medium text-gray-600 mb-1.5">{{ t('outline.selectCharacters') }}</label>
        <div class="flex flex-wrap gap-2">
          <button
            v-for="ch in characters" :key="ch.id"
            @click="toggleCharacter(ch.id)"
            :class="[
              'px-3 py-1.5 rounded-full text-xs font-medium transition-colors border',
              selectedCharacterIds.includes(ch.id)
                ? 'bg-amber-100 border-amber-400 text-amber-800'
                : 'bg-gray-50 border-gray-200 text-gray-600 hover:border-amber-300'
            ]"
          >
            {{ ch.name }}<span v-if="ch.role" class="text-gray-400 ml-1">({{ ch.role }})</span>
          </button>
        </div>
      </div>
      <button @click="aiGenerate" :disabled="store.loading || !selectedWorldbuildingId"
        class="bg-amber-600 hover:bg-amber-700 disabled:bg-amber-300 text-white rounded-lg px-5 py-2 font-medium transition-colors text-sm">
        <font-awesome-icon v-if="store.loading" icon="fa-solid fa-spinner" spin class="mr-1.5" />{{ t('outline.generateOutline') }}
      </button>
    </div>
  </div>

  
  <Form v-if="editingId" ref="editPanel" :validation-schema="validationSchema" :initial-values="initialForm" @submit="updateForm"
    class="bg-white rounded-xl shadow-sm border border-gray-200 p-6 mb-6">
    <div class="flex items-center justify-between mb-4">
      <span class="text-lg font-semibold text-gray-900">
        <font-awesome-icon icon="fa-solid fa-edit" class="mr-2 text-amber-600" />{{ t('outline.editTitle') }}
      </span>
      <button type="button" @click="cancelEdit" class="text-gray-400 hover:text-gray-600 transition-colors">
        <font-awesome-icon icon="fa-solid fa-times" class="text-lg" />
      </button>
    </div>
    <div class="space-y-4">
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">{{ t('outline.name') }} <span class="text-red-500">*</span></label>
        <Field name="title" v-slot="{ field, errorMessage }">
          <input v-bind="field" type="text" :placeholder="t('outline.namePlaceholder')"
            class="w-full border rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-amber-500"
            :class="errorMessage ? 'border-red-400' : 'border-gray-300'" />
        </Field>
        <ErrorMessage name="title" class="text-red-500 text-xs mt-1" />
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">{{ t('outline.description') }}</label>
        <Field name="description" v-slot="{ field }">
          <textarea v-bind="field" rows="3" :placeholder="t('outline.descriptionPlaceholder')"
            class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-amber-500"></textarea>
        </Field>
      </div>

      <div>
        <div class="flex items-center gap-2 mb-1">
          <label class="block text-sm font-medium text-gray-700">{{ t('common.aiContent') }}</label>
          <button type="button" @click="regenSummary" :disabled="regenLoading"
            class="p-1 rounded text-gray-400 hover:text-amber-600 hover:bg-amber-50 transition-colors"
            :title="t('common.regenerateSummary')">
            <font-awesome-icon
              :icon="regenLoading ? 'fa-solid fa-spinner' : 'fa-solid fa-arrows-rotate'"
              :spin="regenLoading"
              class="text-xs"/>
          </button>
        </div>
        <Field name="summary" v-slot="{ field }">
          <textarea v-bind="field" rows="3" :placeholder="t('common.aiContentPlaceholder')"
            class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-amber-500"></textarea>
        </Field>
      </div>

      
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">{{ t('outline.chapterList') }}</label>
        <div class="space-y-2">
          <div v-for="(ch, idx) in chapters" :key="ch.id"
            class="flex items-start gap-2 bg-gray-50 rounded-lg p-3 border border-gray-200 transition-all"
            :class="{ 'opacity-50': dragIndex === idx }"
            draggable="true"
            @dragstart="onDragStart($event, idx)" @dragover.prevent="onDragOver($event, idx)"
            @drop="onDrop($event, idx)" @dragend="onDragEnd">
            <div class="flex items-center h-9 text-gray-400 cursor-grab active:cursor-grabbing">
              <font-awesome-icon icon="fa-solid fa-grip-vertical" class="text-sm" />
            </div>
            <span class="w-7 h-9 rounded-full bg-amber-100 text-amber-600 flex items-center justify-center text-xs font-bold flex-shrink-0">{{ idx + 1 }}</span>
            <div class="flex-1">
              <input v-model="ch.title" type="text"
                class="w-full border border-gray-300 rounded-md px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-amber-500"
                :placeholder="t('outline.chapterPlaceholder')" />
            </div>
            <button type="button" @click="confirmDelete(idx)" class="text-gray-400 hover:text-red-500 p-1.5 transition-colors flex-shrink-0">
              <font-awesome-icon icon="fa-solid fa-trash" class="text-sm" />
            </button>
          </div>
        </div>
        <button type="button" @click="addChapter"
          class="mt-2 cursor-pointer inline-flex items-center text-sm text-amber-600 hover:text-amber-700 font-medium transition-colors">
          <font-awesome-icon icon="fa-solid fa-plus" class="mr-1" />{{ t('outline.addChapter') }}
        </button>
      </div>

      <div class="flex gap-3">
        <button type="submit" :disabled="store.loading"
          class="bg-amber-600 hover:bg-amber-700 disabled:bg-amber-300 text-white rounded-lg px-4 py-2 font-medium transition-colors text-sm">{{ t('common.save') }}</button>
        <button type="button" @click="cancelEdit"
          class="bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-lg px-4 py-2 font-medium transition-colors text-sm">{{ t('common.cancel') }}</button>
      </div>
    </div>
  </Form>

  <ConfirmModal
    :visible="showConfirm"
    :title="t('common.confirm')"
    :message="t('outline.chapterDeleteConfirm', { title: deletingTitle })"
    @confirm="performDelete"
    @cancel="cancelDelete"
  />
</template><script setup lang="ts">
import { ref, nextTick, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { Form, Field, ErrorMessage } from 'vee-validate'
import { toFormValidator } from '@vee-validate/zod'
import { useOutlineStore } from '../stores/outline'
import { createOutlineSchema } from '../utils/validation'
import * as api from '../api'
import ConfirmModal from './ConfirmModal.vue'

const props = defineProps({ novelId: { type: Number, required: true } })
const { t } = useI18n()
const store = useOutlineStore()
const validationSchema = toFormValidator(createOutlineSchema())
const editingId = ref<number | null>(null)
const description = ref('')
const selectedWorldbuildingId = ref<number | null>(null)
const worldbuildingList = ref([])
const editPanel = ref<any>(null)
const chapters = ref([])
const dragIndex = ref<number | null>(null)
const regenLoading = ref(false)
const initialForm = ref({})
const characters = ref([])
const selectedCharacterIds = ref([])

function emptySnapshot() {
  return { title: '', summary: '' }
}

async function updateForm(values) {
  await store.update(editingId.value, { title: values.title, description: values.description, summary: values.summary })

  for (let i = 0; i < chapters.value.length; i++) {
    const ch = chapters.value[i]
    if (typeof ch.id === 'number' && ch.id > 0) {
      await api.updateChapterTitle(ch.id, { title: ch.title, idx: i })
    } else {
      await api.createChapterTitle({ outline_id: editingId.value, title: ch.title, idx: i })
    }
  }
  cancelEdit()
}

async function loadChapters(outlineId) {
  try {
    const res = await api.getChapterTitles(outlineId)
    chapters.value = (res.data || []).map(ch => ({ ...ch }))
  } catch {
    chapters.value = []
  }
}

async function startEdit(ol) {
  editingId.value = ol.id
  initialForm.value = {
    title: ol.title || '',
    description: ol.description || '',
    summary: ol.summary || ''
  }
  await loadChapters(ol.id)
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
  chapters.value = []
}

function addChapter() {
  chapters.value.push({ id: -Date.now(), title: '' })
}

const deletingIdx = ref<number | null>(null)
const deletingTitle = ref('')
const showConfirm = ref(false)

function confirmDelete(idx) {
  const ch = chapters.value[idx]
  if (!ch) return
  deletingIdx.value = idx
  deletingTitle.value = `${t('chapter.chapterNum', { n: idx + 1 })} ${ch.title || ''}`
  showConfirm.value = true
}

function cancelDelete() {
  deletingIdx.value = null
  deletingTitle.value = ''
  showConfirm.value = false
}

async function performDelete() {
  const idx = deletingIdx.value
  if (idx === null) return
  const ch = chapters.value[idx]
  if (ch && typeof ch.id === 'number' && ch.id > 0) {
    await api.deleteChapterTitle(ch.id)
  }
  chapters.value.splice(idx, 1)
  cancelDelete()
}

function onDragStart(e, idx) { dragIndex.value = idx; e.dataTransfer.effectAllowed = 'move'; e.dataTransfer.setData('text/plain', idx) }
function onDragOver(e, idx) { if (dragIndex.value != null && dragIndex.value !== idx) e.dataTransfer.dropEffect = 'move' }
function onDrop(e, idx) {
  const from = dragIndex.value
  if (from == null || from === idx) return
  const item = chapters.value.splice(from, 1)[0]
  chapters.value.splice(idx, 0, item)

  if (typeof item.id === 'number' && item.id > 0) {
    const prevItem = idx > 0 ? chapters.value[idx - 1] : null
    const nextItem = idx < chapters.value.length - 1 ? chapters.value[idx + 1] : null
    api.reorderChapterTitles({
      outline_id: editingId.value,
      moved_id: item.id,
      prev_id: prevItem?.id ?? null,
      next_id: nextItem?.id ?? null
    })
  }
}
function onDragEnd() { dragIndex.value = null }

async function aiGenerate() {
  await store.generateOutline({
    novel_id: props.novelId,
    worldbuilding_id: selectedWorldbuildingId.value,
    description: description.value,
    character_ids: selectedCharacterIds.value.length > 0 ? selectedCharacterIds.value : undefined
  })
}

function toggleCharacter(id) {
  const idx = selectedCharacterIds.value.indexOf(id)
  if (idx === -1) {
    selectedCharacterIds.value.push(id)
  } else {
    selectedCharacterIds.value.splice(idx, 1)
  }
}

async function fetchCharacters() {
  try {
    const res = await api.getCharacters({ novelId: props.novelId })
    characters.value = res.data
  } catch (e) {
    
  }
}

async function fetchWorldbuildings() {
  try {
    const res = await api.getWorldbuildings(props.novelId)
    worldbuildingList.value = res.data || []
  } catch (e) {
    console.error('Failed to load worldbuilding list', e)
  }
}

onMounted(() => {
  fetchCharacters()
  fetchWorldbuildings()
})

defineExpose({ startEdit })
</script>