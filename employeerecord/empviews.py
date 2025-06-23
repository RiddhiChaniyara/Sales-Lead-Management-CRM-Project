from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.decorators import login_required
from ersapp.models import CustomUser,Employees,empeducation,empexperience,Lead,LeadRemark,Attendance,RegisteredFace,LeaveRequest
from .forms import LeaveRequestForm
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
from django.http import JsonResponse
import cv2
import numpy as np
import base64
from datetime import datetime
import os
from geopy.geocoders import Nominatim  # Import geopy for reverse geocoding
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
User = get_user_model()




def EMPSIGNUP(request):
    if request.method == "POST":
        pic = request.FILES.get('pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        mobno = request.POST.get('mobno')        
        password = request.POST.get('password')

        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request, 'Email already exists')
            return redirect('empsignup')
        if CustomUser.objects.filter(username=username).exists():
            messages.warning(request, 'Username already exists')
            return redirect('empsignup')

        # Set default profile image if not uploaded
        if not pic:
            pic = 'media/profile_pic/default.jpg'  # Ensure this file exists

        user = CustomUser(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            user_type=2,
            profile_pic=pic,
        )
        user.set_password(password)
        user.save()

        emp = Employees(
            admin=user,
            mobilenumber=mobno,
        )
        emp.save()

        messages.success(request, 'Signup Successfully')
        return redirect('empsignup')

    return render(request, 'employee/emp_reg.html')

login_required(login_url='/')
def EMP_PROFILE(request):
    
    emp =Employees.objects.get(admin_id =request.user.id)
    
    context = {
        
        "emp":emp,
    }
    return render(request,'employee/emp_profile.html',context)

@login_required(login_url = '/')
def EMP_PROFILE_UPDATE(request):
    if request.method == "POST":
        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            emp = Employees.objects.get(admin_id=request.user.id)

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

            messages.success(request, "Your profile has been updated successfully")
            return redirect('emp_profile')
        except ObjectDoesNotExist:
            messages.error(request, "User or employee profile not found")
        except IntegrityError:
            messages.error(request, "Employee code must be unique")
            return redirect('emp_profile')
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")

    return render(request, 'employee/emp_profile.html')

@login_required(login_url='/')
def EMP_EDUCATION(request):
    # Check if the user is authenticated
    if request.user.is_authenticated:
        if request.method == "POST":
            # Retrieve the Employees instance associated with the current user
            employee = Employees.objects.get(admin_id=request.user.id)
            custom_user = employee.admin
            # Create an instance of EmpEducation and assign the admin attribute of the Employees instance to the empid field
            empedu = empeducation(
                CoursePG=request.POST.get('CoursePG'),
                SchoolCollegePG=request.POST.get('SchoolCollegePG'),
                YearPassingPG=request.POST.get('YearPassingPG'),
                PercentagePG=request.POST.get('PercentagePG'),
                CourseGra=request.POST.get('CourseGra'),
                SchoolCollegeGra=request.POST.get('SchoolCollegeGra'),
                YearPassingGra=request.POST.get('YearPassingGra'),
                PercentageGra=request.POST.get('PercentageGra'),
                CourseSSC=request.POST.get('CourseSSC'),
                SchoolCollegeSSC=request.POST.get('SchoolCollegeSSC'),
                YearPassingSSC=request.POST.get('YearPassingSSC'),
                PercentageSSC=request.POST.get('PercentageSSC'),
                CourseHSC=request.POST.get('CourseHSC'),
                SchoolCollegeHSC=request.POST.get('SchoolCollegeHSC'),
                YearPassingHSC=request.POST.get('YearPassingHSC'),
                PercentageHSC=request.POST.get('PercentageHSC'),
                empid=custom_user  # Assign the Employees instance to the empid field
            )
            empedu.save()
           
            return redirect("emp_education")
        else:
            # Retrieve existing education details for the current user
            try:
                eedu = empeducation.objects.get(empid=request.user.id)
                context = {'eedu': eedu}
            except empeducation.DoesNotExist:
                context = {}  # If no education details found, pass an empty context
            return render(request, 'employee/myeducation.html', context)
    else:
        messages.error(request, 'You need to login to access this page.')
        return redirect('login')  # Redirect to the login page if the user is not authenticated

        
