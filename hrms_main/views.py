from datetime import timezone
import json
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from rest_framework import status, viewsets
from django.template import loader
from rest_framework.decorators import api_view
from rest_framework.response import Response
# from .serializers import Award_typeCreateSerializer, Award_typeViewSerializer, BranchCreateSerializer, CompetenciesCreateSerializer, CompetenciesViewSerializer, Contract_typeCreateSerializer, Contract_typeViewSerializer, DepartmentCreateSerializer, DesignationCreateSerializer, Expence_typeCreateSerializer, Expence_typeViewSerializer, Goal_typeCreateSerializer, Goal_typeViewSerializer, Income_typeCreateSerializer, Income_typeViewSerializer, Job_categoryCreateSerializer, Job_categoryViewSerializer, Job_stageCreateSerializer, Job_stageViewSerializer, LeavesCreateSerializer, Document_typeCreateSerializer, Payment_typeCreateSerializer, Payment_typeViewSerializer, Payslip_typeCreateSerializer, Allowance_optionCreateSerializer, Loan_optionCreateSerializer, Deduction_optionCreateSerializer, Performance_typeCreateSerializer, Performance_typeViewSerializer, RegisterSerializer, Termination_typeCreateSerializer, Termination_typeViewSerializer, Training_typeCreateSerializer, Training_typeViewSerializer
# from .serializers import BranchViewSerializer, DepartmentViewSerializer, DesignationViewSerializer, LeavesViewSerializer, Document_typeViewSerializer, Payslip_typeViewSerializer, Allowance_optionViewSerializer, Loan_optionViewSerializer, Deduction_optionViewSerializer
from .models import *
from .serializers import *
# from .models import Award_type, Branch, Competencies, Contract_type,Department, Designation, Expence_type, Goal_type, Income_type, Job_category, Job_stage, Leaves, Document_type, Payment_type, Payslip_type, Allowance_option, Loan_option, Deduction_option, Performance_type, Termination_type, Training_type
from rest_framework import generics, status
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.utils import timezone



class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'id': user.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]
    
        
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        users = User.objects.all()
        # for user in users:
        #     print(user.username, user.password)
        #     if check_password('your_password', user.password):
        #         print("Password is correct")
        #     else:
        #         print("Password is incorrect")
        
        # print(f"Attempting login with username: {username}")
        
        if not User.objects.filter(username=username).exists():
            print(f"User with username '{username}' does not exist.")
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        
        
        user = authenticate(request, username=username, password=password)
        if user.is_superuser == "false":
            employee=Employee.objects.get(Email=user.email)
            role=Role.objects.get(name=employee.Role)
       
        
            if user is not None:
                token, created = Token.objects.get_or_create(user=user)  # Use Django REST Framework token system
                return Response({
                    'access': token.key,
                    'is_superuser': user.is_superuser,
                    'is_staff': user.is_staff,
                    'User_Info': user.email,
                    'User_Role_Id':role.id,
                    'Curr_User':employee.Role,
                    'Curr_Emp_id':employee.Employee_id,
                    'Curr_Emp_name':employee.Employee_name
                })
            else:
                print("Authentication failed. Invalid credentials.")
                
        else:
            if user is not None:
                token, created = Token.objects.get_or_create(user=user)  # Use Django REST Framework token system
                return Response({
                    'access': token.key,
                    'is_superuser': user.is_superuser,
                    'is_staff': user.is_staff,
                    'User_Info': user.email,
                    # 'User_Role_Id':role.id,
                    'Curr_User':"admin",
                    # 'Curr_Emp_id':employee.Employee_id,
                    # 'Curr_Emp_name':employee.Employee_name
                })
            else:
                print("Authentication failed. Invalid credentials.")
        
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)



