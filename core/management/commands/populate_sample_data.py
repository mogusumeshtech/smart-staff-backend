from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal
from users.models import CustomUser
from staff_management.models import StaffCategory, Designation, Department, Staff
from payroll.models import PayrollPeriod, Payroll
from salary_advances.models import SalaryAdvance


class Command(BaseCommand):
    help = 'Populate database with sample data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting sample data population...'))

        # Create Staff Categories
        self.stdout.write('Creating staff categories...')
        teaching_cat, _ = StaffCategory.objects.get_or_create(
            name='Teaching',
            defaults={'description': 'Teaching staff members'}
        )
        non_teaching_cat, _ = StaffCategory.objects.get_or_create(
            name='Non-Teaching',
            defaults={'description': 'Non-teaching support staff'}
        )

        # Create Designations
        self.stdout.write('Creating designations...')
        designations_data = [
            ('Principal', teaching_cat, '150000'),
            ('Vice Principal', teaching_cat, '120000'),
            ('Teacher - Science', teaching_cat, '60000'),
            ('Teacher - Mathematics', teaching_cat, '60000'),
            ('Teacher - English', teaching_cat, '60000'),
            ('Teacher - Social Studies', teaching_cat, '55000'),
            ('Librarian', non_teaching_cat, '45000'),
            ('Office Staff', non_teaching_cat, '35000'),
            ('Peon', non_teaching_cat, '25000'),
            ('Gardener', non_teaching_cat, '25000'),
        ]

        designations = {}
        for name, category, salary in designations_data:
            des, _ = Designation.objects.get_or_create(
                name=name,
                defaults={'category': category, 'salary_scale': Decimal(salary)}
            )
            designations[name] = des

        # Create Departments
        self.stdout.write('Creating departments...')
        departments_data = [
            ('Science Department', 'Mr. Rajesh'),
            ('Mathematics Department', 'Dr. Priya'),
            ('English Department', 'Mrs. Anjali'),
            ('Social Studies Department', 'Mr. Vikram'),
            ('Administration', 'Mr. Suresh'),
        ]

        departments = {}
        for name, head in departments_data:
            dept, _ = Department.objects.get_or_create(
                name=name,
                defaults={'head_name': head}
            )
            departments[name] = dept

        # Create Staff Members
        self.stdout.write('Creating staff members...')
        staff_data = [
            ('ST001', 'Rajesh', 'Kumar', 'rajesh.kumar@school.edu', 'M', 'Teaching', designations['Principal'], departments['Administration'], '9876543210', '1980-01-15', Decimal('150000')),
            ('ST002', 'Priya', 'Singh', 'priya.singh@school.edu', 'F', 'Teaching', designations['Vice Principal'], departments['Administration'], '9876543211', '1982-03-20', Decimal('120000')),
            ('ST003', 'Vikram', 'Patel', 'vikram.patel@school.edu', 'M', 'Teaching', designations['Teacher - Science'], departments['Science Department'], '9876543212', '1985-05-10', Decimal('60000')),
            ('ST004', 'Anjali', 'Sharma', 'anjali.sharma@school.edu', 'F', 'Teaching', designations['Teacher - Mathematics'], departments['Mathematics Department'], '9876543213', '1987-07-25', Decimal('60000')),
            ('ST005', 'Suresh', 'Gupta', 'suresh.gupta@school.edu', 'M', 'Teaching', designations['Teacher - English'], departments['English Department'], '9876543214', '1988-08-30', Decimal('60000')),
            ('ST006', 'Meera', 'Verma', 'meera.verma@school.edu', 'F', 'Non-Teaching', designations['Librarian'], departments['Administration'], '9876543215', '1990-09-12', Decimal('45000')),
            ('ST007', 'Arun', 'Singh', 'arun.singh@school.edu', 'M', 'Non-Teaching', designations['Office Staff'], departments['Administration'], '9876543216', '1992-10-18', Decimal('35000')),
            ('ST008', 'Pooja', 'Nair', 'pooja.nair@school.edu', 'F', 'Teaching', designations['Teacher - Social Studies'], departments['Social Studies Department'], '9876543217', '1991-11-22', Decimal('55000')),
            ('ST009', 'Ramesh', 'Rao', 'ramesh.rao@school.edu', 'M', 'Non-Teaching', designations['Peon'], departments['Administration'], '9876543218', '1975-12-05', Decimal('25000')),
            ('ST010', 'Lakshmi', 'Das', 'lakshmi.das@school.edu', 'F', 'Non-Teaching', designations['Gardener'], departments['Administration'], '9876543219', '1978-04-14', Decimal('25000')),
        ]

        staff_members = {}
        for staff_id, first, last, email, gender, category_name, designation, dept, phone, dob, salary in staff_data:
            category = teaching_cat if category_name == 'Teaching' else non_teaching_cat

            staff, _ = Staff.objects.get_or_create(
                email=email,
                defaults={
                    'staff_id': staff_id,
                    'first_name': first,
                    'last_name': last,
                    'gender': gender,
                    'category': category,
                    'designation': designation,
                    'department': dept,
                    'phone_number': phone,
                    'date_of_birth': datetime.strptime(dob, '%Y-%m-%d').date(),
                    'date_of_joining': timezone.now().date() - timedelta(days=365 * 3),
                    'basic_salary': salary,
                    'status': 'active',
                    'permanent_address': f'{first} Street, City, State 123456'
                }
            )
            staff_members[f"{first} {last}"] = staff

        # Create Payroll Periods
        self.stdout.write('Creating payroll periods...')
        current_date = timezone.now()
        payroll_periods = []
        for month in range(1, 13):
            period, _ = PayrollPeriod.objects.get_or_create(
                month=month,
                year=current_date.year,
                defaults={
                    'start_date': datetime(current_date.year, month, 1).date(),
                    'end_date': datetime(current_date.year, month, 28).date(),
                    'status': 'finalized' if month < current_date.month else 'draft'
                }
            )
            payroll_periods.append(period)

        # Create Payroll Records
        self.stdout.write('Creating payroll records...')
        for period in payroll_periods[:3]:  # Only create for last 3 months
            for staff in Staff.objects.all()[:5]:  # Create for first 5 staff
                basic_salary = staff.basic_salary
                gross_earnings = basic_salary * Decimal('1.2')
                total_deductions = basic_salary * Decimal('0.15')
                net_salary = gross_earnings - total_deductions

                payroll, _ = Payroll.objects.get_or_create(
                    period=period,
                    staff=staff,
                    defaults={
                        'basic_salary': basic_salary,
                        'gross_earnings': gross_earnings,
                        'total_deductions': total_deductions,
                        'net_salary': net_salary,
                        'days_worked': 30,
                        'working_days': 30,
                        'status': 'disbursed' if period.status == 'finalized' else 'draft'
                    }
                )

        # Create Salary Advances
        self.stdout.write('Creating salary advances...')
        advance_statuses = ['pending', 'approved', 'approved', 'disbursed', 'recovered']
        for i, staff in enumerate(Staff.objects.all()[:5]):
            advance, _ = SalaryAdvance.objects.get_or_create(
                staff=staff,
                requested_date=timezone.now() - timedelta(days=30 - i * 5),
                defaults={
                    'amount': Decimal('10000') + (i * Decimal('2000')),
                    'reason': f'Personal emergency - {i+1}',
                    'status': advance_statuses[i],
                    'repayment_months': 3,
                    'approved_by': 'admin' if advance_statuses[i] in ['approved', 'disbursed', 'recovered'] else None,
                    'approval_date': timezone.now() - timedelta(days=25 - i * 5) if advance_statuses[i] in ['approved', 'disbursed', 'recovered'] else None,
                    'disbursal_date': timezone.now() - timedelta(days=20 - i * 5) if advance_statuses[i] in ['disbursed', 'recovered'] else None,
                }
            )

        self.stdout.write(self.style.SUCCESS('✓ Sample data population completed successfully!'))
        self.stdout.write(self.style.SUCCESS(f'Created:'))
        self.stdout.write(f'  - {StaffCategory.objects.count()} staff categories')
        self.stdout.write(f'  - {Designation.objects.count()} designations')
        self.stdout.write(f'  - {Department.objects.count()} departments')
        self.stdout.write(f'  - {Staff.objects.count()} staff members')
        self.stdout.write(f'  - {PayrollPeriod.objects.count()} payroll periods')
        self.stdout.write(f'  - {Payroll.objects.count()} payroll records')
        self.stdout.write(f'  - {SalaryAdvance.objects.count()} salary advances')
