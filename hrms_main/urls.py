from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from .views import Award_type_create, Award_typeDetailView, Award_typeList, Competencies_create, CompetenciesDetailView, CompetenciesList, Contract_type_create, Contract_typeDetailView, Contract_typeList, Expence_type_create, Expence_typeDetailView, Expence_typeList, Goal_type_create, Goal_typeDetailView, Goal_typeList, Income_type_create, Income_typeDetailView, Income_typeList, Job_category_create, Job_categoryDetailView, Job_categoryList, Job_stage_create, Job_stageDetailView, Job_stageList, LoginView, LogoutView, Payment_type_create, Payment_typeDetailView, Payment_typeList, Performance_type_create, Performance_typeDetailView, Performance_typeList, RegisterView,  Termination_type_create, Termination_typeDetailView, Termination_typeList, Training_type_create, Training_typeDetailView, Training_typeList, hello_world
from .views import branch_create, Department_create, Designation_create, Leave_create, Document_type_create, Payslip_type_create, Allowance_option_create, Loan_option_create, Deduction_option_create
from .views import BranchList, BranchDetailView, DepartmentList, DepartmentDetailView, DesignationList, DesignationDetailView ,LeaveList ,LeaveDetailView, Document_typeList, Document_typeDetailView, Payslip_typeList, Payslip_typeDetailView, Allowance_optionList, Allowance_optionDetailView, Loan_optionList, Loan_optionDetailView, Deduction_optionList, Deduction_optionDetailView
from .views import *
urlpatterns = [
    
    path('', views.index, name='index'),
    path('api/hello/', hello_world),
    path('api/register/', RegisterView.as_view()),
    path('api/login/', LoginView.as_view()),
    path('api/logout/', LogoutView.as_view()),
    path('api/clock_in/', ClockInView.as_view()),
    path('api/clock_out/', ClockOutView.as_view()),
    path('api/user/', UserDetailView.as_view()),
    path('api/attandance/', AttendanceDetailView.as_view()),
    path('api/branch_create/', branch_create),
    path('api/branch_view/', BranchList.as_view()),
    path('api/branch_view/<int:pk>/', BranchDetailView.as_view()),
    path('api/department_create/', Department_create),
    path('api/department_view/', DepartmentList.as_view()),
    path('api/department_view/<int:pk>/', DepartmentDetailView.as_view()),
    path('api/designation_create/', Designation_create),
    path('api/designation_view/', DesignationList.as_view()),
    path('api/designation_view/<int:pk>/', DesignationDetailView.as_view()),
    path('api/leave_create/', Leave_create),
    path('api/leave_view/', LeaveList.as_view()),
    path('api/leave_view/<int:pk>/', LeaveDetailView.as_view()),
    path('api/document_type_create/', Document_type_create),
    path('api/document_type_view/', Document_typeList.as_view()),
    path('api/document_type_view/<int:pk>/', Document_typeDetailView.as_view()),
    path('api/payslip_type_create/', Payslip_type_create),
    path('api/payslip_type_view/', Payslip_typeList.as_view()),
    path('api/payslip_type_view/<int:pk>/', Payslip_typeDetailView.as_view()),
    path('api/allowance_option_create/', Allowance_option_create),
    path('api/allowance_option_view/', Allowance_optionList.as_view()),
    path('api/allowance_option_view/<int:pk>/', Allowance_optionDetailView.as_view()),
    path('api/loan_option_create/', Loan_option_create),
    path('api/loan_option_view/', Loan_optionList.as_view()),
    path('api/loan_option_view/<int:pk>/', Loan_optionDetailView.as_view()),
    path('api/deduction_option_create/', Deduction_option_create),
    path('api/deduction_option_view/', Deduction_optionList.as_view()),
    path('api/deduction_option_view/<int:pk>/', Deduction_optionDetailView.as_view()),
    # New APIs 
    path('api/goal_type_create/', Goal_type_create),
    path('api/goal_type_view/', Goal_typeList.as_view()),
    path('api/goal_type_view/<int:pk>/', Goal_typeDetailView.as_view()),
    path('api/training_type_create/', Training_type_create),
    path('api/training_type_view/', Training_typeList.as_view()),
    path('api/training_type_view/<int:pk>/', Training_typeDetailView.as_view()),
    path('api/award_type_create/', Award_type_create),
    path('api/award_type_view/', Award_typeList.as_view()),
    path('api/award_type_view/<int:pk>/', Award_typeDetailView.as_view()),
    path('api/termination_type_create/', Termination_type_create),
    path('api/termination_type_view/', Termination_typeList.as_view()),
    path('api/termination_type_view/<int:pk>/', Termination_typeDetailView.as_view()),
    path('api/job_category_create/', Job_category_create),
    path('api/job_category_view/', Job_categoryList.as_view()),
    path('api/job_category_view/<int:pk>/', Job_categoryDetailView.as_view()),
    path('api/job_stage_create/', Job_stage_create),
    path('api/job_stage_view/', Job_stageList.as_view()),
    path('api/job_stage_view/<int:pk>/', Job_stageDetailView.as_view()),
    path('api/performance_type_create/', Performance_type_create),
    path('api/performance_type_view/', Performance_typeList.as_view()),
    path('api/performance_type_view/<int:pk>/', Performance_typeDetailView.as_view()),
    path('api/compentencies_create/', Competencies_create),
    path('api/compentencies_view/', CompetenciesList.as_view()),
    path('api/compentencies_view/<int:pk>/', CompetenciesDetailView.as_view()),
    path('api/expence_type_create/', Expence_type_create),
    path('api/expence_type_view/', Expence_typeList.as_view()),
    path('api/expence_type_view/<int:pk>/', Expence_typeDetailView.as_view()),
    path('api/income_type_create/', Income_type_create),
    path('api/income_type_view/', Income_typeList.as_view()),
    path('api/income_type_view/<int:pk>/', Income_typeDetailView.as_view()),
    path('api/payment_type_create/', Payment_type_create),
    path('api/payment_type_view/', Payment_typeList.as_view()),
    path('api/payment_type_view/<int:pk>/', Payment_typeDetailView.as_view()),
    path('api/contract_type_create/', Contract_type_create),
    path('api/contract_type_view/', Contract_typeList.as_view()),
    path('api/contract_type_view/<int:pk>/', Contract_typeDetailView.as_view()),
    
    #new apis
    path('api/modules_create/', Module_create),
    path('api/modules/', ModuleViewSet.as_view()),
    path('api/permissions_create/', PermissionCreate),
    path('api/permissions/', PermissionViewSet.as_view()),
    path('api/roles_create/', role_create),
    path('api/roles_view/', RoleViewSet.as_view()),
    path('api/roles_view/<int:pk>/', RoleDetailView.as_view()),
    path('api/roles_update/<int:pk>/', update_role),
    path('api/role_permissions/', RolePermissionViewSet.as_view()),
    
    path('api/employee_create/', EmployeeCreate),
    path('api/employee_view/', EmployeeListView.as_view()),
    path('api/employee_view/<int:pk>/', employee_detail),
  
    path('api/employee_salary_create/', EmployeeSalaryCreate),
    path('api/employee_salary_view/', EmployeeSalaryListView.as_view()),
    path('api/employee_salary_view/<int:pk>/', EmployeeSalaryDetailView.as_view()),
  
    path('api/allowance_create/', AllowanceCreate),
    path('api/allowance_view/', AllowanceListView.as_view()),
    path('api/allowance_view/<int:pk>/', AllowanceDetailView.as_view()),

    path('api/commission-create/', CommissionCreate),
    path('api/commission-view/', CommissionListView.as_view()),
    path('api/commission-view/<int:pk>/', CommissionDetailView.as_view()),

    path('api/loan-create/', LoanCreate),
    path('api/loan-view/', LoanListView.as_view()),
    path('api/loan-view/<int:pk>/', LoanDetailView.as_view()),
    
    path('api/saturation-deductions-create/', Saturation_DeductionCreate),
    path('api/saturation-deductions-view/', Saturation_DeductionList.as_view()),
    path('api/saturation-deductions-view/<int:pk>/', Saturation_DeductionDetailView.as_view()),
    
    path('api/other-payments-create/', Other_PaymentCreate),
    path('api/other-payments/', Other_PaymentList.as_view(), name='other-payment-list'),
    path('api/other-payments/<int:pk>/', Other_PaymentDetailView.as_view(), name='other-payment-detail'),
    
    path('api/overtimes-create/', OvertimeCreate),
    path('api/overtimes/', OvertimeList.as_view(), name='overtime-list'),
    path('api/overtimes/<int:pk>/', OvertimeDetailView.as_view(), name='overtime-detail'),
    
    path('api/timesheets-create/', TimesheetCreate),
    path('api/timesheets/', TimesheetList.as_view(), name='timesheet-list'),
    path('api/timesheets/<int:pk>/', TimesheetDetailView.as_view(), name='timesheet-detail'),
    
    path('api/create-leaves-create/', Create_LeavesCreate),
    path('api/create-leaves/', Create_LeavesList.as_view(), name='create-leaves-list'),
    path('api/create-leaves/<int:pk>/', Create_LeavesDetailView.as_view(), name='create-leaves-detail'),
    
    path('api/indicators-create/', IndicatorCreate),
    path('api/indicators/', IndicatorList.as_view(), name='indicator-list'),
    path('api/indicators/<int:pk>/', IndicatorDetailView.as_view(), name='indicator-detail'),
    
    path('api/appraisals-create/', AppraisalCreate),
    path('api/appraisals/', AppraisalList.as_view(), name='appraisal-list'),
    path('api/appraisals/<int:pk>/', AppraisalDetailView.as_view(), name='appraisal-detail'),
    
    path('api/goal-trackings-create/', Goal_trackingCreate),
    path('api/goal-trackings/', Goal_trackingList.as_view(), name='goal-tracking-list'),
    path('api/goal-trackings/<int:pk>/', Goal_trackingDetailView.as_view(), name='goal-tracking-detail'),
    
    path('api/accounts-create/', AccountCreate),
    path('api/accounts/', AccountList.as_view(), name='account-list'),
    path('api/accounts/<int:pk>/', AccountDetailView.as_view(), name='account-detail'),
    
    path('api/payees-create/', PayeeCreate),
    path('api/payees/', PayeeList.as_view(), name='payee-list'),
    path('api/payees/<int:pk>/', PayeeDetailView.as_view(), name='payee-detail'),
    
    path('api/payers-create/', PayerCreate),
    path('api/payers/', PayerList.as_view(), name='payer-list'),
    path('api/payers/<int:pk>/', PayerDetailView.as_view(), name='payer-detail'),
    
    path('api/deposits-create/', DepositCreate),
    path('api/deposits/', DepositList.as_view(), name='deposit-list'),
    path('api/deposits/<int:pk>/', DepositDetailView.as_view(), name='deposit-detail'),
    
    path('api/expenses-create/', ExpenseCreate),
    path('api/expenses/', ExpenseList.as_view(), name='expense-list'),
    path('api/expenses/<int:pk>/', ExpenseDetailView.as_view(), name='expense-detail'),
    
    path('api/transfer-balances-create/', Transfer_balanceCreate),
    path('api/transfer-balances/', Transfer_balanceList.as_view(), name='transfer-balance-list'),
    path('api/transfer-balances/<int:pk>/', Transfer_balanceDetailView.as_view(), name='transfer-balance-detail'),
    
    path('api/trainings-create/', TrainingCreate),
    path('api/trainings/', TrainingList.as_view(), name='training-list'),
    path('api/trainings/<int:pk>/', TrainingDetailView.as_view(), name='training-detail'),
    
    path('api/trainers-create/', TrainerCreate),
    path('api/trainers/', TrainerList.as_view(), name='trainer-list'),
    path('api/trainers/<int:pk>/', TrainerDetailView.as_view(), name='trainer-detail'),
    
    path('api/awards-create/', AwardCreate),
    path('api/awards/', AwardList.as_view(), name='award-list'),
    path('api/awards/<int:pk>/', AwardDetailView.as_view(), name='award-detail'),
    
    path('api/transfers-create/', TransferCreate),
    path('api/transfers/', TransferList.as_view(), name='transfer-list'),
    path('api/transfers/<int:pk>/', TransferDetailView.as_view(), name='transfer-detail'),
    
    path('api/resignations-create/', ResignationCreate),
    path('api/resignations/', ResignationList.as_view(), name='resignation-list'),
    path('api/resignations/<int:pk>/', ResignationDetailView.as_view(), name='resignation-detail'),
    
    path('api/trips-create/', TripCreate),
    path('api/trips/', TripList.as_view(), name='trip-list'),
    path('api/trips/<int:pk>/', TripDetailView.as_view(), name='trip-detail'),
    
    path('api/promotions-create/', PromotionCreate),
    path('api/promotions/', PromotionList.as_view(), name='promotion-list'),
    path('api/promotions/<int:pk>/', PromotionDetailView.as_view(), name='promotion-detail'),
    
    path('api/complaints-create/', ComplaintCreate),
    path('api/complaints/', ComplaintList.as_view(), name='complaint-list'),
    path('api/complaints/<int:pk>/', ComplaintDetailView.as_view(), name='complaint-detail'),
    
    path('api/warnings-create/', WarningCreate),
    path('api/warnings/', WarningList.as_view(), name='warning-list'),
    path('api/warnings/<int:pk>/', WarningDetailView.as_view(), name='warning-detail'),
    
    path('api/terminations-create/', TerminationCreate),
    path('api/terminations/', TerminationList.as_view(), name='termination-list'),
    path('api/terminations/<int:pk>/', TerminationDetailView.as_view(), name='termination-detail'),
    
    path('api/announcements-create/', AnnouncementCreate),
    path('api/announcements/', AnnouncementList.as_view(), name='announcement-list'),
    path('api/announcements/<int:pk>/', AnnouncementDetailView.as_view(), name='announcement-detail'),
    
    path('api/holidays-create/', HolidayCreate),
    path('api/holidays/', HolidayList.as_view(), name='holiday-list'),
    path('api/holidays/<int:pk>/', HolidayDetailView.as_view(), name='holiday-detail'),
    
    path('api/jobs-create/', JobCreate),
    path('api/jobs/', JobList.as_view(), name='job-list'),
    path('api/jobs/<int:pk>/', JobDetailView.as_view(), name='job-detail'),
    
    path('api/job-applications-create/', Job_ApplicationCreate),
    path('api/job-applications/', Job_ApplicationList.as_view(), name='job-application-list'),
    path('api/job-applications/<int:pk>/', Job_ApplicationDetailView.as_view(), name='job-application-detail'),
    
    path('api/job-on-boarding-create/', Job_On_BoardingCreate),
    path('api/job-on-boarding/', Job_On_BoardingList.as_view(), name='job-on-boarding-list'),
    path('api/job-on-boarding/<int:pk>/', Job_On_BoardingDetailView.as_view(), name='job-on-boarding-detail'),
    
    path('api/interview-schedules-create/', Interview_scheduleCreate),
    path('api/interview-schedules/', Interview_scheduleList.as_view(), name='interview-schedule-list'),
    path('api/interview-schedules/<int:pk>/', Interview_scheduleDetailView.as_view(), name='interview-schedule-detail'),
    
    path('api/contracts-create/', ContractCreate),
    path('api/contracts/', ContractList.as_view(), name='contract-list'),
    path('api/contracts/<int:pk>/', ContractDetailView.as_view(), name='contract-detail'),
    
    path('api/tickets-create/', TicketCreate),
    path('api/tickets/', TicketList.as_view(), name='ticket-list'),
    path('api/tickets/<int:pk>/', TicketDetailView.as_view(), name='ticket-detail'),
    
    path('api/events-create/', EventCreate),
    path('api/events/', EventList.as_view(), name='event-list'),
    path('api/events/<int:pk>/', EventDetailView.as_view(), name='event-detail'),
    
    path('api/meetings-create/', MeetingCreate),
    path('api/meetings/', MeetingList.as_view(), name='meeting-list'),
    path('api/meetings/<int:pk>/', MeetingDetailView.as_view(), name='meeting-detail'),
    
    path('api/zooms-create/', ZoomCreate),
    path('api/zooms/', ZoomList.as_view(), name='zoom-list'),
    path('api/zooms/<int:pk>/', ZoomDetailView.as_view(), name='zoom-detail'),
    
    path('api/assets-create/', AssetsCreate),
    path('api/assets/', AssetsList.as_view(), name='assets-list'),
    path('api/assets/<int:pk>/', AssetsDetailView.as_view(), name='assets-detail'),
    
    path('api/documents-create/', DocumentCreate),
    path('api/documents/', DocumentList.as_view(), name='document-list'),
    path('api/documents/<int:pk>/', DocumentDetailView.as_view(), name='document-detail'),
    
    path('api/company_policy_create/', create_company_policy),
    path('api/company-policies/', CompanyPolicyList.as_view()),
    path('api/company-policies/<int:pk>/', CompanyPolicyDetailView.as_view()),
    path('api/company_policy_update/<int:pk>/', update_company_policy),
    path('api/company_policy_delete/<int:pk>/', delete_company_policy),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)