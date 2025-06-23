from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from ersapp.models import CustomUser,Employees,empeducation,empexperience,Lead,LeadRemark,LeaveRequest,Attendance
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
User = get_user_model()
from django.db.models import Q  # Import the Q object
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
import logging
from django.http import JsonResponse



login_required(login_url='/')
def ADMIN_PROFILE(request):
    user = CustomUser.objects.get(id = request.user.id)
    context = {
        "user":user,
    }
    return render(request,'admin/admin_profile.html',context)
@login_required(login_url = '/')
def ADMIN_PROFILE_UPDATE(request):
    if request.method == "POST":
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        print(profile_pic)
        

        try:
            customuser = CustomUser.objects.get(id = request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            

            
            if profile_pic !=None and profile_pic != "":
               customuser.profile_pic = profile_pic
            customuser.save()
            messages.success(request,"Your profile has been updated successfully")
            return redirect('admin_profile')

        except:
            messages.error(request,"Your profile updation has been failed")
    return render(request, 'admin/admin_profile.html')


@login_required(login_url='/')
def ALL_EMPLOYEES(request):
    query = request.GET.get('q')

    if query:
        emp_list = Employees.objects.filter(
            Q(admin__first_name__icontains=query) |
            Q(admin__last_name__icontains=query) |
            Q(admin__email__icontains=query)
        )
    else:
        emp_list = Employees.objects.all()

    paginator = Paginator(emp_list, 10)  # Show 10 employees per page

    page_number = request.GET.get('page')
    try:
        emplist = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        emplist = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        emplist = paginator.page(paginator.num_pages)

    context = {'emplist': emplist}
    return render(request, 'admin/all_employees.html', context)



login_required(login_url='/')
def VIEW_EMP_PROFILE(request,id):    
    emp = Employees.objects.get(id =id)    
    context = {
        
        "emp":emp,
    }
    return render(request,'admin/update_emp_profile.html',context)

def UPDATE_EMPLOYEES_PROFILE(request):
    if request.method == 'POST':
        try:
            empid = request.POST.get('empid')
            emp = Employees.objects.get(admin_id=empid)
            customuser = CustomUser.objects.get(id=empid)
            # Update user data
            customuser.first_name = request.POST.get('first_name', customuser.first_name)
            customuser.last_name = request.POST.get('last_name', customuser.last_name)
            if 'profile_pic' in request.FILES:
                customuser.profile_pic = request.FILES['profile_pic']
            customuser.save()
            # Update employee data
            emp.mobilenumber = request.POST.get('mobilenumber', emp.mobilenumber)
            emp.gender = request.POST.get('gender', emp.gender)
            emp.empcode = request.POST.get('empcode', emp.empcode)
            emp.empdept = request.POST.get('empdept', emp.empdept)
            emp.gender = request.POST.get('gender', emp.gender)
            emp.empdesignation = request.POST.get('empdesignation', emp.empdesignation)
            emp.address = request.POST.get('address', emp.address)
            emp.save()
            
            messages.success(request, "Employee detail has been updated successfully")
            return redirect('all_employees')
        except:
            messages.error(request, "Failed to update employee detail")
            return redirect('all_employees')  # Redirect to an appropriate page
    return render(request, 'admin/update_emp_profile.html')


login_required(login_url='/')
def VIEW_EMP_EDUCATION(request, admin_id):
    try:
        emp_edu = empeducation.objects.get(empid=admin_id)
        context = {"emp_edu": emp_edu}
        return render(request, 'admin/view_emp_education.html', context)
    except ObjectDoesNotExist:
        messages.error(request, "Education data does not exist for the provided ID.")
        return redirect('all_employees')



login_required(login_url='/')
def UPDATE_EMPLOYEES_EDUCATION(request):
    if request.method == "POST":
        employee_id = request.POST.get('employee_id')
        CoursePG = request.POST.get('CoursePG')
        SchoolCollegePG = request.POST.get('SchoolCollegePG')
        YearPassingPG = request.POST.get('YearPassingPG')
        PercentagePG = request.POST.get('PercentagePG')
        CourseGra = request.POST.get('CourseGra')
        SchoolCollegeGra = request.POST.get('SchoolCollegeGra')
        YearPassingGra = request.POST.get('YearPassingGra')
        PercentageGra = request.POST.get('PercentageGra')
        CourseSSC = request.POST.get('CourseSSC')
        SchoolCollegeSSC = request.POST.get('SchoolCollegeSSC')
        YearPassingSSC = request.POST.get('YearPassingSSC')
        PercentageSSC = request.POST.get('PercentageSSC')
        CourseHSC = request.POST.get('CourseHSC')
        SchoolCollegeHSC = request.POST.get('SchoolCollegeHSC')
        YearPassingHSC = request.POST.get('YearPassingHSC')
        PercentageHSC = request.POST.get('PercentageHSC')
        
        # Retrieve the employee education object
        employeeedu = empeducation.objects.get(empid_id=employee_id)
        
        # Update the fields
        employeeedu.CoursePG = CoursePG
        employeeedu.SchoolCollegePG = SchoolCollegePG
        employeeedu.YearPassingPG = YearPassingPG
        employeeedu.PercentagePG = PercentagePG
        employeeedu.CourseGra = CourseGra
        employeeedu.SchoolCollegeGra = SchoolCollegeGra
        employeeedu.YearPassingGra = YearPassingGra
        employeeedu.PercentageGra = PercentageGra
        employeeedu.CourseSSC = CourseSSC
        employeeedu.SchoolCollegeSSC = SchoolCollegeSSC
        employeeedu.YearPassingSSC = YearPassingSSC
        employeeedu.PercentageSSC = PercentageSSC
        employeeedu.CourseHSC = CourseHSC
        employeeedu.SchoolCollegeHSC = SchoolCollegeHSC
        employeeedu.YearPassingHSC = YearPassingHSC
        employeeedu.PercentageHSC = PercentageHSC
        
        # Save the changes
        employeeedu.save()
        
        # Add a success message
        messages.success(request, "Education details have been updated successfully")
        
        # Redirect to the view page
        return redirect('all_employees')

    return render(request, 'admin/view_emp_education.html')





def VIEW_EMP_EXPERIENCE(request, admin_id):
    try:
        emp_exp = empexperience.objects.get(empid=admin_id)
        context = {"emp_exp": emp_exp}
        return render(request, 'admin/emp_experience_view.html', context)
    except ObjectDoesNotExist:
        messages.error(request, "Experience data does not exist for the provided ID.")
        return redirect('all_employees') 



login_required(login_url='/')
def UPDATE_EMPLOYEES_EXPERIENCE(request):
    if request.method == "POST":
        employee_id = request.POST.get('employee_id')
        Employer1Name=request.POST.get('Employer1Name')
        Employer1Designation=request.POST.get('Employer1Designation')
        Employer1CTC=request.POST.get('Employer1CTC')
        Employer1WorkDuration=request.POST.get('Employer1WorkDuration')
        Employer2Name=request.POST.get('Employer2Name')
        Employer2Designation=request.POST.get('Employer2Designation')
        Employer2CTC=request.POST.get('Employer2CTC')
        Employer2WorkDuration=request.POST.get('Employer2WorkDuration')
        Employer3Name=request.POST.get('Employer3Name')
        Employer3Designation=request.POST.get('Employer3Designation')
        Employer3CTC=request.POST.get('Employer3CTC')
        Employer3WorkDuration=request.POST.get('Employer3WorkDuration')
        
        employee_exp = empexperience.objects.get(empid=employee_id)
        
        # Update the fields
        employee_exp.Employer1Name=Employer1Name
        employee_exp.Employer1Designation=Employer1Designation
        employee_exp.Employer1CTC=Employer1CTC
        employee_exp.Employer1WorkDuration=Employer1WorkDuration
        employee_exp.Employer2Name=Employer2Name
        employee_exp.Employer2Designation=Employer2Designation
        employee_exp.Employer2CTC=Employer2CTC
        employee_exp.Employer2WorkDuration=Employer2WorkDuration
        employee_exp.Employer3Name=Employer3Name
        employee_exp.Employer3Designation=Employer3Designation
        employee_exp.Employer3CTC=Employer3CTC
        employee_exp.Employer3WorkDuration=Employer3WorkDuration
    
     # Save the changes
        employee_exp.save()
        
        # Add a success message
        messages.success(request, "Experience details have been updated successfully")
        
        # Redirect to the view page
        return redirect('all_employees')

    return render(request, 'emp_exp_view.html')


def DELETE_EMPLOYEES_DETAILS(request, admin_id):
    try:
        emp_edu = empeducation.objects.get(empid=admin_id)
        emp_edu.delete()
    except ObjectDoesNotExist:
        pass  # If record doesn't exist, just continue

    try:
        emp_exp = empexperience.objects.get(empid=admin_id)
        emp_exp.delete()
    except ObjectDoesNotExist:
        pass  # If record doesn't exist, just continue

    try:
        emp = Employees.objects.get(admin_id=admin_id)
        emp.delete()
    except ObjectDoesNotExist:
        pass  # If record doesn't exist, just continue

    try:
        customuser = CustomUser.objects.get(id=admin_id)
        customuser.delete()
    except ObjectDoesNotExist:
        pass  # If record doesn't exist, just continue

    messages.success(request, 'Record Deleted Successfully!!!')

    return redirect('all_employees')




#add_lead
def add_lead(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        contact_number = request.POST['contact_number']
        city = request.POST['city']
        state = request.POST['state']
        source = request.POST['source']
        services = request.POST['services']
        assigned_user_id = request.POST['assigned_user']

        # Validate contact number length
        if len(contact_number) != 10 or not contact_number.isdigit():
            messages.error(request, 'Contact number must be exactly 10 digits.')
            return render(request, 'admin/add_lead.html', {
                'users': Employees.objects.all()
            })

        try:
            assigned_user = None
            if assigned_user_id:
                assigned_user = Employees.objects.get(id=assigned_user_id)
            Lead.objects.create(
                name=name,
                email=email,
                contact_number=contact_number,
                city=city,
                state=state,
                source=source,
                services=services,
                assigned_user=assigned_user
            )
            messages.success(request, 'Lead added successfully!')
            return redirect('add_lead')
        except Employees.DoesNotExist:
            messages.error(request, 'Invalid Employee selected.')
            return render(request, 'admin/add_lead.html', {
                'users': Employees.objects.all()
            })

    # GET request: Render the form with the list of employees
    return render(request, 'admin/add_lead.html', {'users': Employees.objects.all()})



#manage lead
def manage_lead(request):
    query = request.GET.get('q')
    leads = Lead.objects.all()

    if query:
        leads = leads.filter(
            Q(name__icontains=query) | Q(email__icontains=query) | Q(city__icontains=query)
        )

    paginator = Paginator(leads, 10)  # Show 10 leads per page
    page_number = request.GET.get('page')
    leads = paginator.get_page(page_number)

    context = {
        'leads': leads,
    }
    return render(request, 'admin/manage_lead.html', context)


#edit lead
def edit_lead(request, id):
    lead = get_object_or_404(Lead, id=id)

    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        contact_number = request.POST['contact_number']
        city = request.POST['city']
        state = request.POST['state']
        source = request.POST['source']
        services = request.POST['services']
        assigned_user_id = request.POST['assigned_user']

        # Validate contact number length
        if len(contact_number) != 10 or not contact_number.isdigit():
            messages.error(request, 'Contact number must be exactly 10 digits.')
            return render(request, 'admin/edit_lead.html', {
                'lead': lead,
                'users': Employees.objects.all()
            })

        lead.name = name
        lead.email = email
        lead.contact_number = contact_number
        lead.city = city
        lead.state = state
        lead.source = source
        lead.services = services

        try:
            if assigned_user_id:
                assigned_user = Employees.objects.get(id=assigned_user_id)
                lead.assigned_user = assigned_user
            else:
                lead.assigned_user = None

            lead.save()
            messages.success(request, 'Lead updated successfully!')
            return redirect('manage_lead')
        except Employees.DoesNotExist:
            messages.error(request, 'Invalid Employee selected.')
            return render(request, 'admin/edit_lead.html', {
                'lead': lead,
                'users': Employees.objects.all()
            })
    else:
        return render(request, 'admin/edit_lead.html', {
            'lead': lead,
            'users': Employees.objects.all()
        })

# delete lead
def delete_lead(request, id):
    lead = get_object_or_404(Lead, id=id)
    lead.delete()  # Delete the lead from the database
    return redirect('manage_lead') 


# lead_status 
CALL_CONNECT_STATUS_CHOICES = [
    ('connected', 'Connected'),
    ('not_connected', 'Not Connected'),
    ('follow_up', 'Follow Up'),
]

def lead_status(request):
    remarks = LeadRemark.objects.all()
    query = request.GET.get('q')
    
    if query:
        choice_map = {value.lower(): key for key, value in CALL_CONNECT_STATUS_CHOICES}
        if query.lower() in [v.lower() for v in dict(CALL_CONNECT_STATUS_CHOICES).values()]:
            remarks = remarks.filter(
                Q(lead_name__icontains=query) | 
                Q(employee__admin__first_name__icontains=query) | 
                Q(employee__admin__last_name__icontains=query) | 
                Q(call_connect_status__in=[k for k, v in CALL_CONNECT_STATUS_CHOICES if v.lower() == query.lower()])
            )
        else:
            remarks = remarks.filter(
                Q(lead_name__icontains=query) | 
                Q(employee__admin__first_name__icontains=query) | 
                Q(employee__admin__last_name__icontains=query) | 
                Q(call_connect_status__icontains=query)
            )
        if not remarks.exists():
            messages.warning(request, "Search result not found.")

    # Pagination (outside the if block)
    paginator = Paginator(remarks, 10)
    page_number = request.GET.get('page')
    remarks_page = paginator.get_page(page_number)

    return render(request, 'admin/lead_status.html', {
        'remarks': remarks_page,
        'request': request,  # Added for pagination with search query
    })

#delete lead_status
def delete_lead_remark(request, remark_id):
    remark = get_object_or_404(LeadRemark, id=remark_id)
    
    if request.method == 'POST':
        remark.delete()
        messages.success(request, "Lead remark deleted successfully.")
        return redirect('lead_status')
    
    messages.error(request, "Failed to delete lead remark.")
    return redirect('lead_status')


def leave_request_list(request):
    if not request.user.is_staff:
        return redirect('no_access')
    
    # Fetch all leave requests, ordered by creation date
    leave_requests = LeaveRequest.objects.all().order_by('-created_at')
    
    # Filter by employee name if search query exists
    search_query = request.GET.get('q', '')
    if search_query:
        leave_requests = leave_requests.filter(user__username__icontains=search_query)
    
    # Pagination
    paginator = Paginator(leave_requests, 10)  # Show 10 requests per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'admin/leave_request_list.html', {
        'leave_requests': page_obj,
        'request': request  # Pass request object for template to access GET parameters
    })

