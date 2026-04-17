# SMART STAFF - COMPLETE SYSTEM ARCHITECTURE
## April 13, 2026 - Comprehensive Rebuild

This document maps EVERY file needed for the complete production system based on user's original design.

---

## DASHBOARD (Welcome + Statistics)

### What User Wants:
- Welcome message with current date/time
- 4 statistics cards: Total Staff, Active Staff, Pending Advances, This Month Payroll
- Financial overview (monthly amount)
- Analysis/graphs (if applicable)

### Files Needed:
- `DashboardHome.jsx` - Main dashboard with welcome + stats
- `StaffStatsCard.jsx` - Reusable statistics card component
- `FinancialOverview.jsx` - Monthly financial summary component

---

## PAYROLL MANAGEMENT

### What User Wants:
- Generate payroll for specific month
- Auto-calculate: PAYE, NSSF, SHA (formerly NHIF), Housing Levy
- Show totals, deductions for each member
- Support for basic salary + allowances
- Mark as disbursed when receipt printed

### Files Needed:
- `PayrollManagement.jsx` - List of payroll periods
- `PayrollGeneration.jsx` - Generate payroll for month (3-step workflow)
- `PayrollDetails.jsx` - View/edit specific payroll
- `PayrollApproval.jsx` - Approve payroll before disbursement
- Backend ViewSet: Already exists (✓ Render deployed)

---

## STAFF MANAGEMENT

### What User Wants:
- List all staff with filters (department, status, etc.)
- Each staff has: staff_id, name, email, phone, department, designation, status
- Actions on each row:
  - Eye icon → View full profile
  - Edit → Edit staff details
  - Delete → Remove staff
  - Print Badge → Staff identification badge
  - Print Form → Registration form with photo
  - Print Card → Staff card (like ID card)
- Can add new staff
- Can edit existing staff

### Files Needed:
- `StaffManagement.jsx` - Staff list page with actions
- `StaffForm.jsx` - Add/edit staff form
- `StaffSearch.jsx` - Search component (optional but user mentioned)
- `PrintStaffBadge.jsx` - Print badge component
- `PrintStaffForm.jsx` - Print registration form with photo
- `PrintStaffCard.jsx` - Print staff ID card
- Backend ViewSet: Already exists (✓ Render deployed)

---

## STAFF PROFILE

### What User Wants:
When clicking eye icon on staff → shows full profile with:
- Personal details (name, ID, email, phone, address, KRA PIN, National ID)
- Professional info (department, designation, salary, employment status, hire date)
- Passport photo / profile picture
- Documents section
- Salary history (list of all salary slips received)
- Leave history (if applicable)
- Print salary receipt button

### Files Needed:
- `StaffProfile.jsx` - Full staff profile page
- `StaffPersonalDetails.jsx` - Personal information tab
- `StaffProfessionalInfo.jsx` - Professional information tab
- `StaffDocuments.jsx` - Documents/attachments tab
- `StaffSalaryHistory.jsx` - Historical salary records tab
- Backend ViewSet: Already exists (✓ Render deployed)

---

## SALARY SLIPS / RECEIPTS

### What User Wants:
- Generate receipt showing:
  - Logo, school name, address
  - Staff name, ID, designation
  - Period (month/year)
  - Basic salary, allowances
  - Deductions (PAYE, NSSF, SHA, etc.)
  - Net salary
  - Disbursement status
- Can print from:
  - Staff profile → Print receipt
  - Payroll view → Print receipt for each staff
- Reprint ability with disbursement indicator

### Files Needed:
- `SalaryReceiptTemplate.jsx` - Receipt template
- `PrintSalaryReceipt.jsx` - Receipt print page
- Backend ViewSet: Already exists (✓ Render deployed)

---

## SALARY ADVANCES

### What User Wants:
- Staff can request advance (deducted from end-of-month)
- Fields: amount, reason, staff name, number of months to recover
- Dashboard showing: total pending requests, total advanced amount
- Admin workflow: View requests → Approve → Disburse → Track recovery
- Deductions spread over specified months

