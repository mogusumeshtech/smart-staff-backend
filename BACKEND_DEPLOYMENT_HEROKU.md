# 🚀 DEPLOY BACKEND TO HEROKU (Step by Step)

## 📋 What You Need

1. **Heroku Account** (Free) - Sign up at https://www.heroku.com
2. **Heroku CLI** - Will install on your machine
3. **Git** - Already on your machine

---

## ✅ STEP 1: Sign Up for Heroku (5 minutes)

1. Go to: https://www.heroku.com/signup
2. **Email**: Your email
3. **Password**: Create a strong password
4. **Verify email** - Check your email inbox
5. Click the verification link
6. Done! ✅

---

## ✅ STEP 2: Download Heroku CLI (5 minutes)

**For Windows:**
1. Go to: https://devcenter.heroku.com/articles/heroku-cli
2. Click **Download for Windows**
3. Run the installer
4. Click **Next** until installed
5. **Restart your computer** (important!)

**Verify installation:**
Open Terminal (PowerShell in VS Code) and type:
```powershell
heroku --version
```

Should show version number like: `heroku/8.0.0`

---

## ✅ STEP 3: Login to Heroku from Terminal

Open Terminal and run:
```powershell
heroku login
```

**A browser will open** → Sign in with your Heroku account → Close the browser → Terminal says "Login successful"

---

## ✅ STEP 4: Create Heroku App

```powershell
cd "C:\Users\Admin\Desktop\SMART STAFF\backend"
heroku create smart-staff-api
```

**You'll see:**
```
Creating ⬢ smart-staff-api... done
https://smart-staff-api.herokuapp.com/
```

**Copy this URL!** You'll use it later.

---

## ✅ STEP 5: Add Database

```powershell
heroku addons:create heroku-postgresql:hobby-dev -a smart-staff-api
```

**Wait for it to complete** (might take 2-3 minutes)

---

## ✅ STEP 6: Deploy Backend

```powershell
cd "C:\Users\Admin\Desktop\SMART STAFF\backend"

# Initialize Git (if not already done)
git init
git add .
git commit -m "Deploy to Heroku"

# Add Heroku remote
heroku git:remote -a smart-staff-api

# Deploy
git push heroku master
```

**Watch for:**
```
Enumerating objects...
Compressing objects...
Writing objects...

remote: -----> Building on the Heroku platform
remote: -----> Python app detected
...
remote: -----> Release command output:
remote:        python manage.py migrate
```

When done, you'll see:
```
remote: -----> Discovering process types
remote:        Procfile declares types -> web, release
remote: -----> Compressing...
remote: -----> Launching...
remote: ✓ Deployed to Heroku

https://smart-staff-api.herokuapp.com/ deployed to Heroku
```

**SUCCESS!** ✅

---

## ✅ STEP 7: Test Backend

```powershell
heroku open -a smart-staff-api
```

Browser opens → Should see Django running (or 404 page - that's OK)

Or go to:
```
https://smart-staff-api.herokuapp.com/api/v1/auth/login/
```

Should work! ✅

---

## 📝 YOUR BACKEND URL

```
https://smart-staff-api.herokuapp.com
```

**Save this!** You'll need it to connect frontend.

---

## 🆘 If Something Goes Wrong

**Check logs:**
```powershell
heroku logs -a smart-staff-api --tail
```

**Restart app:**
```powershell
heroku restart -a smart-staff-api
```

**Check if database connected:**
```powershell
heroku pg:info -a smart-staff-api
```

---

## 📋 Next Step After Deployment

Once backend is deployed, tell me the URL and I'll:
1. Update frontend to use this URL
2. Fix the login credentials
3. Redeploy frontend
4. Everything will work! 🎉

---

**Follow these steps and tell me the backend URL when done!** ✅

Time needed: ~20 minutes
