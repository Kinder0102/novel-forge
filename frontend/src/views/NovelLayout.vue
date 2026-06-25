<template>
  <router-view />
</template><script setup lang="ts">
import { onMounted } from 'vue'
import { useNovelStore } from '../stores/novel'

const props = defineProps({
  novelId: { type: String, required: true }
})

const novelStore = useNovelStore()

onMounted(async () => {
  await novelStore.fetchOne(props.novelId)
})
</script>