@login_required
def update_leave_request_status(request, leave_request_id):
    if not request.user.is_staff:
        return redirect('no_access')
    
    try:
        # Fetch the specific leave request by ID
        leave_request = LeaveRequest.objects.get(id=leave_request_id)
    except LeaveRequest.DoesNotExist:
        # Handle case where leave request doesn't exist
        leave_requests = LeaveRequest.objects.all().order_by('-created_at')
        paginator = Paginator(leave_requests, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'admin/leave_request_list.html', {
            'leave_requests': page_obj,
            'request': request,
            'error': 'Leave request not found.'
        })
    
    if request.method == 'POST':
        # Get the new status from the form submission
        status = request.POST.get('status')
        if status in dict(LeaveRequest.STATUS_CHOICES):  # Validate status
            leave_request.status = status
            leave_request.save()
            return redirect('admin_leave_request_list')
        else:
            leave_requests = LeaveRequest.objects.all().order_by('-created_at')
            paginator = Paginator(leave_requests, 10)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            return render(request, 'admin/leave_request_list.html', {
                'leave_requests': page_obj,
                'request': request,
                'error': 'Invalid status selected.'
            })
    
    # If not POST, just show the list again
    leave_requests = LeaveRequest.objects.all().order_by('-created_at')
    paginator = Paginator(leave_requests, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'admin/leave_request_list.html', {
        'leave_requests': page_obj,
        'request': request
    })
