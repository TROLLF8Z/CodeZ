from django.db import models

# Create your models here.

# 用户基础数据ORM模型
class ZUser(models.Model):
    userid = models.BigIntegerField(primary_key=True, max_length=15, unique=True)
    password = models.CharField(max_length=50)
    phonenumber = models.BigIntegerField()
    thirdpartyauth = models.CharField(max_length=255, blank=True)

# 用户功能数据ORM模型
class ZUserProfile(models.Model):
    userid = models.BigIntegerField(primary_key=True, max_length=15, unique=True)
    displayname = models.CharField(max_length=50)
    age = models.IntegerField(max_length=3)
    gender = models.CharField(max_length=1)
    zcoins = models.BigIntegerField(default=0)
    avatar = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    school = models.CharField(max_length=30, blank=True)
    corrects = models.IntegerField(default=0)
    finishes = models.IntegerField(default=0)
    medals = models.CharField(max_length=255, blank=True)
    displaymedals = models.CharField(max_length=255, blank=True)
    unlockedbanks = models.CharField(max_length=255, blank=True)

# 题库内容ORM模型
class Bank(models.Model):
    bankid = models.BigIntegerField(primary_key=True, max_length=15, unique=True)
    bankname = models.CharField(max_length=50)
    description = models.TextField()
    status = models.IntegerField(max_length=1)
    price = models.IntegerField()
    questions = models.CharField(max_length=255)

# 题目内容ORM模型
class Question(models.Model):
    questionid = models.BigIntegerField(primary_key=True, max_length=15, unique=True)
    name = models.CharField(max_length=50, default="")
    type = models.IntegerField(max_length=1)
    content = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)

# 管理员数据ORM模型
class ZAdmin(models.Model):
    adminid = models.BigIntegerField(primary_key=True, max_length=15, unique=True)
    adminname = models.CharField(max_length=50, default = 'CodeZ_Admin')
    password = models.CharField(max_length=50, default = '159159159')

# 题库与用户关系对应ORM模型
class User_Bank_Status(models.Model):
    id = models.BigIntegerField(primary_key=True, max_length=15, unique=True, default=0)
    userid = models.BigIntegerField(max_length=15, default=0)
    bankid = models.BigIntegerField(max_length=15, default=0)
    finished = models.IntegerField(default=0)
    unlocked = models.IntegerField(default=0)

# 题目与用户关系对应ORM模型
class User_Question_Status(models.Model):
    id = models.BigIntegerField(primary_key=True, max_length=15, unique=True, default=0)
    userid = models.BigIntegerField(max_length=15, default=0)
    questionid = models.BigIntegerField(max_length=15, default=0)
    finished = models.IntegerField(default=0)
    time = models.IntegerField(default=0)
    attempts = models.IntegerField(default=0)