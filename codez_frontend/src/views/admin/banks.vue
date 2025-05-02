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

  <el-drawer :model-value="this.drawerVisible" :with-header="false" :before-close="drawerclose">
    <div style="display: flex; align-items: center">
      <el-text style="font-size: 20px; color: #333333; font-weight: 500;">编辑题库内容</el-text>
      <el-button type="danger" autocomplete="off" @click="drawerclose" style="margin-left: auto"><el-icon class="el-icon--left"><CircleCloseFilled /></el-icon>关闭</el-button>
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
      bankform: {
        bankId: '',
        bankName: '',
      },
      searching: false,
      resultform: [],
      drawerVisible: false,
      drawerMode: -1,

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
    drawerclose() {
      this.drawerVisible = false;
    },
    edit_bank(index, row, mode) {
      this.drawerMode = mode;
      if (mode === 1) {
        this.$request.post("/codez/admin/banks/info/", {
          qid: row.qid,
        }).then(res => {
          if (res.data.meta.status === 200) {
            this.edit_qform= {
              qid: res.data.data.qid,
              name: "",
              description: "",
              status: 0,
              price: 0,
              questions: [],
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
          this.$request.post("/codez/admin/banks/change/", {
            qid: this.edit_qform.qid,
            name: this.edit_qform.name,
            type: this.edit_qform.type,
            content: this.edit_qform.content,
            answer: this.edit_qform.answer,
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
