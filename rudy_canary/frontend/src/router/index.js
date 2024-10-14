import { createRouter, createWebHistory } from 'vue-router';
import HelloWorld from '../components/HelloWorld.vue';  
import LoginPage from '../components/LoginPage.vue';

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: LoginPage
  },
  {
    path: '/',
    name: 'Home',
    component: HelloWorld
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;
