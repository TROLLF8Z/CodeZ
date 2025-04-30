<template>
  <el-text style="font-size: 20px; color: #409EFF; font-weight: 500;">根据UID或昵称搜索用户</el-text>
  <el-form :model="userform" label-width="120px" style="margin-top: 30px;" label-position="right" :inline="true">
    <el-form-item label="用户UID">
      <el-input placeholder="请输入用户UID..." v-model="userform.userId" @keyup.enter.native="search_user" />
    </el-form-item>
    <el-form-item label="用户昵称">
      <el-input placeholder="请输入用户昵称..." v-model="userform.userName" @keyup.enter.native="search_user" />
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="search_user" :disabled="searching">搜索用户</el-button>
    </el-form-item>
  </el-form>
  <el-divider />

  <el-table :data="this.resultform" stripe border>
    <el-table-column label="用户ID" prop="uid">
      <template #default="scope">
        <div style="display: flex; align-items: center"><el-text style="font-size: 16px; color: #000000; font-weight: 400;">{{ scope.row.uid }}</el-text></div>
      </template>
    </el-table-column>

    <el-table-column label="用户昵称" prop="name">
      <template #default="scope">
        <div style="display: flex; align-items: center"><el-text style="font-size: 16px; color: #000000; font-weight: 400;">{{ scope.row.name }}</el-text></div>
      </template>
    </el-table-column>

    <el-table-column label="操作">
      <template #default="scope">
        <el-button size="small" type="primary" autocomplete="off" @click="edit_user(scope.$index, scope.row)">编辑</el-button>
        <el-button size="small" type="danger" autocomplete="off" @click="" style="margin-left: 20px">删除</el-button>
      </template>
    </el-table-column>
  </el-table>

  <el-drawer :model-value="this.drawerVisible" title="编辑用户信息" :before-close="drawerclose">

  </el-drawer>
</template>

<script>
export default {
  data() {
    return {
      userform: {
        userId: '',
        userName: '',
      },
      searching: false,
      resultform: [],
      drawerVisible: false,

      edit_userform: {
        uid: 0,
        password: "",
        phonenumber: "",
        thirdpartyauth: "",
        displayname: "",
        age: 0,
        gender: 0,
        zcoins: 0,
        avatar: "",
        description: "",
        school: "",
        corrects: 0,
        finishes: 0,
        medals: "",
        displaymedals: "",
        unlockedbanks: "",
      }

    };
  },

  methods: {
    search_user() {
      this.searching = true;
      if (this.userform.userId === "" && this.userform.userName === "") {
        this.$message.error("请至少输入一个查询条件")
        this.searching = false;
      } else {
        this.$request.post("/codez/admin/search_user/", {
          uid: this.userform.userId,
          displayname: this.userform.userName,
        }).then(res => {
          if (res.data.meta.status === 200) {
            this.resultform= [];
            let user = {};
            for (user of res.data.data.search_results) {
              this.resultform.push({
                "uid": user.uid,
                "name": user.username,
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

    edit_user(index, row) {
      this.$request.post("/codez/admin/user_info/", {
        uid: row.uid,
      }).then(res => {
        if (res.data.meta.status === 200) {
          this.edit_userform.uid = res.data.data.uid;
          this.edit_userform.name = res.data.data.displayname;
          this.edit_userform.age = res.data.data.age;
          this.edit_userform.gender = res.data.data.gender;
          this.edit_userform.zcoins = res.data.data.zcoins;
          this.edit_userform.password = res.data.data.password;
          this.edit_userform.school = res.data.data.school;
          this.edit_userform.phonenumber = res.data.data.phonenumber;
          this.edit_userform.thirdpartyauth = res.data.data.thirdpartyauth;
          this.edit_userform.avatar = res.data.data.avatar;
          this.edit_userform.description = res.data.data.description;
          this.edit_userform.medals = res.data.data.medals;
          this.edit_userform.displaymedals = res.data.data.displaymedals;
          this.edit_userform.unlockedbanks = res.data.data.unlockedbanks;
          this.drawerVisible = true;
        } else {
          this.searching= false;
          this.$message.error(res.data.meta.message);
        }
      })
    },
    drawerclose() {
      this.drawerVisible = false;
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
