import { createRouter, createWebHistory } from "vue-router";
import NProgress from "nprogress"; //进度条
import "nprogress/nprogress.css";

NProgress.configure({
  showSpinner: false, //通过将其设置为 false 来关闭加载微调器。
});

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      redirect: "/order/list",
      hidden: true,
    },
    {
      path: "/login",
      name: "login",
      meta: { title: "登录" },
      component: () => import("@/views/login/login.vue"),
      hidden: true,
    },
    {
      path: "/register",
      name: "register",
      meta: { title: "注册" },
      component: () => import("@/views/login/register.vue"),
      hidden: true,
    },
    {
      path: "/main",
      name: "main",
      meta: { title: "首页" },
      component: () => import("@/views/main/main.vue"),
      hidden: true,
    },
    {
      path: "/user",
      name: "user",
      meta: { title: "个人中心" },
      component: () => import("@/views/user/user.vue"),
      hidden: true,
    },
    {
      path: "/search",
      name: "search",
      meta: { title: "搜索" },
      component: () => import("@/views/search/search.vue"),
      hidden: true,
    },
    {
      path: "/bank",
      name: "bank",
      meta: { title: "题库详情" },
      component: () => import("@/views/bank/bank.vue"),
      hidden: true,
    },
    {
      path: "/exam",
      name: "exam",
      meta: { title: "作答" },
      component: () => import("@/views/exam/exam.vue"),
      hidden: true,
    },
    {
      path: "/admin/login",
      name: "admin-login",
      meta: { title: "管理员登录" },
      component: () => import("@/views/admin/login.vue"),
      hidden: true,
    },
    {
      path: "/admin",
      name: "admin",
      meta: { title: "管理员系统" },
      component: () => import("@/views/admin/main.vue"),
      children: [
        {
          path: "users",
          name: "用户管理",
          meta: { title: "用户管理" },
          component: () => import("@/views/admin/users.vue"),
        },
        {
          path: "banks",
          name: "题库管理",
          meta: { title: "题库管理" },
          component: () => import("@/views/admin/banks.vue"),
        },
        {
          path: "questions",
          name: "题目管理",
          meta: { title: "题目管理" },
          component: () => import("@/views/admin/questions.vue"),
        },
      ],
    },
  ],
});

import defaultSettings from "@/settings";

//路由全局前置钩子
router.beforeEach((to, from, next) => {
  NProgress.start();
  document.title = `${to.meta.title || "CodeZ"} - ${defaultSettings.title}`;
  let token = localStorage.getItem("token");
  let aid = localStorage.getItem("aid");
  if (token) {
    if (to.path == "/login" || to.path == "/register") {
      next({
        path: "/main",
      });
    } else if (to.path == '/admin/users') {
      if (aid) {
        next();
      } else {
        next({
          path: "/main",
        });
      }
    } else if (to.path == '/admin/login') {
      if (aid) {
        next({
          path: "/admin/users",
        });
      } else {
        next();
      }
    }else {
      next();
    }
  } else {
    if (to.path == "/login") {
      next();
    } else if (to.path == "/register") {
      next();
    } else if (to.path == "/admin/login") {
      next();
    } else {
      next({
        path: "/login",
      });
    }
  }
});

// //路由全局后置钩子
router.afterEach(() => {
  NProgress.done();
});

export default router;
