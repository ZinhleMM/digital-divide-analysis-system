from django.db import models
from .household import Household

class TechnologyAccess(models.Model):
    """
    Model to track household-level technology ownership and internet access.
    """
    household = models.OneToOneField(
        Household,
        on_delete=models.CASCADE,
        related_name='technology_access'
    )

    # Internet Access
    has_internet = models.BooleanField(default=False)
    internet_type = models.CharField(
        max_length=50,
        choices=[
            ('none', 'No Internet'),
            ('broadband', 'Broadband'),
            ('mobile', 'Mobile Data'),
            ('satellite', 'Satellite'),
            ('dial_up', 'Dial-up'),
            ('other', 'Other')
        ],
        default='none'
    )
    internet_speed_mbps = models.FloatField(null=True, blank=True)

    # Device Ownership
    num_smartphones = models.PositiveIntegerField(default=0)
    num_computers = models.PositiveIntegerField(default=0)
    num_tablets = models.PositiveIntegerField(default=0)

    # Smart Home Devices
    has_smart_tv = models.BooleanField(default=False)
    has_smart_speaker = models.BooleanField(default=False)
    has_smart_thermostat = models.BooleanField(default=False)

    # Additional Technology
    has_gaming_console = models.BooleanField(default=False)
    has_streaming_service = models.BooleanField(default=False)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Technology Access"
        db_table = 'technology_access'

    def __str__(self):
        return f"Technology Access for Household {self.household.id}"

    def get_total_devices(self):
        """
        Calculate the total number of digital devices in the household.
        """
        return self.num_smartphones + self.num_computers + self.num_tablets

    def has_any_smart_devices(self):
        """
        Check if the household has any smart home devices.
        """
        return any([
            self.has_smart_tv,
            self.has_smart_speaker,
            self.has_smart_thermostat
        ])

    def get_technology_score(self):
        """
        Calculate a basic technology adoption score (0-10).
        """
        score = 0

        # Internet access (0-3 points)
        if self.has_internet:
            score += 2
            if self.internet_type in ['broadband', 'fiber']:
                score += 1

        # Devices (0-3 points)
        devices_score = min(3, self.get_total_devices() / 2)
        score += devices_score

        # Smart devices (0-2 points)
        smart_devices = sum([
            self.has_smart_tv,
            self.has_smart_speaker,
            self.has_smart_thermostat
        ])
        score += min(2, smart_devices)

        # Additional technology (0-2 points)
        additional_tech = sum([
            self.has_gaming_console,
            self.has_streaming_service
        ])
        score += min(2, additional_tech)

        return round(score, 1)