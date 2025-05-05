from .TokenAuthtication import TokenAuthtication
from rest_framework.response import Response
from django.core.paginator import Paginator
from django.db.models import Q
from rest_framework.views import APIView
from django.views import View
from django.http import HttpResponse,JsonResponse
from codez_backend import settings
from .Serializer import *
from .models import *
import datetime
import jwt
import os

# 密码登录接口
class Login_Pwd_View(APIView):
    def post(self, request):
        ret = {
            "data": {},
            "meta": {
                "status": 200,
                "message": ""
            }
        }
        try:
            phonenumber = request.data["phonenumber"]
            password = request.data["password"]

            user = ZUser.objects.filter(phonenumber=phonenumber, password=password)
            if user.count() == 0:
                ret["meta"]["status"] = 500
                ret["meta"]["message"] = "用户不存在或密码错误"
                return Response(ret)
            elif user and user.first().password:
                jwtdict = {
                    "exp": datetime.datetime.now() + datetime.timedelta(days=1),  # 过期时间
                    "iat": datetime.datetime.now(),  # 开始时间
                    "uid": user.first().userid,
                }
                token = jwt.encode(jwtdict, settings.SECRET_KEY, algorithm="HS256")
                userprofile = ZUserProfile.objects.filter(userid=user.first().userid)
                ret["data"]["token"] = token
                ret["data"]["userid"] = user.first().userid
                ret["data"]["avatar"] = userprofile.first().avatar
                ret["data"]["displayname"] = userprofile.first().displayname
                ret["data"]["zcoins"] = userprofile.first().zcoins
                ret["meta"]["status"] = 200
                ret["meta"]["message"] = "登录成功"
                return Response(ret)
            else:
                ret["meta"]["status"] = 500
                ret["meta"]["message"] = "用户不存在或密码错误"
                return Response(ret)
        except Exception as error:
            print(error)
            ret["meta"]["status"] = 500
            ret["meta"]["message"] = "内部错误"
            return Response(ret)

# 短信登录接口
class Login_Sms_View(APIView):
    def post(self, request):
        pass

# 手机号注册接口
class Registry_Phone_View(APIView):
    def post(self, request):
        ret = {
            "data": {},
            "meta": {
                "status": 200,
                "message": ""
            }
        }
        try:
            phonenumber = request.data["phonenumber"]
            password = request.data["password"]

            user = ZUser.objects.filter(phonenumber=phonenumber)
            if not user.count():
                newuser = ZUser()
                testo = True
                newuid = 10000 + ZUser.objects.count()
                while testo:
                    newuid += 1
                    tmpuser = ZUser.objects.filter(userid=newuid)
                    testo = (tmpuser.count())
                newuser.userid = newuid
                newuser.phonenumber = phonenumber
                newuser.password = password
                newuser.save()

                newuserprofile = ZUserProfile()
                newuserprofile.userid = newuser.userid
                newuserprofile.displayname = 'CodeZ用户' + str(newuserprofile.userid)
                newuserprofile.zcoins = 0
                newuserprofile.age = -1
                newuserprofile.gender = 0
                newuserprofile.save()

                ret["meta"]["status"] = 200
                ret["meta"]["message"] = "嘻嘻嘻哈"
                return Response(ret)
            else:
                ret["meta"]["status"] = 500
                ret["meta"]["message"] = "该手机号码已被使用"
                return Response(ret)

        except Exception as error:
            ret["meta"]["status"] = 500
            ret["meta"]["message"] = "内部错误"
            return Response(ret)

# 头像上传接口
class Avatar_Upload_View(APIView):
    def post(self, request):
        ret = {
            "data": {},
            "meta": {
                "status": 200,
                "message": ""
            }
        }
        try:
            suffix = request.data['file'].name.split('.')[-1]
            with open('../codez_frontend/src/assets/avatar/' + request.data['uid'] + '.' + suffix, 'wb') as f:
                f.write(request.data['file'].file.read())
            user = ZUserProfile.objects.filter(userid=int(request.data['uid']))
            if user.count():
                user = user[0]
                user.avatar = 'src/assets/avatar/' + request.data['uid'] + '.' + suffix
                user.save()
            ret["data"]["avatar"] = 'src/assets/avatar/' + request.data['uid'] + '.' + suffix
            ret["meta"]["status"] = 200
            ret["meta"]["message"] = "上传成功"
            return Response(ret)
        except Exception as error:
            ret["meta"]["status"] = 500
            ret["meta"]["message"] = "内部错误"
            return Response(ret)

