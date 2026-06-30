<template>
  <nav class="bg-gray-900 text-white shadow-lg">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-16">
        <div class="flex items-center space-x-4">
          <router-link to="/" class="flex items-center space-x-2 text-xl font-bold hover:text-indigo-300 transition-colors">
            <font-awesome-icon icon="fa-solid fa-feather" class="text-indigo-400" />
            <span>NovelForge</span>
          </router-link>
          <template v-if="novelTitle">
            <span class="text-gray-400">|</span>
            <span class="text-sm text-gray-300 font-medium truncate max-w-[200px]">
              {{ novelTitle }}
            </span>
          </template>
        </div>

        <div class="hidden md:flex space-x-1">
          <router-link
            v-for="item in navItems"
            :key="item.path"
            :to="item.path"
            class="flex items-center space-x-1.5 px-3 py-2 rounded-lg text-sm font-medium transition-colors"
            :class="isActive(item) ? 'bg-gray-800 text-white' : 'text-gray-300 hover:bg-gray-800 hover:text-white'"
          >
            <font-awesome-icon :icon="item.icon" class="text-xs" />
            <span>{{ item.label }}</span>
          </router-link>
        </div>

        <button @click="mobileOpen = !mobileOpen" class="md:hidden p-2 rounded-lg hover:bg-gray-800 transition-colors">
          <font-awesome-icon :icon="mobileOpen ? 'fa-solid fa-times' : 'fa-solid fa-bars'" />
        </button>
      </div>
    </div>

    <div v-if="mobileOpen" class="md:hidden border-t border-gray-800">
      <div class="px-2 pt-2 pb-3 space-y-1">
        <router-link
          v-for="item in navItems"
          :key="item.path"
          :to="item.path"
          @click="mobileOpen = false"
          class="flex items-center space-x-2 px-3 py-2 rounded-lg text-base font-medium transition-colors"
          :class="isActive(item) ? 'bg-gray-800 text-white' : 'text-gray-300 hover:bg-gray-800 hover:text-white'"
        >
          <font-awesome-icon :icon="item.icon" class="text-sm w-4" />
          <span>{{ item.label }}</span>
        </router-link>
      </div>
    </div>
  </nav>
</template>
<script setup lang="ts">
import { ref, type PropType } from 'vue'
import { useRoute } from 'vue-router'

interface NavItem {
  path: string
  icon: string
  label: string
}

const props = defineProps({
  navItems: { type: Array as PropType<NavItem[]>, required: true },
  novelTitle: { type: String, default: '' },
  activeMode: { type: String, default: 'exact' }
})

const route = useRoute()
const mobileOpen = ref(false)

function isActive(item: NavItem) {
  if (props.activeMode === 'prefix') {
    const isParent = props.navItems.some(
      other => other.path !== item.path && other.path.startsWith(item.path + '/')
    )
    if (isParent) {
      return route.path === item.path
    }
    if (route.path === item.path) return true
    return route.path.startsWith(item.path + '/') || route.path.startsWith(item.path + '?')
  }
  return route.path === item.path
}
</script>