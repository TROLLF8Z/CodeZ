<template>
  <el-text style="font-size: 20px; color: #409EFF; font-weight: 500;">根据题库ID搜索题库</el-text>
  <el-form :model="bankform" label-width="120px" style="margin-top: 30px;" label-position="right" :inline="true">
    <el-form-item label="题库ID">
      <el-input placeholder="请输入题库ID..." v-model="bankform.bankId" @keyup.enter.native="search_bank" />
    </el-form-item>
    <el-form-item label="题库名称">
      <el-input placeholder="请输入题库名称..." v-model="bankform.bankName" @keyup.enter.native="search_bank" />
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="search_bank" :disabled="searching">搜索题库</el-button>
    </el-form-item>
    <el-form-item>
      <el-button type="success" @click="edit_bank(0, 0, 2)" :disabled="searching">新增题库</el-button>
    </el-form-item>
  </el-form>
  <el-divider />

  <el-table :data="this.resultform" stripe border>
    <el-table-column label="题库ID" prop="bid">
      <template #default="scope">
        <div style="display: flex; align-items: center"><el-text style="font-size: 16px; color: #000000; font-weight: 400;">{{ scope.row.bid }}</el-text></div>
      </template>
    </el-table-column>

    <el-table-column label="题库名称" prop="name">
      <template #default="scope">
        <div style="display: flex; align-items: center"><el-text style="font-size: 16px; color: #000000; font-weight: 400;">{{ scope.row.name }}</el-text></div>
      </template>
    </el-table-column>

    <el-table-column label="操作">
      <template #default="scope">
        <el-button size="small" type="primary" autocomplete="off" @click="edit_bank(scope.$index, scope.row, 1)">编辑</el-button>
        <el-button size="small" type="danger" autocomplete="off" @click="" style="margin-left: 20px">删除</el-button>
      </template>
    </el-table-column>
  </el-table>

  <el-drawer :model-value="this.drawerVisible" :with-header="false" :before-close="drawerclose" size="50%">
    <div style="display: flex; align-items: center">
      <el-text style="font-size: 20px; color: #333333; font-weight: 500;">编辑题库内容</el-text>
      <el-button type="danger" autocomplete="off" @click="drawerclose(1)" style="margin-left: auto"><el-icon class="el-icon--left"><CircleCloseFilled /></el-icon>关闭</el-button>
    </div>
    <el-divider />
    <el-form :model="this.edit_bform" label-width="120px" label-position="right">
      <el-text style="font-size: 16px; color: #000000; font-weight: 400; margin-bottom: 30px;">题库ID：{{ this.edit_bform.bid }}</el-text>

      <el-form-item label="题库名称" style="margin-top: 20px;">
        <el-input placeholder="请输入题库名称..." v-model="edit_bform.name" />
      </el-form-item>

      <el-form-item label="题库简介" style="margin-top: 20px;">
        <el-input type="textarea" :autosize="{ minRows: 6 }" placeholder="请输入题题库简介..." v-model="edit_bform.description" />
      </el-form-item>

      <el-form-item label="题库状态" style="margin-top: 20px;">
        <el-select
            v-model="edit_bform.status"
            placeholder="选择题库状态"
            style="width: 120px"
        >
          <el-option
              v-for="item in statusSelect"
              :key="item.value"
              :label="item.label"
              :value="item.value"
          />
        </el-select>
      </el-form-item>

      <el-form-item v-if="edit_bform.status===1" label="题库解锁价格" style="margin-top: 20px;">
        <el-input type="textarea" placeholder="请输入题库解锁价格..." v-model="edit_bform.price" />
      </el-form-item>

      <el-form-item style="margin-top: 20px;">
        <el-button type="primary" autocomplete="off" @click="edit_questions(this.edit_bform.bid, this.drawerMode)">编辑题库所含题目</el-button>
      </el-form-item>
    </el-form>

    <div>
      <el-drawer :model-value="this.innerdrawerVisible" label-width="120px" size="50%"  :append-to-body="true" :before-close="drawerclose" :with-header="false">
        <div style="display: flex; align-items: center">
          <el-text style="font-size: 20px; color: #333333; font-weight: 500;">题库题目列表</el-text>
          <el-button type="danger" autocomplete="off" @click="drawerclose(2)" style="margin-left: auto"><el-icon class="el-icon--left"><CircleCloseFilled /></el-icon>关闭</el-button>
        </div>
        <el-divider />

        <el-button type="success" autocomplete="off" @click="opendialog">添加题目</el-button>
        <el-table :data="question_list" stripe border style="margin-top: 20px;">
          <el-table-column label="题目ID" prop="qid">
            <template #default="scope">
              <div style="display: flex; align-items: center"><el-text style="font-size: 16px; color: #000000; font-weight: 400;">{{ scope.row.qid }}</el-text></div>
            </template>
          </el-table-column>

          <el-table-column label="题目名称" prop="name">
            <template #default="scope">
              <div style="display: flex; align-items: center"><el-text style="font-size: 16px; color: #000000; font-weight: 400;">{{ scope.row.name }}</el-text></div>
            </template>
          </el-table-column>

          <el-table-column label="操作">
            <template #default="scope">
              <el-button size="small" type="primary" autocomplete="off" @click="edit_questions(scope.row, 3)">编辑</el-button>
              <el-button size="small" type="danger" autocomplete="off" @click="delete_question(scope.$index, scope.row)" style="margin-left: 20px">删除</el-button>
            </template>
          </el-table-column>
        </el-table>

        <el-dialog :model-value="dialogVisible" width="30%" :before-close="dialogclose" :show-close="false">
          <template #header="{ close, titleId, titleClass }">
            <div style="display: flex; align-items: center; justify-content: space-between;">
              <el-text style="font-size: 20px; color: #000000; font-weight: 400" v-if="this.dialogMode <= 2">添加题目</el-text>
              <el-text style="font-size: 20px; color: #000000; font-weight: 400" v-if="this.dialogMode === 3">编辑题目</el-text>
              <el-button type="danger" @click="dialogclose">
                <el-icon class="el-icon--left"><CircleCloseFilled /></el-icon>
                关闭
              </el-button>
            </div>
          </template>
          <div style="display: flex; align-items: center; justify-content: center" v-if="this.dialogMode <= 2">
            <el-button type="primary" autocomplete="off" @click="dialogdiv(1)">添加已有题目</el-button>
            <el-button type="success" autocomplete="off" @click="dialogdiv(2)">添加新增题目</el-button>
          </div>
          <el-divider />

          <div v-if="this.dialogMode === 1" style="display: flex; flex-direction: column; align-items: center; justify-content: center">
            <el-input placeholder="请输入题目ID..." v-model="this.dialogform.qid" @input="getqname"/>
            <el-text style="font-size: 16px; color: #000000; font-weight: 400; margin-top: 20px;">题目名称：{{ this.qname }}</el-text>
            <el-button type="success" autocomplete="off" @click="addquestion" style="margin-top: 20px;">确认添加</el-button>
          </div>

          <div v-if="this.dialogMode === 2 || this.dialogMode === 3" style="display: flex; flex-direction: column; align-items: center; justify-content: center">
            <el-form :model="this.dialogform" label-width="120px" label-position="right">
              <el-form-item label="题目ID">
                <el-input placeholder="请输入题目ID..." v-model="this.dialogform.qid" disabled/>
              </el-form-item>

              <el-form-item label="题目名称" style="margin-top: 20px;">
                <el-input placeholder="请输入题目名称..." v-model="this.dialogform.name"/>
              </el-form-item>

              <el-form-item label="题目类型" style="margin-top: 20px;">
                <el-select
                    v-model="dialogform.type"
                    placeholder="选择题目类型"
                    style="width: 120px"
                >
                  <el-option
                      v-for="item in typeSelect"
                      :key="item.value"
                      :label="item.label"
                      :value="item.value"
                  />
                </el-select>
              </el-form-item>

              <el-form-item label="题目内容" style="margin-top: 20px;">
                <el-input type="textarea" :autosize="{ minRows: 6 }" placeholder="请输入题目内容..." v-model="this.dialogform.content"/>
              </el-form-item>

              <el-form-item label="题目答案" style="margin-top: 20px;">
                <el-input type="textarea" :autosize="{ minRows: 6 }" placeholder="请输入题目答案..." v-model="this.dialogform.answer"/>
              </el-form-item>
            </el-form>
            <el-button type="success" autocomplete="off" @click="addquestion" style="margin-top: 20px;" v-if="this.dialogMode === 2">确认添加</el-button>
            <el-button type="success" autocomplete="off" @click="addquestion" style="margin-top: 20px;" v-if="this.dialogMode === 3">确认修改</el-button>
          </div>
        </el-dialog>
      </el-drawer>
    </div>

    <div style="display: flex; align-items: center; justify-content: center;">
      <el-button type="success" autocomplete="off" @click="applychange">提交修改</el-button>
    </div>
  </el-drawer>