@login_required(login_url='/')
def EMP_EXPERIENCE(request):
    if request.method == "POST":
        # Check if the user is authenticated
        if request.user.is_authenticated:
            # Retrieve the Employees instance associated with the current user
            employee = Employees.objects.get(admin_id=request.user.id)
            # Retrieve the CustomUser instance associated with the Employees instance
            custom_user = employee.admin
            
            # Now create an instance of empexperience and assign the admin attribute of the Employees instance to the empid field
            empexp = empexperience(
                Employer1Name=request.POST.get('Employer1Name'),
                Employer1Designation=request.POST.get('Employer1Designation'),
                Employer1CTC=request.POST.get('Employer1CTC'),
                Employer1WorkDuration=request.POST.get('Employer1WorkDuration'),
                Employer2Name=request.POST.get('Employer2Name'),
                Employer2Designation=request.POST.get('Employer2Designation'),
                Employer2CTC=request.POST.get('Employer2CTC'),
                Employer2WorkDuration=request.POST.get('Employer2WorkDuration'),
                Employer3Name=request.POST.get('Employer3Name'),
                Employer3Designation=request.POST.get('Employer3Designation'),
                Employer3CTC=request.POST.get('Employer3CTC'),
                Employer3WorkDuration=request.POST.get('Employer3WorkDuration'),
                empid=custom_user  # Assign the CustomUser instance to the empid field
            )
            empexp.save()
            
            return redirect("emp_exp")
    else:
        if request.user.is_authenticated:
            # Retrieve existing experience details for the current user
            try:
                eexp = empexperience.objects.get(empid=request.user.id)
                context = {'eexp': eexp}
            except empexperience.DoesNotExist:
                context = {}  # If no experience details found, pass an empty context
            return render(request, 'employee/myexp.html', context)
        else:
            messages.error(request, 'You need to login to access this page.')
            return redirect('login')
      
  


@login_required(login_url='/')
def EMP_EDUCATION_VIEW(request):
    try:
        emp_edu = empeducation.objects.get(empid_id=request.user.id)
    except empeducation.DoesNotExist:
        # If the education data doesn't exist for the user, set emp_edu to None
        emp_edu = None

    context = {
        "emp_edu": emp_edu,
    }
    return render(request, 'employee/emp_education_view.html', context)

login_required(login_url='/')
def UPDATE_EMPLOYEE_EDUCATIONS(request):
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
        return redirect('emp_education_view')

    return render(request, 'employee/emp_education_view.html')



@login_required(login_url='/')
def EMP_EXPERIENCE_VIEW(request):
    try:
        emp_exp = empexperience.objects.get(empid_id=request.user.id)
    except empexperience.DoesNotExist:
        # If the experience data doesn't exist for the user, set emp_exp to None
        emp_exp = None

    context = {
        "emp_exp": emp_exp,
    }
    return render(request, 'employee/emp_exp_view.html', context)


login_required(login_url='/')
def UPDATE_EMP_EXPERIENCE(request):
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
        
        employee_exp = empexperience.objects.get(empid_id=employee_id)
        
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
        return redirect('emp_experience_view')

    return render(request, 'employee/emp_exp_view.html')


# today_leads
@login_required(login_url='/')
def today_leads(request):
    user = request.user

    try:
        employee = Employees.objects.get(admin=user)
    except Employees.DoesNotExist:
        employee = None

    # Show only the leads assigned to the currently logged-in employee
    leads = Lead.objects.filter(assigned_user=employee)

    # Get the list of lead IDs updated by the user from the session
    updated_leads = request.session.get('updated_leads', {})
    updated_leads_for_user = updated_leads.get(str(user.id), [])

    # Exclude leads updated by the current user
    leads = [lead for lead in leads if lead.id not in updated_leads_for_user]

    context = {'leads': leads}
    return render(request, 'employee/today_leads.html', context)


