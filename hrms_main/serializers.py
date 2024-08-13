from django.contrib.auth.models import User
from rest_framework import serializers
# from .models import  Allowance, Award_type, Branch, Commission, Competencies, Contract_type, Department ,Designation, Employee, Employee_Salary, Expence_type, Income_type, Job_category, Job_stage, Leaves, Document_type, Loan, Payment_type, Payslip_type, Allowance_option,Loan_option, Deduction_option ,Goal_type, Performance_type, Roles, Termination_type, Training_type
from .models import *

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class UserViewSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields= '__all__'
   
class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'
   
     
        
class EmployeeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee
        fields = ['Employee_id', 'Employee_name', 'Employee_phone', 'Date_of_Birth', 'Gender', 'Email', 'Password', 'Address', 'Branch', 'Department', 'Role', 'Designation', 'Date_Of_Joining', 'Employee_type', 'Document', 'Account_holder', 'Account_number', 'Bank_name', 'Bank_identifier_code', 'Branch_location', 'Tax_payer_id']
        read_only_fields = ['Employee_id']
    def create(self, validated_data):
        print(validated_data.get('Email'))
        email = validated_data.get('Email')
        password = validated_data.get('Password')
        User.objects.create_user(username=email, email=email, password=password)
        employee = Employee.objects.create(**validated_data)

        return employee     
       
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        user = instance.user
        instance.Employee_id = validated_data.get('Employee_id', instance.Employee_id)
        instance.Employee_name = validated_data.get('Employee_name', instance.Employee_name)
        instance.Employee_phone = validated_data.get('Employee_phone', instance.Employee_phone)
        instance.Date_of_Birth = validated_data.get('Date_of_Birth', instance.Date_of_Birth)
        instance.Gender = validated_data.get('Gender', instance.Gender)
        instance.Address = validated_data.get('Address', instance.Address)
        instance.Branch = validated_data.get('Branch', instance.Branch)
        instance.Department = validated_data.get('Department', instance.Department)
        instance.Role = validated_data.get('Role', instance.Role)
        instance.Designation = validated_data.get('Designation', instance.Designation)
        instance.Date_Of_Joining = validated_data.get('Date_Of_Joining', instance.Date_Of_Joining)
        instance.Employee_type = validated_data.get('Employee_type', instance.Employee_type)
        instance.Document = validated_data.get('Document', instance.Document)
        instance.Account_holder = validated_data.get('Account_holder', instance.Account_holder)
        instance.Account_number = validated_data.get('Account_number', instance.Account_number)
        instance.Bank_name = validated_data.get('Bank_name', instance.Bank_name)
        instance.Bank_identifier_code = validated_data.get('Bank_identifier_code', instance.Bank_identifier_code)
        instance.Branch_location = validated_data.get('Branch_location', instance.Branch_location)
        instance.Tax_payer_id = validated_data.get('Tax_payer_id', instance.Tax_payer_id)

        user.username = user_data.get('username', user.username)
        user.email = user_data.get('email', user.email)
        if user_data.get('password'):
            user.set_password(user_data.get('password'))
        user.save()

        instance.save()
        return instance        

class BranchCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = ['branch_id', 'branch_type', 'branch_country', 'branch_state', 'branch_district', 'branch_address']
        read_only_fields = ['branch_id']
        
class BranchViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = '__all__'
        
class DepartmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['department_id', 'department_category', 'department_name']
        read_only_fields = ['department_id']
        
class DepartmentViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'
        
class DesignationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Designation
        fields = ['designation_id', 'designation_department', 'designation_name']
        read_only_fields = ['designation_id']
        
class DesignationViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Designation
        fields = '__all__'
        
class LeavesCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leaves
        fields = ['leave_name', 'days_per_year']
        # read_only_fields = ['designation_id']
        
class LeavesViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leaves
        fields = '__all__'
        
class Document_typeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document_type
        fields = ['document_name', 'required_feild']
        # read_only_fields = ['designation_id']
        
