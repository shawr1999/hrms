from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser, Group, Permission

from hrms_main.admin import User


# class CustomUser(AbstractUser):
#     groups = models.ManyToManyField(
#         Group,
#         related_name='custom_user_set',  # Change related_name
#         blank=True,
#         help_text='The groups this user belongs to.',
#         verbose_name='groups'
#     )
#     user_permissions = models.ManyToManyField(
#         Permission,
#         related_name='custom_user_set',  # Change related_name
#         blank=True,
#         help_text='Specific permissions for this user.',
#         verbose_name='user permissions'
#     )

class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    clock_in = models.DateTimeField(auto_now_add=True)
    clock_out = models.DateTimeField(null=True, blank=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.date}'

class Branch(models.Model):
  branch_id = models.CharField(max_length=255, unique=True, blank=True)
  branch_type = models.CharField(max_length=255)
  branch_country = models.CharField(max_length=255)
  branch_state = models.CharField(max_length=255)
  branch_district = models.CharField(max_length=255)
  branch_address = models.CharField(max_length=255)


  def __str__(self):
      return self.branch_id
    
    

  
    
@receiver(pre_save, sender=Branch)
def generate_branch_id(sender, instance, **kwargs):
    if not instance.branch_id:
        # Get first 3 letters of country, state, and district
        country_code = instance.branch_country[:3].upper()
        state_code = instance.branch_state[:3].upper()
        # district_code = instance.branch_district[:3].upper()
        
        # Generate sequential number
        existing_ids = Branch.objects.filter(
            branch_country=instance.branch_country,
            branch_state=instance.branch_state,
            # branch_district=instance.branch_district
        ).count()
        sequential_number = f'{existing_ids + 1:03}'

        # Combine to form branch_id
        instance.branch_id = f'{country_code}{state_code}{sequential_number}'


class Department(models.Model):
  department_id = models.CharField(max_length=255, unique=True, blank=True)
  department_category = models.CharField(max_length=255)
  department_name = models.CharField(max_length=255)

@receiver(pre_save, sender=Department)
def generate_department_id(sender, instance, **kwargs):
    if not instance.department_id:
        # Get first 3 letters of country, state, and district
        category_code = instance.department_category[:3].upper()
        name_code = instance.department_name[:3].upper()
        # district_code = instance.branch_district[:3].upper()
        
        # Generate sequential number
        existing_ids = Department.objects.filter(
            department_category=instance.department_category,
            department_name=instance.department_name,
            # branch_district=instance.branch_district
        ).count()
        sequential_number = f'{existing_ids + 1:03}'

        # Combine to form branch_id
        instance.department_id = f'{category_code}{name_code}{sequential_number}'


class Designation(models.Model):
  designation_id = models.CharField(max_length=255, unique=True, blank=True)
  designation_department = models.CharField(max_length=255)
  designation_name = models.CharField(max_length=255)
  
@receiver(pre_save, sender=Designation)
def generate_designation_id(sender, instance, **kwargs):
    if not instance.designation_id:
        # Get first 3 letters of country, state, and district
        department_code = instance.designation_department[:3].upper()
        name_code = instance.designation_name[:3].upper()
        # district_code = instance.branch_district[:3].upper()
        
        # Generate sequential number
        existing_ids = Designation.objects.filter(
            designation_department=instance.designation_department,
            designation_name=instance.designation_name,
            # branch_district=instance.branch_district
        ).count()
        sequential_number = f'{existing_ids + 1:03}'

        # Combine to form branch_id
        instance.designation_id = f'{department_code}{name_code}{sequential_number}'

class Leaves(models.Model):
#   leave_id = models.CharField(max_length=255, unique=True, blank=True)
  leave_name = models.CharField(max_length=255)
  days_per_year = models.CharField(max_length=255)


class Document_type(models.Model):
#   leave_id = models.CharField(max_length=255, unique=True, blank=True)
  document_name = models.CharField(max_length=255)
  required_feild = models.CharField(max_length=255)

class Payslip_type(models.Model):
#   leave_id = models.CharField(max_length=255, unique=True, blank=True)
  payslip_name = models.CharField(max_length=255)
#   required_feild = models.CharField(max_length=255)

