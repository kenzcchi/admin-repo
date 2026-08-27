from django.db import models

class ProviderVerification(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    # Provider Details
    full_name = models.CharField(max_length=255)
    
    # Document Uploads (Saved in media/verifications/)
    id_photo = models.ImageField(upload_to='verifications/ids/')
    selfie = models.ImageField(upload_to='verifications/selfies/')
    
    # Verification Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name} - {self.status}"