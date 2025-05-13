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

    # 获取用户与题库关系接口
    path('user/bank/status/', views.User_Bank_Status_View.as_view()),

    # 获取用户与题目关系接口
    path('user/question/status/', views.User_Question_Status_View.as_view()),

    # 用户购买题库接口
    path('user/bank/purchase/', views.User_Bank_Purchase_View.as_view()),

    # 获取用户作答题目内容接口
    path('exam/current_question/', views.User_Current_Question_View.as_view()),

    # 用户作答用时记录接口
    path('exam/record_time/', views.User_Time_Record_View.as_view()),

    # 用户提交答案获取评分接口
    path('exam/submit/', views.User_Exam_Submit_View.as_view()),

    # 获取题目评论接口
    path('comment/info/', views.Question_Comment_View.as_view()),

    # 提交评论接口
    path('comment/submit/', views.Comment_Submit_View.as_view()),

    # 删除评论接口
    path('comment/delete/', views.Comment_Delete_View.as_view()),

    # 首页获取题库列表接口
    path('banklist/', views.Bank_List_View.as_view()),

    # 搜索题库接口
    path('search/bank/', views.Search_Bank_View.as_view()),

    # 搜索用户接口
    path('search/user/', views.Search_User_View.as_view()),

    # 管理员登录接口
    path('login_admin/', views.Login_Admin_View.as_view()),

    # 管理员搜寻用户接口
    path('admin/user/search/', views.Admin_Search_User_View.as_view()),

    # 管理员获取用户所有信息接口
    path('admin/user/info/', views.Admin_User_Info_View.as_view()),

    # 管理员获取可用的新UID接口
    path('admin/user/available_id/', views.Admin_Available_ID_View.as_view()),

    # 管理员修改用户所有信息接口
    path('admin/user/change/', views.Admin_User_Change_View.as_view()),

    # 管理员获取可用的新题目ID接口
    path('admin/questions/available_id/', views.Admin_Question_ID_View.as_view()),

    # 管理员新增题目接口
    path('admin/questions/create/', views.Admin_Question_Create_View.as_view()),

    # 管理员获取题目内容接口
    path('admin/questions/info/', views.Admin_Question_Info_View.as_view()),

    # 管理员搜寻题目接口
    path('admin/questions/search/', views.Admin_Search_Question_View.as_view()),

    # 管理员修改题目内容接口
    path('admin/questions/change/', views.Admin_Question_Change_View.as_view()),

    # 管理员搜寻题库接口
    path('admin/banks/search/', views.Admin_Search_Bank_View.as_view()),

    # 管理员获取可用的新题库ID接口
    path('admin/banks/available_id/', views.Admin_Bank_ID_View.as_view()),

    # 管理员新增题库接口
    path('admin/banks/create/', views.Admin_Bank_Create_View.as_view()),

    # 管理员获取题库包含题目列表接口
    path('admin/banks/questions/', views.Admin_Bank_Questions_View.as_view()),

    # 管理员获取题库内容列表接口
    path('admin/banks/info/', views.Admin_Bank_Info_View.as_view()),

    # 管理员修改题库内容接口
    path('admin/banks/change/', views.Admin_Bank_Change_View.as_view()),
]