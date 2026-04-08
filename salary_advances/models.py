from django.db import models
from django.utils import timezone
from core.models import BaseModel
from staff_management.models import Staff

class SalaryAdvance(BaseModel):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('disbursed', 'Disbursed'),
        ('recovered', 'Recovered'),
    )
    
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='salary_advances')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    reason = models.TextField()
    requested_date = models.DateTimeField(auto_now_add=True)
    approval_date = models.DateTimeField(blank=True, null=True)
    disbursal_date = models.DateTimeField(blank=True, null=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    approved_by = models.CharField(max_length=100, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    
    repayment_months = models.IntegerField(default=3)
    amount_recovered = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    class Meta:
        verbose_name = 'Salary Advance'
        verbose_name_plural = 'Salary Advances'
        ordering = ['-requested_date']
        indexes = [
            models.Index(fields=['staff', 'status']),
            models.Index(fields=['requested_date']),
        ]
    
    def __str__(self):
        return f"{self.staff.get_full_name()} - {self.amount} ({self.status})"


class SalaryAdvanceRecovery(BaseModel):
    salary_advance = models.ForeignKey(SalaryAdvance, on_delete=models.CASCADE, related_name='recoveries')
    payroll_month = models.DateField()
    amount_recovered = models.DecimalField(max_digits=12, decimal_places=2)
    remarks = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = 'Salary Advance Recovery'
        verbose_name_plural = 'Salary Advance Recoveries'
        ordering = ['payroll_month']
        unique_together = ['salary_advance', 'payroll_month']
    
    def __str__(self):
        return f"{self.salary_advance.staff.get_full_name()} - {self.amount_recovered}"