# 用户功能信息获取接口
class User_Profile_View(APIView):
    def post(self, request):
        ret = {
            "data": {},
            "meta": {
                "status": 200,
                "message": ""
            }
        }
        try:
            userid = request.data["userid"]
            user = ZUserProfile.objects.filter(userid=userid)
            if user.count():
                ret['data']['avatar'] = user.first().avatar
                ret['data']['displayname'] = user.first().displayname
                ret['data']['zcoins'] = user.first().zcoins
                ret['data']['description'] = user.first().description
                ret['data']['age'] = user.first().age
                ret['data']['gender'] = user.first().gender
                ret['data']['school'] = user.first().school
                ret['data']['corrects'] = user.first().corrects
                ret['data']['finishes'] = user.first().finishes
                ret['data']['medals'] = user.first().medals
                ret['data']['displaymedals'] = user.first().displaymedals
                ret["meta"]["status"] = 200
                ret["meta"]["message"] = "获取成功"
                return Response(ret)
            else:
                ret["meta"]["status"] = 404
                ret["meta"]["message"] = "该用户不存在"
                return Response(ret)
        except Exception as error:
            ret["meta"]["status"] = 500
            ret["meta"]["message"] = "内部错误"
            return Response(ret)

# 用户更改名称接口
class User_Change_Name_View(APIView):
    def post(self, request):
        ret = {
            "data": {},
            "meta": {
                "status": 200,
                "message": ""
            }
        }
        try:
            displayname = request.data["displayname"]
            user = ZUserProfile.objects.filter(userid=int(request.data["userid"]))
            if user.count():
                user = user[0]
                user.displayname = displayname
                user.save()
                ret["meta"]["status"] = 200
                ret["meta"]["message"] = "更改成功"
                return Response(ret)
            else:
                ret["meta"]["status"] = 404
                ret["meta"]["message"] = "该用户不存在"
                return Response(ret)
        except Exception as error:
            ret["meta"]["status"] = 500
            ret["meta"]["message"] = "内部错误"
            return Response(ret)

# 用户更改简介接口
class User_Change_Desc_View(APIView):
    def post(self, request):
        ret = {
            "data": {},
            "meta": {
                "status": 200,
                "message": ""
            }
        }
        try:
            description = request.data["description"]
            user = ZUserProfile.objects.filter(userid=int(request.data["userid"]))
            if user.count():
                user = user[0]
                user.description = description
                user.save()
                ret["meta"]["status"] = 200
                ret["meta"]["message"] = "更改成功"
                return Response(ret)
            else:
                ret["meta"]["status"] = 404
                ret["meta"]["message"] = "该用户不存在"
                return Response(ret)
        except Exception as error:
            ret["meta"]["status"] = 500
            ret["meta"]["message"] = "内部错误"
            return Response(ret)

# 用户更改年龄、性别、院校接口
class User_Change_Info_View(APIView):
    def post(self, request):
        ret = {
            "data": {},
            "meta": {
                "status": 200,
                "message": ""
            }
        }
        try:
            gender = request.data["gender"]
            age = request.data["age"]
            school = request.data["school"]
            user = ZUserProfile.objects.filter(userid=int(request.data["userid"]))
            if user.count():
                user = user[0]
                user.gender = gender
                user.age = age
                user.school = school
                user.save()
                ret["meta"]["status"] = 200
                ret["meta"]["message"] = "更改成功"
                return Response(ret)
            else:
                ret["meta"]["status"] = 404
                ret["meta"]["message"] = "该用户不存在"
                return Response(ret)
        except Exception as error:
            ret["meta"]["status"] = 500
            ret["meta"]["message"] = "内部错误"
            return Response(ret)

