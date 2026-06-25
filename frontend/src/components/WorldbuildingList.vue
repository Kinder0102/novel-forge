<template>
  <div>
    <div v-if="store.loading && !store.worldbuildings.length" class="flex justify-center py-8">
      <font-awesome-icon icon="fa-solid fa-spinner" spin class="text-indigo-600 text-2xl" />
    </div>

    <div v-else-if="!store.worldbuildings.length" class="text-center py-8 text-gray-400">
      <font-awesome-icon icon="fa-solid fa-globe" class="text-4xl mb-3" />
      <p>尚未建立任何世界觀</p>
      <p class="text-sm mt-1">使用上方表單建立第一個世界觀吧！</p>
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div
        v-for="wb in store.worldbuildings"
        :key="wb.id"
        class="bg-white rounded-xl shadow-md p-6 hover:shadow-lg transition-shadow"
      >
        <div class="flex items-start justify-between">
          <div class="flex-1">
            <h3 class="text-lg font-semibold text-gray-900">{{ wb.title }}</h3>
            <p v-if="wb.genre" class="text-sm text-indigo-600 mt-1">{{ wb.genre }}</p>
          </div>
          <div class="flex space-x-1 ml-2">
            <button
              @click="editWorld(wb)"
              class="p-1.5 rounded-lg text-gray-400 hover:text-indigo-600 hover:bg-indigo-50 transition-colors"
              title="編輯"
            >
              <font-awesome-icon icon="fa-solid fa-edit" class="text-sm" />
            </button>
            <button
              @click="deleteWorld(wb.id)"
              class="p-1.5 rounded-lg text-gray-400 hover:text-red-600 hover:bg-red-50 transition-colors"
              title="刪除"
            >
              <font-awesome-icon icon="fa-solid fa-trash" class="text-sm" />
            </button>
          </div>
        </div>
        <p v-if="wb.description" class="text-gray-500 text-sm mt-2 line-clamp-3">{{ wb.description }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useWorldbuildingStore } from '../stores/worldbuilding'

const store = useWorldbuildingStore()

function editWorld(wb) {
  // Access parent's form startEdit via template ref pattern
  // We'll emit to parent instead for cleaner architecture
  window.dispatchEvent(new CustomEvent('edit-worldbuilding', { detail: wb }))
}

async function deleteWorld(id) {
  await store.remove(id)
}
</script>
