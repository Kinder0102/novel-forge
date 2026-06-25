<template>
  <div>
    <div v-if="store.loading && !store.worldbuildings.length" class="flex justify-center py-8">
      <font-awesome-icon icon="fa-solid fa-spinner" spin class="text-indigo-600 text-2xl" />
    </div>

    <div v-else-if="!store.worldbuildings.length" class="text-center py-8 text-gray-400">
      <font-awesome-icon icon="fa-solid fa-globe" class="text-4xl mb-3" />
      <p>{{ t('worldbuilding.noWorldbuilding') }}</p>
      <p class="text-sm mt-1">{{ t('worldbuilding.noWorldbuildingDesc') }}</p>
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div
        v-for="wb in store.worldbuildings"
        :key="wb.id"
        class="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-lg transition-shadow"
      >
        <div class="flex items-start justify-between">
          <div class="flex-1">
            <h3 class="text-lg font-semibold text-gray-900">{{ wb.title }}</h3>
            <p v-if="wb.genre" class="text-sm text-indigo-600 mt-1">{{ wb.genre }}</p>
          </div>
          <div class="flex space-x-1 ml-2">
            <button
              @click="$emit('edit-worldbuilding', wb)"
              class="p-1.5 rounded-lg text-gray-400 hover:text-indigo-600 hover:bg-indigo-50 transition-colors"
              :title="t('common.edit')"
            >
              <font-awesome-icon icon="fa-solid fa-edit" class="text-sm" />
            </button>
            <button
              @click="confirmDelete(wb.id)"
              class="p-1.5 rounded-lg text-gray-400 hover:text-red-600 hover:bg-red-50 transition-colors"
              :title="t('common.delete')"
            >
              <font-awesome-icon icon="fa-solid fa-trash" class="text-sm" />
            </button>
          </div>
        </div>
        <p v-if="wb.description" class="text-gray-500 text-sm mt-2 line-clamp-3">{{ wb.description }}</p>
      </div>
    </div>

    <ConfirmModal
      :visible="showConfirm"
      :title="t('common.confirm')"
      :message="t('worldbuilding.deleteConfirm')"
      @confirm="performDelete"
      @cancel="cancelDelete"
    />
  </div>
</template><script setup lang="ts">
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { useWorldbuildingStore } from '../stores/worldbuilding'
import ConfirmModal from './ConfirmModal.vue'

defineEmits<{
  'edit-worldbuilding': [wb: Record<string, unknown>]
}>()

const { t } = useI18n()
const store = useWorldbuildingStore()
const deletingId = ref<number | null>(null)
const showConfirm = ref(false)

function confirmDelete(id: number) {
  deletingId.value = id
  showConfirm.value = true
}

function cancelDelete() {
  deletingId.value = null
  showConfirm.value = false
}

async function performDelete() {
  if (deletingId.value != null) {
    await store.remove(deletingId.value)
  }
  cancelDelete()
}
</script>