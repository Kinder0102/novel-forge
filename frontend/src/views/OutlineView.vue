<template>
  <div>
    <h1 class="text-2xl font-bold text-gray-900 mb-6">
      <font-awesome-icon icon="fa-solid fa-list" class="text-indigo-600 mr-2" />
      故事大綱生成器
    </h1>

    <div v-if="outlineStore.error" class="bg-red-50 border border-red-200 text-red-700 rounded-lg p-4 mb-4">
      {{ outlineStore.error }}
    </div>

    <div class="mb-6">
      <label class="block text-sm font-medium text-gray-700 mb-1">選擇世界觀</label>
      <select
        v-model="selectedWorldId"
        @change="onWorldChange"
        class="w-full md:w-80 border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
      >
        <option :value="null">-- 請選擇世界觀 --</option>
        <option v-for="w in wbStore.worldbuildings" :key="w.id" :value="w.id">{{ w.title }}</option>
      </select>
    </div>

    <template v-if="selectedWorldId">
      <OutlineForm ref="formRef" :worldbuilding-id="selectedWorldId" />
      <OutlineList :worldbuilding-id="selectedWorldId" @edit-outline="onEditOutline" />
    </template>
    <p v-else class="text-gray-400 text-center py-8">請先選擇一個世界觀</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useOutlineStore } from '../stores/outline'
import { useWorldbuildingStore } from '../stores/worldbuilding'
import OutlineForm from '../components/OutlineForm.vue'
import OutlineList from '../components/OutlineList.vue'

const outlineStore = useOutlineStore()
const wbStore = useWorldbuildingStore()
const selectedWorldId = ref(null)
const formRef = ref(null)

onMounted(() => {
  wbStore.fetchAll()
})

function onWorldChange() {
  if (selectedWorldId.value) {
    outlineStore.fetchAll(selectedWorldId.value)
  } else {
    outlineStore.outlines = []
  }
}

function onEditOutline(ol) {
  formRef.value?.startEdit(ol)
}
</script>