# 获取题库列表接口
class Bank_List_View(APIView):
    def post(self, request):
        ret = {
            "data": {
                "result": [],
            },
            "meta": {
                "status": 200,
                "message": ""
            }
        }
        try:
            bank = Bank.objects.all()
            for i in bank:
                if i.status != 2:
                    tmpobj = {"bid": i.bankid, "name": i.bankname, "description": i.description, "status": i.status}
                    ret['data']['result'].append(tmpobj)
            ret["meta"]["status"] = 200
            ret["meta"]["message"] = "获取成功"
            return Response(ret)
        except Exception as error:
            print(error)
            ret["meta"]["status"] = 500
            ret["meta"]["message"] = "内部错误"
            return Response(ret)

# 搜寻题库接口
class Search_Bank_View(APIView):
    def post(self, request):
        ret = {
            "data": {
                "search_results": [],
            },
            "meta": {
                "status": 200,
                "message": ""
            }
        }
        try:
            query = request.data["query"]
            filters = Q()
            try:
                filters = filters | Q(bankid=int(query))
            except Exception as error:
                pass
            filters = filters | Q(bankname__contains=query)
            bank = Bank.objects.filter(filters)
            if bank.count():
                for b in bank:
                    tmpobj = {
                        'bid': b.bankid,
                        'name': b.bankname,
                        'description': b.description,
                        'status': b.status,
                        'price': b.price
                    }
                    ret["data"]["search_results"].append(tmpobj)
                ret["meta"]["status"] = 200
                ret["meta"]["message"] = "搜寻成功"
                return Response(ret)
            else:
                ret["meta"]["status"] = 404
                ret["meta"]["message"] = "搜寻结果为空"
                return Response(ret)

        except Exception as error:
            print(error)
            ret["meta"]["status"] = 500
            ret["meta"]["message"] = "内部错误"
            return Response(ret)

# 搜寻用户接口
class Search_User_View(APIView):
    def post(self, request):
        ret = {
            "data": {
                "search_results": [],
            },
            "meta": {
                "status": 200,
                "message": ""
            }
        }
        try:
            query = request.data["query"]
            filters = Q()
            try:
                filters = filters | Q(userid=int(query))
            except Exception as error:
                pass
            filters = filters | Q(displayname__contains=str(query))

            user = ZUserProfile.objects.filter(filters)
            if user.count():
                for u in user:
                    tmpobj = {
                        'uid': u.userid,
                        'name': u.displayname,
                        'description': u.description
                    }
                    ret["data"]["search_results"].append(tmpobj)
                ret["meta"]["status"] = 200
                ret["meta"]["message"] = "搜寻成功"
                return Response(ret)
            else:
                ret["meta"]["status"] = 404
                ret["meta"]["message"] = "搜寻结果为空"
                return Response(ret)

        except Exception as error:
            print(error)
            ret["meta"]["status"] = 500
            ret["meta"]["message"] = "内部错误"
            return Response(ret)

# 管理员登录接口
class Login_Admin_View(APIView):
    def post(self, request):
        ret = {
            "data": {},
            "meta": {
                "status": 200,
                "message": ""
            }
        }
        try:
            aid = request.data["aid"]
            password = request.data["password"]

            user = ZAdmin.objects.filter(adminid=aid, password=password)
            if not user.count():
                ret["meta"]["status"] = 500
                ret["meta"]["message"] = "管理员不存在或密码错误"
                return Response(ret)
            elif user and user.first().password:
                jwtdict = {
                    "exp": datetime.datetime.now() + datetime.timedelta(days=1),  # 过期时间
                    "iat": datetime.datetime.now(),  # 开始时间
                    "aid": user.first().adminid,
                }
                token = jwt.encode(jwtdict, settings.SECRET_KEY, algorithm="HS256")
                ret["data"]["token"] = token
                ret["data"]["adminid"] = aid
                ret["data"]["adminname"] = user.first().adminname
                ret["meta"]["status"] = 200
                ret["meta"]["message"] = "登录成功"
                return Response(ret)
            else:
                ret["meta"]["status"] = 500
                ret["meta"]["message"] = "管理员不存在或密码错误"
                return Response(ret)
        except Exception as error:
            print(error)
            ret["meta"]["status"] = 500
            ret["meta"]["message"] = "内部错误"
            return Response(ret)

