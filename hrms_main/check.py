from .models import CustomUser

# List all users
users = CustomUser.objects.all()
for user in users:
    print(user.username, user.password)