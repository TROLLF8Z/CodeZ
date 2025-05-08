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
      <div class="maincard" v-if="this.type === 3">
        <el-card style="width: 50%; margin-right: 30px;">
          <div style="display: flex; align-items: center; justify-content: space-between">
            <div style="display: flex; align-items: center">
              <el-button type="info" @click="this.$router.push('/bank?id=' + this.bid)">返回</el-button>
              <el-text style="font-size: 30px; color: #333333; font-weight: 500">{{ this.name }}</el-text>
              <el-tag size="large" style="margin-left: 15px;">{{ this.question_type[this.type] }}</el-tag>
            </div>
            <div style="display: flex; align-items: center">
              <el-text style="font-size: 14px; color: #333333; font-weight: 500">已提交次数：{{ this.attempts }}<br/>{{ this.displaytime }}</el-text>
            </div>
            <div style="display: flex; align-items: center">
              <el-text style="font-size: 14px; color: #333333; font-weight: 500; margin-left: auto;">当前题库：{{ this.bankname }}<br/>当前题目索引：{{ this.curindex + 1 }} / {{ this.totals }}</el-text>
            </div>
          </div>
          <el-divider />
          <el-text style="font-size: 20px; color: #000000; font-weight: 500; white-space: pre-line">{{ this.content }}</el-text>
        </el-card>
        <el-card style="width: 100%">
          <div style="display: flex; align-items: center">
            <el-button type="primary" @click="submit_answer">提交作答</el-button>
          </div>
          <el-card shadow="never" style="margin-top: 20px;" v-loading="submitting">
            <PythonEditor v-model="this.user_answer" />
          </el-card>
        </el-card>
      </div>

      <div class="maincard" v-else>
        <el-card style="width: 1000px">
          <div style="display: flex; align-items: center; justify-content: space-between">
            <div style="display: flex; align-items: center">
              <el-button type="info" @click="this.$router.push('/bank?id=' + this.bid)">返回</el-button>
              <el-text style="font-size: 30px; color: #333333; font-weight: 500; margin-left: 30px;">{{ this.name }}</el-text>
              <el-tag size="large" style="margin-left: 15px;">{{ this.question_type[this.type] }}</el-tag>
            </div>
            <div style="display: flex; align-items: center">
              <el-text style="font-size: 14px; color: #333333; font-weight: 500">已提交次数：{{ this.attempts }}<br/>{{ this.displaytime }}</el-text>
            </div>
            <div style="display: flex; align-items: center">
              <el-text style="font-size: 14px; color: #333333; font-weight: 500; margin-left: auto;">当前题库：{{ this.bankname }}<br/>当前题目索引：{{ this.curindex + 1 }} / {{ this.totals }}</el-text>
            </div>
          </div>
          <el-divider />
          <el-text style="font-size: 20px; color: #000000; font-weight: 500; white-space: pre-line">{{ this.content }}</el-text>
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

      <el-dialog style="width: 500px" v-model="this.dialogVisible" title="获取评分" :before-close="dialogClose">
        <div style="display: flex; justify-content: center; align-items: center" v-if="this.return_score === ''">
          <el-text style="font-size: 30px; color: #000000; font-weight: 600">等待AI评分中...</el-text>
        </div>
        <div style="display: flex; justify-content: center; align-items: center" v-if="this.return_score !== ''"><el-text style="font-size: 28px; color: #000000; font-weight: 500">AI评分</el-text></div>
        <div style="display: flex; align-items: center" v-if="this.return_score !== ''"><el-text style="font-size: 16px; color: #000000; font-weight: 400">AI打分：{{ this.return_score }}</el-text></div>
        <div style="display: flex; align-items: center" v-if="this.return_score !== ''"><el-text style="font-size: 16px; color: #000000; font-weight: 400">打分理由：{{ this.return_reason }}</el-text></div>
        <div style="display: flex; justify-content: center; align-items: center" v-if="this.return_score !== ''"><el-button type="primary" @click="dialogconfirm">确定</el-button></div>
      </el-dialog>
    </el-main>
  </el-container>
</template>

<script>
import { defineComponent } from "vue";
import { format } from "date-fns";
import { basicSetup } from 'codemirror'
import { EditorView } from '@codemirror/view'
import { EditorState } from '@codemirror/state'
import { python } from '@codemirror/lang-python'
import PythonEditor from '@/components/PythonEditor.vue'

