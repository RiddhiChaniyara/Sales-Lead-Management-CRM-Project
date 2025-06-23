from django.db import models
import datetime

from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    USER ={
        (1,'admin'),
        (2,'employee'),
        
    }
    user_type = models.CharField(choices=USER,max_length=50,default=1)

    profile_pic = models.ImageField(upload_to='media/profile_pic', default='media/profile_pic/default.jpg')


class Employees(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    mobilenumber = models.CharField(max_length=11)
    gender = models.CharField(max_length=100,default="0")
    empcode = models.CharField(max_length=20)
    empdept = models.CharField(max_length=100,default="0")
    empdesignation = models.CharField(max_length=150,default="0")
    address = models.CharField(max_length=250,default="0")
    joiningdate = models.CharField(max_length=200,default="0")
    regdate_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Field to store face encoding (as binary data) for face recognition
    # face_encoding = models.BinaryField(null=True, blank=True)

    def _str_(self):
        if self.admin:
            return f"{self.admin.first_name} {self.admin.last_name} - {self.mobilenumber} {self.empcode}"
        else:
            return f"User not associated - {self.mobilenumber} {self.empcode}"
        

class RegisteredFace(models.Model):
    employee = models.ForeignKey(Employees, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='faces/')
    registered_at = models.DateTimeField(auto_now_add=True)  
    

    def _str_(self):
        return f"Face of {self.employee.empcode}"

class Attendance(models.Model):
    employee = models.ForeignKey(Employees, on_delete=models.CASCADE)
    date = models.DateField(default=datetime.date.today)
    marked_at = models.DateTimeField(auto_now_add=True)
    latitude = models.FloatField(null=True, blank=True)  # Ensure these fields are present
    longitude = models.FloatField(null=True, blank=True)
    

    class Meta:
        unique_together = ('employee', 'date')

    def _str_(self):
        return f"{self.employee.empcode} - {self.date}"

class empeducation(models.Model):
    empid = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    CoursePG =models.CharField(max_length=200,default="0")
    SchoolCollegePG =models.CharField(max_length=200,default="0")
    YearPassingPG =models.CharField(max_length=200,default="0")
    PercentagePG =models.CharField(max_length=200,default="0")
    CourseGra =models.CharField(max_length=200,default="0")
    SchoolCollegeGra =models.CharField(max_length=200,default="0")
    YearPassingGra =models.CharField(max_length=200,default="0")
    PercentageGra =models.CharField(max_length=200,default="0")
    CourseSSC =models.CharField(max_length=200,default="0")
    SchoolCollegeSSC =models.CharField(max_length=200,default="0")
    YearPassingSSC =models.CharField(max_length=200,default="0")
    PercentageSSC =models.CharField(max_length=200,default="0")
    CourseHSC =models.CharField(max_length=200,default="0")
    SchoolCollegeHSC =models.CharField(max_length=200,default="0")
    YearPassingHSC =models.CharField(max_length=200,default="0")
    PercentageHSC =models.CharField(max_length=200,default="0")
    creationdate = models.DateTimeField(auto_now_add=True)

class empexperience(models.Model):
    empid = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    Employer1Name =models.CharField(max_length=200,default="0")
    Employer1Designation = models.CharField(max_length=200,default="0")
    Employer1CTC = models.CharField(max_length=200,default="0")
    Employer1WorkDuration =models.CharField(max_length=200,default="0")
    Employer2Name =models.CharField(max_length=200,default="0")
    Employer2Designation =models.CharField(max_length=200,default="0")
    Employer2CTC =models.CharField(max_length=200,default="0")
    Employer2WorkDuration =models.CharField(max_length=200,default="0")
    Employer3Name =models.CharField(max_length=200,default="0")
    Employer3Designation =models.CharField(max_length=200,default="0")
    Employer3CTC =models.CharField(max_length=200,default="0")
    Employer3WorkDuration =models.CharField(max_length=200,default="0")
    creationdate = models.DateTimeField(auto_now_add=True)


class Lead(models.Model):
    SOURCE_CHOICES = (
        ('instagram', 'Instagram'),
        ('facebook', 'Facebook'),
        ('referred', 'Referred'),
        ('google', 'Google'),
        ('other', 'Other'),
    )
    SERVICE_CHOICES = (
        ('seo', 'SEO'),
        ('android_development', 'Android Development'),
        ('logo_design', 'Logo Design'),
        ('website', 'Website'),
        ('other', 'Other'),
    )
    
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    assigned_user = models.ForeignKey(Employees, on_delete=models.SET_NULL, null=True)  # Assigned Employee
    source = models.CharField(max_length=50, choices=SOURCE_CHOICES, default='other')
    services = models.CharField(max_length=50, choices=SERVICE_CHOICES, default='other')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 
    def __str__(self):
        return self.name

class LeadRemark(models.Model):
    CALL_STATUS_CHOICES = [
        ('connected', 'Connected'),
        ('not_connected', 'Not Connected'),
        ('follow_up', 'Follow Up'),
    ]

    lead = models.ForeignKey(Lead, on_delete=models.CASCADE)  # Link remark to lead
    employee = models.ForeignKey(Employees, on_delete=models.CASCADE)  # Employee adding remark
    lead_name = models.CharField(max_length=255)  # Store lead's name separately
    lead_contact_number = models.CharField(max_length=15)  # Store lead's contact number separately
    remark = models.TextField()
    call_connect_status = models.CharField(max_length=20, choices=CALL_STATUS_CHOICES, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"Remark for"
    

class LeaveRequest(models.Model):
    LEAVE_REASONS = [
        ('personal', 'Personal'),
        ('medical', 'Medical'),
        ('other', 'Other')
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    leave_reason = models.CharField(max_length=20, choices=LEAVE_REASONS)
    from_date = models.DateField()
    from_time = models.TimeField()
    to_date = models.DateField()
    to_time = models.TimeField()
    place_visit = models.CharField(max_length=200)
    remarks = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.leave_reason} Leave"

    class Meta:
        ordering = ['-created_at']
    

class TodoItem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    task = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.task} - {self.user.username}"