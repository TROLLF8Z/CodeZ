<template>
  <el-container>
    <el-header>
      <div style="display:flex; justify-content: center; align-items: center;">
        <el-image style="width: 40px; height: 40px; margin-right: 10px;" src="src/assets/codez.png" @click="$router.push('/main')"/>
        <el-text style="font-size: 30px; color: #409EFF; font-weight: 1000;">CodeZ</el-text>
      </div>

      <div style="display:flex; justify-content: center; align-items: center">
        <div style="display:flex; justify-content: center; align-items: center">
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
      </div>
    </el-header>
    <el-main>
      <div class="maincard">
        <el-card class="maincard.card">
        </el-card>
        <el-card class="maincard.card">
        </el-card>
      </div>
    </el-main>
  </el-container>
</template>

<script>
import {Plus} from "@element-plus/icons-vue";

export default {
  components: {Plus},
  data() {
    return {
      uid: 0,
      bid: 0,
      qid: 0,

      displayname: '',
      avatar: '',
      zcoin: 0,

      content: '',
      name: '',
      bankname: '',
      time: 0,
      attempts: 0,
      totals: 0,
      curindex: 0,
    }
  },
  mounted() {
    this.bid = this.$route.query.bid;
    this.uid = localStorage.getItem('uid');
    this.displayname = localStorage.getItem("displayname");
    this.avatar = localStorage.getItem("avatar");
    this.zcoin = localStorage.getItem("zcoins");
    if (this.avatar === '' || !this.avatar) {
      this.avatar = 'src/assets/avatar/defaultavatar.png';
    };
    this.getquestion();
  },
  methods: {
    quitLogin() {
      localStorage.clear()
      this.$router.push('/login')
      this.$message.success('退出成功')
    },
    getquestion() {
      this.$request.post("/codez/exam/current_question/", {
        bid: this.bid,
        uid: this.uid,
      }).then(res => {
        if (res.data.meta.status === 200) {
          this.name = res.data.data.name;
          this.bankname = res.data.data.bankname;
          this.content = res.data.data.content;
          this.time = res.data.data.time;
          this.attempts = res.data.data.attempts;
          this.curindex = res.data.data.curindex;
          this.totals = res.data.data.totals;
          this.qid = res.data.data.questionid;
          this.pageready();
        } else {
          this.$router.push('/bank?id=' + this.bid);
          this.$message.error(res.data.meta.message);
        }
      });
    },
    pageready() {

    }
  }
}
</script>

<style scoped>
.maincard {
  display: flex;
  justify-content: center;
  align-items: stretch;
  height: 100%;
  width: 100%;
  margin: auto;
  max-width: 1000px;
}

.maincard>card {
  height: 100%;
  width: 80%;
}

.el-icon.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 178px;
  height: 178px;
  text-align: center;
}

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