# 管理员搜寻用户接口
class Admin_Search_User_View(APIView):
    def post(self, request):
        ret = {
            "data": {
                "search_results": [],
            },
            "meta": {
                "status": 200,
                "message": ""
            }
        }
        try:
            uid = request.data["uid"]
            name = request.data["displayname"]
            filters = Q()
            if uid:
                filters = filters & Q(userid=int(uid))
            if name:
                filters = filters & Q(displayname__contains=name)

            user = ZUserProfile.objects.filter(filters)
            if user.count():
                for u in user:
                    tmpobj = {'uid': u.userid, 'username': u.displayname}
                    ret["data"]["search_results"].append(tmpobj)
                ret["meta"]["status"] = 200
                ret["meta"]["message"] = "搜寻成功"
                return Response(ret)
            else:
                ret["meta"]["status"] = 404
                ret["meta"]["message"] = "搜寻结果为空"
                return Response(ret)

        except Exception as error:
            print(error)
            ret["meta"]["status"] = 500
            ret["meta"]["message"] = "内部错误"
            return Response(ret)

# 管理员查看用户所有信息接口
class Admin_User_Info_View(APIView):
    def post(self, request):
        ret = {
            "data": {},
            "meta": {
                "status": 200,
                "message": ""
            }
        }
        try:
            uid = request.data["uid"]
            user = ZUser.objects.filter(userid=int(uid))
            userprofile = ZUserProfile.objects.filter(userid=int(uid))

            if user.count():
                user = user[0]
                userprofile = userprofile[0]
                ret['data']['uid'] = user.userid
                ret['data']['password'] = user.password
                ret['data']['phonenumber'] = user.phonenumber
                ret['data']['thirdpartyauth'] = user.thirdpartyauth
                ret['data']['displayname'] = userprofile.displayname
                ret['data']['age'] = userprofile.age
                ret['data']['gender'] = userprofile.gender
                ret['data']['school'] = userprofile.school
                ret['data']['zcoins'] = userprofile.zcoins
                ret['data']['avatar'] = userprofile.avatar
                ret['data']['description'] = userprofile.description
                ret['data']['corrects'] = userprofile.corrects
                ret['data']['finishes'] = userprofile.finishes
                ret['data']['medals'] = userprofile.medals
                ret['data']['displaymedals'] = userprofile.displaymedals
                ret['data']['unlockedbanks'] = userprofile.unlockedbanks
                ret["meta"]["status"] = 200
                ret["meta"]["message"] = "获取成功"
                return Response(ret)
            else:
                ret["meta"]["status"] = 404
                ret["meta"]["message"] = "用户ID不存在"
                return Response(ret)

        except Exception as error:
            print(error)
            ret["meta"]["status"] = 500
            ret["meta"]["message"] = "内部错误"
            return Response(ret)

# 管理员获取可用新UID接口
class Admin_Available_ID_View(APIView):
    def post(self, request):
        ret = {
            "data": {},
            "meta": {
                "status": 200,
                "message": ""
            }
        }
        try:
            result = True
            newuid = 10000 + ZUser.objects.count()
            while result:
                newuid += 1
                tmpuser = ZUser.objects.filter(userid=newuid)
                result = (tmpuser.count())
            ret['data']['new_uid'] = newuid
            ret["meta"]["status"] = 200
            ret["meta"]["message"] = "获取成功"
            return Response(ret)

        except Exception as error:
            print(error)
            ret["meta"]["status"] = 500
            ret["meta"]["message"] = "内部错误"
            return Response(ret)