@login_required
def no_access(request):
    return render(request, 'no_access.html')


# Attendance Records
# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@login_required(login_url='/')
def attendance_record(request):
    if not request.user.is_staff:  # Restrict to admins only
        return redirect('no_access')

    # Fetch all attendance records
    attendance_list = Attendance.objects.all().order_by('-date', '-marked_at')

    # Implement search functionality
    query = request.GET.get('q')
    if query:
        attendance_list = attendance_list.filter(
            Q(employee__admin__first_name__icontains=query) |
            Q(employee__admin__last_name__icontains=query) |
            Q(employee__empcode__icontains=query) |
            Q(date__icontains=query)
        )
        if not attendance_list.exists():
            messages.warning(request, "No attendance records found for your search.")

    # Reverse geocode latitude/longitude to human-readable location
    geolocator = Nominatim(user_agent="attendance_admin_panel")
    for record in attendance_list:
        if record.latitude and record.longitude:
            try:
                location = geolocator.reverse((record.latitude, record.longitude), timeout=10)
                record.location_name = location.address if location else "Unknown location"
            except (GeocoderTimedOut, GeocoderUnavailable) as e:
                logger.error(f"Geocoding error for lat={record.latitude}, lon={record.longitude}: {str(e)}")
                record.location_name = "Geocoding service unavailable"
        else:
            record.location_name = "Location not available"

    # Pagination
    paginator = Paginator(attendance_list, 10)  # Show 10 records per page
    page_number = request.GET.get('page')
    try:
        attendance_page = paginator.page(page_number)
    except PageNotAnInteger:
        attendance_page = paginator.page(1)
    except EmptyPage:
        attendance_page = paginator.page(paginator.num_pages)

    context = {
        'attendance_records': attendance_page,
        'request': request  # Pass request object for template to access GET parameters
    }
    return render(request, 'admin/attendance_record.html', context)


# follow up
def edit_remark(request, remark_id):
    remark = get_object_or_404(LeadRemark, id=remark_id)
    employees = Employees.objects.all()

    if request.method == 'POST':
        employee_id = request.POST.get('employee')
        selected_employee = Employees.objects.get(id=employee_id) if employee_id else None

        if selected_employee:
            remark.employee = selected_employee
            remark.save()

            lead = remark.lead
            lead.assigned_user = selected_employee
            lead.save()

            return JsonResponse({'success': True, 'message': 'Remark updated successfully.'})

        return JsonResponse({'success': False, 'message': 'Please select an employee to assign.'})

    context = {'remark': remark, 'employees': employees}
    return render(request, 'admin/edit_remark.html', context)

def edit_remark_redirect(request):
    messages.error(request, "Please select a remark to edit.")
    return redirect('lead_status')