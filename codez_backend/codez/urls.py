from django.urls import path,re_path
from . import views

urlpatterns = [
    # 登录接口
    path('login_pwd/', views.Login_Pwd_View.as_view()),
    path('login_sms/', views.Login_Sms_View.as_view()),

    # 注册接口
    path('reg_phone/', views.Registry_Phone_View.as_view()),

    # 头像上传接口
    path('avatar/upload', views.Avatar_Upload_View.as_view()),

    # 用户功能信息获取接口
    path('user/profile', views.User_Profile_View.as_view()),

    # 用户信息更改接口
    path('user/change/displayname', views.User_Change_Name_View.as_view()),
    path('user/change/description', views.User_Change_Desc_View.as_view()),
    path('user/change/info', views.User_Change_Info_View.as_view()),

    # 管理员登录接口
    path('login_admin/', views.Login_Admin_View.as_view()),

    # 管理员搜寻用户接口
    path('admin/search_user/', views.Admin_Search_User_View.as_view()),

    # 管理员获取用户所有信息接口
    path('admin/user_info/', views.Admin_User_Info_View.as_view()),
]