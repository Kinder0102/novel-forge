<template>
  <div>
    <div v-if="store.loading && !store.outlines.length" class="flex justify-center py-8">
      <font-awesome-icon icon="fa-solid fa-spinner" spin class="text-indigo-600 text-2xl" />
    </div>

    <div v-else-if="!store.outlines.length" class="text-center py-8 text-gray-400">
      <font-awesome-icon icon="fa-solid fa-list" class="text-4xl mb-3" />
      <p>尚未建立任何大綱</p>
    </div>

    <div v-else class="space-y-4">
      <div
        v-for="ol in store.outlines"
        :key="ol.id"
        class="bg-white rounded-xl shadow-md p-6"
      >
        <div class="flex items-start justify-between">
          <div class="flex-1">
            <h3 class="text-lg font-semibold text-gray-900">{{ ol.title }}</h3>
            <p class="text-gray-500 text-sm mt-1">{{ ol.summary }}</p>
          </div>
          <div class="flex space-x-1 ml-2">
            <button
              @click="editOutline(ol)"
              class="p-1.5 rounded-lg text-gray-400 hover:text-indigo-600 hover:bg-indigo-50 transition-colors"
            >
              <font-awesome-icon icon="fa-solid fa-edit" class="text-sm" />
            </button>
            <button
              @click="deleteOutline(ol.id)"
              class="p-1.5 rounded-lg text-gray-400 hover:text-red-600 hover:bg-red-50 transition-colors"
            >
              <font-awesome-icon icon="fa-solid fa-trash" class="text-sm" />
            </button>
          </div>
        </div>

        <!-- Chapters -->
        <div v-if="ol.chapters" class="mt-4">
          <p class="text-sm font-medium text-gray-700 mb-2">章節列表</p>
          <div class="space-y-1.5">
            <div
              v-for="(ch, idx) in parseChapters(ol.chapters)"
              :key="idx"
              class="text-sm text-gray-600 flex items-center px-3 py-1.5 bg-gray-50 rounded-lg"
            >
              <span class="w-8 h-8 rounded-full bg-indigo-100 text-indigo-600 flex items-center justify-center text-xs font-bold mr-3 shrink-0">
                {{ idx + 1 }}
              </span>
              <div>
                <p class="font-medium text-gray-800">{{ ch.title }}</p>
                <p class="text-xs text-gray-400">{{ ch.summary }}</p>
              </div>
            </div>
          </div>
        </div>

        <div class="flex gap-2 mt-4 pt-3 border-t border-gray-100">
          <router-link
            :to="`/scene/${ol.id}`"
            class="inline-flex items-center text-sm bg-gray-200 hover:bg-gray-300 text-gray-700 rounded-lg px-3 py-1.5 transition-colors"
          >
            <font-awesome-icon icon="fa-solid fa-clapperboard" class="mr-1" />
            規劃場景
          </router-link>
          <router-link
            :to="`/chapter/${ol.id}`"
            class="inline-flex items-center text-sm bg-indigo-100 hover:bg-indigo-200 text-indigo-700 rounded-lg px-3 py-1.5 transition-colors"
          >
            <font-awesome-icon icon="fa-solid fa-book" class="mr-1" />
            生成章節
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useOutlineStore } from '../stores/outline'

const props = defineProps({
  worldbuildingId: { type: Number, required: true }
})

const emit = defineEmits(['edit-outline'])

const store = useOutlineStore()

function parseChapters(chapters) {
  if (typeof chapters === 'string') {
    try { return JSON.parse(chapters) } catch { return [] }
  }
  return chapters || []
}

function editOutline(ol) {
  emit('edit-outline', ol)
}

async function deleteOutline(id) {
  await store.remove(id)
}
</script>
