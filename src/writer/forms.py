from django.forms import ModelForm

from account.models import CustomUser
from common.django_utils import AsyncModelFormMixin
from writer.models import Article

class ArticleForm(ModelForm, AsyncModelFormMixin):
    class Meta:
        model = Article

        fields = (
            'title', 'content', 'is_premium',
        )

class UpdateUserForm(ModelForm, AsyncModelFormMixin):
    class Meta:
        model = CustomUser

        fields = (
            'email', 'firstName', 'lastName',
        )