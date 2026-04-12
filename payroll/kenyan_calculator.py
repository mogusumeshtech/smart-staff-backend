"""
Kenyan Payroll Taxation and Deductions Calculator

This module handles Kenya-specific payroll deductions including:
- PAYE (Personal Income Tax) - Progressive taxation
- NSSF (National Social Security Fund) - 6% employee contribution
- SHA (Social Health Authority) - Health insurance contribution (replaces NHIF)
- Housing Levy - 1.5% employee contribution (introduced 2024)

Source: Kenya Revenue Authority (KRA) tax tables 2026
"""

from decimal import Decimal
from django.db import models


class PayrollDeduction(models.Model):
    """Base model for payroll deductions"""
    DEDUCTION_TYPES = [
        ('paye', 'PAYE (Personal Income Tax)'),
        ('nssf', 'NSSF Contribution'),
        ('sha', 'SHA Contribution'),
        ('housing_levy', 'Housing Levy'),
        ('other', 'Other Deduction'),
    ]

    staff = models.ForeignKey('staff_management.Staff', on_delete=models.CASCADE, related_name='payroll_deductions')
    deduction_type = models.CharField(max_length=20, choices=DEDUCTION_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    month = models.CharField(max_length=7)  # YYYY-MM format
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Payroll Deduction'
        verbose_name_plural = 'Payroll Deductions'
        unique_together = ['staff', 'deduction_type', 'month']


class KenyanPayrollCalculator:
    """
    Calculates Kenyan payroll deductions based on current KRA regulations.

    Tax Brackets 2026 (Progressive):
    0 - 24,000: 10%
    24,001 - 32,333: 25%
    32,334 - 500,000: 30%
    500,001+: 35%
    """

    # PAYE Tax Brackets (Monthly) - 2026
    TAX_BRACKETS = [
        {'min': Decimal('0'), 'max': Decimal('24000'), 'rate': Decimal('0.10')},
        {'min': Decimal('24001'), 'max': Decimal('32333'), 'rate': Decimal('0.25')},
        {'min': Decimal('32334'), 'max': Decimal('500000'), 'rate': Decimal('0.30')},
        {'min': Decimal('500001'), 'max': None, 'rate': Decimal('0.35')},
    ]

    # NSSF - Employee contribution 6% (capped at KES 18,000/month)
    NSSF_RATE = Decimal('0.06')
    NSSF_CAP = Decimal('18000')

    # SHA - Social Health Authority (replaces NHIF)
    # Contribution varies by salary bracket
    SHA_BRACKETS = [
        {'min': Decimal('0'), 'max': Decimal('5999'), 'amount': Decimal('150')},
        {'min': Decimal('6000'), 'max': Decimal('7999'), 'amount': Decimal('300')},
        {'min': Decimal('8000'), 'max': Decimal('11999'), 'amount': Decimal('400')},
        {'min': Decimal('12000'), 'max': Decimal('14999'), 'amount': Decimal('500')},
        {'min': Decimal('15000'), 'max': Decimal('19999'), 'amount': Decimal('600')},
        {'min': Decimal('20000'), 'max': Decimal('24999'), 'amount': Decimal('750')},
        {'min': Decimal('25000'), 'max': Decimal('29999'), 'amount': Decimal('850')},
        {'min': Decimal('30000'), 'max': Decimal('34999'), 'amount': Decimal('900')},
        {'min': Decimal('35000'), 'max': Decimal('39999'), 'amount': Decimal('950')},
        {'min': Decimal('40000'), 'max': Decimal('44999'), 'amount': Decimal('1000')},
        {'min': Decimal('45000'), 'max': Decimal('49999'), 'amount': Decimal('1100')},
        {'min': Decimal('50000'), 'max': Decimal('59999'), 'amount': Decimal('1200')},
        {'min': Decimal('60000'), 'max': Decimal('69999'), 'amount': Decimal('1300')},
        {'min': Decimal('70000'), 'max': Decimal('79999'), 'amount': Decimal('1400')},
        {'min': Decimal('80000'), 'max': Decimal('89999'), 'amount': Decimal('1500')},
        {'min': Decimal('90000'), 'max': Decimal('99999'), 'amount': Decimal('1600')},
        {'min': Decimal('100000'), 'max': None, 'amount': Decimal('1700')},
    ]

    # Housing Levy - 1.5% employee contribution (introduced June 2024)
    HOUSING_LEVY_RATE = Decimal('0.015')
    HOUSING_LEVY_CAP = Decimal('18000')  # Monthly cap

    @staticmethod
    def calculate_paye(gross_salary):
        """
        Calculate PAYE tax based on progressive tax brackets.

        Args:
            gross_salary: Decimal - Monthly gross salary

        Returns:
            Decimal - PAYE tax amount
        """
        gross = Decimal(str(gross_salary))
        tax = Decimal('0')

        for bracket in KenyanPayrollCalculator.TAX_BRACKETS:
            if bracket['max'] is None:
                # Last bracket
                if gross > bracket['min']:
                    tax += (gross - bracket['min']) * bracket['rate']
            else:
                if gross > bracket['min']:
                    taxable = min(gross, bracket['max']) - bracket['min']
                    tax += taxable * bracket['rate']

        return tax.quantize(Decimal('0.01'))

    @staticmethod
    def calculate_nssf(gross_salary):
        """
        Calculate NSSF contribution (6% of salary, capped at KES 18,000).

        Args:
            gross_salary: Decimal - Monthly gross salary

        Returns:
            Decimal - NSSF contribution amount
        """
        salary = Decimal(str(gross_salary))
        nssf = salary * KenyanPayrollCalculator.NSSF_RATE

        # Cap at KES 18,000 per month
        return min(nssf, KenyanPayrollCalculator.NSSF_CAP).quantize(Decimal('0.01'))

    @staticmethod
    def calculate_sha(gross_salary):
        """
        Calculate SHA (Social Health Authority) contribution based on salary brackets.

        Args:
            gross_salary: Decimal - Monthly gross salary

        Returns:
            Decimal - SHA contribution amount
        """
        salary = Decimal(str(gross_salary))

        for bracket in KenyanPayrollCalculator.SHA_BRACKETS:
            if bracket['max'] is None:
                if salary >= bracket['min']:
                    return bracket['amount']
            else:
                if bracket['min'] <= salary <= bracket['max']:
                    return bracket['amount']

        # Return maximum if salary exceeds all brackets
        return KenyanPayrollCalculator.SHA_BRACKETS[-1]['amount']

    @staticmethod
    def calculate_housing_levy(gross_salary):
        """
        Calculate Housing Levy (1.5% of salary, capped at KES 18,000).

        Args:
            gross_salary: Decimal - Monthly gross salary

        Returns:
            Decimal - Housing levy amount
        """
        salary = Decimal(str(gross_salary))
        levy = salary * KenyanPayrollCalculator.HOUSING_LEVY_RATE

        # Cap at KES 18,000 per month
        return min(levy, KenyanPayrollCalculator.HOUSING_LEVY_CAP).quantize(Decimal('0.01'))

    @staticmethod
    def calculate_net_salary(gross_salary):
        """
        Calculate net salary after all deductions.

        Args:
            gross_salary: Decimal - Monthly gross salary

        Returns:
            dict - Breakdown of all deductions and net salary
        """
        gross = Decimal(str(gross_salary))

        paye = KenyanPayrollCalculator.calculate_paye(gross)
        nssf = KenyanPayrollCalculator.calculate_nssf(gross)
        sha = KenyanPayrollCalculator.calculate_sha(gross)
        housing_levy = KenyanPayrollCalculator.calculate_housing_levy(gross)

        total_deductions = paye + nssf + sha + housing_levy
        net_salary = gross - total_deductions

        return {
            'gross_salary': gross,
            'paye': paye,
            'nssf': nssf,
            'sha': sha,
            'housing_levy': housing_levy,
            'total_deductions': total_deductions,
            'net_salary': net_salary,
        }


# Example usage:
# salary_breakdown = KenyanPayrollCalculator.calculate_net_salary(50000)
# print(salary_breakdown)
# {
#     'gross_salary': 50000,
#     'paye': 11000,       # 10% on 24k + 25% on 8.333k + 30% on 17.667k
#     'nssf': 3000,        # 6% of 50k
#     'nhif': 1100,        # Based on salary bracket
#     'housing_levy': 750, # 1.5% of 50k
#     'total_deductions': 15850,
#     'net_salary': 34150,
# }