# 管理员修改用户所有信息接口
class Admin_User_Change_View(APIView):
    def post(self, request):
        ret = {
            "data": {},
            "meta": {
                "status": 200,
                "message": ""
            }
        }
        try:
            uid = request.data["uid"]
            password = request.data["password"]
            phonenumber = request.data["phonenumber"]
            thirdpartyauth = request.data["thirdpartyauth"]
            displayname = request.data["displayname"]
            zcoins = request.data["zcoins"]
            age = request.data["age"]
            gender = request.data["gender"]
            school = request.data["school"]
            description = request.data["description"]
            corrects = request.data["corrects"]
            finishes = request.data["finishes"]
            medals = request.data["medals"]
            unlockedbanks = request.data["unlockedbanks"]
            user = ZUser.objects.filter(userid=int(uid))
            userprofile = ZUserProfile.objects.filter(userid=int(uid))

            if user.count():
                user = user[0]
                userprofile = userprofile[0]

                user.password = password
                user.phonenumber = phonenumber
                user.thirdpartyauth = thirdpartyauth
                user.save()

                userprofile.displayname = displayname
                userprofile.age = age
                userprofile.gender = gender
                userprofile.school = school
                userprofile.zcoins = zcoins
                userprofile.description = description
                userprofile.corrects = corrects
                userprofile.finishes = finishes
                userprofile.medals = medals
                userprofile.unlockedbanks = unlockedbanks
                userprofile.save()

                ret['data']['uid'] = user.userid
                ret["meta"]["status"] = 200
                ret["meta"]["message"] = "更改成功"
                return Response(ret)
            else:
                ret["meta"]["status"] = 404
                ret["meta"]["message"] = "用户ID不存在"
                return Response(ret)

        except Exception as error:
            print(error)
            ret["meta"]["status"] = 500
            ret["meta"]["message"] = "内部错误"
            return Response(ret)

# 管理员获取可用新题目ID接口
class Admin_Question_ID_View(APIView):
    def post(self, request):
        ret = {
            "data": {},
            "meta": {
                "status": 200,
                "message": ""
            }
        }
        try:
            result = True
            newqid = 100000 + Question.objects.count()
            while result:
                newqid += 1
                tmpquestion = Question.objects.filter(questionid=newqid)
                result = (tmpquestion.count())
            ret['data']['new_qid'] = newqid
            ret["meta"]["status"] = 200
            ret["meta"]["message"] = "获取成功"
            return Response(ret)

        except Exception as error:
            print(error)
            ret["meta"]["status"] = 500
            ret["meta"]["message"] = "内部错误"
            return Response(ret)

# 管理员新增题目接口
class Admin_Question_Create_View(APIView):
    def post(self, request):
        ret = {
            "data": {},
            "meta": {
                "status": 200,
                "message": ""
            }
        }
        try:
            qid = request.data["qid"]
            name = request.data["name"]
            type = request.data["type"]
            content = request.data["content"]
            answer = request.data["answer"]

            question = Question.objects.filter(questionid=qid)
            if not question.count():
                newq = Question()
                newq.questionid = qid
                newq.name = name
                newq.type = type
                newq.content = content
                newq.answer = answer
                newq.save()

                ret["meta"]["status"] = 200
                ret["meta"]["message"] = "新增成功"
                return Response(ret)
            else:
                ret["meta"]["status"] = 500
                ret["meta"]["message"] = "该题目ID已存在"
                return Response(ret)

        except Exception as error:
            print(error)
            ret["meta"]["status"] = 500
            ret["meta"]["message"] = "内部错误"
            return Response(ret)

# 管理员获取题目内容接口
class Admin_Question_Info_View(APIView):
    def post(self, request):
        ret = {
            "data": {},
            "meta": {
                "status": 200,
                "message": ""
            }
        }
        try:
            qid = request.data["qid"]

            question = Question.objects.filter(questionid=qid)
            if question.count():
                question = question[0]
                ret["data"]["qid"] = qid
                ret["data"]["name"] = question.name
                ret["data"]["type"] = question.type
                ret["data"]["content"] = question.content
                ret["data"]["answer"] = question.answer

                ret["meta"]["status"] = 200
                ret["meta"]["message"] = "新增成功"
                return Response(ret)
            else:
                ret["meta"]["status"] = 500
                ret["meta"]["message"] = "该题目ID不存在"
                return Response(ret)

        except Exception as error:
            print(error)
            ret["meta"]["status"] = 500
            ret["meta"]["message"] = "内部错误"
            return Response(ret)

# 管理员搜寻题目接口
class Admin_Search_Question_View(APIView):
    def post(self, request):
        ret = {
            "data": {
                "search_results": [],
            },
            "meta": {
                "status": 200,
                "message": ""
            }
        }
        try:
            qid = request.data["qid"]
            name = request.data["name"]
            filters = Q()
            if qid:
                filters = filters & Q(questionid=int(qid))
            if name:
                filters = filters & Q(name__contains=name)

            question = Question.objects.filter(filters)
            if question.count():
                for u in question:
                    tmpobj = {'qid': u.questionid, 'name': u.name}
                    ret["data"]["search_results"].append(tmpobj)
                ret["meta"]["status"] = 200
                ret["meta"]["message"] = "搜寻成功"
                return Response(ret)
            else:
                ret["meta"]["status"] = 404
                ret["meta"]["message"] = "搜寻结果为空"
                return Response(ret)

        except Exception as error:
            print(error)
            ret["meta"]["status"] = 500
            ret["meta"]["message"] = "内部错误"
            return Response(ret)