class Document_typeViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document_type
        fields = '__all__'
        
class Payslip_typeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payslip_type
        fields = ['payslip_name']
        # read_only_fields = ['designation_id']
        
class Payslip_typeViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payslip_type
        fields = '__all__'

class Allowance_optionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Allowance_option
        fields = ['allowance_option_name']
        # read_only_fields = ['designation_id']
        
class Allowance_optionViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Allowance_option
        fields = '__all__'

class Loan_optionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan_option
        fields = ['Loan_option_name']
        # read_only_fields = ['designation_id']
        
class Loan_optionViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan_option
        fields = '__all__'

class Deduction_optionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deduction_option
        fields = ['Deduction_option_name']
        # read_only_fields = ['designation_id']
        
class Deduction_optionViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deduction_option
        fields = '__all__'

class Goal_typeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal_type
        fields = ['Goal_name']
        # read_only_fields = ['designation_id']
        
class Goal_typeViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal_type
        fields = '__all__'

class Training_typeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Training_type
        fields = ['Training_name']
        # read_only_fields = ['designation_id']
        
class Training_typeViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Training_type
        fields = '__all__'

class Award_typeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Award_type
        fields = ['Award_name']
        # read_only_fields = ['designation_id']
        
class Award_typeViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Award_type
        fields = '__all__'

class Termination_typeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Termination_type
        fields = ['Termination']
        # read_only_fields = ['designation_id']
        
class Termination_typeViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Termination_type
        fields = '__all__'

class Job_categoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job_category
        fields = ['Job_category_title']
        # read_only_fields = ['designation_id']
        
class Job_categoryViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job_category
        fields = '__all__'

class Job_stageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job_stage
        fields = ['Job_stage_title']
        # read_only_fields = ['designation_id']
        
class Job_stageViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job_stage
        fields = '__all__'

class Performance_typeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performance_type
        fields = ['Performance_type_name']
        # read_only_fields = ['designation_id']
        
class Performance_typeViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performance_type
        fields = '__all__'

class CompetenciesCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competencies
        fields = ['Competencies_name', 'Competencies_type']
        # read_only_fields = ['designation_id']
        
class CompetenciesViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competencies
        fields = '__all__'

class Expence_typeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expence_type
        fields = ['Expence_type_name']
        # read_only_fields = ['designation_id']
        
class Expence_typeViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expence_type
        fields = '__all__'

class Income_typeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income_type
        fields = ['Income_type_name']
        # read_only_fields = ['designation_id']
        
class Income_typeViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income_type
        fields = '__all__'

class Payment_typeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment_type
        fields = ['Payment_type_name']
        # read_only_fields = ['designation_id']
        
class Payment_typeViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment_type
        fields = '__all__'

class Contract_typeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract_type
        fields = ['Contract_type_name']
        # read_only_fields = ['designation_id']
        
class Contract_typeViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract_type
        fields = '__all__'

class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = '__all__'

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'

class RolePermissionSerializer(serializers.ModelSerializer):
    permissions = serializers.PrimaryKeyRelatedField(queryset=Permission.objects.all(), many=True)

    class Meta:
        model = RolePermission
        fields = '__all__'

class RoleSerializer(serializers.ModelSerializer):
    role_permissions = RolePermissionSerializer(source='rolepermission_set', many=True, required=False)

    class Meta:
        model = Role
        fields = ['id', 'name', 'role_permissions']
    
    def update(self, instance, validated_data):
        role_permissions_data = validated_data.pop('role_permissions')
        instance.name = validated_data.get('name', instance.name)
        instance.save()

        # Clear existing role_permissions
        instance.role_permissions.all().delete()

        # Add new role_permissions
        for role_permission_data in role_permissions_data:
            RolePermission.objects.create(role=instance, **role_permission_data)

        return instance

