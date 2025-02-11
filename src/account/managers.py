"""
Customizes - via inheritance - the 'BaseUserManager'. This class
then participates in creating custom user models. We can give
our users specific permissions with class.

See:
    https://docs.djangoproject.com/en/5.1/topics/auth/customizing
    https://docs.djangoproject.com/en/5.1/topics/auth/customizing/#writing-a-manager-for-a-custom-user-model
    https://docs.djangoproject.com/en/5.1/topics/auth/customizing/#a-full-example
"""

from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _t

class CustomUserManager(BaseUserManager):
    
    def create_user(self, email: str, password: str, **extras):
        """
        From https://docs.djangoproject.com/en/5.1/topics/auth/customizing/#writing-a-manager-for-a-custom-user-model :
            The prototype of createUser() should accept the username field,
            plus all required fields as arguments.
            For example, if your user model uses email as the username field,
            and has dateOfBirth as a required field, then createUser
            should be defined as:
                createUser(self, email, dateOfBirth, password = None): ...
        """

        if not email.strip():
            raise ValueError(_t('The given email must be a non-empty string.'))
        
        user = self.model(
            email=self.normalize_email(email),
            **extras,
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email:str, password: str, **extras):
        """
        From a source of the Internet:
            A superuser in Django is a special type of user account that has
            all the permissions and privileges to manage the Django project.
            A superuser can create, edit, delete, and view any data or content
            in the project, as well as access the Django admin interface.
            Having a superuser is important for setting up and mantaining the
            project, as well as troubleshooting any issues that may arise.
        """

        mustBeTrueFields = ('is_staff', 'is_superuser', 'is_active')
        for field in mustBeTrueFields:
            if field in extras and not extras[field]:
                raise ValueError(_t('Superuser must have all fields set to True.'))
            extras[field] = True

        user = self.create_user(email, password, **extras)
        user.is_admin = True
        user.save()
        return user