<template>
  <div class="bg-white rounded-xl shadow-md p-6 mb-6">
    <button
      @click="expanded = !expanded"
      class="flex items-center justify-between w-full text-left"
    >
      <span class="text-lg font-semibold text-gray-900">
        <font-awesome-icon icon="fa-solid fa-plus" class="mr-2 text-indigo-600" />
        {{ editingId ? '編輯世界觀' : '建立世界觀' }}
      </span>
      <font-awesome-icon
        :icon="expanded ? 'fa-solid fa-chevron-up' : 'fa-solid fa-chevron-down'"
        class="text-gray-400"
      />
    </button>

    <div v-if="expanded" class="mt-4 space-y-4">
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">標題 <span class="text-red-500">*</span></label>
        <input
          v-model="form.title"
          type="text"
          class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
          placeholder="世界觀標題"
        />
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">類型</label>
        <input
          v-model="form.genre"
          type="text"
          class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
          placeholder="奇幻、科幻、武俠…"
        />
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">描述</label>
        <textarea
          v-model="form.description"
          rows="3"
          class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
          placeholder="描述這個世界的概況…"
        ></textarea>
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">環境設定</label>
        <textarea
          v-model="form.setting"
          rows="3"
          class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
          placeholder="地理環境、時代背景…"
        ></textarea>
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">世界規則</label>
        <textarea
          v-model="form.rules"
          rows="3"
          class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
          placeholder="魔法體系、科技規則、社會制度…"
        ></textarea>
      </div>

      <div class="flex flex-wrap gap-3">
        <button
          v-if="!editingId"
          @click="submitForm"
          :disabled="store.loading || !form.title"
          class="bg-indigo-600 hover:bg-indigo-700 disabled:bg-indigo-300 text-white rounded-lg px-4 py-2 font-medium transition-colors"
        >
          <font-awesome-icon v-if="store.loading" icon="fa-solid fa-spinner" spin class="mr-1" />
          建立
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

      <!-- AI generate section (for new creation) -->
      <div v-if="!editingId" class="border-t border-gray-200 pt-4 mt-4">
        <p class="text-sm font-medium text-gray-700 mb-3">
          <font-awesome-icon icon="fa-solid fa-magic-wand-sparkles" class="text-indigo-600 mr-1" />
          AI 快速生成
        </p>
        <div class="flex gap-3">
          <input
            v-model="aiTheme"
            type="text"
            class="flex-1 border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
            placeholder="輸入主題概念，如：蒸汽龐克魔法學院"
          />
          <button
            @click="aiGenerate"
            :disabled="store.loading || !aiTheme"
            class="bg-indigo-600 hover:bg-indigo-700 disabled:bg-indigo-300 text-white rounded-lg px-4 py-2 font-medium transition-colors"
          >
            <font-awesome-icon v-if="store.loading" icon="fa-solid fa-spinner" spin class="mr-1" />
            生成
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useWorldbuildingStore } from '../stores/worldbuilding'

const store = useWorldbuildingStore()
const expanded = ref(true)
const editingId = ref(null)
const aiTheme = ref('')

const emptyForm = () => ({
  title: '',
  genre: '',
  description: '',
  setting: '',
  rules: ''
})

const form = reactive(emptyForm())

async function submitForm() {
  const data = await store.create({ ...form })
  if (data) {
    Object.assign(form, emptyForm())
  }
}

async function updateForm() {
  await store.update(editingId.value, { ...form })
  cancelEdit()
}

async function aiGenerate() {
  const tempData = await store.create({ title: aiTheme.value, genre: '', description: '', setting: '', rules: '' })
  if (tempData) {
    const result = await store.generateWorldbuilding(tempData.id, aiTheme.value)
    if (result) {
      const idx = store.worldbuildings.findIndex(w => w.id === tempData.id)
      if (idx !== -1) {
        store.worldbuildings[idx] = result
      }
    }
    aiTheme.value = ''
  }
}

function startEdit(wb) {
  editingId.value = wb.id
  Object.assign(form, {
    title: wb.title,
    genre: wb.genre || '',
    description: wb.description || '',
    setting: wb.setting || '',
    rules: wb.rules || ''
  })
  expanded.value = true
}

function cancelEdit() {
  editingId.value = null
  Object.assign(form, emptyForm())
}

defineExpose({ startEdit })
</script>
