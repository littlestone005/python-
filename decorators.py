from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user

def role_required(*allowed_roles):
    """
    允许的角色标识：
    - 'admin'
    - 'lead_teacher'
    - 'assistant'
    - 'student'
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('请先登录。', 'error')
                return redirect(url_for('login'))

            # 计算出当前用户的角色标识
            if current_user.role == 'teacher':
                user_role_id = current_user.sub_role  # 'lead_teacher' 或 'assistant'
            else:
                user_role_id = current_user.role       # 'admin' 或 'student'

            if user_role_id not in allowed_roles:
                flash('您没有权限访问此页面。', 'error')
                return redirect(url_for('dashboard'))

            return f(*args, **kwargs)
        return decorated_function
    return decorator