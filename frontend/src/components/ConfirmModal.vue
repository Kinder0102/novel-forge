<template>
  <div v-if="visible" class="fixed inset-0 z-50 flex items-center justify-center">
    <div class="absolute inset-0 bg-black/40" @click="$emit('cancel')"></div>
    <div class="relative bg-white rounded-xl shadow-xl border border-gray-200 p-6 mx-4 max-w-sm w-full">
      <h3 class="text-lg font-semibold text-gray-900 mb-2">{{ title }}</h3>
      <p class="text-sm text-gray-500 mb-6">{{ message }}</p>
      <div class="flex justify-end gap-3">
        <button
          @click="$emit('cancel')"
          class="bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-lg px-4 py-2 text-sm font-medium transition-colors"
        >
          {{ t('common.cancel') }}
        </button>
        <button
          @click="$emit('confirm')"
          class="bg-red-600 hover:bg-red-700 text-white rounded-lg px-4 py-2 text-sm font-medium transition-colors"
        >
          {{ t('common.confirm') }}
        </button>
      </div>
    </div>
  </div>
</template><script setup lang="ts">
import { useI18n } from 'vue-i18n'

defineProps<{
  visible: boolean
  title: string
  message: string
}>()

const emit = defineEmits<{
  confirm: []
  cancel: []
}>()

const { t } = useI18n()
</script>