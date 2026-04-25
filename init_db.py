import pymysql
from app import create_app
from models import db, User
from config import Config

def create_database():
    """创建 MySQL 数据库"""
    try:
        # 连接到 MySQL 服务器
        connection = pymysql.connect(
            host=Config.MYSQL_HOST,
            port=Config.MYSQL_PORT,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            charset='utf8mb4'
        )
        
        cursor = connection.cursor()
        
        # 检查数据库是否已存在
        cursor.execute("SHOW DATABASES")
        databases = [db[0] for db in cursor.fetchall()]
        
        if Config.MYSQL_DATABASE in databases:
            print(f"✅ 数据库 '{Config.MYSQL_DATABASE}' 已存在")
        else:
            # 创建数据库
            create_db_query = f"""
            CREATE DATABASE {Config.MYSQL_DATABASE} 
            CHARACTER SET utf8mb4 
            COLLATE utf8mb4_unicode_ci
            """
            cursor.execute(create_db_query)
            print(f"✅ 数据库 '{Config.MYSQL_DATABASE}' 创建成功！")
        
        cursor.close()
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ 创建数据库失败: {e}")
        return False

def test_database_connection():
    """测试数据库连接"""
    try:
        connection = pymysql.connect(
            host=Config.MYSQL_HOST,
            port=Config.MYSQL_PORT,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database=Config.MYSQL_DATABASE,
            charset='utf8mb4'
        )
        
        cursor = connection.cursor()
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()
        print(f"✅ 数据库连接成功！MySQL 版本: {version[0]}")
        
        # 检查是否有表
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        if tables:
            print(f"📊 当前数据库中的表: {[table[0] for table in tables]}")
        else:
            print("📊 数据库中暂无表")
        
        cursor.close()
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ 数据库连接失败: {e}")
        return False

def init_database_tables():
    """初始化数据库表结构并创建默认用户"""
    try:
        app = create_app()
        
        with app.app_context():
            # 创建数据库表
            print("🔄 创建数据库表...")
            db.create_all()
            print("✅ 数据库表创建成功！")
            
            # 创建默认用户
            print("👥 创建默认用户...")
            User.create_default_users()
            print("✅ 默认用户创建成功！")
            
            # 验证用户创建
            users = User.query.all()
            print(f"\n📋 当前用户列表 ({len(users)} 个用户):")
            for user in users:
                print(f"   - ID: {user.id}, Username: {user.username}, Role: {user.role}")
            
            print("\n🎉 数据库初始化完成！")
            print("💡 现在可以运行 'python app.py' 启动应用了")
            
    except Exception as e:
        print(f"❌ 数据库初始化失败: {e}")
        return False
    
    return True

def main():
    print("🚀 开始初始化 Flask 认证系统数据库...")
    
    # 1. 创建数据库
    print("\n1. 检查并创建数据库...")
    if not create_database():
        print("❌ 数据库创建失败，退出程序")
        return False
    
    # 2. 测试连接
    print("\n2. 测试数据库连接...")
    if not test_database_connection():
        print("❌ 数据库连接测试失败，退出程序")
        return False
    
    # 3. 初始化表结构和默认用户
    print("\n3. 初始化表结构和默认用户...")
    if not init_database_tables():
        print("❌ 表结构初始化失败")
        return False
    
    print("\n🎊 Flask 认证系统设置完成！")
    print("📋 默认用户信息:")
    print("   管理员: admin / admin123")
    print("   主讲教师: teacher_lead / teacher123")
    print("   助教: teacher_assist / assist123")
    print("   学生: student1 / student123")
    print("💡 现在可以运行 'python app.py' 启动应用了")
    return True

if __name__ == '__main__':
    main()