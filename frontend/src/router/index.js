import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import WorldbuildingView from '../views/WorldbuildingView.vue'
import CharacterView from '../views/CharacterView.vue'
import OutlineView from '../views/OutlineView.vue'
import ScenePlannerView from '../views/ScenePlannerView.vue'
import ChapterView from '../views/ChapterView.vue'
import SettingsView from '../views/SettingsView.vue'

const routes = [
  { path: '/', name: 'Home', component: HomeView },
  { path: '/worldbuilding', name: 'Worldbuilding', component: WorldbuildingView },
  { path: '/character', name: 'Character', component: CharacterView },
  { path: '/outline', name: 'Outline', component: OutlineView },
  { path: '/scene/:outlineId', name: 'ScenePlanner', component: ScenePlannerView, props: true },
  { path: '/chapter/:outlineId', name: 'Chapter', component: ChapterView, props: true },
  { path: '/settings', name: 'Settings', component: SettingsView }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
