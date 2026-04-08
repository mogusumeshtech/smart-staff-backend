from django.contrib import admin
from staff_management.models import Staff, StaffCategory, Designation, Department, Allowance, Deduction

@admin.register(StaffCategory)
class StaffCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name',)

@admin.register(Designation)
class DesignationAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'salary_scale', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('name',)

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'head_name', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'head_name')

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('staff_id', 'get_full_name', 'email', 'designation', 'department', 'status')
    list_filter = ('category', 'designation', 'department', 'status', 'gender', 'created_at')
    search_fields = ('staff_id', 'first_name', 'last_name', 'email')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {'fields': ('staff_id', 'first_name', 'middle_name', 'last_name', 'email', 'phone_number')}),
        ('Personal Details', {'fields': ('date_of_birth', 'gender', 'nationality', 'marital_status', 'mother_tongue', 'blood_group')}),
        ('Identification (Kenya)', {'fields': ('national_id', 'kra_pin', 'passport_number', 'passport_expiry_date'), 'description': 'Kenya-specific identification documents'}),
        ('Employment', {'fields': ('category', 'designation', 'department', 'status', 'date_of_joining', 'basic_salary')}),
        ('Address', {'fields': ('permanent_address', 'current_address')}),
        ('Bank Details (Kenya)', {'fields': ('bank_account_number', 'bank_name', 'bank_branch'), 'description': 'Kenya bank details'}),
        ('Emergency Contact', {'fields': ('emergency_contact_name', 'emergency_contact_phone', 'emergency_contact_relationship')}),
        ('Media', {'fields': ('profile_picture', 'passport_photo')}),
        ('Metadata', {'fields': ('created_at', 'updated_at', 'is_active')}),
    )

    def get_full_name(self, obj):
        return obj.get_full_name()
    get_full_name.short_description = 'Full Name'

@admin.register(Allowance)
class AllowanceAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount', 'is_taxable', 'is_active')
    list_filter = ('is_taxable', 'is_active')
    search_fields = ('name',)

@admin.register(Deduction)
class DeductionAdmin(admin.ModelAdmin):
    list_display = ('name', 'percentage', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)