# 管理员修改题目内容接口
class Admin_Question_Change_View(APIView):
    def post(self, request):
        ret = {
            "data": {},
            "meta": {
                "status": 200,
                "message": ""
            }
        }
        try:
            qid = request.data["qid"]
            name = request.data["name"]
            type = request.data["type"]
            content = request.data["content"]
            answer = request.data["answer"]

            question = Question.objects.filter(questionid=qid)
            if question.count():
                question = question[0]
                question.name = name
                question.type = type
                question.content = content
                question.answer = answer
                question.save()

                ret["meta"]["status"] = 200
                ret["meta"]["message"] = "修改成功"
                return Response(ret)
            else:
                ret["meta"]["status"] = 500
                ret["meta"]["message"] = "该题目ID不存在"
                return Response(ret)

        except Exception as error:
            print(error)
            ret["meta"]["status"] = 500
            ret["meta"]["message"] = "内部错误"
            return Response(ret)

# 管理员搜寻题库接口
class Admin_Search_Bank_View(APIView):
    def post(self, request):
        ret = {
            "data": {
                "search_results": [],
            },
            "meta": {
                "status": 200,
                "message": ""
            }
        }
        try:
            bid = request.data["bid"]
            name = request.data["name"]
            filters = Q()
            if bid:
                filters = filters & Q(bankid=int(bid))
            if name:
                filters = filters & Q(bankname__contains=name)

            bank = Bank.objects.filter(filters)
            if bank.count():
                for b in bank:
                    tmpobj = {'bid': b.bankid, 'bankname': b.bankname}
                    ret["data"]["search_results"].append(tmpobj)
                ret["meta"]["status"] = 200
                ret["meta"]["message"] = "搜寻成功"
                return Response(ret)
            else:
                ret["meta"]["status"] = 404
                ret["meta"]["message"] = "搜寻结果为空"
                return Response(ret)

        except Exception as error:
            print(error)
            ret["meta"]["status"] = 500
            ret["meta"]["message"] = "内部错误"
            return Response(ret)

# 管理员获取可用的新题库ID接口
class Admin_Bank_ID_View(APIView):
    def post(self, request):
        ret = {
            "data": {},
            "meta": {
                "status": 200,
                "message": ""
            }
        }
        try:
            result = True
            newbid = 10000 + Bank.objects.count()
            while result:
                newbid += 1
                tmpbank = Bank.objects.filter(bankid=newbid)
                result = (tmpbank.count())
            ret['data']['new_bid'] = newbid
            ret["meta"]["status"] = 200
            ret["meta"]["message"] = "获取成功"
            return Response(ret)

        except Exception as error:
            print(error)
            ret["meta"]["status"] = 500
            ret["meta"]["message"] = "内部错误"
            return Response(ret)

# 管理员新增题库接口
class Admin_Bank_Create_View(APIView):
    def post(self, request):
        ret = {
            "data": {},
            "meta": {
                "status": 200,
                "message": ""
            }
        }
        try:
            bid = request.data["bid"]
            name = request.data["name"]
            description = request.data["description"]
            status = request.data["status"]
            price = request.data["price"]
            questions = request.data["questions"]

            bank = Bank.objects.filter(bankid=bid)
            if not bank.count():
                newb = Bank()
                newb.bankid = bid
                newb.bankname = name
                newb.description = description
                newb.status = status
                newb.price = price
                newb.questions = questions
                newb.save()

                ret["meta"]["status"] = 200
                ret["meta"]["message"] = "新增成功"
                return Response(ret)
            else:
                ret["meta"]["status"] = 500
                ret["meta"]["message"] = "该题库ID已存在"
                return Response(ret)

        except Exception as error:
            print(error)
            ret["meta"]["status"] = 500
            ret["meta"]["message"] = "内部错误"
            return Response(ret)