class Allowance_option(models.Model):
#   leave_id = models.CharField(max_length=255, unique=True, blank=True)
  allowance_option_name = models.CharField(max_length=255)
#   required_feild = models.CharField(max_length=255)

class Loan_option(models.Model):
#   leave_id = models.CharField(max_length=255, unique=True, blank=True)
  Loan_option_name = models.CharField(max_length=255)
#   required_feild = models.CharField(max_length=255)

class Deduction_option(models.Model):
#   leave_id = models.CharField(max_length=255, unique=True, blank=True)
  Deduction_option_name = models.CharField(max_length=255)
#   required_feild = models.CharField(max_length=255)

class Goal_type(models.Model):
#   leave_id = models.CharField(max_length=255, unique=True, blank=True)
  Goal_name = models.CharField(max_length=255)
#   required_feild = models.CharField(max_length=255)

class Training_type(models.Model):
#   leave_id = models.CharField(max_length=255, unique=True, blank=True)
  Training_name = models.CharField(max_length=255)
#   required_feild = models.CharField(max_length=255)

class Award_type(models.Model):
#   leave_id = models.CharField(max_length=255, unique=True, blank=True)
  Award_name = models.CharField(max_length=255)
#   required_feild = models.CharField(max_length=255)

class Termination_type(models.Model):
#   leave_id = models.CharField(max_length=255, unique=True, blank=True)
  Termination = models.CharField(max_length=255)
#   required_feild = models.CharField(max_length=255)

class Job_category(models.Model):
#   leave_id = models.CharField(max_length=255, unique=True, blank=True)
  Job_category_title = models.CharField(max_length=255)
#   required_feild = models.CharField(max_length=255)

class Job_stage(models.Model):
#   leave_id = models.CharField(max_length=255, unique=True, blank=True)
  Job_stage_title = models.CharField(max_length=255)
#   required_feild = models.CharField(max_length=255)

class Performance_type(models.Model):
#   leave_id = models.CharField(max_length=255, unique=True, blank=True)
  Performance_type_name = models.CharField(max_length=255)
#   required_feild = models.CharField(max_length=255)

class Competencies(models.Model):
#   leave_id = models.CharField(max_length=255, unique=True, blank=True)
  Competencies_name = models.CharField(max_length=255)
  Competencies_type = models.CharField(max_length=255)

class Expence_type(models.Model):
#   leave_id = models.CharField(max_length=255, unique=True, blank=True)
  Expence_type_name = models.CharField(max_length=255)
  # Competencies_type = models.CharField(max_length=255)

class Income_type(models.Model):
#   leave_id = models.CharField(max_length=255, unique=True, blank=True)
  Income_type_name = models.CharField(max_length=255)
  # Competencies_type = models.CharField(max_length=255)

class Payment_type(models.Model):
#   leave_id = models.CharField(max_length=255, unique=True, blank=True)
  Payment_type_name = models.CharField(max_length=255)
  # Competencies_type = models.CharField(max_length=255)

class Contract_type(models.Model):
#   leave_id = models.CharField(max_length=255, unique=True, blank=True)
  Contract_type_name = models.CharField(max_length=255)
  # Competencies_type = models.CharField(max_length=255)
  
