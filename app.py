from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models import db, User, validate_role_assignment
from config import Config
from decorators import role_required

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # 初始化扩展
    db.init_app(app)
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    login_manager.login_message = '请先登录以访问此页面。'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # 基础页面
    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            
            user = User.query.filter_by(username=username).first()
            
            if user and user.check_password(password):
                login_user(user)
                flash(f'欢迎回来，{username}！', 'success')
                
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('dashboard'))
            else:
                flash('用户名或密码错误！', 'error')
        
        return render_template('login.html')
    
    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        flash('您已成功退出登录。', 'info')
        return redirect(url_for('index'))
    
    # 用户注册
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))

        if request.method == 'POST':
            username = request.form.get('username', '').strip()
            password = request.form.get('password', '').strip()
            confirm = request.form.get('confirm', '').strip()

            # 基本校验
            if not username or not password:
                flash('用户名和密码不能为空。', 'error')
            elif password != confirm:
                flash('两次输入的密码不一致。', 'error')
            elif len(password) < 6:
                flash('密码长度不能少于6位。', 'error')
            elif User.query.filter_by(username=username).first():
                flash('用户名已存在，请更换。', 'error')
            else:
                # 新用户默认角色为学生，无子角色
                new_user = User(username=username, role='student', sub_role=None)
                new_user.set_password(password)
                db.session.add(new_user)
                db.session.commit()
                flash('注册成功，请登录。', 'success')
                return redirect(url_for('login'))

        return render_template('register.html')
    
    # 仪表盘分发
    @app.route('/dashboard')
    @login_required
    def dashboard():
        if current_user.role == 'admin':
            return redirect(url_for('admin_dashboard'))
        elif current_user.role == 'teacher':
            if current_user.sub_role == 'lead_teacher':
                return redirect(url_for('lead_teacher_dashboard'))
            elif current_user.sub_role == 'assistant':
                return redirect(url_for('assistant_dashboard'))
        else:  # student
            return redirect(url_for('student_dashboard'))
    
    # 各角色面板
    @app.route('/admin')
    @login_required
    @role_required('admin')
    def admin_dashboard():
        all_users = User.query.all()
        return render_template('admin.html', users=all_users)

    @app.route('/admin/update_role', methods=['POST'])
    @login_required
    @role_required('admin')
    def update_role():
        user_id = request.form.get('user_id')
        new_role = request.form.get('role')
        new_sub_role = request.form.get('sub_role') or None  # 空字符串视为 None

        user = User.query.get(int(user_id))
        if not user:
            flash('用户不存在。', 'error')
            return redirect(url_for('admin_dashboard'))

        if user.id == current_user.id:
            flash('不能修改自己的角色。', 'error')
            return redirect(url_for('admin_dashboard'))

        # 静态职能分离校验
        is_valid, msg = validate_role_assignment(user, new_role, new_sub_role)
        if not is_valid:
            flash(f'角色冲突：{msg}', 'error')
            return redirect(url_for('admin_dashboard'))

        # 执行更新
        user.role = new_role
        user.sub_role = new_sub_role if new_role == 'teacher' else None
        db.session.commit()
        flash(f'已成功将 {user.username} 的角色更新为 {user.get_role_display()}。', 'success')
        return redirect(url_for('admin_dashboard'))

    @app.route('/teacher/lead')
    @login_required
    @role_required('lead_teacher')
    def lead_teacher_dashboard():
        return render_template('lead_teacher.html')

    @app.route('/teacher/assistant')
    @login_required
    @role_required('assistant')
    def assistant_dashboard():
        return render_template('assistant.html')

    @app.route('/student')
    @login_required
    @role_required('student')
    def student_dashboard():
        return render_template('student.html')

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='127.0.0.1', port=5000)