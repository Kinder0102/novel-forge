<template>
  <div>
    <div v-if="store.loading && !store.scenes.length" class="flex justify-center py-4">
      <font-awesome-icon icon="fa-solid fa-spinner" spin class="text-indigo-600 text-xl" />
    </div>

    <div v-else-if="!store.scenes.length" class="text-center py-8 text-gray-400">
      <font-awesome-icon icon="fa-solid fa-clapperboard" class="text-3xl mb-2" />
      <p>此章節尚無場景</p>
      <p class="text-sm mt-1">使用 AI 或手動建立場景</p>
    </div>

    <div v-else class="space-y-3">
      <div
        v-for="scene in store.scenes"
        :key="scene.id"
        class="bg-white rounded-xl shadow-md p-5"
      >
        <div class="flex items-start justify-between">
          <div class="flex-1">
            <div class="flex items-center space-x-2 mb-1">
              <span class="w-6 h-6 rounded-full bg-indigo-100 text-indigo-600 flex items-center justify-center text-xs font-bold">
                {{ scene.scene_number }}
              </span>
              <h4 class="font-semibold text-gray-900">{{ scene.title }}</h4>
              <span
                class="text-xs px-2 py-0.5 rounded-full"
                :class="scene.status === 'draft' ? 'bg-yellow-100 text-yellow-700' : 'bg-green-100 text-green-700'"
              >
                {{ scene.status === 'completed' ? '已完成' : '草稿' }}
              </span>
            </div>
            <p class="text-sm text-gray-500">{{ scene.summary }}</p>

            <!-- Generated content -->
            <div v-if="scene.content" class="mt-3">
              <button @click="scene._expanded = !scene._expanded" class="text-sm text-indigo-600 hover:text-indigo-800">
                <font-awesome-icon :icon="scene._expanded ? 'fa-solid fa-chevron-up' : 'fa-solid fa-chevron-down'" class="mr-1 text-xs" />
                {{ scene._expanded ? '收起內容' : '展開內容' }}
              </button>
              <div v-if="scene._expanded" class="mt-2 p-3 bg-gray-50 rounded-lg text-sm text-gray-700 whitespace-pre-wrap">
                {{ scene.content }}
              </div>
            </div>
          </div>
          <div class="flex flex-col space-y-1 ml-2">
            <button
              @click="generateContent(scene.id)"
              :disabled="store.loading"
              class="p-1.5 rounded-lg text-gray-400 hover:text-indigo-600 hover:bg-indigo-50 transition-colors text-xs"
              title="AI 生成內容"
            >
              <font-awesome-icon :icon="store.loading ? 'fa-solid fa-spinner' : 'fa-solid fa-magic-wand-sparkles'" :spin="store.loading" />
            </button>
            <button
              @click="deleteScene(scene.id)"
              class="p-1.5 rounded-lg text-gray-400 hover:text-red-600 hover:bg-red-50 transition-colors text-xs"
            >
              <font-awesome-icon icon="fa-solid fa-trash" />
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useSceneStore } from '../stores/scene'

const props = defineProps({
  outlineId: { type: Number, required: true },
  chapterIndex: { type: Number, required: true }
})

const store = useSceneStore()

async function generateContent(id) {
  await store.generateContent(id)
}

async function deleteScene(id) {
  await store.remove(id)
}
</script>
