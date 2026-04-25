# Flask 多层级角色访问控制系统

一个基于 Flask 的用户认证管理系统，实现多层级角色划分与静态职能分离约束。

## 🚀 功能特性

- 用户注册与登录
- 多层级角色管理（管理员 / 教师（主讲教师、助教） / 学生）
- 基于角色的细粒度权限控制
- 静态职能分离（SoD）验证
- 管理员面板支持动态角色修改与冲突检查
- 响应式前端界面

## 📋 技术栈

- Python 3.11
- Flask
- Flask-Login
- SQLAlchemy
- MySQL

## 🛠️ 安装步骤

### 1. 安装依赖

```bash
pip install flask flask-login flask-sqlalchemy pymysql
```

### 2. 配置数据库

编辑 `config.py`，配置 MySQL 连接参数：

```python
class Config:
    MYSQL_HOST = 'localhost'
    MYSQL_PORT = 3306
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = '你的密码'
    MYSQL_DATABASE = 'flask_db'
    SECRET_KEY = 'your-secret-key'
    
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
```

### 3. 初始化数据库

首次运行前，执行数据库初始化：

```bash
python init_db.py
```

这将自动创建数据库、表结构及默认用户。

### 4. 启动应用

```bash
python app.py
```

应用将在 `http://127.0.0.1:5000` 启动。

## 👥 默认用户

初始化后，系统会创建以下默认用户：

| 用户名           | 密码          | 一级角色 | 二级角色     |
|------------------|---------------|----------|--------------|
| admin            | admin123      | 管理员   | —            |
| teacher_lead     | teacher123    | 教师     | 主讲教师     |
| teacher_assist   | assist123     | 教师     | 助教         |
| student1         | student123    | 学生     | —            |

## 🗂️ 项目结构

```
project/
├── app.py                 # 主应用，路由分发与角色管理
├── init_db.py             # 数据库初始化脚本
├── config.py              # 配置文件
├── models.py              # 数据模型与职能分离校验
├── decorators.py          # 权限装饰器
├── templates/             # HTML 模板
│   ├── base.html          # 基础模板（含导航栏）
│   ├── index.html         # 首页
│   ├── login.html         # 登录页
│   ├── admin.html         # 管理员面板（含角色管理）
│   ├── lead_teacher.html  # 主讲教师面板
│   ├── assistant.html     # 助教面板
│   ├── student.html       # 学生面板
│   └── user.html          # 旧版普通用户面板（已弃用）
└── requirements.txt       # 依赖文件
```

## 🔐 使用说明

### 访问网站

1. 打开浏览器访问 `http://127.0.0.1:5000`
2. 点击登录按钮进入登录页面
3. 使用任一默认账号登录，体验不同面板

### 多层级角色

- **管理员**（`admin`）：可查看所有用户，动态修改角色与子角色，并受职能分离规则约束。
- **主讲教师**（`lead_teacher`）：可管理课程、上传资料、查看学生名单、分配助教任务、录入成绩。
- **助教**（`assistant`）：可查看任务清单、批改作业、回答提问、阅读公告。
- **学生**（`student`）：可查看已选课程、提交作业、查看成绩、向教师或助教提问。

### 职能分离规则（静态约束）

管理员在修改角色时会自动校验以下冲突：
- 管理员不能兼任教师（不可设置子角色）
- 学生不能担任助教或主讲教师（不可设置子角色）
- 教师必须指定一个子角色（主讲教师或助教）
违反规则时，页面会显示具体冲突信息，并阻止修改。

### 页面导航

- `/` — 首页
- `/login` — 登录页面
- `/dashboard` — 仪表盘（根据角色自动跳转）
- `/admin` — 管理员面板
- `/teacher/lead` — 主讲教师面板
- `/teacher/assistant` — 助教面板
- `/student` — 学生面板
- `/logout` — 退出登录

## ⚙️ 维护命令

### 重新初始化数据库

```bash
python init_db.py
```