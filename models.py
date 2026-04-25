from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='student')  # admin / teacher /student
    sub_role = db.Column(db.String(30), nullable=True) # lead_teacher / assistant (仅当role='teacher'时有值)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    def set_password(self, password):
        """设置密码哈希"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """检查密码"""
        return check_password_hash(self.password_hash, password)
    
    # 身份判断方法
    def is_admin(self):
        """检查用户是否为管理员"""
        return self.role == 'admin'
    
    def is_lead_teacher(self):
        return self.role == 'teacher' and self.sub_role == 'lead_teacher'
    
    def is_assistant(self):
        return self.role == 'teacher' and self.sub_role == 'assistant'
    
    def is_sutdent(self):
        return self.role == 'student'
    
    # 显示角色标识
    def get_role_display(self):
        if self.role == 'teacher':
            return f'教师 - {"主讲教师" if self.sub_role == "lead_teacher" else "助教"}'
        elif self.role == 'admin':
            return '管理员'
        else:
            return '学生'

    def __repr__(self):
        return f'<User {self.username}>'
    
    @classmethod
    def create_default_users(cls):
        """创建默认用户（仅在数据库为空时）"""
        defaults = [
            ('admin', 'admin123', 'admin', None),
            ('teacher_lead', 'teacher123', 'teacher', 'lead_teacher'),
            ('teacher_assist', 'assist123', 'teacher', 'assistant'),
            ('student1', 'student123', 'student', None),
        ]
        for uname, pwd, role, sub in defaults:
            if not cls.query.filter_by(username=uname).first():
                user = cls(username=uname, role=role, sub_role=sub)
                user.set_password(pwd)
                db.session.add(user)
        db.session.commit()

# 职能分离冲突检查函数
def validate_role_assignment(user, new_role, new_sub_role):
    """
    检查角色分配是否违反静态职能分离约束。
    返回 (is_valid, message)
    """
    # 管理员不能拥有子角色（即不能兼任教师）
    if new_role == 'admin' and new_sub_role is not None:
        return False, '管理员不能兼任主讲教师或助教。'

    # 学生不能拥有任何子角色
    if new_role == 'student' and new_sub_role is not None:
        return False, '学生不能担任助教或主讲教师。'

    # 教师必须选择一个有效的子角色，且不能为 None
    if new_role == 'teacher':
        if new_sub_role not in ['lead_teacher', 'assistant']:
            return False, '教师角色必须指定为主讲教师或助教。'
    else:
        # 非教师角色，子角色必须为 None
        if new_sub_role is not None:
            return False, f'{new_role} 角色不能拥有子角色。'

    return True, ''