# 管理员获取题库包含题目接口
class Admin_Bank_Questions_View(APIView):
    def post(self, request):
        ret = {
            "data": {
                "result": [],
            },
            "meta": {
                "status": 200,
                "message": ""
            }
        }
        try:
            bid = request.data["bid"]
            bank = Bank.objects.filter(bankid=bid)
            if bank.count():
                bank = bank[0]
                if bank.questions:
                    for qid in bank.questions.split(','):
                        tmpq = Question.objects.filter(questionid=qid)
                        if tmpq.count():
                            tmpq = tmpq[0]
                            tmpobj = {'qid': tmpq.questionid, 'name': tmpq.name}
                            ret["data"]["result"].append(tmpobj)
                ret["meta"]["status"] = 200
                ret["meta"]["message"] = "获取成功"
                return Response(ret)
            else:
                ret["meta"]["status"] = 404
                ret["meta"]["message"] = "搜寻结果为空"
                return Response(ret)

        except Exception as error:
            print(error)
            ret["meta"]["status"] = 500
            ret["meta"]["message"] = "内部错误"
            return Response(ret)

# 管理员获取题库内容接口
class Admin_Bank_Info_View(APIView):
    def post(self, request):
        ret = {
            "data": {},
            "meta": {
                "status": 200,
                "message": ""

            }
        }
        try:
            bid = request.data["bid"]

            bank = Bank.objects.filter(bankid=bid)
            if bank.count():
                bank = bank[0]
                ret["data"]["bid"] = bid
                ret["data"]["name"] = bank.bankname
                ret["data"]["description"] = bank.description
                ret["data"]["status"] = bank.status
                ret["data"]["price"] = bank.price
                ret["data"]["questions"] = bank.questions

                ret["meta"]["status"] = 200
                ret["meta"]["message"] = "获取成功"
                return Response(ret)
            else:
                ret["meta"]["status"] = 404
                ret["meta"]["message"] = "该题库ID不存在"
                return Response(ret)

        except Exception as error:
            print(error)
            ret["meta"]["status"] = 500
            ret["meta"]["message"] = "内部错误"
            return Response(ret)

# 管理员修改题库内容接口
class Admin_Bank_Change_View(APIView):
    def post(self, request):
        ret = {
            "data": {},
            "meta": {
                "status": 200,
                "message": ""
            }
        }
        try:
            bid = request.data["bid"]
            name = request.data["name"]
            description = request.data["description"]
            status = request.data["status"]
            price = request.data["price"]
            questions = request.data["questions"]

            bank = Bank.objects.filter(bankid=bid)
            if bank.count():
                bank = bank[0]
                bank.bankname = name
                bank.description = description
                bank.status = status
                bank.price = price
                bank.questions = questions
                bank.save()

                ret["meta"]["status"] = 200
                ret["meta"]["message"] = "修改成功"
                return Response(ret)
            else:
                ret["meta"]["status"] = 500
                ret["meta"]["message"] = "该题库ID已被使用"
                return Response(ret)

        except Exception as error:
            print(error)
            ret["meta"]["status"] = 500
            ret["meta"]["message"] = "内部错误"
            return Response(ret)

# 获取用户与题库关系接口
class User_Bank_Status_View(APIView):
    def post(self, request):
        ret = {
            "data": {},
            "meta": {
                "status": 200,
                "message": ""
            }
        }
        try:
            bid = request.data["bid"]
            uid = request.data["uid"]

            stat = User_Bank_Status.objects.filter(bankid=bid, userid=uid)
            if stat.count():
                stat = stat[0]
                ret["data"]["finished"] = stat.finished
                ret["data"]["unlocked"] = stat.unlocked
                ret["meta"]["status"] = 200
                ret["meta"]["message"] = "获取成功"
                return Response(ret)
            else:
                stat = User_Bank_Status()
                result = True
                newid = 1000000 + User_Bank_Status.objects.count()
                while result:
                    newid += 1
                    tmpstat = User_Bank_Status.objects.filter(id=newid)
                    result = tmpstat.count()
                stat.id = newid
                stat.userid = uid
                stat.bankid = bid
                stat.finished = 0
                stat.unlocked = 0
                stat.save()
                ret["meta"]["status"] = 200
                ret["meta"]["message"] = "未找到对应关系词条，已成功创建"
                return Response(ret)

        except Exception as error:
            print(error)
            ret["meta"]["status"] = 500
            ret["meta"]["message"] = "内部错误"
            return Response(ret)