export default defineComponent({
  components: { PythonEditor },
  props: {
    modelValue: {
      type: String,
      default: ''
    },
    height: {
      type: String,
      default: '500px'
    }
  },
  emits: ['update:modelValue'],
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
      return_score: '',
      return_reason: '',

      requestsum: 0,
      dialogVisible: false,
      submitting: false,
      displaytime: '',
      timerID: 0,

      editor: null,
      state: null,

      question_type: ['选择题', '填空题', '简答题', '编程题']
    }
  },
  mounted() {
    this.initializeEditor();
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
          if (res.data.meta.message === "获取成功") {
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
            this.formattime();
            this.timerecorder();
          } else if (res.data.meta.message === "用户已完成题库") {
            this.$message.success("恭喜你已完成该题库！");
            setTimeout(()=>{
              this.$router.push('/bank?id=' + this.bid);
            })
          }
        } else {
          this.$router.push('/bank?id=' + this.bid);
          this.$message.error(res.data.meta.message);
        }
      });
    },
    timerecorder() {
      if (this.timerID !== 0) {
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
      }
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
    async submit_answer() {
      if (this.user_answer === '') {
        this.$message.error("您的作答为空，无法提交")
      } else {
        if (this.type === 0 || this.type === 1) {
          await this.$request.post("/codez/exam/submit/", {
            qid: this.qid,
            uid: this.uid,
            answer: this.user_answer,
          }).then(res => {
            if (res.data.meta.status === 200) {
              if (res.data.meta.message === '回答正确') {
                localStorage.setItem("zcoins", res.data.data.zcoin);
                this.attempts = res.data.data.attempts;
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
        } else if (this.type === 2) {
          this.return_score = '';
          this.return_reason = '';
          this.dialogVisible = true;
          this.$request.post("/codez/exam/submit/", {
            qid: this.qid,
            uid: this.uid,
            answer: this.user_answer,
          }).then(res => {
            if (res.data.meta.status === 200) {
              this.return_score = res.data.data.score;
              this.return_reason = res.data.data.reason;
              if (Number(this.return_score) >= 60) {
                this.zcoin = res.data.data.zcoins
                localStorage.setItem("zcoins", res.data.data.zcoin);
              } else {
                this.attempts = res.data.data.attempts;
              }
            } else {
              this.$message.error(res.data.meta.message);
            }
          });
        } else if (this.type === 3) {
          this.submitting = true;
          let user_code = this.user_answer.split('\n');
          let line = '';
          let answerlist = [];
          for (line of user_code) {
            answerlist.push(line);
          }
          await this.$request.post("/codez/exam/submit/", {
            qid: this.qid,
            uid: this.uid,
            answer: answerlist,
          }).then(res => {
            if (res.data.meta.status === 200) {
              if (res.data.meta.message === '回答正确') {
                localStorage.setItem("zcoins", res.data.data.zcoin);
                this.attempts = res.data.data.attempts;
                this.$message.success("回答正确");
                setTimeout(() => {
                  this.getquestion();
                }, 1000)
              } else {
                this.submitting = false;
                this.attempts = res.data.data.attempts;
                this.$message.error(res.data.meta.message);
                console.log(res.data.data.result);
                this.$message.info(res.data.data.result);
              }
            } else {
              this.$message.error(res.data.meta.message);
            }
          });
        }
      }
    },
    dialogClose(done) {
      if (this.return_score === '') {
        return 1
      } else {
        done()
      }
    },
    dialogconfirm() {
      if (Number(this.return_score) >= 60) {
        this.getquestion();
      } else {
        this.dialogVisible = false;
      }
    },
    initializeEditor() {
      const extensions = [
        basicSetup,
        python(),
        EditorView.lineWrapping,
        EditorView.updateListener.of((update) => {
          if (update.docChanged) {
            this.$emit('update:modelValue', update.state.doc.toString())
          }
        })
      ]

      this.state = EditorState.create({
        doc: this.modelValue,
        extensions
      })

      this.editor = new EditorView({
        state: this.state,
        parent: this.$refs.editorContainer
      })
    }
  },
  beforeRouteLeave() {
    if (this.editor) {
      this.editor.destroy();
    }
    this.leavingpage();
  },
  beforeUnmount() {
    if (this.editor) {
      this.editor.destroy();
    }
    this.leavingpage();
  },
  watch: {
    modelValue(newVal) {
      if (newVal !== this.editor.state.doc.toString()) {
        this.editor.dispatch({
          changes: {
            from: 0,
            to: this.editor.state.doc.length,
            insert: newVal
          }
        })
      }
    }
  }
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap');

.jetbrains-editor .cm-editor {
  font-family: 'JetBrains Mono', monospace;
  font-size: 14px;
  font-weight: 400;
  line-height: 1.6;
}

.jetbrains-editor .cm-content {
  font-family: 'JetBrains Mono', monospace;
  font-size: 14px;
  font-weight: 400;
  line-height: 1.6;
}

.jetbrains-editor .cm-gutters {
  font-family: 'JetBrains Mono', monospace;
  font-size: 13px;
}

.jetbrains-editor .cm-cursor {
  border-left-color: #ffcc00;
}

.jetbrains-editor .cm-selectionBackground {
  background: rgba(100, 255, 100, 0.2);
}

.editor-container {
  height: 100%;
  overflow: hidden;
  border: 1px solid #444;
  border-radius: 4px;
}

.cm-editor {
  height: 100%;
}

.cm-scroller {
  overflow: auto;
}

.maincard {
  display: flex;
  justify-content: center;
  align-items: stretch;
  height: 100%;
  width: 100%;
  margin: auto;
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
