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
      <div class="maincard" v-if="!this.type === '3'">
        <el-card class="maincard.card">
        </el-card>
        <el-card class="maincard.card">
        </el-card>
      </div>
      <div class="maincard" v-else>
        <el-card style="width: 1000px">
          <div style="display: flex; align-items: center; justify-content: space-between">
            <div style="display: flex; align-items: center">
              <el-text style="font-size: 30px; color: #333333; font-weight: 500">{{ this.name }}</el-text>
              <el-tag size="large" style="margin-left: 15px;">{{ this.question_type[this.type] }}</el-tag>
            </div>
            <div style="display: flex; align-items: center">
              <el-text style="font-size: 14px; color: #333333; font-weight: 500">已提交次数：{{ this.attempts }}<br/>{{ this.displaytime }}</el-text>
            </div>
            <div style="display: flex; align-items: center"><el-text style="font-size: 14px; color: #333333; font-weight: 500; margin-left: auto;">当前题库：{{ this.bankname }}<br/>当前题目索引：{{ this.curindex + 1 }} / {{ this.totals }}</el-text></div>
          </div>
          <el-divider />
          <el-text style="font-size: 20px; color: #000000; font-weight: 500">{{ this.content }}</el-text>
          <el-divider />
          <el-card shadow="never">
            <div style="display: flex; align-items: center" v-if="this.type === 0">
              <el-radio-group v-model="this.user_answer">
                <el-radio label="A" size="large"/>
                <el-radio label="B" size="large">B</el-radio>
                <el-radio label="C" size="large">C</el-radio>
                <el-radio label="D" size="large">D</el-radio>
              </el-radio-group>
            </div>
            <div style="display: flex; align-items: center" v-if="this.type === 1 || this.type === 2">
              <el-input style="font-size: 16px; color: #000000; font-weight: 500" type="textarea" :autosize="{ minRows: 6 }" placeholder="请输入答案..." v-model="this.user_answer" />
            </div>
          </el-card>
          <div style="display: flex; align-items: center; justify-content: center; margin-top: 15px;"><el-button type="primary" @click="submit_answer">提交作答</el-button></div>
        </el-card>
      </div>
    </el-main>
  </el-container>
</template>

<script>
import {Plus} from "@element-plus/icons-vue";
import { format } from "date-fns";

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
      type: 0,
      bankname: '',
      time: 0,
      attempts: 0,
      totals: 0,
      curindex: 0,
      user_answer: '',

      requestsum: 0,
      displaytime: '',
      timerID: 0,

      question_type: ['选择题', '填空题', '简答题', '编程题']
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
    async getquestion() {
      await this.$request.post("/codez/exam/current_question/", {
        bid: this.bid,
        uid: this.uid,
      }).then(res => {
        if (res.data.meta.status === 200) {
          this.name = res.data.data.name;
          this.bankname = res.data.data.bankname;
          this.content = res.data.data.content;
          this.time = res.data.data.time;
          this.type = res.data.data.type;
          this.attempts = res.data.data.attempts;
          this.curindex = res.data.data.curindex;
          this.totals = res.data.data.totals;
          this.qid = res.data.data.questionid;
          this.requestsum = 0;
            this.user_answer = '';
        } else {
          this.$router.push('/bank?id=' + this.bid);
          this.$message.error(res.data.meta.message);
        }
      });
      this.formattime();
      this.timerecorder();
    },
    timerecorder() {
      this.timerID = setInterval(() => {
        this.time++;
        this.formattime();
        this.requestsum++;
        if (this.requestsum >= 5) {
          this.requestsum = 0;
          this.$request.post("/codez/exam/record_time/", {
            qid: this.qid,
            uid: this.uid,
            time: this.time,
          }).then(res => {
            if (res.data.meta.status === 200) {
            } else {
              this.$message.error(res.data.meta.message);
            }
          });
        }
      }, 1000);
    },
    formattime() {
      this.displaytime = '已用时：' + format(new Date(this.time * 1000), 'mm:ss');
    },
    leavingpage() {
      this.$request.post("/codez/exam/record_time/", {
        qid: this.qid,
        uid: this.uid,
        time: this.time,
      }).then(res => {
        if (res.data.meta.status === 200) {
        } else {
          this.$message.error(res.data.meta.message);
        }
      });
      if (this.timerID) {
        clearInterval(this.timerID);
        this.timerID = null;
      }
    },
    submit_answer() {
      if (this.user_answer === '') {
        this.$message.error("您的作答为空，无法提交")
      } else {
        this.$request.post("/codez/exam/submit/", {
          qid: this.qid,
          uid: this.uid,
          answer: this.user_answer,
        }).then(res => {
          if (res.data.meta.status === 200) {
            if (res.data.meta.message === '回答正确') {
              localStorage.setItem("zcoins", res.data.data.zcoins);
              this.$message.success("回答正确");
              setTimeout(() => {
                this.getquestion();
              }, 1000)
            } else {
              this.attempts = res.data.data.attempts;
              this.$message.error(res.data.meta.message);
            }
          } else {
            this.$message.error(res.data.meta.message);
          }
        });
      }
    }
  },
  beforeRouteLeave() {
    this.leavingpage();
  },
  beforeUnmount() {
    this.leavingpage();
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
