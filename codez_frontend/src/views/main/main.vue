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
          <el-radio-button label="全部题库" @change="changetab"/>
          <el-radio-button label="免费题库" @change="changetab"/>
          <el-radio-button label="收费题库" @change="changetab"/>
        </el-radio-group>
      </div>

      <div  style="display: flex; justify-content: center; align-items: center; flex-direction: column;">
        <el-card v-for="bank in this.displaylist" shadow="hover" style="width: 60%; margin-top: 10px; margin-bottom: 20px;" @click="card_click(bank)">
          <div>
            <el-text style="font-size: 20px; font-weight: 500; color:#000000; margin-right: 15px;">{{ bank.name }}</el-text>
            <el-tag :type="this.display_status[bank.status].type">{{ this.display_status[bank.status].label }}</el-tag>
          </div>
          <div style="margin-top: 10px;"><el-text style="font-size: 14px; font-weight: 500; color:#000000; white-space: pre-line">{{ bank.description }}</el-text></div>
        </el-card>
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
      banklist: [],
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
    this.getbanklist();
    setTimeout(() => {
      this.tabname = '全部题库';
      this.changetab();
    }, 100);
  },
  methods: {
    quitLogin() {
      localStorage.clear()
      this.$router.push('/login')
      this.$message.success('退出成功')
    },
    getbanklist() {
      this.$request.post("/codez/banklist/", {
        uid: this.uid,
      }).then(res => {
        if (res.data.meta.status === 200) {
          this.banklist = [];
          let b = {};
          for (b of res.data.data.result) {
            this.banklist.push(b);
          }
        } else {
          this.$message.error(res.data.meta.message);
        }
        return true;
      });
    },
    changetab() {
      this.displaylist = [];
      let b = {};
      let i = 0;
      for (b of this.banklist) {
        if (this.tabname === '全部题库') {
          b.index = i;
          this.displaylist.push(b);
        } else if (this.tabname === '免费题库') {
          if (b.status === 0) {
            b.index = i;
            this.displaylist.push(b);
          }
        } else if (this.tabname === '收费题库') {
          if (b.status === 1) {
            b.index = i;
            this.displaylist.push(b);
          }
        }
        i++;
      }
    },
    push_search() {
      if (this.search === '') {
        this.$message.error("搜索内容不得为空")
      } else {
        this.search = encodeURIComponent(this.search);
        this.$router.push('/search?search_param=' + this.search);
      }
    },
    card_click(item) {
      this.$router.push('/bank?id=' + item.bid);
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