</template>

<script>
import {ElMessageBox} from "element-plus";

export default {
  data() {
    return {
      bankform: {
        bankId: '',
        bankName: '',
      },
      searching: false,
      resultform: [],
      question_list: [],
      drawerVisible: false,
      innerdrawerVisible: false,
      drawerMode: -1,
      dialogVisible: false,
      dialogMode: -1,
      qname: '',

      edit_bform: {
        bid: '',
        name: '',
        description: '',
        status: 0,
        price: 0,
        questions: '',
      },

      statusSelect: [
        {
          value: 0,
          label: "公开",
        },
        {
          value: 1,
          label: "收费",
        },
        {
          value: 2,
          label: "隐藏",
        }
      ],

      typeSelect: [
        {
          value: 0,
          label: "选择题",
        },
        {
          value: 1,
          label: "填空题",
        },
        {
          value: 2,
          label: "简答题",
        },
        {
          value: 3,
          label: "编程题",
        }
      ],

      dialogform: {
        qid: 0,
        name: '',
        type: 0,
        content: '',
        answer: '',
      }
    };
  },

  methods: {
    search_bank() {
      this.searching = true;
      if (this.bankform.bankId === "" && this.bankform.bankName === "") {
        this.$message.error("请至少输入一个查询条件")
        this.searching = false;
      } else {
        this.$request.post("/codez/admin/banks/search/", {
          bid: this.bankform.bankId,
          name: this.bankform.bankName,
        }).then(res => {
          if (res.data.meta.status === 200) {
            this.resultform= [];
            let b= {};
            for (b of res.data.data.search_results) {
              this.resultform.push({
                "bid": b.bid,
                "name": b.bankname,
              })
            }
            this.searching = false;
          } else {
            this.searching= false;
            this.$message.error(res.data.meta.message);
          }
        });
      }
    },
    drawerclose(done) {
      if (this.innerdrawerVisible) {
        this.innerdrawerVisible = false;
      } else if (this.drawerVisible) {
        if (this.drawerMode === 2) {
          if (this.edit_bform.name !== '' || this.edit_bform.description !== '' || this.edit_bform.questions !== '') {
            ElMessageBox.confirm('当前有未保存信息，请问是否退出？', '警告：', {
              confirmButtonText: 'OK',
              cancelButtonText: 'Cancel',
              type: 'warning',
            }).then(() => {
              this.drawerVisible = false;
              done()
            })
                .catch()
          } else {
            this.drawerVisible = false;
        }

      } else {
          this.drawerVisible = false;
        }
      }
    },
    dialogclose(done) {
      if (this.dialogMode === 1|| this.dialogMode === 3) {
        this.dialogVisible = false;
      } else if (this.dialogMode === 2) {
        if (this.dialogform.name !== '' || this.dialogform.content !== '' || this.dialogform.answer !== '') {
          ElMessageBox.confirm('当前有未保存信息，请问是否退出？', '警告：', {
            confirmButtonText: 'OK',
            cancelButtonText: 'Cancel',
            type: 'warning',
          }).then(() => {
            this.dialogVisible = false;
            done()
          })
              .catch()
        } else {
          this.dialogVisible = false;
          done()
        }
      }
    },
    edit_bank(index, row, mode) {
      this.drawerMode = mode;
      if (mode === 1) {
        this.$request.post("/codez/admin/banks/info/", {
          bid: row.bid,
        }).then(res => {
          if (res.data.meta.status === 200) {
            this.edit_bform= {
              bid: res.data.data.bid,
              name: res.data.data.name,
              description: res.data.data.description,
              status: res.data.data.status,
              price: res.data.data.price,
              questions: res.data.data.questions,
            };
            this.drawerVisible = true;
          } else {
            this.$message.error(res.data.meta.message);
          }
        });
      } else if (mode === 2) {
        this.$request.post("/codez/admin/banks/available_id/", {
          mode: "newbank",
        }).then(res => {
          if (res.data.meta.status === 200) {
            this.edit_bform= {
              bid: res.data.data.new_bid,
              name: '',
              description: '',
              status: 0,
              price: 0,
              questions: '',
            };
            this.drawerVisible = true;
          } else {
            this.$message.error(res.data.meta.message);
          }
        });
      }
    },
    applychange() {
      if (this.edit_bform.name === '') {
        this.$message.error("题库名称不得为空")
      } else if (this.edit_bform.description === '') {
        this.$message.error("题库简介不得为空")
      } else if (this.edit_bform.status === 1 && this.edit_bform.price <= 0) {
        this.$message.error("题库解锁价格不合法")
      } else {
        if (this.drawerMode === 1) {
          this.$request.post("/codez/admin/banks/change/", {
            bid: this.edit_bform.bid,
            name: this.edit_bform.name,
            status: this.edit_bform.status,
            price: this.edit_bform.price,
            questions: this.edit_bform.questions,
            description: this.edit_bform.description,
          }).then(res => {
            if (res.data.meta.status === 200) {
              this.$message.success("成功修改");
              this.drawerVisible = false;
            } else {
              this.$message.error(res.data.meta.message);
            }
          });
        } else if (this.drawerMode === 2) {
          this.$request.post("/codez/admin/banks/create/", {
            bid: this.edit_bform.bid,
            name: this.edit_bform.name,
            description: this.edit_bform.description,
            status: this.edit_bform.status,
            price: this.edit_bform.price,
            questions: this.edit_bform.questions,
          }).then(res => {
            if (res.data.meta.status === 200) {
              this.$message.success("成功新增题库, 题库ID为：" + String(this.edit_bform.bid));
              this.drawerVisible = false;
            } else {
              this.$message.error(res.data.meta.message);
            }
          });
        }
      }
    },
    edit_questions(id, mode) {
      if (mode === 1) {
        this.question_list = [];
        if (this.edit_bform.questions !== '') {
          let q = "";
          for (q of this.edit_bform.questions.split(",")) {
            this.$request.post("/codez/admin/questions/info/", {
              qid: q,
            }).then(res => {
              if (res.data.meta.status === 200) {
                this.question_list.push({
                  qid: res.data.data.qid,
                  name: res.data.data.name,
                });
              }
            });
          }
        }
        this.innerdrawerVisible = true;
      } else if (mode === 2) {
        this.question_list = [];
        if (this.edit_bform.questions !== '') {
          let q = "";
          for (q of this.edit_bform.questions.split(",")) {
            this.$request.post("/codez/admin/questions/info/", {
              qid: q,
            }).then(res => {
              if (res.data.meta.status === 200) {
                this.question_list.push({
                  qid: res.data.data.qid,
                  name: res.data.data.name,
                });
              }
            });
          }
        }
        this.innerdrawerVisible = true;
      } else if (mode === 3) {
        this.dialogMode = 3;
        this.$request.post("/codez/admin/questions/info/", {
          qid: id.qid,
        }).then(res => {
          if (res.data.meta.status === 200) {
            this.dialogform = {
              qid: id.qid,
              name: res.data.data.name,
              type: res.data.data.type,
              content: res.data.data.content,
              answer: res.data.data.answer,
            };
            this.dialogVisible = true;
          }
        });
      }
    },
    opendialog() {
      this.dialogMode = 1;
      this.dialogform = {
        qid: '',
        name: '',
        type: 0,
        content: '',
        answer: '',
      };
      this.qname = ''
      this.dialogVisible = true;
    },
    dialogdiv(mode) {
      if (mode === 1) {
        if (this.dialogform.name !== '' || this.dialogform.content !== '' || this.dialogform.answer !== '') {
          ElMessageBox.confirm('当前有未保存信息，请问是否切换模式？', '警告：', {
            confirmButtonText: 'OK',
            cancelButtonText: 'Cancel',
            type: 'warning',
          }).then(() => {
            this.dialogform = {
              qid: '',
              name: '',
              type: 0,
              content: '',
              answer: '',
            };
            this.dialogMode = mode;
          })
              .catch()
        } else {
          this.dialogform = {
            qid: '',
            name: '',
            type: 0,
            content: '',
            answer: '',
          };
          this.dialogMode = mode;
        }
      } else if (mode === 2) {
        this.$request.post("/codez/admin/questions/available_id/", {
          mode: "newquestion",
        }).then(res => {
          if (res.data.meta.status === 200) {
            this.dialogform = {
              qid: res.data.data.new_qid,
              name: '',
              type: 0,
              content: '',
              answer: '',
            };
            this.dialogMode = mode;
          } else {
            this.$message.error(res.data.meta.message);
          }
        });
      }
    },
    getqname() {
      if (this.dialogform.qid !== '' && String(this.dialogform).length >= 6) {
        this.$request.post("/codez/admin/questions/info/", {
          qid: this.dialogform.qid,
        }).then(res => {
          if (res.data.meta.status === 200) {
            this.qname = res.data.data.name;
          } else {
            this.qname = '';
          }
        });
      } else {
        this.qname = '';
      }
    },
    pushquestion(id) {
      if (this.edit_bform.questions === '') {
        this.edit_bform.questions = id;
      } else {
        this.edit_bform.questions += ',' + id;
      }
    },
    addquestion() {
      if (this.dialogMode === 1){
        if (this.dialogform.qid !== '' && String(this.dialogform).length >= 6) {
          this.$request.post("/codez/admin/questions/info/", {
            qid: this.dialogform.qid,
          }).then(res => {
            if (res.data.meta.status === 200) {
              this.pushquestion(this.dialogform.qid);
              this.question_list.push({
                qid: this.dialogform.qid,
                name: this.qname,
              });
              this.$message.success("添加成功");
              this.dialogVisible = false;
            } else {
              this.$message.error(res.data.meta.message);
            }
          });
        }
      } else if (this.dialogMode === 2) {
        if (this.dialogform.name === '' || this.dialogform.content === '' || this.dialogform.answer === '') {
          this.$message.error("题目必要信息不得为空");
        } else {
          this.$request.post("/codez/admin/questions/create/", {
            qid: this.dialogform.qid,
            name: this.dialogform.name,
            type: this.dialogform.type,
            content: this.dialogform.content,
            answer: this.dialogform.answer,
          }).then(res => {
            if (res.data.meta.status === 200) {
              this.pushquestion(this.dialogform.qid);
              this.question_list.push({
                qid: this.dialogform.qid,
                name: this.dialogform.name,
              });
              this.$message.success("添加成功");
              this.dialogVisible = false;
            } else {
              this.$message.error(res.data.meta.message);
            }
          });
        }
      } else if (this.dialogMode === 3) {
        if (this.dialogform.name === '' || this.dialogform.content === '' || this.dialogform.answer === '') {
          this.$message.error("题目必要信息不得为空");
        } else {
          this.$request.post("/codez/admin/questions/change/", {
            qid: this.dialogform.qid,
            name: this.dialogform.name,
            type: this.dialogform.type,
            content: this.dialogform.content,
            answer: this.dialogform.answer,
          }).then(res => {
            if (res.data.meta.status === 200) {
              this.$message.success("修改成功");
              this.dialogVisible = false;
            } else {
              this.$message.error(res.data.meta.message);
            }
          });
        }
      }
    },
    delete_question(index, row) {
      ElMessageBox.confirm('请问是否从题库中删除该题目？\n该操作将不可逆！', '警告：', {
        confirmButtonText: 'OK',
        cancelButtonText: 'Cancel',
        type: 'warning',
      }).then(() => {
        this.question_list.splice(index, 1);
        let q = {};
        this.edit_bform.questions = '';
        for (q of this.question_list) {
          if (this.edit_bform.questions === ''){
            this.edit_bform.questions = q.qid
          } else {
            this.edit_bform.questions += ',' + q.qid;
          }
        }
      })
          .catch(() => {})
    }
  }
}
</script>

<style  scoped>
    span {
        color: white;
        font-weight: 1000;
        font-size: 26px;

    }
  .el-row {
    margin-bottom: 20px;
    &:last-child {
      margin-bottom: 0;
    }
  }
  .el-col {
    border-radius: 10px;
    text-align: center;
    line-height:120px;


  }
  .bg-purple-dark {
    background: #99a9bf;
  }
  .bg-purple {
    background: #d3dce6;
  }
  .bg-purple-light {
    background: #e5e9f2;
  }
  .grid-content {
    border-radius: 4px;
    min-height: 150px;
  }
  .row-bg {
    padding: 10px 0;
    background-color: #f9fafc;
  }
</style>
