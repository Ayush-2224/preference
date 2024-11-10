from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .models import Student, College
from django.contrib.auth.decorators import login_required
from django.db import connection
import MySQLdb

from django.http import JsonResponse

# Create your views here.

@login_required(login_url='student_login')  # Redirects to login if user is anonymous
def student_register(request):
    if request.method == 'POST':
        try:
            # Retrieve current user's username as roll_no
            roll_no = request.user.username
            username=request.user.username
            rank = request.POST.get('rank')
            c_name = request.POST.get('c_name')
            gender = request.POST.get('gender')
            dob = request.POST.get('dob')
            c_rank = request.POST.get('c_rank')
            xii_percentage = request.POST.get('xii_percentage')
            category = request.POST.get('category')
            nationality = request.POST.get('nationality')
            address = request.POST.get('address')
            email = request.POST.get('email')
            phone = request.POST.get('phone')

            # Create and save the Student instance
            student = Student(
                username=username,
                roll_no=roll_no,
                rank=rank,
                c_name=c_name,
                gender=gender,
                dob=dob,
                c_rank=c_rank,
                xii_percentage=xii_percentage,
                category=category,
                nationality=nationality,
                address=address,
                email=email,
                phone=phone
            )
            student.save()
            messages.success(request, "Student registered successfully!")
            return redirect('student_home')  # Redirect to the home page after successful registration
        except Exception as e:
            messages.error(request, f"An error occurred during registration: {e}")
            return redirect('student_register')  # Redirect back to the registration page on error

    # If not POST, render the registration form
    return render(request, 'students/register.html')

def student_home(request):
    if request.user.is_anonymous:
        return redirect("student/login")
    return render(request, 'students/home.html')
def college_home(request): 
    if request.user.is_anonymous:
        return redirect("college/login")
    return render(request,'colleges/home.html')
def home(request):
    
    return render(request,'colleges/common_home.html')




def student_logout(request):
    logout(request)
    return redirect("student_login")


def student_signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password == confirm_password:
            
                # Create the User instance
            user = User.objects.create_user(username=username, password=password)
            user.save()

            messages.success(request, "Student registered successfully!")
            return redirect('student_login')  # Redirect to login page after registration
            
        else:
            messages.error(request, "Passwords do not match.")

    return render(request, 'students/signup.html')




# Student login view
def student_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            # Check if the user is associated with a Student
            if Student.objects.filter(username=user.username).exists():
                
                return redirect("student_home")  # Redirect after successful login
            else:
                return redirect ("common_home")
        else:
            messages.error(request, 'Invalid credentials')
            return render(request, 'students/signup.html')

    return render(request, 'students/login.html')  # Render login page


# College login view
def college_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            # Check if the user is associated with a College
            if College.objects.filter(college_id=user.username).exists():
                
                return redirect("college_home")  # Redirect after successful login
            else:
                return redirect ("common_home")
        else:
            messages.error(request, 'Invalid credentials')
            return render(request, 'colleges/login.html')

    return render(request, 'colleges/login.html')  # Render login page


# College signup view
def college_signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password == confirm_password:
            try:
                # Create the User instance
                user = User.objects.create_user(username=username, password=password)
                user.save()

                # Additional college information can be added here if needed
                messages.success(request, "College registered successfully!")
                return redirect('college_login')  # Redirect to login page after registration
            except Exception as e:
                messages.error(request, f"An error occurred: {e}")
        else:
            messages.error(request, "Passwords do not match.")

    return render(request, 'colleges/signup.html')


# College logout view
def college_logout(request):
    logout(request)
    return redirect("college_login")


@login_required(login_url='college_login')  # Redirects to college login if not authenticated
def college_register(request):
    if request.method == 'POST':
        try:
            # Retrieve current user's username as college_id
            college_id = request.user.username
            # Get data from form fields
            college_name = request.POST.get('college_name')
            college_type = request.POST.get('college_type')
            contact_no = request.POST.get('contact_no')
            email = request.POST.get('email')

            # Create and save the College instance
            college = College(
                college_id=college_id,
                college_name=college_name,
                college_type=college_type,
                contact_no=contact_no,
                email=email,
            )
            college.save()
            messages.success(request, "College registered successfully!")
            return redirect('college_home')  # Redirect to the home page after successful registration
        except Exception as e:
            messages.error(request, f"An error occurred during registration: {e}")
            return redirect('college_register')  # Redirect back to the registration page on error

    # If not POST, render the registration form
    return render(request, 'colleges/register.html')


def get_college_list():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM students_college")
        results = cursor.fetchall()
    return results
def get_preference_list():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM preference")
        results = cursor.fetchall()
    return results
def get_course_list():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM course")
        results = cursor.fetchall()
    return results


def college_list(request):
    # student = request.user.username  # Assuming a one-to-one relationship with User
    colleges = get_college_list()
    # preferences = Preference.objects.filter(student=student)
    # preferred_colleges = [preference.course.college.id for preference in preferences]

    return render(request, 'colleges/college_list.html', {
        'colleges': colleges,
        'preference':get_preference_list(),
        'courses':get_course_list()
    })


# preference functions
#######################################################


@login_required(login_url='student_login')
def add_preference(request, college_id, course_id):
    username = request.user.username  # Assuming user model has a username field
    
    with connection.cursor() as cursor:
        try:
            # Find the highest choice_no for the current student
            cursor.execute("""
                SELECT MAX(p.choice_no) 
                FROM can_pref cp
                JOIN preference p ON cp.Choice_id = p.choice_id
                WHERE cp.username = %s
            """, [username])
            max_choice_no = cursor.fetchone()[0] or 0  # If None, start from 0
            
            # Increment choice_no for the new entry
            new_choice_no = max_choice_no + 1
            
            # Insert into preference table with the new choice_no
            cursor.execute(
                "INSERT INTO preference (college_id, course_id, choice_no) VALUES (%s, %s, %s)",
                [college_id, course_id, new_choice_no]
            )
            choice_id = cursor.lastrowid  # Get the last inserted row's ID
            
            # Insert into can_pref table
            cursor.execute("INSERT INTO can_pref (username, Choice_id) VALUES (%s, %s)", 
                           [username, choice_id])
            
            print("Preference added successfully with Choice No:", new_choice_no)
        
        except Exception as e:
            print("Error adding preference:", e)  # Log the error for debugging
    
    return redirect('college_courses')



@login_required(login_url='student_login')
def remove_preference(request, college_id, course_id):
    username = request.user.username
    
    with connection.cursor() as cursor:
        # Corrected SQL syntax
        cursor.execute("DELETE FROM preference WHERE college_id = %s AND course_id = %s", [college_id, course_id])
    
    return redirect('college_courses')
#################################3
@login_required(login_url='student_login') 
def college_course_view(request):
    # SQL query to fetch all college-course relationships
    query = '''
        SELECT c.college_name AS college_name, co.branch_name AS course_name, c.college_id AS college_id, co.course_id AS course_id
        FROM students_college c
        JOIN college_course cc ON c.college_id = cc.college_id
        JOIN course co ON cc.course_id = co.course_id;
    '''
    
    # Execute the query
    with connection.cursor() as cursor:
        cursor.execute(query)
        college_courses = cursor.fetchall()

    # Pass the results to the template
    return render(request, 'students/college_course_list.html', {'college_courses': college_courses})