# lead_details
@login_required(login_url='/')
def lead_details(request, lead_id):
    # Fetch the lead details
    lead = get_object_or_404(Lead, id=lead_id)

    if request.method == 'POST':
        call_connect_status = request.POST.get('call_connect_status')
        remarks = request.POST.get('remarks')

        # Update lead details
        lead.call_connect_status = call_connect_status
        lead.remarks = remarks
        lead.save()

        # Get the logged-in employee
        employee = Employees.objects.filter(admin=request.user).first()

        if employee:
            # Store the remark in LeadRemark table, including lead details
            LeadRemark.objects.create(
                lead=lead,
                employee=employee,
                lead_name=lead.name,  # Store lead name in table
                lead_contact_number=lead.contact_number,  # Store lead contact in table
                remark=remarks,
                call_connect_status=call_connect_status  # Store call status
            )

            # Update the session to store the lead ID as updated by this user
            updated_leads = request.session.get('updated_leads', {})
            user_id = str(request.user.id)
            if user_id not in updated_leads:
                updated_leads[user_id] = []
            if lead.id not in updated_leads[user_id]:  # Prevent duplicate entries
                updated_leads[user_id].append(lead.id)
            request.session['updated_leads'] = updated_leads

        messages.success(request, f"Lead details updated successfully!")
        return redirect('lead_details', lead_id=lead.id) #or redirect('today_leads') depending on desired behavior

    context = {'lead': lead}
    return render(request, 'employee/lead_details.html', context)






