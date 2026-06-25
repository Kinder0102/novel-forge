<template>
  <div class="bg-white rounded-xl shadow-md p-6 mb-6">
    <div class="flex items-center justify-between">
      <h3 class="text-lg font-semibold text-gray-900">建立場景</h3>
    </div>

    <div class="mt-4 space-y-4">
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">場景標題</label>
        <input
          v-model="form.title"
          type="text"
          class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
          placeholder="場景標題"
        />
      </div>

      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">場景摘要</label>
        <textarea
          v-model="form.summary"
          rows="2"
          class="w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
          placeholder="場景摘要…"
        ></textarea>
      </div>

      <div class="flex flex-wrap gap-3">
        <button
          @click="submitForm"
          :disabled="store.loading || !form.title"
          class="bg-indigo-600 hover:bg-indigo-700 disabled:bg-indigo-300 text-white rounded-lg px-4 py-2 text-sm font-medium transition-colors"
        >
          新增場景
        </button>
        <button
          @click="aiGenerateScenes"
          :disabled="store.loading"
          class="bg-gray-200 hover:bg-gray-300 text-gray-700 rounded-lg px-4 py-2 text-sm font-medium transition-colors"
        >
          <font-awesome-icon v-if="store.loading" icon="fa-solid fa-spinner" spin class="mr-1" />
          <font-awesome-icon v-else icon="fa-solid fa-magic-wand-sparkles" class="mr-1" />
          AI 拆分場景
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useSceneStore } from '../stores/scene'
import { useOutlineStore } from '../stores/outline'

const props = defineProps({
  outlineId: { type: Number, required: true },
  chapterIndex: { type: Number, required: true }
})

const store = useSceneStore()
const outlineStore = useOutlineStore()

const form = reactive({
  title: '',
  summary: ''
})
const nextSceneNumber = ref(1)

async function submitForm() {
  await store.create({
    outline_id: props.outlineId,
    chapter_index: props.chapterIndex,
    scene_number: nextSceneNumber.value++,
    title: form.title,
    summary: form.summary
  })
  form.title = ''
  form.summary = ''
}

async function aiGenerateScenes() {
  const chapters = parseOutlineChapters()
  const ch = chapters[props.chapterIndex]
  if (!ch) return

  const outline = outlineStore.current
  const context = outline ? `世界觀：${outline.title}\n${outline.summary}` : ''

  await store.generateScenes({
    outline_id: props.outlineId,
    chapter_index: props.chapterIndex,
    chapter_title: ch.title,
    chapter_summary: ch.summary,
    context
  })
}

function parseOutlineChapters() {
  if (!outlineStore.current?.chapters) return []
  if (typeof outlineStore.current.chapters === 'string') {
    try { return JSON.parse(outlineStore.current.chapters) } catch { return [] }
  }
  return outlineStore.current.chapters
}
</script>
