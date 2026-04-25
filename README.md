# Flask 用户认证系统

一个基于 Flask 的用户认证管理系统，支持管理员和普通用户角色。

## 🚀 功能特性

- 用户注册与登录
- 角色权限管理（管理员/普通用户）
- 会话管理
- 数据库自动初始化
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
pip install -r requirements.txt
```

如果没有 requirements.txt 文件，安装以下包：

```bash
pip install flask flask-login flask-sqlalchemy pymysql
```

### 2. 配置数据库

编辑 `config.py` 文件，配置 MySQL 连接参数：

```python
class Config:
    MYSQL_HOST = 'localhost'      # 数据库主机
    MYSQL_PORT = 3306            # 数据库端口
    MYSQL_USER = 'root'          # 数据库用户名
    MYSQL_PASSWORD = 'password'  # 数据库密码
    MYSQL_DATABASE = 'flask_auth' # 数据库名
    SECRET_KEY = 'your-secret-key'  # 用于会话加密
    
    # SQLALCHEMY 数据库 URI
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
```

### 3. 初始化数据库

首次运行前，需要初始化数据库：

```bash
python init_db.py
```

这将：
- 创建数据库（如果不存在）
- 创建表结构
- 创建默认用户

### 4. 启动应用

```bash
python app.py
```

应用将在 `http://127.0.0.1:5000` 启动。

## 👥 默认用户

初始化后，系统会创建以下默认用户：

| 用户名 | 密码 | 角色 |
|--------|------|------|
| admin | admin123 | 管理员 |
| user1 | user123 | 普通用户 |

## 🗂️ 项目结构

```
project/
├── app.py              # 主应用文件
├── init_db.py          # 数据库初始化脚本
├── config.py           # 配置文件
├── models.py           # 数据模型
├── templates/          # HTML 模板
│   ├── base.html       # 基础模板
│   ├── index.html      # 首页
│   ├── login.html      # 登录页
│   ├── admin.html      # 管理员面板
│   └── user.html       # 用户面板
└── requirements.txt    # 依赖文件
```

## 🔐 使用说明

### 访问网站

1. 打开浏览器访问 `http://127.0.0.1:5000`
2. 点击登录按钮进入登录页面
3. 使用默认账号登录

### 用户角色

- **普通用户**：可以登录并访问个人面板
- **管理员**：拥有额外的管理权限，

### 页面导航

- `/` - 首页
- `/login` - 登录页面
- `/dashboard` - 仪表盘（根据角色重定向）
- `/admin` - 管理员面板
- `/user` - 普通用户面板
- `/logout` - 退出登录

## ⚙️ 维护命令

### 重新初始化数据库

```bash
python init_db.py
```