<template>
  <div>
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-2xl font-bold text-gray-900">
        <font-awesome-icon icon="fa-solid fa-globe" class="text-indigo-600 mr-2" />
        世界觀規劃器
      </h1>
    </div>

    <div v-if="store.error" class="bg-red-50 border border-red-200 text-red-700 rounded-lg p-4 mb-4">
      {{ store.error }}
    </div>

    <WorldbuildingForm ref="formRef" />
    <WorldbuildingList />
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { useWorldbuildingStore } from '../stores/worldbuilding'
import WorldbuildingForm from '../components/WorldbuildingForm.vue'
import WorldbuildingList from '../components/WorldbuildingList.vue'

const store = useWorldbuildingStore()
const formRef = ref(null)

function handleEditWorld(e) {
  formRef.value?.startEdit(e.detail)
}

onMounted(() => {
  store.fetchAll()
  window.addEventListener('edit-worldbuilding', handleEditWorld)
})

onBeforeUnmount(() => {
  window.removeEventListener('edit-worldbuilding', handleEditWorld)
})
</script>
