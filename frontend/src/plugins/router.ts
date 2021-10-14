import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/views/Home.vue'
import Gantt from '@/views/Gantt.vue'
import GanttSimple from '@/views/Gantt-simple.vue'
import NotFound from '@/views/NotFound.vue'
import store from '@/store'

Vue.use(Router)

const router = new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'home',
      component: GanttSimple,
    },
    {
      path: '/gantt',
      name: 'gantt',
      component: Gantt,
    },
    {
      path: '/gantt-simple',
      name: 'gantt-simple',
      component: GanttSimple,
    },
    {
      path: '*',
      name: 'notFound',
      component: NotFound,
    },
  ],
})

router.beforeEach((to, _, next) => {
  const requiresAuth = to.matched.some((record) => record.meta.requiresAuth)
  const user = (store as any).state.AppStore.user

  if (requiresAuth && !user) {
    next('/')
  } else {
    if (to.path === '/' && user) {
      next({ name: 'cabinet', query: to.query })
    } else {
      next()
    }
  }
})

export default router
