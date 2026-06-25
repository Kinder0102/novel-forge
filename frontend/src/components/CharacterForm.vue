<template>
  <div class="bg-white rounded-xl shadow-md p-6 mb-6">
    <button
      @click="expanded = !expanded"
      class="flex items-center justify-between w-full text-left"
    >
      <span class="text-lg font-semibold text-gray-900">
        <font-awesome-icon icon="fa-solid fa-plus" class="mr-2 text-indigo-600" />
        {{ editingId ? '編輯角色' : '建立角色' }}
      </span>
      <font-awesome-icon
        :icon="expanded ? 'fa-solid fa-chevron-up' : 'fa-solid fa-chevron-down'"
        class="text-gray-400"
      />
    </button>

    <div v-if="expanded" class="mt-4 space-y-4">
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">名稱 <span class="text-red-500">*</span></label>
        <input
          v-model="form.name"
          type="text"
          class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
          placeholder="角色名稱"
        />
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">角色定位</label>
        <input
          v-model="form.role"
          type="text"
          class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
          placeholder="主角、反派、導師…"
        />
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">性格特質</label>
        <textarea
          v-model="form.personality"
          rows="2"
          class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
          placeholder="角色的性格描述…"
        ></textarea>
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">背景故事</label>
        <textarea
          v-model="form.background"
          rows="3"
          class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
          placeholder="角色的過往經歷…"
        ></textarea>
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">外貌描寫</label>
        <textarea
          v-model="form.appearance"
          rows="2"
          class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
          placeholder="角色的外貌特徵…"
        ></textarea>
      </div>

      <div class="flex flex-wrap gap-3">
        <button
          v-if="!editingId"
          @click="submitForm"
          :disabled="store.loading || !form.name"
          class="bg-indigo-600 hover:bg-indigo-700 disabled:bg-indigo-300 text-white rounded-lg px-4 py-2 font-medium transition-colors"
        >
          <font-awesome-icon v-if="store.loading" icon="fa-solid fa-spinner" spin class="mr-1" />
          建立
        </button>
        <button
          v-if="editingId"
          @click="updateForm"
          :disabled="store.loading || !form.name"
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
          AI 生成角色
        </p>
        <div class="space-y-3">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">角色描述（選填）</label>
            <textarea
              v-model="aiDescription"
              rows="2"
              class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
              placeholder="角色描述，例如：一個沉默寡言的流浪劍客，背負著滅門之仇…"
            ></textarea>
          </div>
          <button
            @click="aiGenerate"
            :disabled="store.loading"
            class="bg-indigo-600 hover:bg-indigo-700 disabled:bg-indigo-300 text-white rounded-lg px-4 py-2 font-medium transition-colors text-sm"
          >
            <font-awesome-icon v-if="store.loading" icon="fa-solid fa-spinner" spin class="mr-1" />
            生成角色
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useCharacterStore } from '../stores/character'
import { useWorldbuildingStore } from '../stores/worldbuilding'

const props = defineProps({
  worldbuildingId: { type: Number, required: true }
})

const store = useCharacterStore()
const wbStore = useWorldbuildingStore()
const expanded = ref(false)
const editingId = ref(null)
const aiDescription = ref('')

const emptyForm = () => ({
  name: '',
  role: '',
  personality: '',
  background: '',
  appearance: ''
})

const form = reactive(emptyForm())

async function submitForm() {
  const data = await store.create({ ...form, worldbuilding_id: props.worldbuildingId })
  if (data) {
    Object.assign(form, emptyForm())
    expanded.value = false
  }
}

async function updateForm() {
  await store.update(editingId.value, { ...form })
  cancelEdit()
}

async function aiGenerate() {
  const wb = wbStore.worldbuildings.find(w => w.id === props.worldbuildingId)
  const context = wb ? `${wb.title}\n${wb.description}\n${wb.setting}` : ''
  const payload = {
    worldbuilding_id: props.worldbuildingId,
    worldbuilding_context: context
  }
  if (aiDescription.value.trim()) {
    payload.description = aiDescription.value.trim()
  }
  await store.generateCharacters(payload)
}

function startEdit(ch) {
  editingId.value = ch.id
  Object.assign(form, {
    name: ch.name,
    role: ch.role || '',
    personality: ch.personality || '',
    background: ch.background || '',
    appearance: ch.appearance || ''
  })
  expanded.value = true
}

function cancelEdit() {
  editingId.value = null
  Object.assign(form, emptyForm())
}

defineExpose({ startEdit })
</script>
