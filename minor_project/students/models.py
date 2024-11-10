from django.db import models

class Student(models.Model):
    username = models.CharField(max_length=255, unique=True, null=True)
# Username as primary key
    phone = models.CharField(max_length=15)
    roll_no = models.CharField(max_length=15, unique=True)
    c_name = models.CharField(max_length=15)  # Candidate name
    gender = models.CharField(max_length=15)
    dob = models.DateField()  # Date of Birth
    rank = models.IntegerField()  # Candidate rank
    c_rank = models.IntegerField()
    xii_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    category = models.CharField(max_length=15)
    nationality = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    email = models.EmailField()  # Use EmailField for validation

    def __str__(self):
        return str(self.roll_no)

class College(models.Model):
    college_id = models.AutoField(primary_key=True)
    college_name = models.CharField(max_length=255)
    college_type = models.CharField(max_length=20)
    contact_no = models.CharField(max_length=15)  # Using CharField for formatting
    email = models.EmailField()  # For validation

    def __str__(self):
        return self.college_name


