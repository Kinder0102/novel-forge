<template>
  <div class="flex justify-center py-20">
    <font-awesome-icon icon="fa-solid fa-spinner" class="animate-spin text-3xl" :class="colorClass" />
  </div>
</template><script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  color?: 'indigo' | 'violet' | 'emerald' | 'amber' | 'rose'
}>()

const colorMap: Record<string, string> = {
  indigo: 'text-indigo-500',
  violet: 'text-violet-600',
  emerald: 'text-emerald-600',
  amber: 'text-amber-600',
  rose: 'text-rose-600',
}

const colorClass = computed(() => colorMap[props.color || 'indigo'] || 'text-indigo-500')
</script>