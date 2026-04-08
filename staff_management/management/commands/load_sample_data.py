"""
Django management command to load sample data.
Run with: python manage.py load_sample_data
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import date, timedelta
from decimal import Decimal
import random

from staff_management.models import StaffCategory, Designation, Department, Staff, Allowance, Deduction
from salary_advances.models import SalaryAdvance
from payroll.models import PayrollPeriod, Payroll
from users.models import CustomUser

User = get_user_model()


class Command(BaseCommand):
    help = 'Load sample data into the database'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting sample data load...'))

        try:
            # Create users
            self.create_users()

            # Create staff categories
            categories = self.create_staff_categories()

            # Create departments
            departments = self.create_departments()

            # Create designations
            designations = self.create_designations(categories)

            # Create staff
            staff_list = self.create_staff(categories, designations, departments)

            # Create allowances
            self.create_allowances()

            # Create deductions
            self.create_deductions()

            # Create salary advances
            self.create_salary_advances(staff_list)

            # Create payroll periods and records
            self.create_payroll_data(staff_list)

            self.stdout.write(self.style.SUCCESS('✅ Sample data loaded successfully!'))
            self.print_summary(staff_list)

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error loading data: {str(e)}'))
            raise

    def create_users(self):
        """Create sample users with different roles"""
        users_data = [
            {
                'username': 'admin',
                'email': 'admin@smartstaff.ke',
                'first_name': 'Admin',
                'last_name': 'User',
                'role': 'admin',
                'password': 'admin123'
            },
            {
                'username': 'hrmanager',
                'email': 'hr@smartstaff.ke',
                'first_name': 'Sarah',
                'last_name': 'Johnson',
                'role': 'hr_manager',
                'password': 'hr123'
            },
            {
                'username': 'finance',
                'email': 'finance@smartstaff.ke',
                'first_name': 'David',
                'last_name': 'Williams',
                'role': 'finance',
                'password': 'finance123'
            },
            {
                'username': 'principal',
                'email': 'principal@smartstaff.ke',
                'first_name': 'Dr. Peter',
                'last_name': 'Kipchoge',
                'role': 'principal',
                'password': 'principal123'
            },
        ]

        created_count = 0
        for user_data in users_data:
            if not CustomUser.objects.filter(username=user_data['username']).exists():
                password = user_data.pop('password')
                user = CustomUser.objects.create_user(**user_data)
                user.set_password(password)
                user.save()
                created_count += 1

        self.stdout.write(f'  ✅ Created {created_count} users')

    def create_staff_categories(self):
        """Create staff categories"""
        categories_data = [
            {'name': 'Teaching Staff', 'description': 'Classroom teachers and subject specialists'},
            {'name': 'Non-Teaching Staff', 'description': 'Support and administrative staff'},
            {'name': 'Administrative Staff', 'description': 'Administrative and office management'},
            {'name': 'Support Staff', 'description': 'Drivers, janitors, and support personnel'},
            {'name': 'Management', 'description': 'Management and leadership staff'},
        ]

        categories = []
        created_count = 0
        for cat_data in categories_data:
            category, created = StaffCategory.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            if created:
                created_count += 1
            categories.append(category)

        self.stdout.write(f'  ✅ Created/Retrieved {created_count} staff categories')
        return categories

    def create_departments(self):
        """Create departments"""
        departments_data = [
            {'name': 'Primary Section', 'head_name': 'Mrs. Jane Mwangi', 'description': 'Classes 1-6'},
            {'name': 'Secondary Section', 'head_name': 'Mr. Joseph Kimani', 'description': 'Forms 1-4'},
            {'name': 'Science Department', 'head_name': 'Dr. Emily Kiplagat', 'description': 'Science subjects'},
            {'name': 'Languages Department', 'head_name': 'Mr. Thomas Omondi', 'description': 'English, Kiswahili, Languages'},
            {'name': 'Administration', 'head_name': 'Mrs. Rose Kipchoge', 'description': 'Administrative office'},
        ]

        departments = []
        created_count = 0
        for dept_data in departments_data:
            department, created = Department.objects.get_or_create(
                name=dept_data['name'],
                defaults={
                    'head_name': dept_data['head_name'],
                    'description': dept_data['description']
                }
            )
            if created:
                created_count += 1
            departments.append(department)

        self.stdout.write(f'  ✅ Created/Retrieved {created_count} departments')
        return departments

    def create_designations(self, categories):
        """Create job designations"""
        designations_data = [
            # Teaching Staff
            {'name': 'Class Teacher', 'category': categories[0], 'salary_scale': Decimal('45000'), 'description': 'Primary class teacher'},
            {'name': 'Form Teacher', 'category': categories[0], 'salary_scale': Decimal('55000'), 'description': 'Secondary form teacher'},
            {'name': 'Senior Teacher', 'category': categories[0], 'salary_scale': Decimal('65000'), 'description': 'Experienced teacher'},
            {'name': 'Head of Department', 'category': categories[0], 'salary_scale': Decimal('75000'), 'description': 'Department leadership'},

            # Non-Teaching Staff
            {'name': 'Office Assistant', 'category': categories[1], 'salary_scale': Decimal('25000'), 'description': 'Administrative support'},
            {'name': 'Driver', 'category': categories[1], 'salary_scale': Decimal('30000'), 'description': 'School transport'},
            {'name': 'Caretaker', 'category': categories[1], 'salary_scale': Decimal('22000'), 'description': 'Building maintenance'},

            # Administrative
            {'name': 'Secretary', 'category': categories[2], 'salary_scale': Decimal('35000'), 'description': 'Administrative secretary'},
            {'name': 'Accountant', 'category': categories[2], 'salary_scale': Decimal('50000'), 'description': 'Finance management'},

            # Support Staff
            {'name': 'Janitor', 'category': categories[3], 'salary_scale': Decimal('20000'), 'description': 'Cleaning and maintenance'},
            {'name': 'Security Guard', 'category': categories[3], 'salary_scale': Decimal('25000'), 'description': 'School security'},

            # Management
            {'name': 'Deputy Principal', 'category': categories[4], 'salary_scale': Decimal('85000'), 'description': 'School management'},
            {'name': 'Principal', 'category': categories[4], 'salary_scale': Decimal('100000'), 'description': 'School leadership'},
        ]

        designations = []
        created_count = 0
        for desig_data in designations_data:
            category = desig_data.pop('category')
            designation, created = Designation.objects.get_or_create(
                name=desig_data['name'],
                defaults={**desig_data, 'category': category}
            )
            if created:
                created_count += 1
            designations.append(designation)

        self.stdout.write(f'  ✅ Created/Retrieved {created_count} designations')
        return designations

    def create_staff(self, categories, designations, departments):
        """Create sample staff members"""
        first_names = ['John', 'Mary', 'Joseph', 'Susan', 'David', 'Grace', 'Peter', 'Elizabeth',
                      'Michael', 'Patricia', 'James', 'Margaret', 'Robert', 'Anna', 'Thomas',
                      'Catherine', 'Charles', 'Sarah', 'William', 'Jennifer', 'Samuel', 'Rachel',
                      'Daniel', 'Lisa', 'Richard']

        last_names = ['Kipchoge', 'Mwangi', 'Kimani', 'Omondi', 'Kiplagat', 'Kipkemboi', 'Moraa',
                     'Kipketer', 'Kiplagat', 'Kirui', 'Kiplagat', 'Kipkemei', 'Kipchirchir',
                     'Kiplagat', 'Maiyan', 'Kiplagat', 'Kipkemboi', 'Kipkogei', 'Kipchirchir',
                     'Kiplagat', 'Kipkemei', 'Kemboi', 'Kiplagat', 'Kipkogei', 'Kipchoge']

        middle_names = ['Moses', 'Grace', 'David', 'Ruth', 'Samuel', 'Mercy', 'Peter', 'Joy',
                       'Kenneth', 'Faith', 'Paul', 'Hope', 'Steven', 'Gloria', 'Daniel']

        staff_ids = [f'ST{str(i).zfill(4)}' for i in range(1, 26)]

        desig_teaching = designations[0:4]  # Teaching designations
        desig_support = designations[4:7]   # Support designations
        desig_admin = designations[7:9]     # Admin designations

        staff_list = []
        created_count = 0

        for idx in range(25):
            staff_id = staff_ids[idx]
            first_name = first_names[idx]
            last_name = last_names[idx]
            middle_name = random.choice(middle_names)
            email = f'{first_name.lower()}.{last_name.lower()}@school.ke'

            # Assign designations
            if idx < 12:  # Teaching staff
                designation = random.choice(desig_teaching)
                category = categories[0]
                dept = random.choice(departments[0:3])
            elif idx < 18:  # Support staff
                designation = random.choice(desig_support)
                category = categories[1]
                dept = departments[4]
            elif idx < 22:  # Admin staff
                designation = random.choice(desig_admin)
                category = categories[2]
                dept = departments[4]
            else:  # Management
                designation = designations[-1] if idx < 24 else designations[-2]  # Principal or Deputy
                category = categories[4]
                dept = departments[4]

            if not Staff.objects.filter(staff_id=staff_id).exists():
                staff = Staff.objects.create(
                    staff_id=staff_id,
                    first_name=first_name,
                    middle_name=middle_name,
                    last_name=last_name,
                    email=email,
                    phone_number=f'07{str(random.randint(10000000, 99999999))}',
                    date_of_birth=date(1980 + random.randint(0, 20), random.randint(1, 12), random.randint(1, 28)),
                    gender=random.choice(['M', 'F']),
                    category=category,
                    designation=designation,
                    department=dept,
                    date_of_joining=date(2015 + random.randint(0, 8), random.randint(1, 12), random.randint(1, 28)),
                    status='active',
                    basic_salary=designation.salary_scale,
                    bank_account_number=f'{random.randint(1000000000, 9999999999)}',
                    bank_name='KCB Bank Kenya',
                    bank_branch='Eldoret Branch',
                    permanent_address=f'{random.randint(100, 999)} {last_name} Street, Eldoret',
                    current_address=f'{random.randint(100, 999)} Moi Avenue, Eldoret',
                    national_id=f'{random.randint(10000000, 99999999)}',
                    kra_pin=f'A0{random.randint(100000000, 999999999)}',
                    marital_status=random.choice(['single', 'married', 'divorced']),
                    qualification='Bachelor of Education',
                    mother_tongue=random.choice(['Kalenjin', 'Kikuyu', 'Luhya', 'Kamba', 'Kisii']),
                    blood_group=random.choice(['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']),
                )
                created_count += 1
                staff_list.append(staff)
            else:
                staff_list.append(Staff.objects.get(staff_id=staff_id))

        self.stdout.write(f'  ✅ Created/Retrieved {created_count} staff members')
        return staff_list

    def create_allowances(self):
        """Create allowances"""
        allowances_data = [
            {'name': 'House Allowance', 'description': 'Monthly housing allowance', 'amount': Decimal('5000'), 'is_taxable': False},
            {'name': 'Transport Allowance', 'description': 'Monthly transport allowance', 'amount': Decimal('3000'), 'is_taxable': False},
            {'name': 'Meal Allowance', 'description': 'Daily meal allowance', 'amount': Decimal('2000'), 'is_taxable': False},
            {'name': 'Responsibility Allowance', 'description': 'For teachers with extra duties', 'amount': Decimal('4000'), 'is_taxable': True},
            {'name': 'Performance Bonus', 'description': 'Performance-based bonus', 'amount': Decimal('6000'), 'is_taxable': True},
        ]

        created_count = 0
        for allow_data in allowances_data:
            _, created = Allowance.objects.get_or_create(
                name=allow_data['name'],
                defaults={k: v for k, v in allow_data.items() if k != 'name'}
            )
            if created:
                created_count += 1

        self.stdout.write(f'  ✅ Created/Retrieved {created_count} allowances')

    def create_deductions(self):
        """Create deductions"""
        deductions_data = [
            {'name': 'Personal Loan Deduction', 'description': 'Staff personal loan repayment', 'percentage': Decimal('5')},
            {'name': 'Cooperative Shares', 'description': 'SACCO/Cooperative contribution', 'percentage': Decimal('2')},
            {'name': 'Welfare Fund', 'description': 'Staff welfare fund contribution', 'percentage': Decimal('1')},
            {'name': 'Income Tax Advance', 'description': 'Advance income tax withholding', 'percentage': Decimal('10')},
        ]

        created_count = 0
        for ded_data in deductions_data:
            _, created = Deduction.objects.get_or_create(
                name=ded_data['name'],
                defaults={k: v for k, v in ded_data.items() if k != 'name'}
            )
            if created:
                created_count += 1

        self.stdout.write(f'  ✅ Created/Retrieved {created_count} deductions')

    def create_salary_advances(self, staff_list):
        """Create sample salary advances"""
        created_count = 0

        # Create salary advances for random staff
        for _ in range(8):
            staff = random.choice(staff_list)

            if not SalaryAdvance.objects.filter(staff=staff, status='pending').exists():
                advance = SalaryAdvance.objects.create(
                    staff=staff,
                    amount=Decimal(random.randint(10000, 50000)),
                    reason=random.choice([
                        'Medical emergency',
                        'School fees',
                        'Home renovation',
                        'Vehicle repair',
                        'Family obligation',
                    ]),
                    status=random.choice(['pending', 'approved', 'disbursed']),
                    repayment_months=random.randint(2, 6),
                )

                if advance.status in ['approved', 'disbursed']:
                    advance.approval_date = timezone.now() - timedelta(days=random.randint(1, 30))
                    advance.approved_by = 'HR Manager'
                    advance.save()

                created_count += 1

        self.stdout.write(f'  ✅ Created {created_count} salary advances')

    def create_payroll_data(self, staff_list):
        """Create payroll periods and records"""
        # Create PayrollPeriod for last 3 months
        current_date = date.today()
        created_periods = 0
        created_payrolls = 0

        for month_offset in range(0, 3):
            target_date = current_date - timedelta(days=30*month_offset)
            month = target_date.month
            year = target_date.year

            period, created = PayrollPeriod.objects.get_or_create(
                month=month,
                year=year,
                defaults={
                    'start_date': date(year, month, 1),
                    'end_date': date(year, month, 28) if month != 2 else date(year, month, 28),
                    'status': 'draft' if month_offset == 0 else 'finalized',
                }
            )

            if created:
                created_periods += 1

            # Create payroll records for each staff
            for staff in staff_list:
                if not Payroll.objects.filter(period=period, staff=staff).exists():
                    basic_salary = staff.basic_salary
                    gross = basic_salary + Decimal(random.randint(0, 10000))
                    deductions = basic_salary * Decimal('0.2')  # 20% deductions average
                    net = gross - deductions

                    Payroll.objects.create(
                        period=period,
                        staff=staff,
                        basic_salary=basic_salary,
                        gross_earnings=gross,
                        total_deductions=deductions,
                        net_salary=net,
                        days_worked=random.randint(28, 30),
                        working_days=30,
                        status=random.choice(['draft', 'approved']) if month_offset > 0 else 'draft',
                    )
                    created_payrolls += 1

        self.stdout.write(f'  ✅ Created {created_periods} payroll periods and {created_payrolls} payroll records')

    def print_summary(self, staff_list):
        """Print summary of created data"""
        self.stdout.write(self.style.SUCCESS('\n📊 Data Summary:'))
        self.stdout.write(f'  👥 Users: {CustomUser.objects.count()}')
        self.stdout.write(f'  📂 Categories: {StaffCategory.objects.count()}')
        self.stdout.write(f'  🏢 Departments: {Department.objects.count()}')
        self.stdout.write(f'  💼 Designations: {Designation.objects.count()}')
        self.stdout.write(f'  👨‍💼 Staff Members: {Staff.objects.count()}')
        self.stdout.write(f'  💰 Allowances: {Allowance.objects.count()}')
        self.stdout.write(f'  📉 Deductions: {Deduction.objects.count()}')
        self.stdout.write(f'  💸 Salary Advances: {SalaryAdvance.objects.count()}')
        self.stdout.write(f'  📅 Payroll Periods: {PayrollPeriod.objects.count()}')
        self.stdout.write(f'  📋 Payroll Records: {Payroll.objects.count()}')

        self.stdout.write(self.style.SUCCESS('\n🔐 Login Credentials:'))
        self.stdout.write('  Admin:           admin / admin123')
        self.stdout.write('  HR Manager:      hrmanager / hr123')
        self.stdout.write('  Finance:         finance / finance123')
        self.stdout.write('  Principal:       principal / principal123')
