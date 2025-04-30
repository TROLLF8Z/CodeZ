<template>
  <div class="login-container" >
      <el-card v-show="!this.pushin" class="box-card">
            <div class="login-body">
                <el-text class="login-title" size="large">欢迎回到CodeZ</el-text>
                <el-form ref="form" :model="userForm">
                    <el-input placeholder="请输入手机号..." v-model="userForm.accountNumber" class="login-input" @keyup.enter.native="login">
                    </el-input>

                    <el-input placeholder="请输入密码..." v-model="userForm.userPassword" v-if="!this.via_sms" class="login-input" @keyup.enter.native="login" show-password>
                    </el-input>

                    <div v-if="this.via_sms" style="display: flex;justify-content: space-between;">
                      <el-input placeholder="请输入短信验证码..." v-model="userForm.smsCode" class="login-input" />
                      <el-button type="primary" @click="sendsms" v-if="!this.sms_sent">获取验证码</el-button>
                      <el-button type="info" v-if="this.sms_sent" disabled><span>{{ cd_sec }}秒</span></el-button>
                    </div>

                  <el-text class="login-thirdpartytext" >通过第三方登录</el-text>
                  <div class="login-thirdpartydiv">
                    <img style="width: 40px; height: 40px" src="@/views/login/wechat.png" :onclick="wechat_auth">
                  </div>

                    <div class="login-submit" >
                        <el-button type="success" @click="login" :disabled="this.loggin">登录</el-button>
                        <el-button type="warning" autocomplete="off" @click="this.via_sms=true" style="margin-left: 20px" :disabled="this.loggin" v-if="!this.via_sms">使用短信验证码登录</el-button>
                        <el-button type="warning" autocomplete="off" @click="this.via_sms=false" style="margin-left: 20px" :disabled="this.loggin" v-if="this.via_sms">使用密码登录</el-button>
                        <el-button type="primary" autocomplete="off" @click="$router.push('/register')" style="margin-left: 20px" :disabled="this.loggin">注册</el-button>
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
                  accountNumber: '',
                  userPassword: '',
                  smsCode: '',
              },
              loggin: false,
              via_sms: false,
              sms_sent: false,
              cd_sec: 0,
              pushin: false,
          };
      },

      methods: {
          login() {
              this.loggin = true;
              if (this.via_sms) {
                if (this.userForm.accountNumber === "" || this.userForm.smsCode === "") {
                  this.$message.error("手机号码或验证码不得为空")
                  this.loggin = false;
                }
              } else {
                if (this.userForm.accountNumber === "" || this.userForm.userPassword === "") {
                  this.$message.error("手机号码或密码不得为空")
                  this.loggin = false;
                } else {
                  this.$request.post("/codez/login_pwd/", {
                    phonenumber: this.userForm.accountNumber,
                    password: this.userForm.userPassword,
                  }).then(res => {
                    if (res.data.meta.status === 200) {
                      localStorage.setItem("uid", res.data.data.userid);
                      localStorage.setItem("token", res.data.data.token);
                      localStorage.setItem("avatar", res.data.data.avatar);
                      localStorage.setItem("displayname", res.data.data.displayname);
                      localStorage.setItem("zcoins", res.data.data.zcoins);
                      this.$message.success("登录成功")
                      setTimeout(()=>{this.$router.push('/main')}, 1000)
                    } else {
                      this.loggin = false;
                      this.$message.error(res.data.meta.message);
                    }
                  });
                }
              }
          },
          wechat_auth() {
            if (this.loggin === false) {
              this.$message("跳转微信")
            }
          },
          countdownTimer() {
            if (this.cd_sec > -1) {
              setTimeout(() => {
                this.cd_sec--;
                this.countdownTimer();
              }, 1000)
            } else {
              this.sms_sent = false;
            }
          },
          sendsms() {
            this.sms_sent = true;
            this.cd_sec = 60;
            this.countdownTimer();
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