class ClockInView(APIView):

    def post(self, request):
        data = request.data

        # Fetch employee based on the provided UserId
        try:
            employee = Employee.objects.get(Employee_id=data['UserId'])
            user = User.objects.get(email=employee.Email)
        except Employee.DoesNotExist:
            return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        today = timezone.now().date()

        # Check if an attendance record exists for today
        attendance, created = Attendance.objects.get_or_create(user=user, date=today)

        if created:
            # If a new attendance record was created (meaning it's the first clock-in today)
            attendance.clock_in = timezone.now()
            attendance.save()
            return Response({"message": "Clocked in successfully"}, status=status.HTTP_200_OK)
        else:
            
            # If an attendance record already exists and clock-in is recorded
            if attendance.clock_in is not None:
                return Response({"error": "Already clocked in today"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                # Handle edge cases where clock-in might be missing for an existing record
                attendance.clock_in = timezone.now()
                attendance.save()
                return Response({"message": "Clocked in successfully"}, status=status.HTTP_200_OK)


class ClockOutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data

        # Fetch employee based on the provided UserId
        try:
            employee = Employee.objects.get(Employee_id=data['UserId'])
            user = User.objects.get(email=employee.Email)
        except Employee.DoesNotExist:
            return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        today = timezone.now().date()

        try:
            attendance = Attendance.objects.get(user=user, date=today)
        except Attendance.DoesNotExist:
            return Response({"error": "No clock-in record found for today"}, status=status.HTTP_404_NOT_FOUND)

        if attendance.clock_out is None:
            attendance.clock_out = timezone.now()
            attendance.save()
            return Response({"message": "Clocked out successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Already clocked out today"}, status=status.HTTP_400_BAD_REQUEST)

class UserDetailView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserViewSerializer
    
class AttendanceDetailView(generics.ListAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

def index(request):
    template= loader.get_template('index.html')
    return HttpResponse(template.render())


@api_view(['GET'])
def hello_world(request):
    return Response({"message": "Hello, world!"})

@api_view(['POST'])
def create_employee(request):
    serializer = EmployeeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Employee created successfully!'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def employee_detail(request, pk):
    try:
        employee = Employee.objects.get(pk=pk)
    except Employee.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)

    elif request.method == 'PUT':
        data = request.data
        user = User.objects.get(email=data.get('email',employee.Email))

        employee.Employee_id = data.get('Employee_id', employee.Employee_id)
        employee.Employee_name = data.get('Employee_name', employee.Employee_name)
        employee.Employee_phone = data.get('Employee_phone', employee.Employee_phone)
        employee.Date_of_Birth = data.get('Date_of_Birth', employee.Date_of_Birth)
        employee.Gender = data.get('Gender', employee.Gender)
        employee.Email = data.get('Email', employee.Email)
        employee.Password = data.get('Password', employee.Password)
        employee.Address = data.get('Address', employee.Address)
        employee.Branch = data.get('Branch', employee.Branch)
        employee.Department = data.get('Department', employee.Department)
        employee.Role = data.get('Role', employee.Role)
        employee.Designation = data.get('Designation', employee.Designation)
        employee.Date_Of_Joining = data.get('Date_Of_Joining', employee.Date_Of_Joining)
        employee.Employee_type = data.get('Employee_type', employee.Employee_type)
        employee.Document = data.get('Document', employee.Document)
        employee.Account_holder = data.get('Account_holder', employee.Account_holder)
        employee.Account_number = data.get('Account_number', employee.Account_number)
        employee.Bank_name = data.get('Bank_name', employee.Bank_name)
        employee.Bank_identifier_code = data.get('Bank_identifier_code', employee.Bank_identifier_code)
        employee.Branch_location = data.get('Branch_location', employee.Branch_location)
        employee.Tax_payer_id = data.get('Tax_payer_id', employee.Tax_payer_id)

        employee.save()
                # print(data.get('email',employee.Email),'all here')
        
        print(user.username,'all here')
        user.email = data.get('email', employee.Email)
        user.username=data.get('email', employee.Email)
        print(data.get('email', employee.Email),'all123 here')
            
        if data.get('Password'):
            user.set_password(data.get('Password'))
            print("new pass")
        user.save()
        print(data.get('Email', employee.Email),"yaha bhi")
        
        return Response({'message': 'Employee updated successfully'}, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        print(employee.Email,"123432")
        user = User.objects.get(email=employee.Email)
        employee.delete()
        user.delete()
        return Response({'message': 'Employee and associated user deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def branch_create(request):
    if request.method == 'POST':
        print(request.data.get('branch_id'))
        serializer = BranchCreateSerializer(data=request.data)
        if serializer.is_valid():
            branch_instance = serializer.save()
            return Response({
                'message': 'New Branch is Successfully Added!',
                'branch_id': branch_instance.branch_id
            }, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BranchList(generics.ListAPIView):
    queryset = Branch.objects.all()
    serializer_class = BranchViewSerializer


class BranchDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Branch.objects.all()
    serializer_class = BranchViewSerializer
    
    
@api_view(['POST'])
def Department_create(request):
    if request.method == 'POST':
        # print(request.data.get('branch_id'))
        serializer = DepartmentCreateSerializer(data=request.data)
        if serializer.is_valid():
            department_instance = serializer.save()
            return Response({
                'message': 'New Department is Successfully Added!',
                'department_id': department_instance.department_id
            }, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class DepartmentList(generics.ListAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentViewSerializer


class DepartmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentViewSerializer


@api_view(['POST'])
def Designation_create(request):
    if request.method == 'POST':
        # print(request.data.get('branch_id'))
        serializer = DesignationCreateSerializer(data=request.data)
        if serializer.is_valid():
            designation_instance = serializer.save()
            return Response({
                'message': 'New Department is Successfully Added!',
                'designation_id': designation_instance.designation_id
            }, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class DesignationList(generics.ListAPIView):
    queryset = Designation.objects.all()
    serializer_class = DesignationViewSerializer


class DesignationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Designation.objects.all()
    serializer_class = DesignationViewSerializer
    
@api_view(['POST'])
def Leave_create(request):
    if request.method == 'POST':
        
        serializer = LeavesCreateSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            
            return Response({
                'message': 'New Leave is Successfully Added!',
                # 'designation_id': Leave_instance.designation_id
            }, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
class LeaveList(generics.ListAPIView):
    queryset = Leaves.objects.all()
    serializer_class = LeavesViewSerializer
        
class LeaveDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Leaves.objects.all()
    serializer_class = LeavesViewSerializer
    
@api_view(['POST'])
def Document_type_create(request):
    if request.method == 'POST':
        # print(request.data.get('branch_id'))
        serializer = Document_typeCreateSerializer(data=request.data)
        if serializer.is_valid():
            Document_type_instance = serializer.save()
            return Response({
                'message': 'New Leave is Successfully Added!',
                # 'designation_id': Leave_instance.designation_id
            }, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
class Document_typeList(generics.ListAPIView):
    queryset = Document_type.objects.all()
    serializer_class = Document_typeViewSerializer
        
        
class Document_typeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Document_type.objects.all()
    serializer_class = Document_typeViewSerializer
    
@api_view(['POST'])
def Payslip_type_create(request):
    if request.method == 'POST':
        # print(request.data.get('branch_id'))
        serializer = Payslip_typeCreateSerializer(data=request.data)
        if serializer.is_valid():
            Payslip_type_instance = serializer.save()
            return Response({
                'message': 'New Leave is Successfully Added!',
                # 'designation_id': Leave_instance.designation_id
            }, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
class Payslip_typeList(generics.ListAPIView):
    queryset = Payslip_type.objects.all()
    serializer_class = Payslip_typeViewSerializer
        
        
class Payslip_typeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Payslip_type.objects.all()
    serializer_class = Payslip_typeViewSerializer

@api_view(['POST'])
def Allowance_option_create(request):
    if request.method == 'POST':
        # print(request.data.get('branch_id'))
        serializer = Allowance_optionCreateSerializer(data=request.data)
        if serializer.is_valid():
            Allowance_option_instance = serializer.save()
            return Response({
                'message': 'New Leave is Successfully Added!',
                # 'designation_id': Leave_instance.designation_id
            }, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
class Allowance_optionList(generics.ListAPIView):
    queryset = Allowance_option.objects.all()
    serializer_class = Allowance_optionViewSerializer
        
        
class Allowance_optionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Allowance_option.objects.all()
    serializer_class = Allowance_optionViewSerializer

@api_view(['POST'])
def Loan_option_create(request):
    if request.method == 'POST':
        # print(request.data.get('branch_id'))
        serializer = Loan_optionCreateSerializer(data=request.data)
        if serializer.is_valid():
            Loan_option_instance = serializer.save()
            return Response({
                'message': 'New Leave is Successfully Added!',
                # 'designation_id': Leave_instance.designation_id
            }, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
class Loan_optionList(generics.ListAPIView):
    queryset = Loan_option.objects.all()
    serializer_class = Loan_optionViewSerializer
        
        
class Loan_optionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Loan_option.objects.all()
    serializer_class = Loan_optionViewSerializer

@api_view(['POST'])
def Deduction_option_create(request):
    if request.method == 'POST':
        # print(request.data.get('branch_id'))
        serializer = Deduction_optionCreateSerializer(data=request.data)
        if serializer.is_valid():
            Deduction_option_instance = serializer.save()
            return Response({
                'message': 'New Leave is Successfully Added!',
                # 'designation_id': Leave_instance.designation_id
            }, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
class Deduction_optionList(generics.ListAPIView):
    queryset = Deduction_option.objects.all()
    serializer_class = Deduction_optionViewSerializer
        
        
class Deduction_optionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Deduction_option.objects.all()
    serializer_class = Deduction_optionViewSerializer

@api_view(['POST'])
def Goal_type_create(request):
    if request.method == 'POST':
        # print(request.data.get('branch_id'))
        serializer = Goal_typeCreateSerializer(data=request.data)
        if serializer.is_valid():
            Goal_type_instance = serializer.save()
            return Response({
                'message': 'New Leave is Successfully Added!',
                # 'designation_id': Leave_instance.designation_id
            }, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
class Goal_typeList(generics.ListAPIView):
    queryset = Goal_type.objects.all()
    serializer_class = Goal_typeViewSerializer
        
        
class Goal_typeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Goal_type.objects.all()
    serializer_class = Goal_typeViewSerializer

@api_view(['POST'])
def Training_type_create(request):
    if request.method == 'POST':
        # print(request.data.get('branch_id'))
        serializer = Training_typeCreateSerializer(data=request.data)
        if serializer.is_valid():
            Training_type_instance = serializer.save()
            return Response({
                'message': 'New Leave is Successfully Added!',
                # 'designation_id': Leave_instance.designation_id
            }, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
class Training_typeList(generics.ListAPIView):
    queryset = Training_type.objects.all()
    serializer_class = Training_typeViewSerializer
        
        
class Training_typeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Training_type.objects.all()
    serializer_class = Training_typeViewSerializer

@api_view(['POST'])
def Award_type_create(request):
    if request.method == 'POST':
        # print(request.data.get('branch_id'))
        serializer = Award_typeCreateSerializer(data=request.data)
        if serializer.is_valid():
            Award_type_instance = serializer.save()
            return Response({
                'message': 'New Leave is Successfully Added!',
                # 'designation_id': Leave_instance.designation_id
            }, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
class Award_typeList(generics.ListAPIView):
    queryset = Award_type.objects.all()
    serializer_class = Award_typeViewSerializer
        
        
class Award_typeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Award_type.objects.all()
    serializer_class = Award_typeViewSerializer

@api_view(['POST'])
def Termination_type_create(request):
    if request.method == 'POST':
        # print(request.data.get('branch_id'))
        serializer = Termination_typeCreateSerializer(data=request.data)
        if serializer.is_valid():
            Termination_type_instance = serializer.save()
            return Response({
                'message': 'New Leave is Successfully Added!',
                # 'designation_id': Leave_instance.designation_id
            }, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
class Termination_typeList(generics.ListAPIView):
    queryset = Termination_type.objects.all()
    serializer_class = Termination_typeViewSerializer
        
        
class Termination_typeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Termination_type.objects.all()
    serializer_class = Termination_typeViewSerializer

@api_view(['POST'])
def Job_category_create(request):
    if request.method == 'POST':
        # print(request.data.get('branch_id'))
        serializer = Job_categoryCreateSerializer(data=request.data)
        if serializer.is_valid():
            Job_category_instance = serializer.save()
            return Response({
                'message': 'New Leave is Successfully Added!',
                # 'designation_id': Leave_instance.designation_id
            }, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
class Job_categoryList(generics.ListAPIView):
    queryset = Job_category.objects.all()
    serializer_class = Job_categoryViewSerializer
        
        
class Job_categoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Job_category.objects.all()
    serializer_class = Job_categoryViewSerializer

@api_view(['POST'])
def Job_stage_create(request):
    if request.method == 'POST':
        # print(request.data.get('branch_id'))
        serializer = Job_stageCreateSerializer(data=request.data)
        if serializer.is_valid():
            Job_stage_instance = serializer.save()
            return Response({
                'message': 'New Leave is Successfully Added!',
                # 'designation_id': Leave_instance.designation_id
            }, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
class Job_stageList(generics.ListAPIView):
    queryset = Job_stage.objects.all()
    serializer_class = Job_stageViewSerializer
        
        
class Job_stageDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Job_stage.objects.all()
    serializer_class = Job_stageViewSerializer

@api_view(['POST'])
def Competencies_create(request):
    if request.method == 'POST':
        # print(request.data.get('branch_id'))
        serializer = CompetenciesCreateSerializer(data=request.data)
        if serializer.is_valid():
            Competencies_instance = serializer.save()
            return Response({
                'message': 'New Leave is Successfully Added!',
                # 'designation_id': Leave_instance.designation_id
            }, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
class CompetenciesList(generics.ListAPIView):
    queryset = Competencies.objects.all()
    serializer_class = CompetenciesViewSerializer
        
        
class CompetenciesDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Competencies.objects.all()
    serializer_class = CompetenciesViewSerializer

@api_view(['POST'])
def Expence_type_create(request):
    if request.method == 'POST':
        # print(request.data.get('branch_id'))
        serializer = Expence_typeCreateSerializer(data=request.data)
        if serializer.is_valid():
            Expence_type_instance = serializer.save()
            return Response({
                'message': 'New Leave is Successfully Added!',
                # 'designation_id': Leave_instance.designation_id
            }, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
class Expence_typeList(generics.ListAPIView):
    queryset = Expence_type.objects.all()
    serializer_class = Expence_typeViewSerializer
        
        
class Expence_typeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Expence_type.objects.all()
    serializer_class = Expence_typeViewSerializer

@api_view(['POST'])
def Income_type_create(request):
    if request.method == 'POST':
        # print(request.data.get('branch_id'))
        serializer = Income_typeCreateSerializer(data=request.data)
        if serializer.is_valid():
            Income_type_instance = serializer.save()
            return Response({
                'message': 'New Leave is Successfully Added!',
                # 'designation_id': Leave_instance.designation_id
            }, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
class Income_typeList(generics.ListAPIView):
    queryset = Income_type.objects.all()
    serializer_class = Income_typeViewSerializer
        
        
class Income_typeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Income_type.objects.all()
    serializer_class = Income_typeViewSerializer

@api_view(['POST'])
def Payment_type_create(request):
    if request.method == 'POST':
        # print(request.data.get('branch_id'))
        serializer = Payment_typeCreateSerializer(data=request.data)
        if serializer.is_valid():
            Payment_type_instance = serializer.save()
            return Response({
                'message': 'New Leave is Successfully Added!',
                # 'designation_id': Leave_instance.designation_id
            }, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
class Payment_typeList(generics.ListAPIView):
    queryset = Payment_type.objects.all()
    serializer_class = Payment_typeViewSerializer
        
        
class Payment_typeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Payment_type.objects.all()
    serializer_class = Payment_typeViewSerializer

@api_view(['POST'])
def Contract_type_create(request):
    if request.method == 'POST':
        # print(request.data.get('branch_id'))
        serializer = Contract_typeCreateSerializer(data=request.data)
        if serializer.is_valid():
            Contract_type_instance = serializer.save()
            return Response({
                'message': 'New Leave is Successfully Added!',
                # 'designation_id': Leave_instance.designation_id
            }, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
class Contract_typeList(generics.ListAPIView):
    queryset = Contract_type.objects.all()
    serializer_class = Contract_typeViewSerializer
        
        
class Contract_typeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Contract_type.objects.all()
    serializer_class = Contract_typeViewSerializer

@api_view(['POST'])
def Performance_type_create(request):
    if request.method == 'POST':
        # print(request.data.get('branch_id'))
        serializer = Performance_typeCreateSerializer(data=request.data)
        if serializer.is_valid():
            Performance_type_instance = serializer.save()
            return Response({
                'message': 'New Leave is Successfully Added!',
                # 'designation_id': Leave_instance.designation_id
            }, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
class Performance_typeList(generics.ListAPIView):
    queryset = Performance_type.objects.all()
    serializer_class = Performance_typeViewSerializer
        
        
class Performance_typeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Performance_type.objects.all()
    serializer_class = Performance_typeViewSerializer
    
# Add your new views here
@api_view(['POST'])
def Module_create(request):
    if request.method == 'POST':
        # print(request.data.get('branch_id'))
        serializer = ModuleSerializer(data=request.data)
        if serializer.is_valid():
            Performance_type_instance = serializer.save()
            return Response({
                'message': 'New Leave is Successfully Added!',
                # 'designation_id': Leave_instance.designation_id
            }, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ModuleViewSet(generics.ListAPIView):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer

@api_view(['POST'])
def PermissionCreate(request):
    if request.method == 'POST':
        # print(request.data.get('branch_id'))
        serializer = PermissionSerializer(data=request.data)
        if serializer.is_valid():
            Performance_type_instance = serializer.save()
            return Response({
                'message': 'New Leave is Successfully Added!',
                # 'designation_id': Leave_instance.designation_id
            }, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class PermissionViewSet(generics.ListAPIView):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer

@api_view(['POST'])
def role_create(request):
    if request.method == 'POST':
        # print(request.data.get('branch_id'))
        serializer = RoleCreateSerializer(data=request.data)
        if serializer.is_valid():
            Performance_type_instance = serializer.save()
            return Response({
                'message': 'New Leave is Successfully Added!',
                # 'designation_id': Leave_instance.designation_id
            }, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RoleViewSet(generics.ListAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    
@api_view(['PUT'])
def update_role(request, pk):
    try:
        role = Role.objects.get(pk=pk)
    except Role.DoesNotExist:
        return Response({'error': 'Role not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = RoleCreateSerializer(role, data=request.data)
    if serializer.is_valid():
        role = serializer.save()
        return Response({
            'message': 'Role updated successfully!',
            'role_id': role.id
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class RoleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

class RoleUpdateDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleCreateSerializer

        
class RolePermissionViewSet(generics.ListAPIView):
    queryset = RolePermission.objects.all()
    serializer_class = RolePermissionSerializer

@api_view(['POST'])
def EmployeeCreate(request):
    serializer = EmployeeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Employee created successfully!'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployeeListView(generics.ListAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeViewSerializer
    
class EmployeeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeViewSerializer
    

@api_view(['POST'])
def EmployeeSalaryCreate(request):
    if request.method == 'POST':
        # print(request.data.get('branch_id'))
        serializer = Employee_SalaryCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'New Role is Successfully Added!',
                # 'designation_id': Leave_instance.designation_id
            }, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EmployeeSalaryListView(generics.ListAPIView):
    queryset = Employee_Salary.objects.all()
    serializer_class = Employee_SalaryViewSerializer
    
class EmployeeSalaryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee_Salary.objects.all()
    serializer_class = Employee_SalaryViewSerializer

    
@api_view(['POST'])
def AllowanceCreate(request):
    if request.method == 'POST':
        # print(request.data.get('branch_id'))
        serializer = AllowanceCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'New Role is Successfully Added!',
                # 'designation_id': Leave_instance.designation_id
            }, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AllowanceListView(generics.ListAPIView):
    queryset = Allowance.objects.all()
    serializer_class = AllowanceViewSerializer

class AllowanceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Allowance.objects.all()
    serializer_class = AllowanceViewSerializer

    
@api_view(['POST'])
def CommissionCreate(request):
    if request.method == 'POST':
        # print(request.data.get('branch_id'))
        serializer = CommissionCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'New Role is Successfully Added!',
                # 'designation_id': Leave_instance.designation_id
            }, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  


class CommissionListView(generics.ListAPIView):
    queryset = Commission.objects.all()
    serializer_class = CommissionViewSerializer

class CommissionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Commission.objects.all()
    serializer_class = CommissionViewSerializer
    
@api_view(['POST'])
def LoanCreate(request):
    if request.method == 'POST':
        # print(request.data.get('branch_id'))
        serializer = LoanCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'New Role is Successfully Added!',
                # 'designation_id': Leave_instance.designation_id
            }, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  

class LoanListView(generics.ListAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanViewSerializer

class LoanDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanViewSerializer
    
@api_view(['POST'])
def Saturation_DeductionCreate(request):
    if request.method == 'POST':
        # print(request.data.get('branch_id'))
        serializer = SaturationDeductionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'New Role is Successfully Added!',
                # 'designation_id': Leave_instance.designation_id
            }, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)      

class Saturation_DeductionList(generics.ListAPIView):
    queryset = Saturation_Deduction.objects.all()
    serializer_class = SaturationDeductionSerializer

class Saturation_DeductionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Saturation_Deduction.objects.all()
    serializer_class = SaturationDeductionSerializer

@api_view(['POST'])
def Other_PaymentCreate(request):
    if request.method == 'POST':
        # print(request.data.get('branch_id'))
        serializer = OtherPaymentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'New Role is Successfully Added!',
                # 'designation_id': Leave_instance.designation_id
            }, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

class Other_PaymentList(generics.ListAPIView):
    queryset = Other_Payment.objects.all()
    serializer_class = OtherPaymentSerializer

class Other_PaymentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Other_Payment.objects.all()
    serializer_class = OtherPaymentSerializer

@api_view(['POST'])
def OvertimeCreate(request):
    if request.method == 'POST':
        # print(request.data.get('branch_id'))
        serializer = OvertimeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'New Role is Successfully Added!',
                # 'designation_id': Leave_instance.designation_id
            }, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

class OvertimeList(generics.ListAPIView):
    queryset = Overtime.objects.all()
    serializer_class = OvertimeSerializer

class OvertimeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Overtime.objects.all()
    serializer_class = OvertimeSerializer
    
@api_view(['POST'])
def TimesheetCreate(request):
    if request.method == 'POST':
        # print(request.data.get('branch_id'))
        serializer = TimesheetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'New Role is Successfully Added!',
                # 'designation_id': Leave_instance.designation_id
            }, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    


class TimesheetList(generics.ListAPIView):
    queryset = timesheet.objects.all()
    serializer_class = TimesheetSerializer

class TimesheetDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = timesheet.objects.all()
    serializer_class = TimesheetSerializer
    
@api_view(['POST'])
def Create_LeavesCreate(request):
    if request.method == 'POST':
        # print(request.data.get('branch_id'))
        serializer = CreateLeavesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'New Role is Successfully Added!',
                # 'designation_id': Leave_instance.designation_id
            }, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  

class Create_LeavesList(generics.ListAPIView):
    queryset = Create_Leaves.objects.all()
    serializer_class = CreateLeavesSerializer

class Create_LeavesDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Create_Leaves.objects.all()
    serializer_class = CreateLeavesSerializer

@api_view(['POST'])
def IndicatorCreate(request):
    if request.method == 'POST':
        # print(request.data.get('branch_id'))
        serializer = IndicatorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'New Role is Successfully Added!',
                # 'designation_id': Leave_instance.designation_id
            }, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  

class IndicatorList(generics.ListAPIView):
    queryset = Indicator.objects.all()
    serializer_class = IndicatorSerializer

class IndicatorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Indicator.objects.all()
    serializer_class = IndicatorSerializer

@api_view(['POST'])
def AppraisalCreate(request):
    if request.method == 'POST':
        # print(request.data.get('branch_id'))
        serializer = AppraisalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'New Role is Successfully Added!',
                # 'designation_id': Leave_instance.designation_id
            }, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  

class AppraisalList(generics.ListAPIView):
    queryset = Appraisal.objects.all()
    serializer_class = AppraisalSerializer

class AppraisalDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Appraisal.objects.all()
    serializer_class = AppraisalSerializer


@api_view(['POST'])
def Goal_trackingCreate(request):
    if request.method == 'POST':
        # print(request.data.get('branch_id'))
        serializer = GoalTrackingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'New Role is Successfully Added!',
                # 'designation_id': Leave_instance.designation_id
            }, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  

class Goal_trackingList(generics.ListAPIView):
    queryset = Goal_tracking.objects.all()
    serializer_class = GoalTrackingSerializer

class Goal_trackingDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Goal_tracking.objects.all()
    serializer_class = GoalTrackingSerializer

@api_view(['POST'])
def AccountCreate(request):
    if request.method == 'POST':
        # print(request.data.get('branch_id'))
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'New Role is Successfully Added!',
                # 'designation_id': Leave_instance.designation_id
            }, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  


class AccountList(generics.ListAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

class AccountDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

@api_view(['POST'])
def PayeeCreate(request):
    if request.method == 'POST':
        # print(request.data.get('branch_id'))
        serializer = PayeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'New Role is Successfully Added!',
                # 'designation_id': Leave_instance.designation_id
            }, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  

class PayeeList(generics.ListAPIView):
    queryset = Payee.objects.all()
    serializer_class = PayeeSerializer

class PayeeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Payee.objects.all()
    serializer_class = PayeeSerializer

@api_view(['POST'])
def PayerCreate(request):
    if request.method == 'POST':
        # print(request.data.get('branch_id'))
        serializer = PayerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'New Role is Successfully Added!',
                # 'designation_id': Leave_instance.designation_id
            }, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  

class PayerList(generics.ListAPIView):
    queryset = Payer.objects.all()
    serializer_class = PayerSerializer

class PayerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Payer.objects.all()
    serializer_class = PayerSerializer

@api_view(['POST'])
def DepositCreate(request):
    if request.method == 'POST':
        # print(request.data.get('branch_id'))
        serializer = DepositSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'New Role is Successfully Added!',
                # 'designation_id': Leave_instance.designation_id
            }, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  

class DepositList(generics.ListAPIView):
    queryset = Deposit.objects.all()
    serializer_class = DepositSerializer

class DepositDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Deposit.objects.all()
    serializer_class = DepositSerializer

@api_view(['POST'])
def ExpenseCreate(request):
    if request.method == 'POST':
        # print(request.data.get('branch_id'))
        serializer = ExpenseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'New Role is Successfully Added!',
                # 'designation_id': Leave_instance.designation_id
            }, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  

class ExpenseList(generics.ListAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

class ExpenseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

@api_view(['POST'])
def Transfer_balanceCreate(request):
    if request.method == 'POST':
        # print(request.data.get('branch_id'))
        serializer = TransferBalanceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'New Role is Successfully Added!',
                # 'designation_id': Leave_instance.designation_id
            }, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  

class Transfer_balanceList(generics.ListAPIView):
    queryset = Transfer_balance.objects.all()
    serializer_class = TransferBalanceSerializer

class Transfer_balanceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Transfer_balance.objects.all()
    serializer_class = TransferBalanceSerializer

@api_view(['POST'])
def TrainingCreate(request):
    if request.method == 'POST':
        # print(request.data.get('branch_id'))
        serializer = TrainingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'New Role is Successfully Added!',
                # 'designation_id': Leave_instance.designation_id
            }, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  

class TrainingList(generics.ListAPIView):
    queryset = Training.objects.all()
    serializer_class = TrainingSerializer

class TrainingDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Training.objects.all()
    serializer_class = TrainingSerializer

@api_view(['POST'])
def TrainerCreate(request):
    if request.method == 'POST':
        # print(request.data.get('branch_id'))
        serializer = TrainerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'New Role is Successfully Added!',
                # 'designation_id': Leave_instance.designation_id
            }, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  

class TrainerList(generics.ListAPIView):
    queryset = Trainer.objects.all()
    serializer_class = TrainerSerializer

class TrainerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Trainer.objects.all()
    serializer_class = TrainerSerializer

@api_view(['POST'])
def AwardCreate(request):
    if request.method == 'POST':
        # print(request.data.get('branch_id'))
        serializer = AwardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'New Role is Successfully Added!',
                # 'designation_id': Leave_instance.designation_id
            }, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  

class AwardList(generics.ListAPIView):
    queryset = Award.objects.all()
    serializer_class = AwardSerializer

class AwardDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Award.objects.all()
    serializer_class = AwardSerializer

@api_view(['POST'])
def TransferCreate(request):
    if request.method == 'POST':
        # print(request.data.get('branch_id'))
        serializer = TransferSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'New Role is Successfully Added!',
                # 'designation_id': Leave_instance.designation_id
            }, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  

class TransferList(generics.ListAPIView):
    queryset = Transfer.objects.all()
    serializer_class = TransferSerializer

class TransferDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Transfer.objects.all()
    serializer_class = TransferSerializer

@api_view(['POST'])
def ResignationCreate(request):
    if request.method == 'POST':
        # print(request.data.get('branch_id'))
        serializer = ResignationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'New Role is Successfully Added!',
                # 'designation_id': Leave_instance.designation_id
            }, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  


class ResignationList(generics.ListAPIView):
    queryset = Resignation.objects.all()
    serializer_class = ResignationSerializer

class ResignationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Resignation.objects.all()
    serializer_class = ResignationSerializer


@api_view(['POST'])
def TripCreate(request):
    if request.method == 'POST':
        # print(request.data.get('branch_id'))
        serializer = TripSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'New Role is Successfully Added!',
                # 'designation_id': Leave_instance.designation_id
            }, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  

class TripList(generics.ListAPIView):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer

class TripDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer

@api_view(['POST'])
def PromotionCreate(request):
    if request.method == 'POST':
        # print(request.data.get('branch_id'))
        serializer = PromotionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'New Role is Successfully Added!',
                # 'designation_id': Leave_instance.designation_id
            }, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  

class PromotionList(generics.ListAPIView):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer

class PromotionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer

@api_view(['POST'])
def ComplaintCreate(request):
    if request.method == 'POST':
        # print(request.data.get('branch_id'))
        serializer = ComplaintSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'New Role is Successfully Added!',
                # 'designation_id': Leave_instance.designation_id
            }, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  

class ComplaintList(generics.ListAPIView):
    queryset = Complaint.objects.all()
    serializer_class = ComplaintSerializer

class ComplaintDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Complaint.objects.all()
    serializer_class = ComplaintSerializer

@api_view(['POST'])
def WarningCreate(request):
    if request.method == 'POST':
        # print(request.data.get('branch_id'))
        serializer = WarningSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'New Role is Successfully Added!',
                # 'designation_id': Leave_instance.designation_id
            }, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  

class WarningList(generics.ListAPIView):
    queryset = Warning.objects.all()
    serializer_class = WarningSerializer

class WarningDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Warning.objects.all()
    serializer_class = WarningSerializer

@api_view(['POST'])
def TerminationCreate(request):
    if request.method == 'POST':
        # print(request.data.get('branch_id'))
        serializer = TerminationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'New Role is Successfully Added!',
                # 'designation_id': Leave_instance.designation_id
            }, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  

class TerminationList(generics.ListAPIView):
    queryset = Termination.objects.all()
    serializer_class = TerminationSerializer

class TerminationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Termination.objects.all()
    serializer_class = TerminationSerializer

@api_view(['POST'])
def AnnouncementCreate(request):
    if request.method == 'POST':
        # print(request.data.get('branch_id'))
        serializer = AnnouncementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'New Role is Successfully Added!',
                # 'designation_id': Leave_instance.designation_id
            }, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  

class AnnouncementList(generics.ListAPIView):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer

class AnnouncementDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer

@api_view(['POST'])
def HolidayCreate(request):
    if request.method == 'POST':
        # print(request.data.get('branch_id'))
        serializer = HolidaySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'New Role is Successfully Added!',
                # 'designation_id': Leave_instance.designation_id
            }, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  

class HolidayList(generics.ListAPIView):
    queryset = Holiday.objects.all()
    serializer_class = HolidaySerializer

class HolidayDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Holiday.objects.all()
    serializer_class = HolidaySerializer

@api_view(['POST'])
def JobCreate(request):
    if request.method == 'POST':
        # print(request.data.get('branch_id'))
        serializer = JobSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'New Role is Successfully Added!',
                # 'designation_id': Leave_instance.designation_id
            }, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  

class JobList(generics.ListAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer

class JobDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer

@api_view(['POST'])
def Job_ApplicationCreate(request):
    if request.method == 'POST':
        # print(request.data.get('branch_id'))
        serializer = JobApplicationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'New Role is Successfully Added!',
                # 'designation_id': Leave_instance.designation_id
            }, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  


class Job_ApplicationList(generics.ListAPIView):
    queryset = Job_Application.objects.all()
    serializer_class = JobApplicationSerializer

class Job_ApplicationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Job_Application.objects.all()
    serializer_class = JobApplicationSerializer

@api_view(['POST'])
def Job_On_BoardingCreate(request):
    if request.method == 'POST':
        # print(request.data.get('branch_id'))
        serializer = JobOnBoardingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'New Role is Successfully Added!',
                # 'designation_id': Leave_instance.designation_id
            }, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  

class Job_On_BoardingList(generics.ListAPIView):
    queryset = Job_On_Boarding.objects.all()
    serializer_class = JobOnBoardingSerializer

class Job_On_BoardingDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Job_On_Boarding.objects.all()
    serializer_class = JobOnBoardingSerializer

@api_view(['POST'])
def Interview_scheduleCreate(request):
    if request.method == 'POST':
        # print(request.data.get('branch_id'))
        serializer = InterviewScheduleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'New Role is Successfully Added!',
                # 'designation_id': Leave_instance.designation_id
            }, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  

class Interview_scheduleList(generics.ListAPIView):
    queryset = Interview_schedule.objects.all()
    serializer_class = InterviewScheduleSerializer

class Interview_scheduleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Interview_schedule.objects.all()
    serializer_class = InterviewScheduleSerializer

@api_view(['POST'])
def ContractCreate(request):
    if request.method == 'POST':
        # print(request.data.get('branch_id'))
        serializer = ContractSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'New Role is Successfully Added!',
                # 'designation_id': Leave_instance.designation_id
            }, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  

class ContractList(generics.ListAPIView):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer

class ContractDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer

@api_view(['POST'])
def TicketCreate(request):
    if request.method == 'POST':
        # print(request.data.get('branch_id'))
        serializer = TicketSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'New Role is Successfully Added!',
                # 'designation_id': Leave_instance.designation_id
            }, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  

class TicketList(generics.ListAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

class TicketDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer

@api_view(['POST'])
def EventCreate(request):
    if request.method == 'POST':
        # print(request.data.get('branch_id'))
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'New Role is Successfully Added!',
                # 'designation_id': Leave_instance.designation_id
            }, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  

class EventList(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

@api_view(['POST'])
def MeetingCreate(request):
    if request.method == 'POST':
        # print(request.data.get('branch_id'))
        serializer = MeetingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'New Role is Successfully Added!',
                # 'designation_id': Leave_instance.designation_id
            }, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  


class MeetingList(generics.ListAPIView):
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer

class MeetingDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer

@api_view(['POST'])
def ZoomCreate(request):
    if request.method == 'POST':
        # print(request.data.get('branch_id'))
        serializer = ZoomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'New Role is Successfully Added!',
                # 'designation_id': Leave_instance.designation_id
            }, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  

class ZoomList(generics.ListAPIView):
    queryset = Zoom.objects.all()
    serializer_class = ZoomSerializer

class ZoomDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Zoom.objects.all()
    serializer_class = ZoomSerializer

@api_view(['POST'])
def AssetsCreate(request):
    if request.method == 'POST':
        # print(request.data.get('branch_id'))
        serializer = AssetsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'New Role is Successfully Added!',
                # 'designation_id': Leave_instance.designation_id
            }, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AssetsList(generics.ListAPIView):
    queryset = Assets.objects.all()
    serializer_class = AssetsSerializer
  

class AssetsDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Assets.objects.all()
    serializer_class = AssetsSerializer

@api_view(['POST'])
def DocumentCreate(request):
    if request.method == 'POST':
        # print(request.data.get('branch_id'))
        serializer = DocumentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'New Role is Successfully Added!',
                # 'designation_id': Leave_instance.designation_id
            }, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  


class DocumentList(generics.ListAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

class DocumentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

@api_view(['POST'])
def create_company_policy(request):
    serializer = CompanyPolicySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        print(serializer.data['branch'])
        Justtry.objects.all()
        trythis=Justtry(name=serializer.data['branch'])
        trythis.save()
        print(Justtry.objects.all()[1].name,"try me")
        
        return Response({
            'message': 'Company policy created successfully!',
            # 'policy_id': policy.id
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

class CompanyPolicyList(generics.ListAPIView):
    queryset = CompanyPolicy.objects.all()
    serializer_class = CompanyPolicyViewSerializer

class CompanyPolicyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CompanyPolicy.objects.all()
    serializer_class = CompanyPolicyViewSerializer

@api_view(['PUT'])
def update_company_policy(request, pk):
    try:
        policy = CompanyPolicy.objects.get(pk=pk)
    except CompanyPolicy.DoesNotExist:
        return Response({'error': 'Policy not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = CompanyPolicySerializer(policy, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({
            'message': 'Company policy updated successfully!',
            'policy_id': serializer.instance.id
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_company_policy(request, pk):
    try:
        policy = CompanyPolicy.objects.get(pk=pk)
    except CompanyPolicy.DoesNotExist:
        return Response({'error': 'Policy not found'}, status=status.HTTP_404_NOT_FOUND)

    policy.delete()
    return Response({'message': 'Company policy deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

