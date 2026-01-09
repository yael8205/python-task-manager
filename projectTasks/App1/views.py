from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime
from App1.models import Person, Task
from django.contrib.auth import logout
from django.contrib.messages import get_messages

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        full_name = request.POST.get('full_name')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, '  Username is exists')
            return render(request, 'register.html')

        if (len(password) < 8 or
                not any(char.isdigit() for char in password) or
                not any(char.isupper() for char in password) or
                not any(char.islower() for char in password)):
            messages.error(request, 'Password must be at least 8 characters long and include a number, an uppercase letter, and a lowercase letter')
            return render(request, 'register.html')

        try:
            user = User.objects.create_user(username=username, email=email,  password=password)
            user.first_name = full_name
            user.save()
            Person.objects.create(user=user)
            login(request, user)
            messages.success(request, 'נרשמת בהצלחה! כעת הגדר את התפקיד שלך.')
            return redirect('profile_setup')
        except Exception as e:
            messages.error(request, 'An error occurred during the registration process')

    return render(request, 'register.html')


def login_view(request):


    if request.method == "POST":
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(username=u, password=p)

        if user is not None:
            login(request, user)
            person, created = Person.objects.get_or_create(user=user)


            messages.success(request, f"Welcome back, {user.first_name if user.first_name else user.username}!")

            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            if person.role == 'ma':
                return redirect('managerhome')
            return redirect('workerhome')
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "login.html")

def logout_view(request):
    logout(request)
    return redirect('login')
@login_required
def profile_setup(request):
    person, created = Person.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        staff_type = request.POST.get('staff_type')
        role = request.POST.get('role')

        if not staff_type or staff_type == "":
            messages.error(request, "Please select a field of expertise")
        else:
            person.nameStaff = staff_type
            person.role = role
            person.save()

            if person.role == 'ma':
                return redirect('managerhome')
            return redirect('workerhome')

    staff_choices = [('', '---  Select Specialization ---')] + list(Person.StaffType.choices)
    context = {
        'person': person,
        'staff_choices': staff_choices,
        'role_choices': Person.UserRole.choices,
    }
    return render(request, 'profile.html', context)


@login_required
def workerhome(request):
    person = request.user.person
    tasks = Task.objects.filter(nameStaff=person.nameStaff).order_by('-id')

    status_filter = request.GET.get('status')
    worker_filter = request.GET.get('worker')

    if status_filter == 'nw':
        tasks = tasks.filter(executor__isnull=True)
    elif status_filter == 'ip':
        tasks = tasks.filter(status='ip')
    elif status_filter == 'my':
        tasks = tasks.filter(executor=person)
    elif status_filter == 'co':
        tasks = tasks.filter(status='co')

    if worker_filter:
        tasks = tasks.filter(executor_id=worker_filter)

    team_workers = Person.objects.filter(nameStaff=person.nameStaff, role='wo')

    return render(request, 'workerhome.html', {
        'tasks': tasks,
        'person': person,
        'team_workers': team_workers,
        'current_status': status_filter,
        'current_worker': worker_filter
    })
@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if not task.executor:
        task.delete()
        messages.success(request, "The task is deleted")
    else:
        messages.error(request, "Cannot delete a task that is in progress")
    return redirect('managerhome')

@login_required
def claim_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    person = request.user.person

    if not task.executor and task.nameStaff == person.nameStaff:
        task.executor = person
        task.status = 'ip'
        task.save()
        messages.success(request, "The task has been successfully assigned to you!")
    else:
        messages.error(request, "This task cannot be assigned.")

    return redirect('workerhome')


@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if task.executor == request.user.person:
        task.status = 'co'
        task.save()
        messages.success(request, f"Task '{task.name}' has been marked as completed!")
    else:
        messages.error(request, "You are not authorized to mark this task as completed.")

    return redirect('workerhome')


@login_required
def managerhome(request):
    person = request.user.person
    tasks = Task.objects.filter(nameStaff=person.nameStaff).order_by('-id')

    status_filter = request.GET.get('status')
    worker_filter = request.GET.get('worker')

    if status_filter:
        tasks = tasks.filter(status=status_filter)
    if worker_filter:
        tasks = tasks.filter(executor_id=worker_filter)

    team_workers = Person.objects.filter(nameStaff=person.nameStaff, role='wo')

    return render(request, 'managerhome.html', {
        'tasks': tasks,
        'person': person,
        'team_workers': team_workers,
        'current_status': status_filter,
        'current_worker': worker_filter
    })
@login_required
def add_task(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        end_date = request.POST.get('end_date')
        worker_id = request.POST.get('worker_id')

        nameStaff = request.user.person.nameStaff

        if name and end_date:
            new_task = Task.objects.create(
                name=name,
                description=description,
                nameStaff=nameStaff,
                end_date=end_date,
                status='nw'
            )

            if worker_id:
                worker = get_object_or_404(Person, id=worker_id)
                new_task.executor = worker
                new_task.status = 'ip'
                new_task.save()

            messages.success(request, "Task added and assigned successfully!")
    return redirect('managerhome')


@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST' and not task.executor:
        task.name = request.POST.get('name')
        task.description = request.POST.get('description')
        task.end_date = request.POST.get('end_date') # עדכון התאריך
        task.save()
        messages.success(request, "Task updated successfully!")
    else:
        messages.error(request, "Tasks in progress cannot be edited.")
    return redirect('managerhome')
