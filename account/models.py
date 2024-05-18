from django.db import models

# Create your models here.


class contact(models.Model):
    name = models.CharField(max_length=70)
    email = models.EmailField(max_length=50)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return f"Message Has Been Sent By : {self.name} on {self.sent_at}" 