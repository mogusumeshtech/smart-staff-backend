"""
Django management command to initialize production database with required data
Run this after migrations on production: python manage.py initialize_production_data
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from staff_management.models import StaffCategory, Designation, Department

User = get_user_model()

class Command(BaseCommand):
    help = 'Initialize production database with required categories, designations, and users'

    def handle(self, *args, **options):
        self.stdout.write("=" * 60)
        self.stdout.write("INITIALIZING PRODUCTION DATABASE")
        self.stdout.write("=" * 60)

        # 1. Create Staff Categories
        self.stdout.write("\n📋 Creating Staff Categories...")
        categories = [
            {'name': 'TEACHING', 'description': 'Teaching Staff'},
            {'name': 'NON-TEACHING', 'description': 'Non-Teaching Staff'},
        ]
        for cat_data in categories:
            cat, created = StaffCategory.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            status = "✅ CREATED" if created else "⚠️  EXISTS"
            self.stdout.write(f"  {status}: {cat.name}")

        # 2. Create Departments
        self.stdout.write("\n📋 Creating Departments...")
        departments = [
            {'name': 'ADMINSTRATION', 'head_name': 'Admin Head'},
            {'name': 'ACADEMICS', 'head_name': 'Academic Head'},
            {'name': 'SPORTS', 'head_name': 'Sports Head'},
            {'name': 'OPERATIONS', 'head_name': 'Operations Head'},
        ]
        for dept_data in departments:
            dept, created = Department.objects.get_or_create(
                name=dept_data['name'],
                defaults={'head_name': dept_data['head_name']}
            )
            status = "✅ CREATED" if created else "⚠️  EXISTS"
            self.stdout.write(f"  {status}: {dept.name}")

        # 3. Create Designations
        self.stdout.write("\n📋 Creating Designations...")
        teaching_cat = StaffCategory.objects.get(name='TEACHING')
        non_teaching_cat = StaffCategory.objects.get(name='NON-TEACHING')
        admin_dept = Department.objects.get(name='ADMINSTRATION')

        designations = [
            {'name': 'PRINCIPAL', 'category': teaching_cat, 'salary_scale': 150000},
            {'name': 'DEPUTY PRINCIPAL', 'category': teaching_cat, 'salary_scale': 120000},
            {'name': 'TEACHER', 'category': teaching_cat, 'salary_scale': 50000},
            {'name': 'COOK', 'category': non_teaching_cat, 'salary_scale': 25000},
            {'name': 'CLEANER', 'category': non_teaching_cat, 'salary_scale': 20000},
            {'name': 'SECURITY', 'category': non_teaching_cat, 'salary_scale': 22000},
        ]
        for desig_data in designations:
            desig, created = Designation.objects.get_or_create(
                name=desig_data['name'],
                defaults={
                    'category': desig_data['category'],
                    'salary_scale': desig_data['salary_scale']
                }
            )
            status = "✅ CREATED" if created else "⚠️  EXISTS"
            self.stdout.write(f"  {status}: {desig.name} (KES {desig.salary_scale})")

        # 4. Create Admin Users
        self.stdout.write("\n👤 Creating Admin Users...")
        users = [
            {'username': 'admin', 'email': 'admin@smartstaff.local', 'role': 'admin', 'password': 'admin'},
            {'username': 'principal', 'email': 'principal@smartstaff.local', 'role': 'principal', 'password': 'principal'},
            {'username': 'finance', 'email': 'finance@smartstaff.local', 'role': 'finance', 'password': 'finance'},
            {'username': 'hrmanager', 'email': 'hr@smartstaff.local', 'role': 'hr_manager', 'password': 'hrmanager'},
        ]
        for user_data in users:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email'],
                    'role': user_data['role'],
                    'is_staff': True,
                }
            )
            if created:
                user.set_password(user_data['password'])
                user.save()
                self.stdout.write(f"  ✅ CREATED: {user_data['username']} ({user_data['role']})")
            else:
                self.stdout.write(f"  ⚠️  EXISTS: {user_data['username']} ({user_data['role']})")

        self.stdout.write("\n" + "=" * 60)
        self.stdout.write("✅ DATABASE INITIALIZATION COMPLETE")
        self.stdout.write("=" * 60)
        self.stdout.write("\n✅ Ready for production use!")
