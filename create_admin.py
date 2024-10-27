import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bite_tracker.settings')
django.setup()

from django.contrib.auth.models import User

def create_admin_user():
    try:
        if User.objects.filter(username='admin').exists():
            user = User.objects.get(username='admin')
            user.is_staff = True
            user.is_superuser = True
            user.set_password('admin123')
            user.save()
            print("Admin user updated successfully!")
        else:
            user = User.objects.create_user(
                username='admin',
                email='admin@example.com',
                password='admin123'
            )
            user.is_staff = True
            user.is_superuser = True
            user.save()
            print("Admin user created successfully!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    create_admin_user()