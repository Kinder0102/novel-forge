import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'
import LandingView from '../views/LandingView.vue'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'Home',
    component: LandingView,
  },
  {
    path: '/projects',
    name: 'Projects',
    component: () => import('../views/ProjectList.vue'),
  },
  {
    path: '/novel/:novelId',
    component: () => import('../views/NovelLayout.vue'),
    props: true,
    children: [
      { path: '', name: 'NovelDashboard', component: () => import('../views/NovelDashboard.vue'), props: true },
      { path: 'worldbuilding', name: 'NovelWorldbuilding', component: () => import('../views/WorldbuildingView.vue'), props: true },
      { path: 'character', name: 'NovelCharacter', component: () => import('../views/CharacterView.vue'), props: true },
      { path: 'outline', name: 'NovelOutline', component: () => import('../views/OutlineView.vue'), props: true },
      { path: 'scene/:outlineId', name: 'NovelScenePlanner', component: () => import('../views/ScenePlannerView.vue'), props: true },
      { path: 'chapter/:outlineId', name: 'NovelChapter', component: () => import('../views/ChapterView.vue'), props: true },
      { path: 'read/:outlineId/:chapterTitleId?', name: 'NovelRead', component: () => import('../views/ReadView.vue'), props: true },
    ],
  },
  {
    path: '/settings',
    name: 'Settings',
    component: () => import('../views/SettingsView.vue'),
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
