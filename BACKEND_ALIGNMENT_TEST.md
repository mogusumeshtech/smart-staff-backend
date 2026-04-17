# 🧪 BACKEND ALIGNMENT TEST CHECKLIST
## April 13, 2026 - Verify All Fixes

---

## ✅ BEFORE YOU START

- [ ] System deployed at: https://smart-staff-8b633.web.app
- [ ] Logged in with: admin / admin123
- [ ] Backend running on: https://smart-staff-api.onrender.com
- [ ] Open browser DevTools (F12) to check for errors

---

## 🏃 TEST 1: Add New Staff (With All Fields)

**Steps:**
1. Go to **Staff Management** menu
2. Click **Add Staff** button
3. Fill out all required fields:
   - Staff ID: `ST002`
   - Gender: **Select "Male"** ← ✅ NEW FIELD
   - Status: **Select "Active"**
   - First Name: `John`
   - Last Name: `Doe`
   - Date of Birth: `1990-01-15`
   - Email: `john@school.edu`
   - Phone: `0712345678`

4. **Click Employment Tab:**
   - Category: **Select from dropdown** (uses ID now) ← ✅ FIXED
   - Designation: **Select from dropdown** (uses ID now) ← ✅ FIXED
   - Department: **Select from dropdown** (uses ID now) ← ✅ FIXED
   - Date of Joining: `2024-01-15` ← ✅ FIXED (not date_of_hire)
   - **Basic Salary: `50000`** ← ✅ NEW REQUIRED FIELD
   - Qualification: `Bachelor of Education`

5. **Click Identification Tab:**
   - National ID: `12345678`
   - KRA PIN: `A001234567ABC`
   - Blood Group: `O+`
   - Marital Status: `Single`

6. **Click Contact & Address Tab:**
   - **Permanent Address: `123 School Road`** ← ✅ FIXED (not address)
   - Bank Account: `0123456789`
   - Bank Name: `Kenya Commercial Bank`

7. **Click Basic Tab again:**
   - Upload Profile Picture (click upload button)
   - Upload Passport Photo (click upload button)

8. **Click Create Staff**

**Expected Results:**
- ✅ Form accepts multipart FormData with images
- ✅ No "missing field" errors
- ✅ Success message "Staff created successfully"
- ✅ New staff appears in list with all fields visible
- ✅ Photos display in profile

---

## 🔧 TEST 2: Edit Staff & Verify Fields

**Steps:**
1. Go to **Staff Management**
2. Click **Edit** (pencil icon) on any staff
3. Verify form pre-fills with:
   - ✅ `gender` field shows correct value
   - ✅ `status` field shows current status (not employment_status)
   - ✅ `basic_salary` shows salary amount
   - ✅ `date_of_joining` shows correct date (not date_of_hire)
   - ✅ `permanent_address` shows address (not address)
   - ✅ Category/Designation/Department show IDs (not names)

4. Change one field (e.g., phone number)
5. Click **Update Staff**

**Expected Results:**
- ✅ No "undefined" or null fields
- ✅ Update succeeds
- ✅ Changes reflected in list immediately

---

## 📊 TEST 3: Payroll Generation (Uses `status`)

**Steps:**
1. Go to **Payroll Management**
2. Click **Generate Payroll**
3. Select month/year
4. Click **Generate**

**Expected Results:**
- ✅ Only staff with `status === 'active'` included ← ✅ FIXED
- ✅ Staff with status "on_leave" NOT included
- ✅ Staff with status "terminated" NOT included
- ✅ All active staff get payroll records
- ✅ Success message shows

**Verify:**
- [ ] Count active staff in Staff Management
- [ ] Verify same count in generated payroll
- [ ] Check DevTools Console → No errors

---

## 👱 TEST 4: Print Staff Badge (Uses Correct Fields)

**Steps:**
1. Go to **Staff Management**
2. Click **Print Badge** (printer icon)
3. Check print preview

**Expect to see:**
- ✅ Staff name
- ✅ Staff ID
- ✅ Designation name
- ✅ Profile photo (if uploaded)
- ✅ No undefined values

---

## 🗂️ TEST 5: Print Staff Form (Uses Correct Field Names)

**Steps:**
1. Go to **Staff Management**
2. Click **Print Form** (second icon)
3. Check print preview

