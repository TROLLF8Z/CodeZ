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
      <div class="maincard">
        <el-scrollbar style="width: 100%; height: 100%">
          <el-card>
            <el-card shadow="never">
              <div style="display: flex; align-items: center">
                <el-text style="font-size: 20px; color: #000000; font-weight: 500">发布评论</el-text>
                <el-button type="info" @click="this.$router.go(-1)" style="margin-left: auto;">返回</el-button>
              </div>
              <el-input v-model="comment_input" type="textarea" :rows="10" resize="none" style="margin-top: 15px;" placeholder="发布一条友好的评论吧..."></el-input>
              <el-button type="primary" @click="submit_comment" style="margin-top: 15px;">发布</el-button>
            </el-card>
            <el-card shadow="hover" v-for="item in this.displaylist" style="margin-top: 10px;">
              <div style="display: flex; align-items: center">
                <el-image style="width: 40px; height: 40px" :src="item.avatar" />
                <el-text style="font-size: 16px; color: #000000; font-weight: 500; margin-left: 15px;">{{ item.username }}</el-text>
                <div style="display: flex; align-items: center; margin-left: auto;">
                  <el-text style="font-size: 16px; color: #000000; font-weight: 500;">评论于 {{ item.time }}</el-text>
                  <el-button type="warning" @click="delete_comment(item.cid)" style="margin-left: 10px;" v-if="this.uid == item.uid">删除</el-button>
                </div>

              </div>
              <el-divider />
              <el-text style="font-size: 18px; color: #000000; font-weight: 500; white-space: pre-line">{{ item.content }}</el-text>
            </el-card>
          </el-card>
          <el-backtop :right="100" :bottom="100" />
        </el-scrollbar>
      </div>
      <el-backtop :right="100" :bottom="100" />
    </el-main>
  </el-container>
</template>

<script>
import {Search} from "@element-plus/icons-vue";
import {ElMessageBox} from "element-plus";

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

      displaylist: [],
      comment_input: '',
      qid: 0,
    }
  },
  created() {
    this.qid = this.$route.query.id;
    this.displayname = localStorage.getItem("displayname");
    this.avatar = localStorage.getItem("avatar");
    this.zcoin = localStorage.getItem("zcoins");
    this.uid = localStorage.getItem("uid");
    if (this.avatar === '' || !this.avatar) {
      this.avatar = 'src/assets/avatar/defaultavatar.png';
    }
    this.getcomment();
  },
  methods: {
    quitLogin() {
      localStorage.clear()
      this.$router.push('/login')
      this.$message.success('退出成功')
    },
    getcomment() {
      this.displaylist = [];
      this.$request.post("/codez/comment/info/", {
        qid: this.qid,
        uid: this.uid,
      }).then(async res => {
        if (res.data.meta.status === 200) {
          let i = '';
          let tmpobj = {};
          for (i of res.data.data.retcomment) {
            tmpobj = {};
            tmpobj.cid = i.cid;
            tmpobj.uid = i.uid;
            tmpobj.content = i.ucomment;
            tmpobj.time = i.time;
            await this.$request.post("/codez/user/profile", {
              userid: i.uid,
            }).then(res => {
              if (res.data.meta.status === 200) {
                tmpobj.avatar = res.data.data.avatar;
                tmpobj.username = res.data.data.displayname;
              } else {
                this.$message.error(res.data.meta.message);
              }
            });
            this.displaylist.push(tmpobj);
          }
        } else {
          this.$message.error(res.data.meta.message);
        }
      });
    },
    submit_comment() {
      if (this.comment_input === '') {
        this.$message.error("评论内容不得为空")
      } else {
        this.$request.post("/codez/comment/submit/", {
          qid: this.qid,
          uid: this.uid,
          ucomment: this.comment_input,
        }).then(res => {
          if (res.data.meta.status === 200) {
            this.$message.success("发布成功");
            this.getcomment();
          } else {
            this.$message.error(res.data.meta.message);
          }
        });
        this.comment_input = '';
      }
    },
    delete_comment(id) {
      ElMessageBox.confirm('您是否确认删除该条评论？', '确认删除？', {
        confirmButtonText: '是',
        cancelButtonText: '否',
        type: 'warning',
      }).then(() => {
        this.$request.post("/codez/comment/delete/", {
          cid: id,
        }).then(res => {
          if (res.data.meta.status === 200) {
            this.$message.success("删除成功");
            this.getcomment();
          } else {
            this.$message.error(res.data.meta.message);
          }
        });
      })
          .catch()
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
  max-width: 1200px;
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

.logo {
  height: 60px;
  line-height: 60px;
  text-align: center;
  /* margin-left: 20px; */
}
</style>
