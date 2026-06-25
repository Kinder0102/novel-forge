<template>
  <div>
    <h1 class="text-2xl font-bold text-gray-900 mb-6">
      <font-awesome-icon icon="fa-solid fa-users" class="text-emerald-600 mr-2" />
      {{ t('character.title') }}
    </h1>

    <ErrorBanner v-if="characterStore.error" :message="characterStore.error" />

    <CharacterForm ref="formRef" :novel-id="novelId" />
    <CharacterList @edit-character="onEditCharacter" />
  </div>
</template><script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { useCharacterStore } from '../stores/character'
import ErrorBanner from '../components/ErrorBanner.vue'
import CharacterForm from '../components/CharacterForm.vue'
import CharacterList from '../components/CharacterList.vue'

const props = defineProps({
  novelId: { type: String, required: true }
})

const { t } = useI18n()

const characterStore = useCharacterStore()
const formRef = ref<any>(null)

const novelId = computed(() => Number.parseInt(props.novelId))

onMounted(() => {
  characterStore.fetchAll({ novelId: novelId.value })
})

function onEditCharacter(ch) {
  formRef.value?.startEdit(ch)
}
</script>