### Files Needed:
- `SalaryAdvances.jsx` - Staff advance requests list
- `SalaryAdvanceRequest.jsx` - Request new advance form (staff side)
- `SalaryAdvanceApproval.jsx` - Approval workflow (admin side)
- `SalaryAdvanceDisbursement.jsx` - Disburse approved advances
- `SalaryAdvanceRecovery.jsx` - Track and manage recovery
- Backend ViewSet: Already exists (✓ Render deployed)

---

## DEDUCTION CONFIGURATION

### What User Wants:
- Configure which deductions apply to which staff
- Options: By designation, by category (teaching/non-teaching), by custom staff list
- Each deduction can be:
  - Fixed amount (e.g., 500 KES)
  - Percentage (e.g., 1%, 1.5%)
- Types: PAYE, NSSF, SHA (not NHIF), Housing Levy, Insurance, etc.
- Can add custom deductions

### Files Needed:
- `DeductionConfiguration.jsx` - Configure deductions
- `DeductionConfigForm.jsx` - Add/edit deduction
- `DeductionAssignment.jsx` - Assign deductions to staff groups
- Backend ViewSet: Already exists (✓ Render deployed)

---

## DEDUCTIONS MANAGEMENT

### What User Wants:
- View deductions for each staff member
- Customize deductions per staff (override config)
- Add/remove deductions per person
- See impact on salary

### Files Needed:
- `DeductionsManagement.jsx` - Deductions per staff
- `DeductionEditor.jsx` - Edit staff-specific deductions
- Backend ViewSet: Already exists (✓ Render deployed)

---

## REPORTS & ANALYTICS

### What User Wants:
- Customizable reports
- Select fields to include
- Export options: PDF, CSV, Word, HTML
- Pre-built reports:
  - Staff list (active, terminated, on leave)
  - Payroll summary
  - Salary advance report
  - Deduction summary
- Can include/exclude columns
- Show totals at bottom

### Files Needed:
- `ReportsPage.jsx` - Reports landing page
- `StaffListReport.jsx` - Staff report builder
- `PayrollSummaryReport.jsx` - Payroll analytics
- `SalaryAdvanceReport.jsx` - Advance requests report
- `DeductionSummaryReport.jsx` - Deduction analytics
- `ReportExporter.jsx` - PDF/CSV/Word export utility
- Backend ViewSet: Already exists (✓ Render deployed)

---

## ADMINISTRATION / SETTINGS

### What User Wants:
- School information (name, logo, address, phone)
- Logo upload and display across system
- Deduction types management
- Departments management
- Designations management
- Categories (teaching/non-teaching) management
- User roles and permissions

### Files Needed:
- `AdminDashboard.jsx` - Administration homepage
- `SettingsPage.jsx` - School settings + logo upload
- `DepartmentManagement.jsx` - CRUD departments
- `DesignationManagement.jsx` - CRUD designations
- `CategoryManagement.jsx` - CRUD categories
- `DeductionTypesManagement.jsx` - CRUD deduction types
- `UserManagement.jsx` - User account management
- `UserRoles.jsx` - Role-based access control
- Backend ViewSet: Already exists (✓ Render deployed)

---

## SIDEBAR NAVIGATION

### Menu Items (Left Sidebar):
1. Dashboard (home icon)
2. Staff Management
   - Staff List
   - Add New Staff
3. Payroll
   - Payroll Periods
   - Generate Payroll
   - Payroll Details
4. Salary Advances
   - View Requests
   - Approve / Disburse
5. Deduction Configuration
6. Deductions Management
7. Reports & Exports
   - Staff Lists
   - Payroll Summary
   - Salary Advances
   - Deductions
8. Administration
   - Settings (School Info, Logo)
   - Departments
   - Designations
   - Categories
   - Deduction Types
9. User Management
   - Users
   - Roles
10. Logout

### Files Needed:
- `Layout.jsx` - Main layout with sidebar
- `Sidebar.jsx` - Navigation sidebar component
- `routes.jsx` - Route definitions

---

## LAYOUT & COMPONENTS

### Shared Components:
- `TopBar.jsx` - Top navigation with user, logout
- `StatsCard.jsx` - Reusable statistics card
- `Table.jsx` - Data table with pagination, sorting, filtering
- `Form.jsx` - Form components (input, select, etc.)
- `Modal.jsx` - Confirmation/action dialogs
- `Button.jsx` - Button styles
- `Loading.jsx` - Loading spinner
- `EmptyState.jsx` - Empty data message
- `ErrorBoundary.jsx` - Error handling
- `ToastNotification.jsx` - Success/error messages

