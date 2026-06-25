<template>
  <button
    @click="handleExport"
    :disabled="store.loading"
    class="bg-green-600 hover:bg-green-700 disabled:bg-green-300 text-white rounded-lg px-4 py-2 font-medium transition-colors text-sm inline-flex items-center"
  >
    <font-awesome-icon
      :icon="store.loading ? 'fa-solid fa-spinner' : 'fa-solid fa-download'"
      :spin="store.loading"
      class="mr-1.5"
    />
    匯出小說
  </button>
</template>

<script setup>
import { useChapterStore } from '../stores/chapter'

const props = defineProps({
  outlineId: { type: Number, required: true }
})

const store = useChapterStore()

async function handleExport() {
  const text = await store.exportChapters(props.outlineId)
  if (text) {
    const blob = new Blob([text], { type: 'text/plain;charset=utf-8' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `novel_outline_${props.outlineId}.txt`
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }
}
</script>
