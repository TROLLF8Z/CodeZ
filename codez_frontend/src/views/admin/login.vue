<template>
  <div class="login-container" >
      <el-card class="box-card">
            <div class="login-body">
                <el-text class="login-title" size="large">CodeZ 管理员登录</el-text>
                <el-form ref="form" :model="userForm">
                    <el-input placeholder="请输入管理员ID..." v-model="userForm.adminID" class="login-input" @keyup.enter.native="admin_login">
                    </el-input>

                    <el-input placeholder="请输入密码..." v-model="userForm.adminPassword" class="login-input" @keyup.enter.native="admin_login" show-password>
                    </el-input>

                    <div class="login-submit" >
                        <el-button type="success" @click="admin_login" :disabled="this.loggin">登录</el-button>
                    </div>
                </el-form>
            </div>
      </el-card>
  </div>
</template>

<script>
  export default {
      data() {
          return {
              userForm: {
                  adminID: '',
                  adminPassword: '',
              },
              loggin: false,
          };
      },

      methods: {
          admin_login() {
              this.loggin = true;
              if (this.userForm.adminID === "" || this.userForm.adminPassword === "") {
                this.$message.error("管理员ID或密码不得为空")
                this.loggin = false;
              } else {
                this.$request.post("/codez/login_admin/", {
                  aid: this.userForm.adminID,
                  password: this.userForm.adminPassword,
                }).then(res => {
                  if (res.data.meta.status === 200) {
                    localStorage.setItem("aid", res.data.data.adminid);
                    localStorage.setItem("token", res.data.data.token);
                    localStorage.setItem("name", res.data.data.adminname);
                    this.$message.success("登录成功")
                    setTimeout(()=>{this.$router.push('/admin')}, 1000)
                  } else {
                    this.loggin = false;
                    this.$message.error(res.data.meta.message);
                  }
                });
              }
          }
      }
  }
</script>

<style scoped>
  .login-container {
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
      width: 100%;
      background-image: url("bg.png");
      background-repeat: no-repeat;
      background-size: cover;
  }

  .login-body {
      padding: 30px;
      width: 300px;
      height: 100%;
  }

  .login-title {
      padding-bottom: 30px;
      display: flex;
      justify-content: center;
      text-align: center;
      font-weight: 600;
      font-size: 30px;
      color: #409EFF;
  }

  .login-input {
      margin-bottom: 20px;
  }

  .login-submit {
      margin-top: 20px;
      display: flex;
      justify-content: center;
  }

  .login-thirdpartydiv {
    margin-top: 20px;
    display: flex;
    justify-content: center;
  }

  .login-thirdpartytext {
    display: flex;
    justify-content: center;
    text-align: center;
    font-size: 10px;
    color: #4e4e52;
  }

  .sign-in-container {
      padding: 0 10px;
  }

  .sign-in-text {
      color: #409EFF;
      font-size: 16px;
      text-decoration: none;
      line-height:28px;
  }
  .other-submit{
      display:flex;
      justify-content: space-between;
      margin-top: 30px;
      margin-left: 200px;
  }
</style>
