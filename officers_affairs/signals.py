from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Officer

@receiver(post_save, sender=Officer)
def create_user_for_officer(sender, instance, created, **kwargs):
    if created:
        # Create a corresponding user
        username = instance.full_name.replace(" ", "").lower()  # Generate a username from the full name
        user = User.objects.create_user(username=username, password='defaultpassword123')  # Default password
        user.first_name = instance.full_name  # Set the user's full name
        user.save()
        
        # Link the user to the officer
        instance.user = user
        instance.save()

        # Assign the user to the branch group
        if instance.branch:
            group, created = Group.objects.get_or_create(name=instance.branch.name)
            user.groups.add(group)

        # Set default user profile data (rank and profile image)
        user.profile_image = instance.profile_image
        user.rank = instance.rank
        user.save()
