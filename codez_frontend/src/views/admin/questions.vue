<template>
  <el-text style="font-size: 20px; color: #409EFF; font-weight: 500;">根据题目ID搜索题目</el-text>
  <el-form :model="questionform" label-width="120px" style="margin-top: 30px;" label-position="right" :inline="true">
    <el-form-item label="题目ID">
      <el-input placeholder="请输入题目ID..." v-model="questionform.questionId" @keyup.enter.native="search_question" />
    </el-form-item>
    <el-form-item label="题目名称">
      <el-input placeholder="请输入题目名称..." v-model="questionform.questionName" @keyup.enter.native="search_question" />
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="search_question" :disabled="searching">搜索题目</el-button>
    </el-form-item>
    <el-form-item>
      <el-button type="success" @click="edit_question(0, 0, 2)" :disabled="searching">新增题目</el-button>
    </el-form-item>
  </el-form>
  <el-divider />

  <el-table :data="this.resultform" stripe border>
    <el-table-column label="题目ID" prop="uid">
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
        <el-button size="small" type="primary" autocomplete="off" @click="edit_user(scope.$index, scope.row, 1)">编辑</el-button>
        <el-button size="small" type="danger" autocomplete="off" @click="" style="margin-left: 20px">删除</el-button>
      </template>
    </el-table-column>
  </el-table>

  <el-drawer :model-value="this.drawerVisible" :with-header="false" :before-close="drawerclose">
    <div style="display: flex; align-items: center">
      <el-text style="font-size: 20px; color: #333333; font-weight: 500;">编辑题目内容</el-text>
      <el-button type="danger" autocomplete="off" @click="drawerclose" style="margin-left: auto"><el-icon class="el-icon--left"><CircleCloseFilled /></el-icon>关闭</el-button>
    </div>
    <el-divider />
    <el-form :model="this.edit_qform" label-width="120px" label-position="right">
      <el-text style="font-size: 16px; color: #000000; font-weight: 400; margin-bottom: 30px;">题目ID：{{ this.edit_qform.qid }}</el-text>

      <el-form-item label="题目名称" style="margin-top: 20px;">
        <el-input placeholder="请输入题目名称..." v-model="edit_qform.name" />
      </el-form-item>

      <el-form-item label="题目类型" style="margin-top: 20px;">
        <el-select
            v-model="edit_qform.type"
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
        <el-input type="textarea" placeholder="请输入题目内容..." v-model="edit_qform.content" />
      </el-form-item>

      <el-form-item label="题目答案" style="margin-top: 20px;">
        <el-input type="textarea" placeholder="请输入题目答案..." v-model="edit_qform.answer" />
      </el-form-item>
    </el-form>
    <div style="display: flex; align-items: center; justify-content: center;">
      <el-button type="success" autocomplete="off" @click="applychange">提交修改</el-button>
    </div>
  </el-drawer>
</template>

<script>
export default {
  data() {
    return {
      questionform: {
        questionId: '',
        questionName: '',
      },
      searching: false,
      resultform: [],
      drawerVisible: false,
      drawerMode: -1,

      edit_qform: {
        qid: '',
        name: '',
        type: 0,
        content: '',
        answer: '',
      },

      typeSelect: [
        {
          value: "0",
          label: "选择题",
        },
        {
          value: "1",
          label: "填空题",
        },
        {
          value: "2",
          label: "简答题",
        },
        {
          value: "3",
          label: "编程题",
        }
      ],
    };
  },

  methods: {
    search_question() {
      this.searching = true;
      if (this.questionform.questionId === "" && this.questionform.questionName === "") {
        this.$message.error("请至少输入一个查询条件")
        this.searching = false;
      } else {
        this.$request.post("/codez/admin/questions/search/", {
          qid: this.questionform.questionId,
          name: this.questionform.questionName,
        }).then(res => {
          if (res.data.meta.status === 200) {
            this.resultform= [];
            let q= {};
            for (q of res.data.data.search_results) {
              this.resultform.push({
                "qid": q.qid,
                "name": q.username,
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
    drawerclose() {
      this.drawerVisible = false;
    },
    edit_question(index, row, mode) {
      this.drawerMode = mode;
      if (mode === 1) {

      } else if (mode === 2) {
        this.$request.post("/codez/admin/questions/available_id/", {
          mode: "newquestion",
        }).then(res => {
          if (res.data.meta.status === 200) {
            this.edit_qform= {
              qid: res.data.data.new_qid,
              name: '',
              type: 0,
              content: '',
              answer: '',
            };
            this.drawerVisible = true;
          } else {
            this.$message.error(res.data.meta.message);
          }
        });
      }
    },
    applychange() {
      if (this.edit_qform.name === '') {
        this.$message.error("题目名称不得为空")
      } else if (this.edit_qform.content === '') {
        this.$message.error("题目内容不得为空")
      } else if (this.edit_qform.answer === '') {
        this.$message.error("题目答案不得为空")
      } else {
        if (this.drawerMode === 1) {

        } else if (this.drawerMode === 2) {
          this.$request.post("/codez/admin/questions/create/", {
            qid: this.edit_qform.qid,
            name: this.edit_qform.name,
            type: this.edit_qform.type,
            content: this.edit_qform.content,
            answer: this.edit_qform.answer,
          }).then(res => {
            if (res.data.meta.status === 200) {
              this.$message.success("成功新增题目, 题目ID为：" + String(this.edit_qform.qid));
              this.drawerVisible = false;
            } else {
              this.$message.error(res.data.meta.message);
            }
          });
        }
      }
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
