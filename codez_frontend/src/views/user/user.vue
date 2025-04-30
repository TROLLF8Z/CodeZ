<template>
  <el-container>
    <el-header>
      <div style="display:flex; justify-content: center; align-items: center;">
        <el-image style="width: 40px; height: 40px; margin-right: 10px;" src="src/assets/codez.png" @click="$router.push('/main')"/>
        <el-text style="font-size: 30px; color: #409EFF; font-weight: 1000;">CodeZ</el-text>
      </div>

      <div style="display:flex; justify-content: center; align-items: center; margin: auto">
        <el-text style="font-size: 30px; font-weight: 600;">个人中心</el-text>
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
          <div style="width: 1000px"><el-image style="width: 120px; height: 120px;" :src="this.vavatar" /></div>
          <div style="margin-top: 10px; margin-left: 17px;">
            <el-button type="default" @click="this.dialogMode = 1;this.dialogTitle = '更换头像';this.dialogVisible = true" v-if="isOperator">更换头像</el-button>
          </div>
          <div style="margin-top: 20px; display: flex; align-items: center;">
            <el-text style="font-size: 20px; font-weight: 600; color:#000000 ">{{ vdisplayname }}</el-text>
            <el-text style="margin-left: 10px; font-size: 10px; font-weight: 300; color:#4e4e52 ">UID: {{ vuid }}</el-text>
            <el-image style="margin-left: 30px; width: 24px; height: 24px;" src="src/assets/zcoin.png" v-if="!isOperator"/>
            <span style="padding-left: 20px; padding-right: 20px; color:#DAA836;" v-if="!isOperator">{{ displayzcoin }}</span>
          </div>
          <div style="margin-top: 10px; margin-left: 17px;">
            <el-button type="default" @click="this.dialogMode = 2;this.dialogTitle = '更换名称';this.changeName = this.displayname;this.dialogVisible = true" v-if="isOperator">更换名称</el-button>
          </div>
          <div style="margin-top: 20px">
            <el-card shadow="hover">
              <el-text class='w-500px mb-2' style="font-size: 16px; font-weight: 600; color:#333333 " truncated>个人简介：{{ description }}</el-text>
            </el-card>
          </div>
          <div style="margin-top: 10px; margin-left: 17px;">
            <el-button type="default" @click="this.dialogMode = 3;this.dialogTitle = '更改简介';this.changeDesc = this.description;this.dialogVisible = true" v-if="isOperator">更改简介</el-button>
          </div>

          <div style="margin-top: 20px; display: block">
            <el-card shadow="hover">
              <el-text class='w-500px mb-2' style="font-size: 16px; font-weight: 600; color:#333333; margin-bottom: 10px;" truncated>性别：{{ genders[gender] }}</el-text><br />
              <el-text class='w-500px mb-2' style="font-size: 16px; font-weight: 600; color:#333333; margin-bottom: 10px;" truncated>年龄：{{ age }}</el-text><br />
              <el-text class='w-500px mb-2' style="font-size: 16px; font-weight: 600; color:#333333" truncated>就读院校：{{ school }}</el-text>
            </el-card>
          </div>
          <div style="margin-top: 10px; margin-left: 17px;">
            <el-button
                type="default"
                @click="this.dialogMode = 4;this.dialogTitle = '更改信息';this.changeInfo.changeAge = this.age;this.changeInfo.changeGender = this.gender; this.changeInfo.changeSchool = this.school;this.dialogVisible = true"
                v-if="isOperator">
              更改信息
            </el-button>
          </div>

          <div style="margin-top: 20px; display: block">
            <el-card shadow="hover">
              <el-text class='w-500px mb-2' style="font-size: 16px; font-weight: 600; color:#333333; margin-bottom: 10px;" truncated>答对题目数：{{ corrects }}</el-text><br />
              <el-text class='w-500px mb-2' style="font-size: 16px; font-weight: 600; color:#333333;" truncated>完成题库数：{{ finishes }}</el-text><br />
            </el-card>
          </div>
        </el-card>

        <el-dialog style="width: 500px" v-model="this.dialogVisible" :title="this.dialogTitle">
          <div style="display: flex; justify-content: center; align-items: center" v-if="this.dialogMode===1">
            <el-upload
                class="avatar-uploader"
                action="http://localhost:8000/codez/avatar/upload"
                :data="this.uploadobj"
                :on-success="uploadedimg"
                :before-upload="precheckimg"
                :show-file-list="false"
            >
              <el-image style="width: 200px; height: 200px;" :src="this.avatar" class="avatar" />
            </el-upload>
          </div>
          <div style="margin-top: 10px; display: flex; justify-content: center; align-items: center"><el-text style="font-size: 15px; font-weight: 400; color:#000000 " v-if="this.dialogMode===1">点击更换头像</el-text></div>

          <div style="display: flex; justify-content: center; align-items: center" v-if="this.dialogMode===2"><el-input v-model="changeName" style="text-align: center"></el-input></div>
          <div style="display: flex; justify-content: center; align-items: center" v-if="this.dialogMode===2">
            <el-button type="primary" @click="changename" style="margin-top: 20px" >确认更改</el-button>
          </div>

          <div style="display: flex; justify-content: center; align-items: center" v-if="this.dialogMode===3">
            <el-input v-model="changeDesc" type="textarea" :rows="10"></el-input>
          </div>
          <div style="display: flex; justify-content: center; align-items: center" v-if="this.dialogMode===3">
            <el-button type="primary" @click="changedescription" style="margin-top: 20px" >确认更改</el-button>
          </div>

          <div style="display: flex; justify-content: center; align-items: center" v-if="this.dialogMode===4">
            <el-form :model="changeInfo" label-width="120px">
              <el-form-item label="性别：">
                <el-select
                    v-model="changeInfo.changeGender"
                    placeholder="Select"
                    size="large"
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
              <el-form-item label="年龄：">
                <el-input v-model="changeInfo.changeAge" style="text-align: center"></el-input>
              </el-form-item>
              <el-form-item label="就读院校：">
                <el-input v-model="changeInfo.changeSchool" style="text-align: center"></el-input>
              </el-form-item>
            </el-form>
          </div>
          <div style="display: flex; justify-content: center; align-items: center" v-if="this.dialogMode===4">
            <el-button type="primary" @click="changeinfo" style="margin-top: 20px" >确认更改</el-button>
          </div>
        </el-dialog>
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
      description: "",
      avatar: "",
      vavatar: "",
      zcoin: 0,
      uid: 0,
      vuid: 0,
      vdisplayname: '',
      age: 0,
      gender: 0,
      school: "",
      corrects: 0,
      finishes: 0,
      medals: "",
      displaymedals: "",
      displayzcoin: 0,
      dialogVisible: false,
      dialogMode: -1,
      dialogTitle: "",
      uploadobj: {},
      isOperator: false,

      changeName: "",
      changeDesc: "",
      changeInfo: {
        changeAge: 0,
        changeGender: 0,
        changeSchool: "",
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
      genders: ['保密', '男', '女', '非二元'],
    }
  },
  mounted() {
    this.vuid = this.$route.query.uid;
    this.uid = localStorage.getItem('uid');
    this.displayname = localStorage.getItem("displayname");
    this.avatar = localStorage.getItem("avatar");
    this.zcoin = localStorage.getItem("zcoins");
    if (this.avatar === '' || !this.avatar) {
      this.avatar = 'src/assets/avatar/defaultavatar.png';
    };
    if (this.vuid === localStorage.getItem('uid')) {
      this.isOperator = true;
      this.vdisplayname = this.displayname;
      this.vavatar = this.avatar;
    } else {
      this.isOperator = false;
    }
    this.uploadobj = {
      uid: this.uid,
    };
    this.$request.post('/codez/user/profile', {userid: this.vuid}).then(res => {
      if (res.data.meta.status === 200) {
        this.vavatar = res.data.data.avatar;
        this.vdisplayname = res.data.data.displayname;
        this.displayzcoin = res.data.data.zcoins
        this.description = res.data.data.description;
        this.school = res.data.data.school;
        this.gender = res.data.data.gender;
        this.medals = res.data.data.medals;
        this.age = res.data.data.age;
        this.corrects = res.data.data.corrects;
        this.finishes = res.data.data.finishes;
        this.displaymedals = res.data.data.displaymedals;
        if (this.vavatar === '' || !this.vavatar) {
          this.vavatar = 'src/assets/avatar/defaultavatar.png'
        }
      } else {
        this.$message.error(res.data.meta.message);
        this.$router.push('/main');
      }
      if (this.age === -1) {
        this.age = '保密';
      }
      if (this.school === '') {
        this.school = '保密';
      }
    })
  },
  methods: {
    quitLogin() {
      localStorage.clear()
      this.$router.push('/login')
      this.$message.success('退出成功')
    },
    uploadedimg(response, file) {
      this.avatar = URL.createObjectURL(file.raw);
      this.vavatar = this.avatar;
      localStorage.setItem("avatar", this.avatar);
    },
    precheckimg(file) {
      if (file.type !== 'image/jpeg' && file.type !== 'image/png' && file.type !== 'image/bmp') {
        this.$message.error("图片格式不受支持，支持的格式为JPG，BMP，PNG")
        return false
      } else if (file.size / 1024 / 1024 > 5) {
        this.$message.error("图片文件大小不可超过5MB")
        return false
      } else {
        return true
      }
    },
    changename() {
      if (this.changeName === '') {
        this.$message.error("用户名称不得为空")
      } else if (this.changeName === this.displayname) {
        this.$message.error("用户名称不得与原来相同")
      } else {
        this.$request.post('/codez/user/change/displayname', {
          userid: this.uid,
          displayname: this.changeName,
        }).then(res => {
          if (res.data.meta.status === 200) {
            this.displayname = this.changeName;
            this.vdisplayname = this.changeName;
            localStorage.setItem("displayname", this.changeName);
            this.$message.success("更改成功")
            this.dialogVisible = false;
          } else {
            this.$message.error(res.data.meta.message);
          }
        })
      }
    },
    changedescription() {
      if (this.changeDesc === this.description) {
        this.$message.error("简介不得与原来相同")
      } else {
        this.$request.post('/codez/user/change/description', {
          userid: this.uid,
          description: this.changeDesc,
        }).then(res => {
          if (res.data.meta.status === 200) {
            this.description = this.changeDesc;
            this.$message.success("更改成功")
            this.dialogVisible = false;
          } else {
            this.$message.error(res.data.meta.message);
          }
        })
      }
    },
    changeinfo() {
      if (this.changeInfo.changeAge === this.age && this.changeInfo.changeSchool === this.school && this.changeInfo.changeGender === this.gender) {
        this.$message.error("信息不得与原来相同")
      } else {
        if (this.changeInfo.changeAge === '保密'){
          this.changeInfo.changeAge = -1
        }
        if (this.changeInfo.changeSchool === '保密') {
          this.changeInfo.changeSchool = ''
        }
        this.$request.post('/codez/user/change/info', {
          userid: this.uid,
          school: this.changeInfo.changeSchool,
          age: this.changeInfo.changeAge,
          gender: this.changeInfo.changeGender,
        }).then(res => {
          if (res.data.meta.status === 200) {
            this.age = this.changeInfo.changeAge;
            this.gender = this.changeInfo.changeGender;
            this.school = this.changeInfo.changeSchool;
            if (this.age === -1) {
              this.age = '保密';
            }
            if (this.school === '') {
              this.school = '保密';
            }
            this.$message.success("更改成功")
            this.dialogVisible = false;
          } else {
            this.$message.error(res.data.meta.message);
          }
        })
      }
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
