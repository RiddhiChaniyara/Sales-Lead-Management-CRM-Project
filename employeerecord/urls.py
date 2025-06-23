from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .import views, adminviews, empviews



urlpatterns = [
    path('admin/', admin.site.urls),
    path('base/', views.BASE, name='base'),
    path('', views.LOGIN, name='login'),
    path('doLogin', views.doLogin, name='doLogin'),
    path('doLogout', views.doLogout, name='logout'),
    path('Dashboard', views.dashboard_view, name='dashboard'),
    path('Password', views.CHANGE_PASSWORD, name='change_password'),
    path('add-todo/', views.add_todo, name='add_todo'),
    path('delete_todo/', views.delete_todo, name='delete_todo'),

    #Admin Panel
    path('AdminProfile', adminviews.ADMIN_PROFILE, name='admin_profile'),
    path('AdminProfile/update', adminviews.ADMIN_PROFILE_UPDATE, name='admin_profile_update'),
    path('AllEmployees', adminviews.ALL_EMPLOYEES, name='all_employees'),
    path('ViewEmpProfile/<str:id>', adminviews.VIEW_EMP_PROFILE, name='view_emp_profile'),
    path('UpdateEmployeeProfile', adminviews.UPDATE_EMPLOYEES_PROFILE, name='update_emp_profile'),
    path('ViewEmpEducation/<int:admin_id>/', adminviews.VIEW_EMP_EDUCATION, name='view_emp_education'),
    path('UpdateEmployeeEducation', adminviews.UPDATE_EMPLOYEES_EDUCATION, name='update_emp_education'),
    path('ViewEmpExperience/<int:admin_id>/', adminviews.VIEW_EMP_EXPERIENCE, name='view_emp_experience'),
    path('UpdateEmployeeExperience', adminviews.UPDATE_EMPLOYEES_EXPERIENCE, name='update_emp_experience'),
    path('DeleteEmployee/<int:admin_id>/', adminviews.DELETE_EMPLOYEES_DETAILS, name='delete_employee_details'),
    path('add_lead/', adminviews.add_lead, name='add_lead'),
    path('manage_lead/', adminviews.manage_lead, name='manage_lead'),
    path('edit_lead/<int:id>/', adminviews.edit_lead, name='edit_lead'),
    path('delete_lead/<int:id>/', adminviews.delete_lead, name='delete_lead'),
    path('lead_status/',adminviews.lead_status, name='lead_status'),
    path('delete-remark/<int:remark_id>/', adminviews.delete_lead_remark, name='delete_remark'),
    path('admin_leave_request_list/', adminviews.leave_request_list, name='admin_leave_request_list'),
    path('update_leave_request_status/<int:leave_request_id>/', adminviews.update_leave_request_status, name='update_leave_request_status'),
    path('no_access/', adminviews.no_access, name='no_access'),
    path('attendance_record/', adminviews.attendance_record, name='attendance_record'),
    path('edit_remark/<int:remark_id>/', adminviews.edit_remark, name='edit_remark'),
    path('edit_remark/', adminviews.edit_remark_redirect, name='edit_remark_invalid'),
     

  
    
        
    

    #Employee Panel
    path('empsignup/', empviews.EMPSIGNUP, name='empsignup'),
    path('EmployeeProfile', empviews.EMP_PROFILE, name='emp_profile'),
    path('EmployeeProfile/update', empviews.EMP_PROFILE_UPDATE, name='emp_profile_update'),
    path('EmployeeEducation', empviews.EMP_EDUCATION, name='emp_education'),
    path('EmployeeExperience', empviews.EMP_EXPERIENCE, name='emp_exp'),
    path('EmployeeEducationView', empviews.EMP_EDUCATION_VIEW, name='emp_education_view'),
    path('EmployeeEducationDetails', empviews.UPDATE_EMPLOYEE_EDUCATIONS, name='update_employeeedu_details'),
    path('EmployeeExperienceView', empviews.EMP_EXPERIENCE_VIEW, name='emp_experience_view'),
    path('EmployeeExperienceDetails', empviews.UPDATE_EMP_EXPERIENCE, name='update_emp_experience'),
    path('today_leads/', empviews.today_leads, name='today_leads'),
    path('lead_details/<int:lead_id>/', empviews.lead_details, name='lead_details'),


    path('register_face/', empviews.register_face, name='register_face'),
    path('mark_attendance/', empviews.mark_attendance, name='mark_attendance'),

    path('submit_leave_request/', empviews.submit_leave_request, name='submit_leave_request'),
    path('leave_request_list/', empviews.leave_request_list, name='employee_leave_request_list'),
    path('edit_leave_request/<int:request_id>/', empviews.edit_leave_request, name='edit_leave_request'),
    path('delete_leave_request/<int:request_id>/', empviews.delete_leave_request, name='delete_leave_request'),

    path('services/', empviews.services, name='services'),

    path('services/', empviews.services, name='services'),
    path('seo/', empviews.seo, name='seo'),
    path('website_development/', empviews.website_development, name='website_development'),
    path('android_development/', empviews.android_development, name='android_development'),
    path('logo_design/', empviews.logo_design, name='logo_design'),
    path('content_writing/', empviews.content_writing, name='content_writing'),
    path('domain_hosting/', empviews.domain_hosting, name='domain_hosting'),
    path('ui_ux_design/', empviews.ui_ux_design, name='ui_ux_design'),
    path('erp_development/', empviews.erp_development, name='erp_development'),
    
    
  
]+static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
