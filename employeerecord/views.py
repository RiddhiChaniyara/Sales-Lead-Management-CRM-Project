from django.http import JsonResponse
from django.shortcuts import render,redirect,HttpResponse, get_object_or_404
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from ersapp.models import CustomUser , Employees, Lead, LeadRemark, Attendance, TodoItem
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.utils import timezone
User = get_user_model()
def BASE(request):
       return render(request,'base.html')

login_required(login_url='/')

@login_required(login_url='/')
def dashboard_view(request):
    # Initialize counts
    emp_count = Employees.objects.all().count()  # Total number of employees
    lead_count = 0  # Initialize lead count for the specific employee
    pending_leads_count = 0  # Initialize pending leads count for the specific employee

    # Count leads with leadremark = 'Not Connected'
    not_connected_leads = LeadRemark.objects.filter(call_connect_status='not_connected').distinct().count()

    # Count of leads with 'connected' status
    connected_leads_count = LeadRemark.objects.filter(call_connect_status='connected').distinct().count()

    # Count of leads with 'follow_up' status
    follow_up_leads_count = LeadRemark.objects.filter(call_connect_status='follow_up').distinct().count()

    # Count attendance records for the current date (system date: March 24, 2025)
    current_date = datetime.now().date()  # Get current date
    attendance_count = Attendance.objects.filter(date=current_date).count()

    # Fetch all to-do items for the logged-in user
    todo_items = TodoItem.objects.filter(user=request.user).order_by('-created_at')

    # Calculate lead counts for the specific employee
    if request.user.is_authenticated:
        try:
            employee = Employees.objects.get(admin=request.user)
            # Fetch leads assigned to this employee
            leads = Lead.objects.filter(assigned_user=employee)
            lead_count = leads.count()  # Total leads for this employee

            # Get updated leads from session
            updated_leads = request.session.get('updated_leads', {})
            updated_leads_for_user = updated_leads.get(str(request.user.id), [])
            # Count pending leads (not updated by the user)
            pending_leads_count = len([lead for lead in leads if lead.id not in updated_leads_for_user])
        except Employees.DoesNotExist:
            lead_count = 0
            pending_leads_count = 0
            print("Lead count:", lead_count)
            print("Pending leads count:", pending_leads_count)

    # Prepare the context
    context = {
        'emp_count': emp_count,  # Total employee count
        'lead_count': lead_count,  # Total leads for this employee
        'not_connected_leads': not_connected_leads,
        'connected_leads': connected_leads_count,
        'follow_up_leads': follow_up_leads_count,
        'attendance_count': attendance_count,
        'pending_leads_count': pending_leads_count,
        'todo_items': todo_items,  # To-do items for the user
    }

    return render(request, 'dashboard.html', context)
 



def LOGIN(request):
    return render(request,'login.html')

def doLogout(request):
    logout(request)
    request.session.flush()  # Clear the session including CSRF token
    return redirect('login')

def doLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
       

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            user_type = user.user_type
            if user_type == '1':
                return redirect('dashboard')
            elif user_type == '2':
                return redirect('dashboard')
        else:
            messages.error(request, 'Email or Password is not valid')
            return redirect('login')  # Redirect back to the login page with an error message
    else:
        # If the request method is not POST, redirect to the login page with an error message
        messages.error(request, 'Invalid request method')
        return redirect('login')
        
login_required(login_url='/')
def CHANGE_PASSWORD(request):
     context ={}
     ch = User.objects.filter(id = request.user.id)
     
     if len(ch)>0:
            data = User.objects.get(id = request.user.id)
            context["data"]:data             # type: ignore
     if request.method == "POST":        
        current = request.POST["cpwd"]
        new_pas = request.POST['npwd']
        user = User.objects.get(id = request.user.id)
        un = user.username
        check = user.check_password(current)
        if check == True:
          user.set_password(new_pas)
          user.save()
          messages.success(request,'Password Change  Succeesfully!!!')
          user = User.objects.get(username=un)
          login(request,user)
        else:
          messages.success(request,'Current Password wrong!!!')
          return redirect("change_password")
     return render(request,'change-password.html')


@login_required
def add_todo(request):
    if request.method == 'POST':
        task = request.POST.get('task')
        if task:
            todo = TodoItem.objects.create(
                user=request.user,
                task=task
            )
            return JsonResponse({
                'success': True,
                'task': task,
                'created_at': todo.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'id': todo.id
            })
    return JsonResponse({'success': False, 'error': 'Invalid request'})

@login_required
def delete_todo(request):
    if request.method == 'POST':
        todo_id = request.POST.get('id')
        try:
            todo = TodoItem.objects.get(id=todo_id, user=request.user)
            todo.delete()
            return JsonResponse({'success': True})
        except TodoItem.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Task not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request'})