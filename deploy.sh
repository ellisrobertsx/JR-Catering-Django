#!/bin/bash

# JR Catering Django App - Heroku Deployment Script

echo "🚀 Starting Heroku deployment for JR Catering Django App..."

# Check if Heroku CLI is installed
if ! command -v heroku &> /dev/null; then
    echo "❌ Heroku CLI is not installed. Please install it first:"
    echo "   https://devcenter.heroku.com/articles/heroku-cli"
    exit 1
fi

# Check if user is logged in to Heroku
if ! heroku auth:whoami &> /dev/null; then
    echo "🔐 Please login to Heroku first:"
    heroku login
fi

# Get app name from user
read -p "Enter your Heroku app name (or press Enter to auto-generate): " APP_NAME

if [ -z "$APP_NAME" ]; then
    echo "📝 Creating Heroku app with auto-generated name..."
    heroku create
    APP_NAME=$(heroku apps:info --json | grep -o '"name":"[^"]*"' | cut -d'"' -f4)
else
    echo "📝 Creating Heroku app: $APP_NAME"
    heroku create $APP_NAME
fi

echo "✅ Heroku app created: $APP_NAME"

# Add PostgreSQL database
echo "🗄️  Adding PostgreSQL database..."
heroku addons:create heroku-postgresql:mini

# Set environment variables
echo "🔧 Setting environment variables..."
heroku config:set SECRET_KEY="$(python -c 'import secrets; print(secrets.token_urlsafe(50))')"
heroku config:set DEBUG=False

# Deploy the app
echo "📦 Deploying to Heroku..."
git add .
git commit -m "Deploy to Heroku"
git push heroku main

# Run database migrations
echo "🔄 Running database migrations..."
heroku run python manage.py migrate

# Collect static files
echo "📁 Collecting static files..."
heroku run python manage.py collectstatic --noinput

# Ask if user wants to create a superuser
read -p "Do you want to create a superuser? (y/n): " CREATE_SUPERUSER
if [[ $CREATE_SUPERUSER =~ ^[Yy]$ ]]; then
    echo "👤 Creating superuser..."
    heroku run python manage.py createsuperuser
fi

# Ask if user wants to add sample data
read -p "Do you want to add sample data? (y/n): " ADD_SAMPLE_DATA
if [[ $ADD_SAMPLE_DATA =~ ^[Yy]$ ]]; then
    echo "📊 Adding sample data..."
    heroku run python manage.py add_sample_data
fi

# Open the app
echo "🌐 Opening your app..."
heroku open

echo "✅ Deployment complete!"
echo "🎉 Your app is now live at: https://$APP_NAME.herokuapp.com"
echo ""
echo "📋 Useful commands:"
echo "   View logs: heroku logs --tail"
echo "   Check app status: heroku ps"
echo "   Access Django shell: heroku run python manage.py shell"
echo "   Monitor database: heroku pg:info" 