from django.db import models
from django.utils import timezone
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
