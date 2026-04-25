from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)  # 从 120 改为 255
    role = db.Column(db.String(20), default='user')  # 'user' 或 'admin'
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    def set_password(self, password):
        """设置密码哈希"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """检查密码"""
        return check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        """检查用户是否为管理员"""
        return self.role == 'admin'
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    @classmethod
    def create_default_users(cls):
        """创建默认用户（仅在数据库为空时）"""
        admin_exists = cls.query.filter_by(username='admin').first()
        user1_exists = cls.query.filter_by(username='user1').first()
        
        if not admin_exists:
            admin_user = cls(username='admin', role='admin')
            admin_user.set_password('admin123')
            db.session.add(admin_user)
        
        if not user1_exists:
            regular_user = cls(username='user1', role='user')
            regular_user.set_password('user123')
            db.session.add(regular_user)
        
        db.session.commit()