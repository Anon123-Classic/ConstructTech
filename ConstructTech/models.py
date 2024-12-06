from django.db import models
from django.contrib.auth.models import User
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    Subject = models.CharField(max_length=200)
    Message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)  # Field for storing the creation timestamp

    def __str__(self):
        return f"{self.name} - {self.Subject}"

class Quote(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=10)  # Adjusted for flexibility in phone numbers
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link each quote to its creator

    def __str__(self):
        return f"Quote request from {self.name} - {self.subject}"


    

class UploadedImage(models.Model):
    title = models.CharField(max_length=100)  # Title for the image
    image = models.ImageField(upload_to='uploaded_images/')  # Save images to this folder

    def __str__(self):
        return self.title