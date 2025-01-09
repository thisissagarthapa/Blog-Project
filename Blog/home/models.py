# models.py
import uuid
from django.db import models
from django.contrib.auth.models import User

class BaseModel(models.Model):
    uuid = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)  # Updated to auto-update on changes

    class Meta:
        abstract = True  # Marking this model as abstract

class BlogModel(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blogs')
    title = models.CharField(max_length=500)
    blog_text = models.TextField()
    main_image = models.ImageField(upload_to='blogs')

    def __str__(self):
        return self.title  # Corrected to return the title
