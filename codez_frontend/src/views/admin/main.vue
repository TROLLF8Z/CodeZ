<template>
  <el-container>
    <el-header>
      <div style="display:flex; justify-content: center; align-items: center;">
        <el-image style="width: 40px; height: 40px; margin-right: 10px;" src="../src/assets/codez.png" @click="$router.push('/admin')"/>
        <el-text style="font-size: 30px; color: #409EFF; font-weight: 1000;">CodeZ 管理员系统</el-text>
      </div>

      <el-dropdown style="cursor: pointer;height:100%;display: flex;line-height: 60px;">
        <div style="padding: 0 12px;display: flex;align-items: center;justify-content: center;">
          <el-avatar :size="26" :src='this.avatar' />
          <span style="margin-left:10px;color:#909399;">{{ displayname }}</span>
        </div>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item @click="quitLogin">退出登录</el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </el-header>
    <el-container>
      <el-aside :style="{ 'fit-content' : '200px' }">
        <el-menu router :default-active="$route.path" active-text-color="#fff"
                 background-color="#011528" text-color="hsla(0,0%,100%,.65)" >
          <div>
            <el-menu-item index="/admin/users"><el-icon><User /></el-icon>用户管理</el-menu-item>
            <el-menu-item index="/admin/banks"><el-icon><Box /></el-icon>题库管理</el-menu-item>
            <el-menu-item index="/admin/questions"><el-icon><Document /></el-icon>题目管理</el-menu-item>
          </div>
        </el-menu>
      </el-aside>
      <el-main>
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
import * as ElementPlusIconVue from "@element-plus/icons-vue";

export default {
  data() {
    return {
      displayname: "",
      avatar: "",
      aid: 0,
    }
  },
  created() {
    this.displayname = localStorage.getItem("name");
    this.avatar = "../src/assets/avatar/admin.png";
    this.aid = localStorage.getItem("aid");
  },
  methods: {
    quitLogin() {
      localStorage.clear()
      this.$router.push('/admin/login')
      this.$message.success('退出成功')
    }
  }
}
</script>

<style scoped>
.el-container {
  height: 100vh;
}

.el-aside {
  color: #fff;
  z-index: 10;
  background-color: #011528;
  box-shadow: 2px 0 6px rgba(0, 21, 41, 0.35);
}

.el-header {
  line-height: 60px;
  padding: 0 10px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: #fff;
  z-index: 9;
  box-shadow: 0 1px 4px rgba(0, 21, 41, 0.08);
}

.el-main {
  background-color: #f0f2f5;
  position: relative;
}

.el-menu {
  border: none;
}

.el-menu-item.is-active {
  background-color: #1890ff !important;
}

.el-menu-item {
  background-color: #000b16;
}

.el-menu-item:hover {
  color: #fff !important;
}

.logo {
  height: 60px;
  line-height: 60px;
  text-align: center;
  /* margin-left: 20px; */
}
</style>
