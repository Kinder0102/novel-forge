<template>
  <div>
    <div v-if="store.loading && !store.characters.length" class="flex justify-center py-8">
      <font-awesome-icon icon="fa-solid fa-spinner" spin class="text-indigo-600 text-2xl" />
    </div>

    <div v-else-if="!store.characters.length" class="text-center py-8 text-gray-400">
      <font-awesome-icon icon="fa-solid fa-users" class="text-4xl mb-3" />
      <p>尚未建立任何角色</p>
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div
        v-for="ch in store.characters"
        :key="ch.id"
        class="bg-white rounded-xl shadow-md p-6 hover:shadow-lg transition-shadow"
      >
        <div class="flex items-start justify-between">
          <div>
            <h3 class="text-lg font-semibold text-gray-900">{{ ch.name }}</h3>
            <p v-if="ch.role" class="text-sm text-indigo-600 mt-0.5">{{ ch.role }}</p>
          </div>
          <div class="flex space-x-1">
            <button
              @click="editChar(ch)"
              class="p-1.5 rounded-lg text-gray-400 hover:text-indigo-600 hover:bg-indigo-50 transition-colors"
            >
              <font-awesome-icon icon="fa-solid fa-edit" class="text-sm" />
            </button>
            <button
              @click="deleteChar(ch.id)"
              class="p-1.5 rounded-lg text-gray-400 hover:text-red-600 hover:bg-red-50 transition-colors"
            >
              <font-awesome-icon icon="fa-solid fa-trash" class="text-sm" />
            </button>
          </div>
        </div>
        <div class="mt-3 space-y-1 text-sm text-gray-500">
          <p v-if="ch.personality"><span class="font-medium text-gray-700">性格：</span>{{ ch.personality }}</p>
          <p v-if="ch.background"><span class="font-medium text-gray-700">背景：</span>{{ truncate(ch.background) }}</p>
          <p v-if="ch.appearance"><span class="font-medium text-gray-700">外貌：</span>{{ truncate(ch.appearance) }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useCharacterStore } from '../stores/character'

const props = defineProps({
  worldbuildingId: { type: Number, required: true }
})

const emit = defineEmits(['edit-character'])

const store = useCharacterStore()

function truncate(text, len = 60) {
  return text.length > len ? text.slice(0, len) + '…' : text
}

function editChar(ch) {
  emit('edit-character', ch)
}

async function deleteChar(id) {
  await store.remove(id)
}
</script>
