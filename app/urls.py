from app import app

from . import views

app.add_url_rule('/', view_func=views.index)
app.add_url_rule('/student', view_func=views.student_view)
app.add_url_rule('/course', view_func=views.course_view)

app.add_url_rule('/admin/course/add', view_func=views.course_add, methods=['POST', 'GET'])
app.add_url_rule('/admin/student/add', view_func=views.student_add, methods=['POST', 'GET'])
app.add_url_rule('/admin/course/<int:course_id>/update', view_func=views.admin_course_update, methods=['POST', 'GET'])
app.add_url_rule('/admin/course/<int:course_id>/delete', view_func=views.admin_course_delete, methods=['POST', 'GET'])
app.add_url_rule('/admin/student/<int:student_id>/update', view_func=views.admin_student_update, methods=['POST', 'GET'])
app.add_url_rule('/admin/student/<int:student_id>/delete', view_func=views.admin_student_delete, methods=['POST', 'GET'])





app.add_url_rule('/account/register', view_func=views.user_register, methods=['POST', 'GET'])
app.add_url_rule('/account/login', view_func=views.user_login, methods=['POST', 'GET'])
app.add_url_rule('/account/logout', view_func=views.user_logout)