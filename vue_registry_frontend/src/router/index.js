import { createRouter, createWebHashHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import CreateView from "../views/CreateView.vue";
import CompanyView from "@/views/CompanyView.vue";

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/create',
    name: 'create',
    component: CreateView
  },
  {
    path: '/company/:reg_code',
    name: 'company',
    component: CompanyView
  },
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