class RoleCreateSerializer(serializers.ModelSerializer):
    role_permissions = RolePermissionSerializer(many=True)
    
    class Meta:
        model = Role
        fields = ['name', 'role_permissions']
    
    def create(self, validated_data):
        
        role_permissions_data = validated_data.pop('role_permissions')
        
        role = Role.objects.create(**validated_data)
        for role_permission_data in role_permissions_data:
            permissions = role_permission_data.pop('permissions')
            role_permission = RolePermission.objects.create(role=role, **role_permission_data)
            role_permission.permissions.set(permissions)
        return role
    
    def update(self, instance, validated_data):
        role_permissions_data = validated_data.pop('role_permissions', [])
        instance.name = validated_data.get('name', instance.name)
        instance.save()

        # Clear existing role permissions
        RolePermission.objects.filter(role=instance).delete()
        
        # Add new role permissions
        for role_permission_data in role_permissions_data:
            module = role_permission_data.pop('module')
            permissions = role_permission_data.pop('permissions')
            
            role_permission = RolePermission.objects.create(role=instance, module=module)
            role_permission.permissions.set(permissions)

        return instance



# class EmployeeCreateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Employee
#         fields = ['Employee_id','Employee_name','Employee_phone','Date_of_Birth','Gender','Email','Password','Address','Branch','Department','Role','Designation','Date_Of_Joining','Employee_type','Document','Account_holder','Account_number','Bank_name','Bank_identifier_code','Branch_location','Tax_payer_id']
        # read_only_fields = ['designation_id']
        
class EmployeeViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'
        
class Employee_SalaryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee_Salary
        fields = ['Payslip_type','Salary']
        # read_only_fields = ['designation_id']
        
class Employee_SalaryViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee_Salary
        fields = '__all__'

class AllowanceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Allowance
        fields = ['Allowance_option','Title','Type','Amount']
        # read_only_fields = ['designation_id']
        
class AllowanceViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Allowance
        fields = '__all__'

class CommissionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commission
        fields = ['Title','Type','Amount']
        # read_only_fields = ['designation_id']
        
class CommissionViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commission
        fields = '__all__'

class LoanCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = ['Title','Loan_options','Type','Loan_amount','Start_date','End_date','Reason']
        # read_only_fields = ['designation_id']
        
class LoanViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = '__all__'

class SaturationDeductionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Saturation_Deduction
        fields = '__all__'

class OtherPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Other_Payment
        fields = '__all__'

class OvertimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Overtime
        fields = '__all__'

class TimesheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = timesheet
        fields = '__all__'

class CreateLeavesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Create_Leaves
        fields = '__all__'
        

class IndicatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Indicator
        fields = '__all__'

class AppraisalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appraisal
        fields = '__all__'

class GoalTrackingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal_tracking
        fields = '__all__'

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'

class PayeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payee
        fields = '__all__'

class PayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payer
        fields = '__all__'

class DepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deposit
        fields = '__all__'

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'

class TransferBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfer_balance
        fields = '__all__'

class TrainingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Training
        fields = '__all__'

class TrainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trainer
        fields = '__all__'

class AwardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Award
        fields = '__all__'

class TransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        fields = '__all__'

class ResignationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resignation
        fields = '__all__'

class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = '__all__'

class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = '__all__'

class ComplaintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaint
        fields = '__all__'

class WarningSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warning
        fields = '__all__'

class TerminationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Termination
        fields = '__all__'

class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = '__all__'

class HolidaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Holiday
        fields = '__all__'

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'

class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job_Application
        fields = '__all__'

class JobOnBoardingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job_On_Boarding
        fields = '__all__'

class InterviewScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interview_schedule
        fields = '__all__'

class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract
        fields = '__all__'

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

class MeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meeting
        fields = '__all__'

class ZoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zoom
        fields = '__all__'

class AssetsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assets
        fields = '__all__'

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'

class CompanyPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyPolicy
        fields = ['id', 'branch', 'title', 'description', 'attachment']
        
class CompanyPolicyViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyPolicy
        fields = '__all__'