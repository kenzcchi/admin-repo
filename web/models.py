# models.py
from django.db import models


# ==========================================
# PROVIDER VERIFICATION
# ==========================================
# Reconstructed from how approve_provider/reject_provider and the
# provider_verification mock data use it in views.py. If your real
# ProviderVerification model has extra fields, swap them back in.
class ProviderVerification(models.Model):
    class Status(models.TextChoices):
        PENDING = "Pending", "Pending"
        APPROVED = "Approved", "Approved"
        REJECTED = "Rejected", "Rejected"

    name = models.CharField(max_length=150)
    id_photo = models.CharField(max_length=255, blank=True)      # path/URL to uploaded ID photo
    selfie = models.CharField(max_length=255, blank=True)        # path/URL to uploaded selfie
    plate_no = models.CharField(max_length=20, blank=True)
    vehicle_type = models.CharField(max_length=50, blank=True)
    vehicle_doc = models.CharField(max_length=255, blank=True)   # path/URL to OR/CR or similar doc
    vehicle_doc_name = models.CharField(max_length=150, blank=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-submitted_at"]

    def __str__(self):
        return f"{self.name} ({self.status})"

# NOTE: SupportTicket / TicketMessage models were removed for now -- the
# support inbox below is a front-end-only mockup (static demo data baked
# into its <script> block, no database table). Re-add them here once you're
# ready to wire the UI up to real persistence.