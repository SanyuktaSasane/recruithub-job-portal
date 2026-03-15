from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("view-jobs/", views.view_jobs, name="view_jobs"),
    path("apply/<int:job_id>/", views.apply_job, name="apply_job"),
    path("applications/", views.view_applications, name="view_applications"),
    path("candidate/dashboard/", views.candidate_dashboard, name="candidate_dashboard"),
    path("company/dashboard/", views.company_dashboard, name="company_dashboard"),
    path("create-job/", views.create_job, name="create_job"),
    path("view_application/<int:app_id>/<str:status>/", 
     views.update_application_status, 
     name="update_application_status"),
     path("my-applications/", views.my_applications, name="my_applications"),
     path("delete-job/<int:job_id>/", views.delete_job, name="delete_job"),
     path("schedule-interview/<int:app_id>/", views.schedule_interview, name="schedule_interview"),

]

