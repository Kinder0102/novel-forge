<template>
  <div class="bg-white rounded-xl shadow-md p-6 mb-6">
    <button
      @click="expanded = !expanded"
      class="flex items-center justify-between w-full text-left"
    >
      <span class="text-lg font-semibold text-gray-900">
        <font-awesome-icon :icon="editingId ? 'fa-solid fa-edit' : 'fa-solid fa-plus'" class="mr-2 text-indigo-600" />
        {{ editingId ? '編輯大綱' : '建立大綱' }}
      </span>
      <font-awesome-icon
        :icon="expanded ? 'fa-solid fa-chevron-up' : 'fa-solid fa-chevron-down'"
        class="text-gray-400"
      />
    </button>

    <div v-if="expanded" class="mt-4 space-y-4">
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">大綱標題 <span class="text-red-500">*</span></label>
        <input
          v-model="form.title"
          type="text"
          class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
          placeholder="大綱標題"
        />
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">摘要</label>
        <textarea
          v-model="form.summary"
          rows="3"
          class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
          placeholder="故事摘要…"
        ></textarea>
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">章節列表（JSON 格式）</label>
        <textarea
          v-model="form.chapters_json"
          rows="6"
          class="w-full border border-gray-300 rounded-lg px-3 py-2 font-mono text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
          placeholder='[{"title": "第一章", "summary": "..."}]'
        ></textarea>
        <p class="text-xs text-gray-400 mt-1">每項包含 title 與 summary，例如：[{"title": "開場", "summary": "主角登場"}]</p>
      </div>

      <div class="flex flex-wrap gap-3">
        <button
          v-if="!editingId"
          @click="submitForm"
          :disabled="store.loading || !form.title"
          class="bg-indigo-600 hover:bg-indigo-700 disabled:bg-indigo-300 text-white rounded-lg px-4 py-2 font-medium transition-colors"
        >
          <font-awesome-icon v-if="store.loading" icon="fa-solid fa-spinner" spin class="mr-1" />
          建立大綱
        </button>
        <button
          v-if="editingId"
          @click="updateForm"
          :disabled="store.loading || !form.title"
          class="bg-indigo-600 hover:bg-indigo-700 disabled:bg-indigo-300 text-white rounded-lg px-4 py-2 font-medium transition-colors"
        >
          儲存
        </button>
        <button
          v-if="editingId"
          @click="cancelEdit"
          class="bg-gray-200 hover:bg-gray-300 text-gray-700 rounded-lg px-4 py-2 font-medium transition-colors"
        >
          取消
        </button>
      </div>

      <!-- AI generate -->
      <div v-if="!editingId" class="border-t border-gray-200 pt-4 mt-4">
        <p class="text-sm font-medium text-gray-700 mb-3">
          <font-awesome-icon icon="fa-solid fa-magic-wand-sparkles" class="text-indigo-600 mr-1" />
          AI 生成大綱（單章）
        </p>
        <div class="space-y-3">
          <div>
            <textarea
              v-model="description"
              rows="2"
              class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
              placeholder="大綱描述（選填）"
            ></textarea>
          </div>
          <button
            @click="aiGenerate"
            :disabled="store.loading"
            class="bg-indigo-600 hover:bg-indigo-700 disabled:bg-indigo-300 text-white rounded-lg px-4 py-2 font-medium transition-colors text-sm"
          >
            <font-awesome-icon v-if="store.loading" icon="fa-solid fa-spinner" spin class="mr-1" />
            生成大綱
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useOutlineStore } from '../stores/outline'
import { useWorldbuildingStore } from '../stores/worldbuilding'

const props = defineProps({
  worldbuildingId: { type: Number, required: true }
})

const store = useOutlineStore()
const wbStore = useWorldbuildingStore()
const expanded = ref(false)
const editingId = ref(null)
const description = ref('')

const emptyForm = () => ({
  title: '',
  summary: '',
  chapters_json: '[]'
})

const form = reactive(emptyForm())

async function submitForm() {
  const data = await store.create({ ...form, worldbuilding_id: props.worldbuildingId, chapters_json: form.chapters_json })
  if (data) {
    Object.assign(form, emptyForm())
    expanded.value = false
  }
}

async function updateForm() {
  await store.update(editingId.value, { ...form })
  cancelEdit()
}

function startEdit(ol) {
  editingId.value = ol.id
  const chapters = typeof ol.chapters === 'string' ? ol.chapters : JSON.stringify(ol.chapters || [])
  Object.assign(form, {
    title: ol.title || '',
    summary: ol.summary || '',
    chapters_json: chapters
  })
  expanded.value = true
}

function cancelEdit() {
  editingId.value = null
  Object.assign(form, emptyForm())
}

defineExpose({ startEdit })

async function aiGenerate() {
  const wb = wbStore.worldbuildings.find(w => w.id === props.worldbuildingId)
  const context = wb ? `${wb.title}（${wb.genre}）\n描述：${wb.description}\n設定：${wb.setting}\n規則：${wb.rules}` : ''
  await store.generateOutline({
    worldbuilding_id: props.worldbuildingId,
    context,
    description: description.value
  })
}
</script>
