<template>
  <div class="reg-container" >
      <el-card class="box-card">
          <div class="reg-body">
              <el-text class="reg-title" size="large">加入CodeZ</el-text>
              <el-form ref="form" :model="userForm">
                  <el-input placeholder="请输入手机号..." v-model="userForm.accountNumber" class="reg-input">
                  </el-input>

                  <el-input placeholder="请输入密码..." v-model="userForm.userPassword" class="reg-input" show-password>
                  </el-input>

                <el-input placeholder="请再次输入密码..." v-model="userForm.confirmPassword" class="reg-input" show-password>
                </el-input>

                <div style="display: flex;justify-content: space-between;margin-bottom: 30px">
                  <el-input placeholder="请输入短信验证码..." v-model="userForm.smsCode" class="login-input" />
                  <el-button type="primary" @click="sendsms" v-if="!this.sms_sent">获取验证码</el-button>
                  <el-button type="info" v-if="this.sms_sent" disabled><span>{{ cd_sec }}秒</span></el-button>
                </div>

                <el-text class="reg-thirdpartytext" >使用第三方注册</el-text>
                <div class="reg-thirdpartydiv">
                  <img style="width: 40px; height: 40px" src="@/views/login/wechat.png" :onclick="wechat_auth">
                </div>

                  <div class="reg-submit" >
                      <el-button type="success" @click="register" :disabled="this.reggin">注册</el-button>
                      <el-button type="primary" autocomplete="off" @click="$router.push('/login')" style="margin-left: 20px" :disabled="this.reggin">返回登录</el-button>
                  </div>
              </el-form>
          </div>
      </el-card>
  </div>
</template>

<script>
  export default {
      name: "register",
      data() {
          return {
              userForm: {
                  accountNumber: '',
                  userPassword: '',
                  confirmPassword: '',
                  smsCode: '',
              },
              reggin: false,
              sms_sent: false,
              cd_sec: 0,
          };
      },

      methods: {
          register() {
            if (this.userForm.userPassword !== this.userForm.confirmPassword) {
              this.$message.error("两次输入的密码不一致")
            } else if (this.userForm.accountNumber === "" || this.userForm.userPassword === "") {
              this.$message.error("手机号码或密码不得为空")
            } else if (this.userForm.accountNumber.length !== 11) {
              this.$message.error("手机号码格式不正确")
            } else if (this.userForm.smsCode === "") {
              this.$message.error("短信验证码不得为空")
            } else {
                this.reggin = true;
                this.$request.post("/codez/reg_phone/", {
                  phonenumber: this.userForm.accountNumber,
                  password: this.userForm.userPassword,
                }).then(res => {
                  console.log(res);
                  if (res.data.meta.status === 200) {
                    this.$message.success("注册成功")
                    setTimeout(()=>{this.$router.push('/login')}, 1000)
                  } else {
                    this.reggin = false;
                    this.$message.error(res.data.meta.message);
                  }
                });
            }
          },
          wechat_auth() {
            this.$message("跳转微信")
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
  .reg-container {
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
      width: 100%;
      background-image: url("bg.png");
      background-repeat: no-repeat;
      background-size: cover;
  }

  .reg-body {
      padding: 30px;
      width: 300px;
      height: 100%;
  }

  .reg-title {
      padding-bottom: 30px;
      display: flex;
      justify-content: center;
      text-align: center;
      font-weight: 600;
      font-size: 30px;
      color: #409EFF;
  }

  .reg-input {
      margin-bottom: 20px;
  }

  .reg-submit {
      margin-top: 20px;
      display: flex;
      justify-content: center;
  }

  .reg-thirdpartydiv {
    margin-top: 20px;
    display: flex;
    justify-content: center;
  }

  .reg-thirdpartytext {
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
