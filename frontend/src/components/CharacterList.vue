<template>
  <div>
    <div v-if="store.loading && !store.characters.length" class="flex justify-center py-8">
      <font-awesome-icon icon="fa-solid fa-spinner" spin class="text-emerald-600 text-2xl" />
    </div>

    <div v-else-if="!store.characters.length" class="text-center py-8 text-gray-400">
      <font-awesome-icon icon="fa-solid fa-users" class="text-4xl mb-3" />
      <p>{{ t('character.noCharacters') }}</p>
      <p class="text-sm mt-1">{{ t('character.noCharactersDesc') }}</p>
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div
        v-for="ch in store.characters"
        :key="ch.id"
        class="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-lg transition-shadow"
      >
        <div class="flex items-start justify-between">
          <div>
            <h3 class="text-lg font-semibold text-gray-900">{{ ch.name }}</h3>
            <p v-if="ch.role" class="text-sm text-emerald-600 mt-0.5">{{ ch.role }}</p>
          </div>
          <div class="flex space-x-1">
            <button
              @click="editChar(ch)"
              class="p-1.5 rounded-lg text-gray-400 hover:text-emerald-600 hover:bg-emerald-50 transition-colors"
            >
              <font-awesome-icon icon="fa-solid fa-edit" class="text-sm" />
            </button>
            <button
              @click="confirmDelete(ch.id)"
              class="p-1.5 rounded-lg text-gray-400 hover:text-red-600 hover:bg-red-50 transition-colors"
            >
              <font-awesome-icon icon="fa-solid fa-trash" class="text-sm" />
            </button>
          </div>
        </div>
        <div class="mt-3 space-y-1 text-sm text-gray-500">
          <p v-if="ch.personality"><span class="font-medium text-gray-700">{{ t('character.personalityLabel') }}</span>{{ ch.personality }}</p>
          <p v-if="ch.background"><span class="font-medium text-gray-700">{{ t('character.backgroundLabel') }}</span>{{ truncate(ch.background) }}</p>
          <p v-if="ch.appearance"><span class="font-medium text-gray-700">{{ t('character.appearanceLabel') }}</span>{{ truncate(ch.appearance) }}</p>
        </div>
      </div>
    </div>

    
    <ConfirmModal
      :visible="showConfirm"
      :title="t('common.confirm')"
      :message="t('character.deleteConfirm')"
      @confirm="performDelete"
      @cancel="cancelDelete"
    />
  </div>
</template><script setup lang="ts">
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { useCharacterStore } from '../stores/character'
import ConfirmModal from './ConfirmModal.vue'

const emit = defineEmits<{ 'edit-character': [ch: any] }>()

const { t } = useI18n()
const store = useCharacterStore()
const deletingId = ref<number | null>(null)
const showConfirm = ref(false)

function truncate(text, len = 60) {
  return text.length > len ? text.slice(0, len) + '…' : text
}

function editChar(ch) {
  emit('edit-character', ch)
}

function confirmDelete(id) {
  deletingId.value = id
  showConfirm.value = true
}

function cancelDelete() {
  deletingId.value = null
  showConfirm.value = false
}

async function performDelete() {
  if (deletingId.value) {
    await store.remove(deletingId.value)
  }
  cancelDelete()
}
</script>