### Files Needed:
- `components/Common/StatsCard.jsx`
- `components/Common/DataTable.jsx`
- `components/Common/Form.jsx`
- `components/Common/Modal.jsx`
- `components/Common/Button.jsx`
- `components/Common/Loading.jsx`
- `components/Common/EmptyState.jsx`
- `components/Common/ErrorBoundary.jsx`
- `components/Common/Toast.jsx`
- `components/Layout/TopBar.jsx`
- `components/Layout/Sidebar.jsx`
- `components/Layout/MainLayout.jsx`
- `components/Print/*` - All print components

---

## UTILITIES & SERVICES

### API Services:
- `services/api.js` - Axios instance with interceptors
- `services/staffService.js` - Staff API calls
- `services/payrollService.js` - Payroll API calls
- `services/advanceService.js` - Salary advance API calls
- `services/deductionService.js` - Deduction API calls
- `services/reportService.js` - Report generation API calls
- `services/settingsService.js` - Settings API calls

### Utilities:
- `utils/dateHelper.js` - Date formatting, calculations
- `utils/currencyFormatter.js` - KES currency formatting
- `utils/calculations.js` - Payroll/tax calculations
- `utils/validation.js` - Form validation
- `utils/exporters.js` - PDF, CSV, Word export
- `utils/constants.js` - App constants (deduction types, statuses, etc.)

### Files Needed:
- All services and utilities listed above

---

## CONFIGURATION

### Files Needed:
- `.env` - Environment variables
- `vite.config.js` - Vite build config
- `tailwind.config.js` - Tailwind CSS config (if using)
- `package.json` - Dependencies
- `.gitignore` - Git ignore rules

---

## STYLING

### Options:
- Ant Design (currently using - good)
- Tailwind CSS (optional - for custom styling)
- CSS Modules or Styled Components

### Theme Files:
- `styles/theme.css` - Main theme colors
- `styles/variables.css` - CSS variables
- `styles/globals.css` - Global styles

---

## STATE MANAGEMENT (if needed)

If using Zustand or Context API:
- `stores/authStore.js` - Auth state
- `stores/staffStore.js` - Staff data
- `stores/payrollStore.js` - Payroll state
- `stores/settingsStore.js` - App settings

---

## SUMMARY OF FILES NEEDED

### Backend (Django) - ALREADY COMPLETED ✓
- All models, serializers, viewsets, URLs
- PostgreSQL database
- Deployed on Render

### Frontend (React) - NEEDS COMPLETION

**Pages (17 total):**
1. Login.jsx
2. DashboardHome.jsx
3. StaffManagement.jsx
4. StaffForm.jsx (add/edit)
5. StaffProfile.jsx
6. PayrollManagement.jsx
7. PayrollGeneration.jsx
8. PayrollDetails.jsx
9. PayrollApproval.jsx
10. SalaryAdvances.jsx
11. SalaryAdvanceRequest.jsx
12. SalaryAdvanceApproval.jsx
13. DeductionConfiguration.jsx
14. DeductionsManagement.jsx
15. ReportsPage.jsx
16. SettingsPage.jsx
17. AdminDashboard.jsx

**Components (40+ total):**
- Print components (Badge, Form, Card, Receipt)
- Layout components (Sidebar, TopBar)
- Common components (Table, Form, Modal, etc.)

**Services (7 total):**
- API service
- Staff service
- Payroll service
- Advance service
- Deduction service
- Report service
- Settings service

**Utilities (7+ utilities):**
- Date helper, currency formatter, calculations
- Validation, exporters, constants

**Configuration:**
- vite.config.js
- package.json
- .env
- styles/

---

## CURRENT STATUS

✅ Backend: COMPLETE (Render deployed)
✅ Database: EXISTS (with your staff data)
❌ Frontend: INCOMPLETE (generic template, needs real components)

## NEXT STEPS

Build ALL 17 page components using real backend data.
Build 40+ reusable components.
Connect all to working APIs.
Test with your actual staff data.
Deploy to Firebase.

---
