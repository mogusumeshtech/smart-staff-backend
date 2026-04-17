from django.db import models
from core.models import BaseModel

class StaffCategory(BaseModel):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Staff Category'
        verbose_name_plural = 'Staff Categories'

    def __str__(self):
        return self.name


class Designation(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey(StaffCategory, on_delete=models.PROTECT, related_name='designations')
    salary_scale = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Designation'
        verbose_name_plural = 'Designations'

    def __str__(self):
        return self.name


class Department(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    head_name = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'

    def __str__(self):
        return self.name


class Staff(BaseModel):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )

    STATUS_CHOICES = (
        ('active', 'Active'),
        ('on_leave', 'On Leave'),
        ('suspended', 'Suspended'),
        ('terminated', 'Terminated'),
    )

    staff_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    category = models.ForeignKey(StaffCategory, on_delete=models.PROTECT, related_name='staff_members')
    designation = models.ForeignKey(Designation, on_delete=models.PROTECT, related_name='staff_members')
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name='staff_members')

    date_of_joining = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

    basic_salary = models.DecimalField(max_digits=12, decimal_places=2)
    bank_account_number = models.CharField(max_length=50, blank=True, null=True)
    bank_name = models.CharField(max_length=100, blank=True, null=True)
    bank_branch = models.CharField(max_length=100, blank=True, null=True)  # Kenya uses branch codes

    permanent_address = models.TextField()
    current_address = models.TextField(blank=True, null=True)

    emergency_contact_name = models.CharField(max_length=100, blank=True, null=True)
    emergency_contact_phone = models.CharField(max_length=15, blank=True, null=True)
    emergency_contact_relationship = models.CharField(max_length=50, blank=True, null=True)

    profile_picture = models.ImageField(upload_to='staff_profiles/', blank=True, null=True)
    passport_photo = models.ImageField(upload_to='staff_passport_photos/', blank=True, null=True)
    national_id = models.CharField(max_length=20, blank=True, null=True)  # Kenya national ID (8 digits)
    kra_pin = models.CharField(max_length=15, blank=True, null=True)  # Kenya Revenue Authority PIN
    passport_number = models.CharField(max_length=20, blank=True, null=True)
    passport_expiry_date = models.DateField(blank=True, null=True)

    marital_status = models.CharField(max_length=20, blank=True, null=True, choices=[
        ('single', 'Single'),
        ('married', 'Married'),
        ('divorced', 'Divorced'),
        ('widowed', 'Widowed'),
    ])
    nationality = models.CharField(max_length=50, default='Kenyan', blank=True)
    qualification = models.CharField(max_length=100, blank=True, null=True)
    mother_tongue = models.CharField(max_length=50, blank=True, null=True)
    blood_group = models.CharField(max_length=5, blank=True, null=True, choices=[
        ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-'),
    ])

    class Meta:
        verbose_name = 'Staff'
        verbose_name_plural = 'Staff'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['staff_id']),
            models.Index(fields=['email']),
            models.Index(fields=['category']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.staff_id})"

    def get_full_name(self):
        if self.middle_name:
            return f"{self.first_name} {self.middle_name} {self.last_name}"
        return f"{self.first_name} {self.last_name}"


class Allowance(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_taxable = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Allowance'
        verbose_name_plural = 'Allowances'

    def __str__(self):
        return self.name


class Deduction(BaseModel):
    """System-wide deduction types (fixed deductions applied to all staff)"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # For percentage-based deductions
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)  # For fixed amount deductions

    class Meta:
        verbose_name = 'Deduction'
        verbose_name_plural = 'Deductions'

    def __str__(self):
        return self.name


class StaffDeductionConfig(BaseModel):
    """Per-staff deduction configuration"""
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='deduction_configs')

    # Statutory deductions
    apply_paye = models.BooleanField(default=True)
    apply_nssf = models.BooleanField(default=True)
    apply_sha = models.BooleanField(default=True)  # Social Health Authority (replaces NHIF in Kenya)
    sha_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    apply_housing_levy = models.BooleanField(default=True)

    # Optional
    full_salary = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)

    # Link to custom deductions
    custom_deductions = models.ManyToManyField(Deduction, blank=True, related_name='staff_configs')

    class Meta:
        verbose_name = 'Staff Deduction Config'
        verbose_name_plural = 'Staff Deduction Configs'
        unique_together = ('staff',)

    def __str__(self):
        return f'Deduction Config for {self.staff.get_full_name()}'


class CategoryDeductionConfig(BaseModel):
    """Deduction configuration for all staff in a category"""
    category = models.OneToOneField(StaffCategory, on_delete=models.CASCADE, related_name='deduction_config')

    # Statutory deductions
    apply_paye = models.BooleanField(default=True)
    apply_nssf = models.BooleanField(default=True)
    apply_sha = models.BooleanField(default=True)
    sha_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    apply_housing_levy = models.BooleanField(default=True)

    notes = models.TextField(blank=True, null=True)

    # Link to custom deductions
    custom_deductions = models.ManyToManyField(Deduction, blank=True, related_name='category_configs')

    class Meta:
        verbose_name = 'Category Deduction Config'
        verbose_name_plural = 'Category Deduction Configs'

    def __str__(self):
        return f'Deduction Config for {self.category.name}'


class DesignationDeductionConfig(BaseModel):
    """Deduction configuration for all staff with a designation"""
    designation = models.OneToOneField(Designation, on_delete=models.CASCADE, related_name='deduction_config')

    # Statutory deductions
    apply_paye = models.BooleanField(default=True)
    apply_nssf = models.BooleanField(default=True)
    apply_sha = models.BooleanField(default=True)
    sha_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    apply_housing_levy = models.BooleanField(default=True)

    notes = models.TextField(blank=True, null=True)

    # Link to custom deductions
    custom_deductions = models.ManyToManyField(Deduction, blank=True, related_name='designation_configs')

    class Meta:
        verbose_name = 'Designation Deduction Config'
        verbose_name_plural = 'Designation Deduction Configs'

    def __str__(self):
        return f'Deduction Config for {self.designation.name}'
