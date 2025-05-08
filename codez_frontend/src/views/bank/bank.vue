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
          <div style="width: 1000px; display: flex; align-items: center">
            <el-text style="font-size: 30px; color: #000000; font-weight: 500;">{{ this.bankname }}</el-text>
            <el-tag size="large" :type="this.display_status[this.status].type" style="margin-left: 15px;">{{ this.display_status[this.status].label }}</el-tag>
          </div>
          <el-divider />
          <div><el-text style="font-size: 14px; color: #000000; font-weight: 500">简介：</el-text></div>
          <div style="margin-top: 10px;">
            <el-card shadow="never">
              <el-text style="font-size: 16px; color: #000000; font-weight: 500;">{{ this.description }}</el-text>
            </el-card>
          </div>
          <el-table :data="this.displaylist" stripe border style="margin-top: 30px;">
            <el-table-column label="题目名称" prop="name">
              <template #default="scope">
                <div style="display: flex; align-items: center"><el-text style="font-size: 16px; color: #000000; font-weight: 400;">{{ scope.row.name }}</el-text></div>
              </template>
            </el-table-column>
            <el-table-column label="题目类型" prop="type">
              <template #default="scope">
                <div style="display: flex; align-items: center"><el-text style="font-size: 16px; color: #000000; font-weight: 400;">{{ this.question_type[scope.row.type] }}</el-text></div>
              </template>
            </el-table-column>
            <el-table-column label="是否已完成" prop="finished">
              <template #default="scope">
                <div style="display: flex; align-items: center">
                  <el-tag type="success" v-if="scope.row.finished === 1" size="large">已完成</el-tag>
                  <el-tag type="danger" v-if="scope.row.finished === 0" size="large">未完成</el-tag>
                </div>
              </template>
            </el-table-column>
            <el-table-column label="已尝试次数" prop="attempts">
              <template #default="scope">
                <div style="display: flex; align-items: center"><el-text style="font-size: 16px; color: #000000; font-weight: 400;">{{ scope.row.attempts }}</el-text></div>
              </template>
            </el-table-column>
            <el-table-column label="评论区">
              <template #default="scope">
                <el-button size="small" type="primary" autocomplete="off" @click="this.$router.push('/comment?id=' + scope.row.qid)" v-if="scope.row.finished === 1">进入</el-button>
                <el-button size="small" type="danger" autocomplete="off" disabled v-if="scope.row.finished === 0">请先完成本题</el-button>
              </template>
            </el-table-column>
          </el-table>
          <div style="display: flex; align-items: center; justify-content: center; margin-top: 50px;" v-if="this.status === 1">
            <el-button type="warning" @click="buybank" v-if="this.bank_unlocked === 0">花费 {{ this.price }}ZCoins 解锁</el-button>
            <el-button type="primary" @click="pushbank" v-if="this.bank_unlocked === 1">开始作答</el-button>
          </div>
          <div style="display: flex; align-items: center; justify-content: center; margin-top: 50px;" v-if="this.status === 0">
            <el-button type="primary" @click="pushbank" >开始作答</el-button>
          </div>
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
      displayname: "",
      avatar: "",
      zcoin: 0,
      uid: 0,

      bid: 0,
      bankname: "",
      description: "",
      status: 0,
      price: 0,
      bank_finished: 0,
      bank_unlocked: 0,
      questions: [],
      displaylist: [],

      display_status: [
        {
          type: "success",
          label: "免费",
        },
        {
          type: "warning",
          label: "收费",
        }
      ],
      question_type: ['选择题', '填空题', '简答题', '编程题']
    }
  },
  mounted() {
    this.bid = this.$route.query.id;
    this.uid = localStorage.getItem('uid');
    this.displayname = localStorage.getItem("displayname");
    this.avatar = localStorage.getItem("avatar");
    this.zcoin = localStorage.getItem("zcoins");
    if (this.avatar === '' || !this.avatar) {
      this.avatar = 'src/assets/avatar/defaultavatar.png';
    };
    this.getbankinfo();
  },
  methods: {
    quitLogin() {
      localStorage.clear()
      this.$router.push('/login')
      this.$message.success('退出成功')
    },
    async getbankinfo() {
      await this.$request.post("/codez/admin/banks/info/", {
        bid: this.bid,
      }).then(res => {
        if (res.data.meta.status === 200) {
          this.bankname = res.data.data.name;
          this.description = res.data.data.description;
          this.status = res.data.data.status;
          this.price = res.data.data.price;
          this.questions = res.data.data.questions;
          if (this.status === 2) {
            this.$router.push('/main');
            this.$message.error("题库当前不可用");
          } else {
            this.displayquestion();
          }
        } else {
          this.$router.push('/main');
          this.$message.error(res.data.meta.message);
        }
      });

      await this.$request.post("/codez/user/bank/status/", {
        bid: this.bid,
        uid: this.uid,
      }).then(res => {
        if (res.data.meta.status === 200) {
          this.bank_finished = res.data.data.finished;
          this.bank_unlocked = res.data.data.unlocked;
        } else {
          this.$message.error(res.data.meta.message);
        }
      });
    },
    async displayquestion() {
      if (this.questions !== '') {
        this.displaylist = [];
        let q = '';
        for (q of this.questions.split(',')) {
          let tmpobj = {};
          await this.$request.post("/codez/admin/questions/info/", {
            qid: q,
          }).then(res => {
            if (res.data.meta.status === 200) {
              tmpobj.qid = res.data.data.qid;
              tmpobj.name = res.data.data.name;
              tmpobj.type = res.data.data.type;
            }
          });

          await this.$request.post("/codez/user/question/status/", {
            uid: this.uid,
            qid: q,
          }).then(res => {
            if (res.data.meta.status === 200) {
              tmpobj.finished = res.data.data.finished;
              tmpobj.time = res.data.data.time;
              tmpobj.attempts = res.data.data.attempts;
            }
          });
          this.displaylist.push(tmpobj);
        }
        console.log(this.displaylist);
      }
    },
    pushbank() {
      this.$router.push('/exam?bid=' + this.bid);
    },
    buybank() {
      this.$request.post("/codez/user/bank/purchase/", {
        uid: this.uid,
        bid: this.bid,
      }).then(res => {
        if (res.data.meta.status === 200) {
          this.$message.success("解锁成功")
          localStorage.setItem("zcoins", res.data.data.zcoins);
          this.bank_unlocked = 1;
        } else {
          this.$message.error(res.data.meta.message);
        }
      });
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
