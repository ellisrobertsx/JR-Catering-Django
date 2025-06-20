@echo off
setlocal enabledelayedexpansion

echo 🚀 Starting Heroku deployment for JR Catering Django App...

REM Check if Heroku CLI is installed
heroku --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Heroku CLI is not installed. Please install it first:
    echo    https://devcenter.heroku.com/articles/heroku-cli
    pause
    exit /b 1
)

REM Check if user is logged in to Heroku
heroku auth:whoami >nul 2>&1
if errorlevel 1 (
    echo 🔐 Please login to Heroku first:
    heroku login
)

REM Get app name from user
set /p APP_NAME="Enter your Heroku app name (or press Enter to auto-generate): "

if "%APP_NAME%"=="" (
    echo 📝 Creating Heroku app with auto-generated name...
    heroku create
    for /f "tokens=*" %%i in ('heroku apps:info --json ^| findstr "name"') do (
        set APP_INFO=%%i
    )
    REM Extract app name from JSON (simplified)
    set APP_NAME=!APP_INFO:~8,-1!
) else (
    echo 📝 Creating Heroku app: %APP_NAME%
    heroku create %APP_NAME%
)

echo ✅ Heroku app created: %APP_NAME%

REM Add PostgreSQL database
echo 🗄️  Adding PostgreSQL database...
heroku addons:create heroku-postgresql:mini

REM Set environment variables
echo 🔧 Setting environment variables...
heroku config:set SECRET_KEY="%RANDOM%%RANDOM%%RANDOM%%RANDOM%%RANDOM%"
heroku config:set DEBUG=False

REM Deploy the app
echo 📦 Deploying to Heroku...
git add .
git commit -m "Deploy to Heroku"
git push heroku main

REM Run database migrations
echo 🔄 Running database migrations...
heroku run python manage.py migrate

REM Collect static files
echo 📁 Collecting static files...
heroku run python manage.py collectstatic --noinput

REM Ask if user wants to create a superuser
set /p CREATE_SUPERUSER="Do you want to create a superuser? (y/n): "
if /i "%CREATE_SUPERUSER%"=="y" (
    echo 👤 Creating superuser...
    heroku run python manage.py createsuperuser
)

REM Ask if user wants to add sample data
set /p ADD_SAMPLE_DATA="Do you want to add sample data? (y/n): "
if /i "%ADD_SAMPLE_DATA%"=="y" (
    echo 📊 Adding sample data...
    heroku run python manage.py add_sample_data
)

REM Open the app
echo 🌐 Opening your app...
heroku open

echo ✅ Deployment complete!
echo 🎉 Your app is now live at: https://%APP_NAME%.herokuapp.com
echo.
echo 📋 Useful commands:
echo    View logs: heroku logs --tail
echo    Check app status: heroku ps
echo    Access Django shell: heroku run python manage.py shell
echo    Monitor database: heroku pg:info

pause 