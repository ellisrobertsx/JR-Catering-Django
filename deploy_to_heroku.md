# Deploy JR Catering Django App to Heroku

## Prerequisites
1. Install Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli
2. Install Git (if not already installed)
3. Have a Heroku account

## Step-by-Step Deployment Guide

### 1. Initialize Git Repository (if not already done)
```bash
git init
git add .
git commit -m "Initial commit for Heroku deployment"
```

### 2. Login to Heroku
```bash
heroku login
```

### 3. Create Heroku App
```bash
heroku create your-app-name
```
Replace `your-app-name` with your desired app name (must be unique across Heroku).

### 4. Add PostgreSQL Database
```bash
heroku addons:create heroku-postgresql:mini
```

### 5. Set Environment Variables
```bash
heroku config:set SECRET_KEY="your-secret-key-here"
heroku config:set DEBUG=False
```

### 6. Run Database Migrations
```bash
heroku run python manage.py migrate
```

### 7. Create Superuser (Optional)
```bash
heroku run python manage.py createsuperuser
```

### 8. Collect Static Files
```bash
heroku run python manage.py collectstatic --noinput
```

### 9. Deploy to Heroku
```bash
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

### 10. Open Your App
```bash
heroku open
```

## Troubleshooting

### If you get a build error:
1. Check that all files are committed to git
2. Ensure `requirements.txt` is in the root directory
3. Verify `Procfile` is in the root directory (no file extension)

### If static files don't load:
1. Run `heroku run python manage.py collectstatic --noinput`
2. Check that `STATIC_ROOT` is set correctly in settings.py

### If database errors occur:
1. Run `heroku run python manage.py migrate`
2. Check that PostgreSQL addon is properly configured

### To view logs:
```bash
heroku logs --tail
```

## Post-Deployment

### Add Sample Data (Optional)
```bash
heroku run python manage.py add_sample_data
```

### Create Admin User (Optional)
```bash
heroku run python manage.py create_admin
```

## Environment Variables Reference

- `SECRET_KEY`: Django secret key for security
- `DEBUG`: Set to `False` for production
- `DATABASE_URL`: Automatically set by Heroku PostgreSQL addon

## Important Notes

1. The app will use PostgreSQL in production (automatically configured by Heroku)
2. Static files are served by WhiteNoise middleware
3. SSL is automatically enabled in production
4. The app will be available at `https://your-app-name.herokuapp.com`

## Monitoring Your App

- View logs: `heroku logs --tail`
- Check app status: `heroku ps`
- Monitor database: `heroku pg:info`
- Access Django shell: `heroku run python manage.py shell` 