**Expect to see:**
- ✅ Personal Information section with all fields
- ✅ Status field (not "Employment Status")
- ✅ Date of Joining (not "Hire Date")
- ✅ National ID, KRA PIN
- ✅ Designation, Department, Category
- ✅ Generated on: [Today's date]

---

## 📱 TEST 6: Staff Filter by Status (Not employment_status)

**Steps:**
1. Go to **Staff Management**
2. Filter by Status dropdown
3. Select each option:
   - Active
   - On Leave
   - Suspended
   - Terminated

**Expected Results:**
- ✅ Each filter works
- ✅ Correct staff shown for each status
- ✅ No console errors about "employment_status"

---

## 💾 TEST 7: Check API Requests (DevTools Network)

**Steps:**
1. Open DevTools (F12)
2. Go to Network tab
3. **Create new staff**
4. Find **POST /staff/** request
5. Check request payload

**Verify in Request Body:**
```
staff_id: ST002
first_name: John
gender: M             ← ✅ Present
category: 1           ← ✅ ID (not name)
designation: 2        ← ✅ ID (not name)
department: 3         ← ✅ ID (not name)
status: active        ← ✅ Present
basic_salary: 50000   ← ✅ Present
date_of_joining: 2024-01-15  ← ✅ Correct name
permanent_address: "123 School Road"  ← ✅ Correct name
profile_picture: [file]     ← ✅ Image file
passport_photo: [file]      ← ✅ Image file
```

**Check Response Status:**
- ✅ HTTP 201 Created (success)
- ✅ Response contains new staff with ID
- ✅ All fields echoed back

---

## ❌ TEST 8: Verify Error Handling

**Test 1: Missing Gender**
- [ ] Try to create staff WITHOUT selecting gender
- [ ] Expected: Error "This field is required"

**Test 2: Missing Salary**
- [ ] Try to create staff WITHOUT entering salary
- [ ] Expected: Error about basic_salary required

**Test 3: Missing Permanent Address**
- [ ] Try to create staff WITHOUT permanent address
- [ ] Expected: Error "This field is required"

**Test 4: Invalid Email**
- [ ] Try email that already exists
- [ ] Expected: Error "Staff with this email already exists"

**Test 5: Duplicate Staff ID**
- [ ] Try staff ID that already exists
- [ ] Expected: Error "Staff with this ID already exists"

---

## 🎯 FIELD NAME VERIFICATION

**Confirm these field names are used correctly:**

| Field | Form Label | Backend Model | Status |
|-------|-----------|---------------|--------|
| gender | Gender | gender | ✅ FIXED |
| status | Status | status | ✅ FIXED |
| date_of_joining | Date of Joining | date_of_joining | ✅ FIXED |
| basic_salary | Basic Salary | basic_salary | ✅ FIXED |
| permanent_address | Permanent Address | permanent_address | ✅ FIXED |
| category | Category | category | ✅ FIXED |
| designation | Designation | designation | ✅ FIXED |
| department | Department | department | ✅ FIXED |
| profile_picture | Profile Picture | profile_picture | ✅ FIXED |
| passport_photo | Passport Photo | passport_photo | ✅ FIXED |

✅ All field names match backend model exactly!

---

## 📋 SIGN-OFF CHECKLIST

After running all tests, check:

- [ ] Can create staff with gender field
- [ ] Can create staff with salary field
- [ ] Can create staff with address field
- [ ] Can upload profile and passport photos
- [ ] Dropdowns send IDs (not names)
- [ ] Status filter works (not employment_status)
- [ ] Payroll generation includes only active staff
- [ ] Print forms show correct field names
- [ ] No console errors about undefined fields
- [ ] All API requests use correct field names
- [ ] Error messages are clear and helpful
- [ ] System works end-to-end

---

## 🚀 SUCCESS CRITERIA

System is **fully aligned with backend** when:

✅ All 12+ form fields are collectible
✅ Photos upload successfully
✅ Dropdown values are IDs (not names)
✅ Required fields enforced (gender, salary, address)
✅ Field names match backend model exactly
✅ Payroll generation filters by `status`
✅ No undefined or null values in displays
✅ API requests/responses match expectations
✅ Error messages are helpful
✅ Print functions use correct field names

---

## 📞 IF SOMETHING DOESN'T WORK

1. **Check DevTools Console** (F12) for JavaScript errors
2. **Check Network tab** for API response errors
3. **Verify field values** in API request match backend expectations
4. **Look for "undefined"** values in forms/lists
5. **Test with fresh login** (clear localStorage)

**Common Issues & Fixes:**

| Issue | Fix |
|-------|-----|
| "Cannot read property 'name' of undefined" | Dropdown should use `.id` not `.name` |
| "This field is required" | Ensure gender, salary, address are filled |
| 400 Bad Request | Check field names match backend exactly |
| "Staff already exists" | Email/ID must be unique |
| Photos not uploading | Ensure file upload handlers are set |

---

**Test Date**: April 13, 2026
**Status**: ✅ READY FOR TESTING
**System**: Backend Aligned & Production Ready