# 获取用户与题目关系接口
class User_Question_Status_View(APIView):
    def post(self, request):
        ret = {
            "data": {},
            "meta": {
                "status": 200,
                "message": ""
            }
        }
        try:
            qid = request.data["qid"]
            uid = request.data["uid"]

            stat = User_Question_Status.objects.filter(questionid=qid, userid=uid)
            if stat.count():
                stat = stat[0]
                ret["data"]["time"] = stat.time
                ret["data"]["attempts"] = stat.attempts
                ret["data"]["finished"] = stat.finished
                ret["meta"]["status"] = 200
                ret["meta"]["message"] = "获取成功"
                return Response(ret)
            else:
                stat = User_Question_Status()
                result = True
                newid = 1000000 + User_Question_Status.objects.count()
                while result:
                    newid += 1
                    tmpstat = User_Question_Status.objects.filter(id=newid)
                    result = tmpstat.count()
                stat.id = newid
                stat.userid = uid
                stat.questionid = qid
                stat.finished = 0
                stat.time = 0
                stat.attempts = 0
                stat.save()
                ret["data"]["time"] = stat.time
                ret["data"]["attempts"] = stat.attempts
                ret["data"]["finished"] = stat.finished
                ret["meta"]["status"] = 200
                ret["meta"]["message"] = "未找到对应关系词条，已成功创建"
                return Response(ret)

        except Exception as error:
            print(error)
            ret["meta"]["status"] = 500
            ret["meta"]["message"] = "内部错误"
            return Response(ret)

# 获取用户当前作答题目内容接口
class User_Current_Question_View(APIView):
    def post(self, request):
        ret = {
            "data": {},
            "meta": {
                "status": 200,
                "message": ""
            }
        }
        try:
            bid = request.data["bid"]
            uid = request.data["uid"]

            stat = User_Bank_Status.objects.filter(bankid=bid, userid=uid)
            bank = Bank.objects.filter(bankid=bid)
            if stat.count() and bank.count():
                stat = stat[0]
                bank = bank[0]
                if bank.status == 1 and stat.unlocked == 0:
                    ret["meta"]["status"] = 500
                    ret["meta"]["message"] = "用户尚未解锁题库"
                    return Response(ret)
                elif bank.status == 2:
                    ret["meta"]["status"] = 500
                    ret["meta"]["message"] = "题库当前不可用"
                    return Response(ret)
                elif stat.finished == 1:
                    ret["meta"]["status"] = 200
                    ret["meta"]["message"] = "用户已完成题库"
                    return Response(ret)
                else:
                    if bank.questions != '':
                        ret["data"]["totals"] = len(bank.questions.split(','))
                        ret["data"]["bankname"] = bank.bankname
                        for i, id in enumerate(bank.questions.split(',')):
                            q = Question.objects.filter(questionid=id)
                            qstat = User_Question_Status.objects.filter(questionid=id, userid=uid)
                            if q.count() and qstat.count():
                                q = q[0]
                                qstat = qstat[0]
                                if qstat.finished == 1:
                                    continue
                                else:
                                    ret["data"]["curindex"] = i
                                    ret["data"]["questionid"] = q.questionid
                                    ret["data"]["name"] = q.name
                                    ret["data"]["type"] = q.type
                                    ret["data"]["time"] = qstat.time
                                    ret["data"]["attempts"] = qstat.attempts
                                    ret["data"]["content"] = q.content
                                    return Response(ret)
                            else:
                                ret["meta"]["status"] = 500
                                ret["meta"]["message"] = "内部错误"
                                return Response(ret)
                    else:
                        ret["meta"]["status"] = 500
                        ret["meta"]["message"] = "题库为空，请联系管理员"
                        return Response(ret)
            else:
                ret["meta"]["status"] = 500
                ret["meta"]["message"] = "用户尚未开启题库"
                return Response(ret)

        except Exception as error:
            print(error)
            ret["meta"]["status"] = 500
            ret["meta"]["message"] = "内部错误"
            return Response(ret)