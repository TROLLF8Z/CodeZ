<template>
  <el-container>
    <el-header>
      <div style="display:flex; justify-content: center; align-items: center;">
        <el-image style="width: 40px; height: 40px; margin-right: 10px;" src="src/assets/codez.png" @click="$router.push('/main')"/>
        <el-text style="font-size: 30px; color: #409EFF; font-weight: 1000;">CodeZ</el-text>
      </div>

      <div style="display:flex; justify-content: center; align-items: center; margin-left: auto">
        <el-image style="width: 24px; height: 24px;" src="src/assets/zcoin.png" />
        <span style="padding-left: 30px; padding-right: 30px; color:#DAA836;">{{ zcoin }}</span>
      </div>

      <el-dropdown style="cursor: pointer;height:100%;display: flex;line-height: 60px;">
        <div style="padding: 0 12px;display: flex;align-items: center;justify-content: center;">
          <el-avatar :size="26" :src='this.avatar' />
          <span style="margin-left:10px;color:#909399;">{{ displayname }}</span>
        </div>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item @click="$router.push({path: '/user', query: {uid: this.uid}})">个人中心</el-dropdown-item>
            <el-dropdown-item divided @click="quitLogin">退出登录</el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>
    </el-header>
    <el-main>
      <div style="display: flex; justify-content: center; align-items: center">
        <div style=" width: 50%; display: flex; justify-content: center; align-items: center">
          <el-input v-model="this.search" :prefix-icon="Search" placeholder="搜索题库、用户..." size="large" style="font-size: 16px;" @keyup.enter.native="push_search"/>
        </div>
      </div>

      <div style="display: flex; justify-content: center; align-items: center">
        <el-radio-group v-model="tabname" size="large" style="margin-top: 20px;">
          <el-radio-button label="题库" @change="changetab"/>
          <el-radio-button label="用户" @change="changetab"/>
        </el-radio-group>
      </div>

      <el-backtop :right="100" :bottom="100" />
    </el-main>
  </el-container>
</template>

<script>
import {Search} from "@element-plus/icons-vue";

export default {
  computed: {
    Search() {
      return Search
    }
  },
  data() {
    return {
      displayname: "",
      avatar: "",
      zcoin: 0,
      uid: 0,
      search: "",
      displaylist: [],
      tabname: '',

      display_status: [
        {
          type: "success",
          label: "免费",
        },
        {
          type: "warning",
          label: "收费",
        },
        {
          type: "danger",
          label: "禁用",
        },
      ]
    }
  },
  created() {
    this.displayname = localStorage.getItem("displayname");
    this.avatar = localStorage.getItem("avatar");
    this.zcoin = localStorage.getItem("zcoins");
    this.uid = localStorage.getItem("uid");
    if (this.avatar === '' || !this.avatar) {
      this.avatar = 'src/assets/avatar/defaultavatar.png';
    }
  },
  mounted() {
    this.search = decodeURIComponent(this.$route.query.search_param);
    setTimeout(()=>{
      this.search_request();
    }, 100);
  },
  methods: {
    quitLogin() {
      localStorage.clear()
      this.$router.push('/login')
      this.$message.success('退出成功')
    },
    push_search() {
      if (this.search === '') {
        this.$message.error("搜索内容不得为空")
      } else {
        this.search = encodeURIComponent(this.search);
        this.$router.push('/search?search_param=' + this.search);
        this.search = decodeURIComponent(this.search);
        console.log(this.search);
      }
    },
    changetab() {

    },
    search_request() {
      if (this.search === '') {
        this.$message.error("搜索内容不得为空")
      } else if (this.tabname === '题库'){
        this.$request.post("/codez/search/bank/", {
          query: this.search,
        }).then(res => {
          if (res.data.meta.status === 200) {
            this.displaylist = [];
            let b = {};
            for (b of res.data.data.search_result) {

            }
          } else {
            this.$message.error(res.data.meta.message);
          }
        });
      } else if (this.tabname === '用户') {
        this.$request.post("/codez/search/user/", {
          query: this.search,
        }).then(res => {
          if (res.data.meta.status === 200) {
          } else {
            this.$message.error(res.data.meta.message);
          }
        });
      }
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

.logo {
  height: 60px;
  line-height: 60px;
  text-align: center;
  /* margin-left: 20px; */
}
</style>
