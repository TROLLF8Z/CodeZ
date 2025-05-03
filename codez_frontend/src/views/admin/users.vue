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
    <el-form-item>
      <el-button type="success" @click="edit_user(0, 0, 2)" :disabled="searching">新增用户</el-button>
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
        <el-button size="small" type="primary" autocomplete="off" @click="edit_user(scope.$index, scope.row, 1)">编辑</el-button>
        <el-button size="small" type="danger" autocomplete="off" @click="" style="margin-left: 20px">删除</el-button>
      </template>
    </el-table-column>
  </el-table>

  <el-drawer :model-value="this.drawerVisible" :with-header="false" :before-close="drawerclose" size="50%">
    <div style="display: flex; align-items: center">
      <el-text style="font-size: 20px; color: #333333; font-weight: 500;">编辑用户信息</el-text>
      <el-button type="danger" autocomplete="off" @click="drawerclose" style="margin-left: auto"><el-icon class="el-icon--left"><CircleCloseFilled /></el-icon>关闭</el-button>
    </div>
    <el-divider />
    <el-form :model="this.edit_userform" label-width="120px" label-position="right">
      <el-text style="font-size: 16px; color: #000000; font-weight: 400; margin-bottom: 30px;">用户ID：{{ this.edit_userform.uid }}</el-text>
      <el-form-item label="用户昵称" style="margin-top: 20px;">
        <el-input placeholder="请输入用户昵称..." v-model="edit_userform.displayname" />
      </el-form-item>
      <el-form-item label="用户密码" style="margin-top: 20px;">
        <el-input placeholder="请输入用户密码..." v-model="edit_userform.password" show-password />
      </el-form-item>
      <el-form-item label="用户手机号码" style="margin-top: 20px;">
        <el-input placeholder="请输入用户手机号码..." v-model="edit_userform.phonenumber" />
      </el-form-item>
      <el-form-item label="第三方授权信息" style="margin-top: 20px;">
        <el-input placeholder="请输入第三方授权信息.." v-model="edit_userform.thirdpartyauth" />
      </el-form-item>
      <el-form-item label="用户ZCoins数量" style="margin-top: 20px;">
        <el-input placeholder="请输入用户ZCoins数量..." v-model="edit_userform.zcoins" />
      </el-form-item>
      <el-form-item label="用户年龄" style="margin-top: 20px;">
        <el-input placeholder="请输入用户年龄..." v-model="edit_userform.age" />
      </el-form-item>
      <el-form-item label="用户性别" style="margin-top: 20px;">
        <el-select
            v-model="edit_userform.gender"
            placeholder="选择性别"
            style="width: 120px"
        >
          <el-option
              v-for="item in genderSelect"
              :key="item.value"
              :label="item.label"
              :value="item.value"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="用户简介" style="margin-top: 20px;">
        <el-input placeholder="请输入用户简介..." v-model="edit_userform.description" />
      </el-form-item>
      <el-form-item label="用户就读院校" style="margin-top: 20px;">
        <el-input placeholder="请输入用户就读院校" v-model="edit_userform.school" />
      </el-form-item>
      <el-form-item label="答对题目数" style="margin-top: 20px;">
        <el-input placeholder="请输入答对题目数..." v-model="edit_userform.corrects" />
      </el-form-item>
      <el-form-item label="完成题库数" style="margin-top: 20px;">
        <el-input placeholder="请输入完成题库数..." v-model="edit_userform.finishes" />
      </el-form-item>
      <el-form-item label="用户奖牌" style="margin-top: 20px;">
        <el-input placeholder="请输入用户奖牌..." v-model="edit_userform.medals" />
      </el-form-item>
      <el-form-item label="用户已解锁题库" style="margin-top: 20px;">
        <el-input placeholder="请输入用户已解锁题库..." v-model="edit_userform.unlockedbanks" />
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
      userform: {
        userId: '',
        userName: '',
      },
      searching: false,
      resultform: [],
      drawerVisible: false,
      drawerMode: -1,

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
      },

      genderSelect: [
        {
          value: "0",
          label: "保密",
        },
        {
          value: "1",
          label: "男",
        },
        {
          value: "2",
          label: "女",
        },
        {
          value: "3",
          label: "非二元",
        }
      ],

    };
  },

  methods: {
    search_user() {
      this.searching = true;
      if (this.userform.userId === "" && this.userform.userName === "") {
        this.$message.error("请至少输入一个查询条件")
        this.searching = false;
      } else {
        this.$request.post("/codez/admin/user/search/", {
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

    edit_user(index, row, mode) {
      this.drawerMode = mode;
      if (mode === 1) {
        this.$request.post("/codez/admin/user/info/", {
          uid: row.uid,
        }).then(res => {
          if (res.data.meta.status === 200) {
            this.edit_userform.uid = res.data.data.uid;
            this.edit_userform.displayname = res.data.data.displayname;
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
            this.$message.error(res.data.meta.message);
          }
        })
      } else if (mode === 2) {
        this.$request.post("/codez/admin/user/available_id/", {
          mode: "newuser"
        }).then(res => {
          if (res.data.meta.status === 200) {
            this.edit_userform = {
              uid: res.data.data.new_uid,
              password: "",
              phonenumber: "",
              thirdpartyauth: "",
              displayname: "CodeZ用户" + res.data.data.new_uid,
              age: -1,
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
            this.drawerVisible = true;
          } else {
            this.$message.error(res.data.meta.message);
          }
        })
      }
    },
    drawerclose() {
      this.drawerVisible = false;
    },
    applychange() {
      if (this.drawerMode === 1) {
        if (this.edit_userform.displayname === "") {
          this.$message.error("用户昵称不得为空")
        } else if (this.edit_userform.password === "") {
          this.$message.error("用户密码不得为空")
        } else if (this.edit_userform.phonenumber === "") {
          this.$message.error("用户手机号码不得为空")
        } else if (!Number.isInteger(Number(this.edit_userform.phonenumber)) || String(this.edit_userform.phonenumber).length !== 11) {
          this.$message.error("用户手机号码格式不正确")
        } else if (!Number.isInteger(Number(this.edit_userform.zcoins)) || this.edit_userform.zcoins < 0) {
          this.$message.error("用户ZCoins数量不正确")
        } else if (!Number.isInteger(Number(this.edit_userform.age)) || this.edit_userform.age < -1) {
          this.$message.error("用户年龄不正确")
        } else if (!Number.isInteger(Number(this.edit_userform.corrects)) || this.edit_userform.corrects < 0) {
          this.$message.error("用户答对题目数不正确")
        } else if (!Number.isInteger(Number(this.edit_userform.finishes)) || this.edit_userform.finishes < 0) {
          this.$message.error("用户完成题库数不正确")
        } else {
          this.$request.post("/codez/admin/user/change/", {
            uid: this.edit_userform.uid,
            password: this.edit_userform.password,
            phonenumber: this.edit_userform.phonenumber,
            thirdpartyauth: this.edit_userform.thirdpartyauth,
            displayname: this.edit_userform.displayname,
            zcoins: this.edit_userform.zcoins,
            age: this.edit_userform.age,
            gender: this.edit_userform.gender,
            description: this.edit_userform.description,
            school: this.edit_userform.school,
            corrects: this.edit_userform.corrects,
            finishes: this.edit_userform.finishes,
            medals: this.edit_userform.medals,
            unlockedbanks: this.edit_userform.unlockedbanks,
          }).then(res => {
            if (res.data.meta.status === 200) {
              this.$message.success("修改成功")
              this.drawerVisible = false;
            } else {
              this.$message.error(res.data.meta.message);
            }
          })
        }
      } else if (this.drawerMode === 2) {

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
