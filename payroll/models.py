from django.db import models
from django.utils import timezone
from decimal import Decimal
from core.models import BaseModel
from staff_management.models import Staff

class PayrollPeriod(BaseModel):
    month = models.IntegerField(choices=[(i, f'Month {i}') for i in range(1, 13)])
    year = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=[('draft', 'Draft'), ('finalized', 'Finalized'), ('locked', 'Locked')],
        default='draft'
    )
    processed_on = models.DateTimeField(blank=True, null=True)
    processed_by = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = 'Payroll Period'
        verbose_name_plural = 'Payroll Periods'
        unique_together = ['month', 'year']
        ordering = ['-year', '-month']

    def __str__(self):
        return f"{self.month}/{self.year}"


class Payroll(BaseModel):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('processed', 'Processed'),
        ('approved', 'Approved'),
        ('disbursed', 'Disbursed'),
    )

    period = models.ForeignKey(PayrollPeriod, on_delete=models.PROTECT, related_name='payrolls')
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='payrolls')

    basic_salary = models.DecimalField(max_digits=12, decimal_places=2)
    gross_earnings = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_deductions = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    net_salary = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    days_worked = models.IntegerField(default=30)
    working_days = models.IntegerField(default=30)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    approved_by = models.CharField(max_length=100, blank=True, null=True)
    approval_date = models.DateTimeField(blank=True, null=True)
    disbursed_on = models.DateTimeField(blank=True, null=True)

    remarks = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Payroll'
        verbose_name_plural = 'Payrolls'
        unique_together = ['period', 'staff']
        ordering = ['-period', 'staff']
        indexes = [
            models.Index(fields=['period', 'status']),
            models.Index(fields=['staff', 'period']),
        ]

    def __str__(self):
        return f"{self.staff.get_full_name()} - {self.period}"

    def calculate_earnings_deductions(self):
        """Calculate gross_earnings and total_deductions from related records."""
        # Calculate gross earnings from PayrollEarning records if they exist
        earnings_sum = Decimal('0')
        if self.pk:  # Only if already saved
            earnings_sum = sum(
                Decimal(e.amount) for e in self.earnings.all()
            ) if self.earnings.exists() else Decimal('0')

        # Use basic_salary as gross earnings base
        self.gross_earnings = self.basic_salary + earnings_sum

        # Calculate total deductions from PayrollDeduction records if they exist
        deductions_sum = Decimal('0')
        if self.pk:  # Only if already saved
            deductions_sum = sum(
                Decimal(d.amount) for d in self.deductions.all()
            ) if self.deductions.exists() else Decimal('0')

        # If no explicit deductions were found, calculate default deductions
        if deductions_sum == 0:
            paye = self.basic_salary * Decimal('0.10')  # 10% PAYE
            nssf = self.basic_salary * Decimal('0.06')  # 6% NSSF
            health = self.basic_salary * Decimal('0.02')  # 2% Health
            housing = self.basic_salary * Decimal('0.015')  # 1.5% Housing levy

            deductions_sum = paye + nssf + health + housing

        self.total_deductions = deductions_sum

        # Calculate net salary
        self.net_salary = self.gross_earnings - self.total_deductions

    def save(self, *args, **kwargs):
        """Automatically calculate salary components before saving."""
        is_new = not self.pk
        
        # Calculate initial values
        self.calculate_earnings_deductions()
        
        # Save first to get an ID
        super().save(*args, **kwargs)

        # After saving, ensure deductions are created for new payrolls
        if is_new and not self.deductions.exists():
            paye = self.basic_salary * Decimal('0.10')
            nssf = self.basic_salary * Decimal('0.06')
            health = self.basic_salary * Decimal('0.02')
            housing = self.basic_salary * Decimal('0.015')

            try:
                self.deductions.create(description='PAYE', amount=paye)
                self.deductions.create(description='NSSF', amount=nssf)
                self.deductions.create(description='SHA (Health)', amount=health)
                self.deductions.create(description='Housing Levy', amount=housing)

                # Recalculate with deductions now in place
                self.calculate_earnings_deductions()
                super().save(*args, **kwargs)
            except Exception as e:
                print(f"Error creating deductions: {e}")
                # Continue even if deductions fail - the payroll record exists


class PayrollEarning(BaseModel):
    payroll = models.ForeignKey(Payroll, on_delete=models.CASCADE, related_name='earnings')
    description = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    is_taxable = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Payroll Earning'
        verbose_name_plural = 'Payroll Earnings'

    def __str__(self):
        return f"{self.payroll} - {self.description}"


class PayrollDeduction(BaseModel):
    payroll = models.ForeignKey(Payroll, on_delete=models.CASCADE, related_name='deductions')
    description = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        verbose_name = 'Payroll Deduction'
        verbose_name_plural = 'Payroll Deductions'

    def __str__(self):
        return f"{self.payroll} - {self.description}"