class Module(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Permission(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Role(models.Model):
    name = models.CharField(max_length=100)
    modules = models.ManyToManyField(Module, through='RolePermission')

    def __str__(self):
        return self.name

class RolePermission(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, blank=True)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    permissions = models.ManyToManyField(Permission)


class Employee(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee', default=None, null=True)
  Employee_id=models.CharField(max_length=255, unique=True, blank=True)
  Employee_name=models.CharField(max_length=255)
  Employee_phone=models.CharField(max_length=255)
  Date_of_Birth=models.CharField(max_length=255)
  Gender=models.CharField(max_length=255)
  Email=models.CharField(max_length=255)
  Password=models.CharField(max_length=255)
  Address=models.CharField(max_length=255)
  
  Branch=models.CharField(max_length=255)
  Department=models.CharField(max_length=255)
  Role=models.CharField(max_length=255)
  Designation=models.CharField(max_length=255)
  Date_Of_Joining=models.CharField(max_length=255)
  Employee_type=models.CharField(max_length=255)
  
  Document=models.CharField(max_length=255)
  
  Account_holder=models.CharField(max_length=255)
  Account_number=models.CharField(max_length=255)
  Bank_name=models.CharField(max_length=255)
  Bank_identifier_code=models.CharField(max_length=255)
  Branch_location=models.CharField(max_length=255)
  Tax_payer_id=models.CharField(max_length=255)
  
  def __str__(self):
    return self.Employee_name
  
@receiver(pre_save, sender=Employee)
def generate_employee_id(sender, instance, **kwargs):
    if not instance.Employee_id:
        # Get first 3 letters of country, state, and district
        country_code = instance.Branch[:3].upper()
        state_code = instance.Department[:3].upper()
        Role = instance.Role[:3].upper()
        
        # Generate sequential number
        existing_ids = Employee.objects.filter(
            Branch=instance.Department,
            Department=instance.Department,
            # branch_district=instance.branch_district
        ).count()
        sequential_number = f'{existing_ids + 1:03}'

        # Combine to form branch_id
        instance.Employee_id = f'{country_code}{state_code}{Role}{sequential_number}'  
  
class Employee_Salary(models.Model):
  Payslip_type=models.CharField(max_length=255)
  Salary=models.CharField(max_length=255)

class Allowance(models.Model):
  Allowance_option=models.CharField(max_length=255)
  Title=models.CharField(max_length=255)
  Type=models.CharField(max_length=255)
  Amount=models.CharField(max_length=255)

class Commission(models.Model):
  Title=models.CharField(max_length=255)
  Type=models.CharField(max_length=255)
  Amount=models.CharField(max_length=255)

class Loan(models.Model):
  Title=models.CharField(max_length=255)
  Loan_options=models.CharField(max_length=255)
  Type=models.CharField(max_length=255)
  Loan_amount=models.CharField(max_length=255)
  Start_date=models.CharField(max_length=255)
  End_date=models.CharField(max_length=255)
  Reason=models.CharField(max_length=255)

class Saturation_Deduction(models.Model):
  Deduction_option=models.CharField(max_length=255)
  Title=models.CharField(max_length=255)
  Type=models.CharField(max_length=255)
  Amount=models.CharField(max_length=255)

class Other_Payment(models.Model):
  Title=models.CharField(max_length=255)
  Type=models.CharField(max_length=255)
  Amount=models.CharField(max_length=255)

class Overtime(models.Model):
  Overtime_Title=models.CharField(max_length=255)
  Number_of_days=models.CharField(max_length=255)
  Hours=models.CharField(max_length=255)
  Rate=models.CharField(max_length=255)
  
class timesheet(models.Model):
  Employee=models.CharField(max_length=255)
  Date=models.CharField(max_length=255)
  Hours=models.CharField(max_length=255)
  Remarks=models.CharField(max_length=255)
  
class Create_Leaves(models.Model):
  Employee_id=models.CharField(max_length=255, default=None)
  Leave_type=models.CharField(max_length=255, default=None)
  Start=models.CharField(max_length=255)
  End=models.CharField(max_length=255)
  Reason=models.CharField(max_length=255)
  Remark=models.CharField(max_length=255)
  Status=models.CharField(max_length=255, default=None, null=True)
  
class Indicator(models.Model):
  Branch=models.CharField(max_length=255)
  Department=models.CharField(max_length=255)
  Designation=models.CharField(max_length=255)
  Outstanding_skilled=models.CharField(max_length=255)
  Outstanding_unskilled=models.CharField(max_length=255)
  Average_skilled=models.CharField(max_length=255)
  Average_unskilled=models.CharField(max_length=255)
  
  
class Appraisal(models.Model):
  Branch=models.CharField(max_length=255)
  Employee=models.CharField(max_length=255)
  Month=models.CharField(max_length=255)
  Remarks=models.CharField(max_length=255)

class Goal_tracking(models.Model):
  Branch=models.CharField(max_length=255)
  Goaltypes=models.CharField(max_length=255)
  Start=models.CharField(max_length=255)
  End=models.CharField(max_length=255)
  Subject=models.CharField(max_length=255)
  Target=models.CharField(max_length=255)
  Description=models.CharField(max_length=255)

class Account(models.Model):
  Account_name=models.CharField(max_length=255)
  Initial_Balance=models.CharField(max_length=255)
  Account_number=models.CharField(max_length=255)
  Branch_code=models.CharField(max_length=255)
  Bank_branch=models.CharField(max_length=255)

class Payee(models.Model):
  Name=models.CharField(max_length=255)
  Number=models.CharField(max_length=255)

class Payer(models.Model):
  Name=models.CharField(max_length=255)
  Number=models.CharField(max_length=255)

class Deposit(models.Model):
  Account=models.CharField(max_length=255)
  Amount=models.CharField(max_length=255)
  Date=models.CharField(max_length=255)
  Category=models.CharField(max_length=255)
  Payer=models.CharField(max_length=255)
  Payment_method=models.CharField(max_length=255)
  Ref=models.CharField(max_length=255)
  Description=models.CharField(max_length=255)
  
class Expense(models.Model):
  Account=models.CharField(max_length=255)
  Amount=models.CharField(max_length=255)
  Date=models.CharField(max_length=255)
  Category=models.CharField(max_length=255)
  Payee=models.CharField(max_length=255)
  Payment_method=models.CharField(max_length=255)
  Ref=models.CharField(max_length=255)
  Description=models.CharField(max_length=255)

class Transfer_balance(models.Model):
  From_account=models.CharField(max_length=255)
  To_account=models.CharField(max_length=255)
  Date=models.CharField(max_length=255)
  Amount=models.CharField(max_length=255)
  Payment_method=models.CharField(max_length=255)
  Ref=models.CharField(max_length=255)
  Description=models.CharField(max_length=255)

class Training(models.Model):
  Branch=models.CharField(max_length=255)
  Trainer_option=models.CharField(max_length=255)
  Training_type=models.CharField(max_length=255)
  Trainer=models.CharField(max_length=255)
  Training_cost=models.CharField(max_length=255)
  Employee=models.CharField(max_length=255)
  Start=models.CharField(max_length=255)
  End=models.CharField(max_length=255)
  Description=models.CharField(max_length=255)
  
class Trainer(models.Model):
  Branch=models.CharField(max_length=255)
  First_name=models.CharField(max_length=255)
  Last_name=models.CharField(max_length=255)
  Contact=models.CharField(max_length=255)
  Email=models.CharField(max_length=255)
  Expertise=models.CharField(max_length=255)
  Address=models.CharField(max_length=255)

class Award(models.Model):
  Employee=models.CharField(max_length=255)
  Award_type=models.CharField(max_length=255)
  Date=models.CharField(max_length=255)
  Gift=models.CharField(max_length=255)
  Address=models.CharField(max_length=255)

class Transfer(models.Model):
  Employee=models.CharField(max_length=255)
  Branch=models.CharField(max_length=255)
  Department=models.CharField(max_length=255)
  Date=models.CharField(max_length=255)
  Description=models.CharField(max_length=255)

class Resignation(models.Model):
  Employee=models.CharField(max_length=255)
  Date=models.CharField(max_length=255)
  Last_working_day=models.CharField(max_length=255)
  Reason=models.CharField(max_length=255)

class Trip(models.Model):
  Employee=models.CharField(max_length=255)
  Start=models.CharField(max_length=255)
  End=models.CharField(max_length=255)
  Purpose=models.CharField(max_length=255)
  Country=models.CharField(max_length=255)
  Description=models.CharField(max_length=255)

class Promotion(models.Model):
  Employee=models.CharField(max_length=255)
  Designation=models.CharField(max_length=255)
  Promotion_title=models.CharField(max_length=255)
  Promotion_date=models.CharField(max_length=255)
  Description=models.CharField(max_length=255)

class Complaint(models.Model):
  Complaint_from=models.CharField(max_length=255)
  Complaint_against=models.CharField(max_length=255)
  Title=models.CharField(max_length=255)
  Complaint_date=models.CharField(max_length=255)
  Description=models.CharField(max_length=255)

class Warning(models.Model):
  Warning_by=models.CharField(max_length=255)
  Warning_to=models.CharField(max_length=255)
  Subject=models.CharField(max_length=255)
  Warning_date=models.CharField(max_length=255)
  Description=models.CharField(max_length=255)

class Termination(models.Model):
  Employee=models.CharField(max_length=255)
  Termination_type=models.CharField(max_length=255)
  Notice_date=models.CharField(max_length=255)
  Termination_date=models.CharField(max_length=255)
  Description=models.CharField(max_length=255)

class Announcement(models.Model):
  Announcement_title=models.CharField(max_length=255)
  Branch=models.CharField(max_length=255)
  Department=models.CharField(max_length=255)
  Employee=models.CharField(max_length=255)
  Announcement_start_date=models.CharField(max_length=255)
  Announcement_end_date=models.CharField(max_length=255)
  Announcement_description=models.CharField(max_length=255)

class Holiday(models.Model):
  Occasion=models.CharField(max_length=255)
  Start=models.CharField(max_length=255)
  End=models.CharField(max_length=255)

class Job(models.Model):
  Title=models.CharField(max_length=255)
  Branch=models.CharField(max_length=255)
  Category=models.CharField(max_length=255)
  No_of_positions=models.CharField(max_length=255)
  Status=models.CharField(max_length=255)
  Start=models.CharField(max_length=255)
  End=models.CharField(max_length=255)
  Skill_box=models.CharField(max_length=255)

class Job_Application(models.Model):
  Job=models.CharField(max_length=255)
  Name=models.CharField(max_length=255)
  Email=models.CharField(max_length=255)
  Phone=models.CharField(max_length=255)
  
class Job_On_Boarding(models.Model):
  Interviewer=models.CharField(max_length=255)
  Joining_date=models.CharField(max_length=255)
  Days_of_week=models.CharField(max_length=255)
  Salary=models.CharField(max_length=255)
  Salary_type=models.CharField(max_length=255)
  Salary_duration=models.CharField(max_length=255)
  Job_Type=models.CharField(max_length=255)
  Status=models.CharField(max_length=255)
  
class Interview_schedule(models.Model):
  Interviewer=models.CharField(max_length=255)
  Assign_employee=models.CharField(max_length=255)
  Interview_date=models.CharField(max_length=255)
  Interview_time=models.CharField(max_length=255)
  Comment=models.CharField(max_length=255)
  
class Contract(models.Model):
  Employee_name=models.CharField(max_length=255)
  Subject=models.CharField(max_length=255)
  Value=models.CharField(max_length=255)
  Type=models.CharField(max_length=255)
  Start=models.CharField(max_length=255)
  Due=models.CharField(max_length=255)
  Description=models.CharField(max_length=255)
  
class Ticket(models.Model):
  Subject=models.CharField(max_length=255)
  Ticket_for=models.CharField(max_length=255)
  Priority=models.CharField(max_length=255)
  End=models.CharField(max_length=255)
  Description=models.CharField(max_length=255)
  
class Event(models.Model):
  Branch=models.CharField(max_length=255)
  Department=models.CharField(max_length=255)
  Event_title=models.CharField(max_length=255)
  Event_start=models.CharField(max_length=255)
  Select_Color=models.CharField(max_length=255)
  Description=models.CharField(max_length=255)
  
class Meeting(models.Model):
  Branch=models.CharField(max_length=255)
  Department=models.CharField(max_length=255)
  Employee=models.CharField(max_length=255)
  Meeting_title=models.CharField(max_length=255)
  Meeting_date=models.CharField(max_length=255)
  Time=models.CharField(max_length=255)
  Note=models.CharField(max_length=255)
  
class Zoom(models.Model):
  Title=models.CharField(max_length=255)
  User=models.CharField(max_length=255)
  Date=models.CharField(max_length=255)
  Duration=models.CharField(max_length=255)
  Password=models.CharField(max_length=255)
  
class Assets(models.Model):
  Employee=models.CharField(max_length=255)
  Name=models.CharField(max_length=255)
  Amount=models.CharField(max_length=255)
  Purchase_date=models.CharField(max_length=255)
  Support_until=models.CharField(max_length=255)
  Description=models.CharField(max_length=255)
  
class Document(models.Model):
  Name=models.CharField(max_length=255)
  Document=models.CharField(max_length=255)
  Role=models.CharField(max_length=255)
  Description=models.CharField(max_length=255)
  
class CompanyPolicy(models.Model):
    branch = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    description = models.TextField()
    attachment = models.FileField(upload_to='policies/', null=True, blank=True)

class Justtry(models.Model):
  name = models.CharField(max_length=255)




  

  
  
  
  
  
  

  
  
  