#Attendance system for employees
@login_required(login_url='/')
@csrf_exempt
def register_face(request):
    if request.method == "POST":
        image_data = request.POST.get("image")
        if not image_data:
            return JsonResponse({"success": False, "error": "No image data provided."})

        # Decode base64 image
        try:
            format, imgstr = image_data.split(';base64,')
            ext = format.split('/')[-1]
            image_bytes = base64.b64decode(imgstr)
            nparr = np.frombuffer(image_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        except Exception as e:
            return JsonResponse({"success": False, "error": "Invalid image data."})

        # Load Haar Cascade for face detection
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        if len(faces) == 0:
            return JsonResponse({"success": False, "error": "No face detected. Please try again."})

        # Get the current employee
        try:
            employee = Employees.objects.get(admin_id=request.user.id)
        except Employees.DoesNotExist:
            return JsonResponse({"success": False, "error": "Employee not found."})

        # Check if face is already registered
        if RegisteredFace.objects.filter(employee=employee).exists():
            return JsonResponse({"success": False, "error": "Your face is already registered."})

        # Save face image with timestamp (auto_now_add handles this, but here's manual option if needed)
        new_face = RegisteredFace(employee=employee)
        new_face.image.save(f"face_{employee.empcode}.{ext}", ContentFile(image_bytes), save=True)

        # Optional: Manually set registered_at (uncomment if auto_now_add fails)
        # new_face.registered_at = timezone.now()
        # new_face.save()

        return JsonResponse({"success": True, "message": "Your face registered successfully!"})

    return render(request, 'employee/register_face.html')



# mark attendance
@login_required(login_url='/')
@csrf_exempt
def mark_attendance(request):
    if request.method == "POST":
        image_data = request.POST.get("image")
        latitude = request.POST.get("latitude")
        longitude = request.POST.get("longitude")

        if not image_data:
            return JsonResponse({"success": False, "error": "No image data provided."})

        # Decode base64 image
        try:
            format, imgstr = image_data.split(';base64,')
            ext = format.split('/')[-1]
            image_bytes = base64.b64decode(imgstr)
            nparr = np.frombuffer(image_bytes, np.uint8)
            captured_img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        except Exception as e:
            return JsonResponse({"success": False, "error": "Invalid image data."})

        # Load Haar Cascade for face detection
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        gray_captured = cv2.cvtColor(captured_img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray_captured, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        if len(faces) == 0:
            return JsonResponse({"success": False, "error": "No face detected. Please try again."})

        # Crop the detected face
        x, y, w, h = faces[0]
        captured_face = gray_captured[y:y+h, x:x+w]

        # Get the logged-in employee's registered faces
        employee = Employees.objects.get(admin=request.user)
        registered_faces = RegisteredFace.objects.filter(employee=employee)

        for reg_face in registered_faces:
            reg_img_path = reg_face.image.path
            reg_img = cv2.imread(reg_img_path, cv2.IMREAD_GRAYSCALE)
            reg_faces = face_cascade.detectMultiScale(reg_img, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
            if len(reg_faces) == 0:
                continue

            rx, ry, rw, rh = reg_faces[0]
            reg_face_crop = reg_img[ry:ry+rh, rx:rx+rw]
            captured_face_resized = cv2.resize(captured_face, (rw, rh))
            difference = cv2.absdiff(captured_face_resized, reg_face_crop)
            similarity_score = np.mean(difference)

            if similarity_score < 70:  # Threshold for match
                today = datetime.today().date()
                attendance, created = Attendance.objects.get_or_create(
                    employee=employee,
                    date=today,
                    defaults={
                        'marked_at': datetime.now(),
                        'latitude': float(latitude) if latitude else None,
                        'longitude': float(longitude) if longitude else None
                    }
                )
                if created:
                    # Reverse geocode latitude and longitude to get location name
                    location_name = "Unknown location"
                    if latitude and longitude:
                        try:
                            geolocator = Nominatim(user_agent="attendance_app")
                            location = geolocator.reverse((latitude, longitude), timeout=10)
                            location_name = location.address if location else "Unknown location"
                        except (GeocoderTimedOut, GeocoderUnavailable) as e:
                            location_name = "Geocoding service unavailable"

                    return JsonResponse({
                        "success": True,
                        "message": "Attendance successfully marked.",
                        "username": request.user.username,
                        "latitude": latitude,
                        "longitude": longitude,
                        "location_name": location_name  # Return the location name
                    })
                else:
                    return JsonResponse({"success": False, "error": "Attendance already marked for today."})

        return JsonResponse({"success": False, "error": "Your face is not matched, attendance failed!"})

    return render(request, 'employee/mark_attendance.html')





#leave for employee 
@login_required
def submit_leave_request(request):
    if request.method == 'POST':
        form = LeaveRequestForm(request.POST)
        if form.is_valid():
            leave_request = form.save(commit=False)
            leave_request.user = request.user
            leave_request.save()
            return redirect('employee_leave_request_list')  # Redirect to employee list
    else:
        form = LeaveRequestForm()
    
    return render(request, 'employee/leave_request_form.html', {'form': form})

@login_required
def leave_request_list(request):
    leave_requests = LeaveRequest.objects.filter(user=request.user)
    return render(request, 'employee/leave_request_list.html', {'leave_requests': leave_requests})

# edit leave
@login_required
def edit_leave_request(request, request_id):
    leave_request = get_object_or_404(LeaveRequest, id=request_id, user=request.user)
    if leave_request.status != 'pending':
        return redirect('employee_leave_request_list')
    
    if request.method == 'POST':
        form = LeaveRequestForm(request.POST, instance=leave_request)
        if form.is_valid():
            form.save()
            return redirect('employee_leave_request_list')
    else:
        form = LeaveRequestForm(instance=leave_request)
    
    return render(request, 'employee/leave_request_form.html', {'form': form, 'edit_mode': True})

# delete leave
@login_required
def delete_leave_request(request, request_id):
    leave_request = get_object_or_404(LeaveRequest, id=request_id, user=request.user)
    if leave_request.status != 'pending':
        return redirect('employee_leave_request_list')
    
    if request.method == 'POST':
        leave_request.delete()
        return redirect('employee_leave_request_list')
    
    return render(request, 'employee/leave_request_delete_confirm.html', {'leave_request': leave_request})

# Services
@login_required
def services(request):
    return render(request, 'employee/services.html')

def seo(request):
    return render(request, 'employee/seo.html')

def website_development(request):
    return render(request, 'employee/website_development.html')

def android_development(request):
    return render(request, 'employee/android_development.html')

def logo_design(request):
    return render(request, 'employee/logo_design.html')

def content_writing(request):
    return render(request, 'employee/content_writing.html')

def domain_hosting(request):
    return render(request, 'employee/domain_hosting.html')

def ui_ux_design(request):
    return render(request, 'employee/ui_ux_design.html')

def erp_development(request):
    return render(request, 'employee/erp_development.html')
