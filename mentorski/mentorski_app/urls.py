
from django.urls import path
from . import views
from django.conf.urls.static import static

urlpatterns = [ 
    path('login/', views.loginPg, name='login'),
    path('logout/', views.logoutPg, name='logout'),
# Mentor
    path('courses/', views.courses, name='courses'),
    path('delete_course/<int:pid>', views.delete_course, name='delete_course'),
    path('course_delete/<int:pid>', views.course_delete, name='course_delete'),
    path('add/', views.Add_course, name='add'),
    path('courses/<int:pid>', views.detail_course, name='detail_course'),
    path('edit_course/<int:pid>', views.edit_course, name='edit_course'),
    path('students/', views.students, name='students'),
# Students
    path('register/', views.register, name='register'),
    path('upisni_list/<int:kid>/', views.upisni_list, name='upisni_list'),
    path('add_subj/<int:pid>/<int:sid>/', views.add_subj, name='add_subj'),
    path('pass_subj/<int:pid>/<int:sid>', views.pass_subj, name='pass_subj'),
    path('remove_subj/<int:id>', views.remove_subj, name='remove_subj'),
    path('repeat_subj/<int:pid>/<int:sid>/', views.repeat_subj, name='repeat_subj'),
]