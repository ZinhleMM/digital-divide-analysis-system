"""
household.py - Household Model for Digital Divide Analysis System

This module defines the Household model representing South African households
and their technology access characteristics.

References:
Statistics South Africa. "General Household Survey 2021." Stats SA, 2022,
www.statssa.gov.za/publications/P0318/P03182021.pdf.

World Bank. "Digital Access Index Methodology." World Bank Group, 2020,
documents.worldbank.org/digital-development/methodology
"""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _


class Household(models.Model):
    """
    Represents a household unit in South Africa with attributes related to
    digital access and socioeconomic factors.
    """

    # Geographic Information
    PROVINCE_CHOICES = [
        ('EC', 'Eastern Cape'),
        ('FS', 'Free State'),
        ('GP', 'Gauteng'),
        ('KZN', 'KwaZulu-Natal'),
        ('LP', 'Limpopo'),
        ('MP', 'Mpumalanga'),
        ('NC', 'Northern Cape'),
        ('NW', 'North West'),
        ('WC', 'Western Cape'),
    ]

    AREA_TYPE_CHOICES = [
        ('URB', 'Urban'),
        ('RUR', 'Rural'),
        ('INF', 'Informal Settlement'),
    ]

    # Unique identifier for the household
    household_id = models.CharField(
        max_length=20,
        primary_key=True,
        help_text=_("Unique identifier for the household")
    )

    # Geographic location details
    province = models.CharField(
        max_length=3,
        choices=PROVINCE_CHOICES,
        help_text=_("Province where the household is located")
    )

    municipality = models.CharField(
        max_length=100,
        help_text=_("Municipality name")
    )

    area_type = models.CharField(
        max_length=3,
        choices=AREA_TYPE_CHOICES,
        help_text=_("Type of settlement area")
    )

    # Household characteristics
    household_size = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        help_text=_("Number of people in the household")
    )

    monthly_income = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_("Monthly household income in Rand")
    )

    # Digital access indicators
    has_electricity = models.BooleanField(
        default=False,
        help_text=_("Whether the household has electricity access")
    )

    has_internet = models.BooleanField(
        default=False,
        help_text=_("Whether the household has internet access")
    )

    INTERNET_TYPE_CHOICES = [
        ('NONE', 'No Internet'),
        ('FIBER', 'Fiber'),
        ('ADSL', 'ADSL'),
        ('MOB', 'Mobile Data'),
        ('SAT', 'Satellite'),
    ]

    internet_type = models.CharField(
        max_length=5,
        choices=INTERNET_TYPE_CHOICES,
        default='NONE',
        help_text=_("Type of internet connection")
    )

    number_of_computers = models.PositiveIntegerField(
        default=0,
        help_text=_("Number of computers/laptops in the household")
    )

    number_of_smartphones = models.PositiveIntegerField(
        default=0,
        help_text=_("Number of smartphones in the household")
    )

    # Digital Access Index (calculated field)
    digital_access_index = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        null=True,
        blank=True,
        help_text=_("Calculated Digital Access Index score (0-1)")
    )

    # Metadata
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text=_("Timestamp when the record was created")
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        help_text=_("Timestamp when the record was last updated")
    )

    class Meta:
        """
        Meta class for additional model configurations
        """
        verbose_name = _("Household")
        verbose_name_plural = _("Households")
        ordering = ['province', 'municipality']
        indexes = [
            models.Index(fields=['province', 'area_type']),
            models.Index(fields=['digital_access_index']),
        ]

    def __str__(self):
        """
        String representation of the Household model
        """
        return f"Household {self.household_id} - {self.municipality}, {self.province}"

    def calculate_digital_access_index(self):
        """
        Calculates the Digital Access Index based on household characteristics.

        The index is calculated using a weighted average of:
        - Internet access and type (40%)
        - Device availability (30%)
        - Infrastructure (electricity) (30%)

        Returns:
            float: Digital Access Index score between 0 and 1
        """
        # Internet score (0-4 points)
        internet_scores = {
            'NONE': 0,
            'MOB': 2,
            'ADSL': 3,
            'FIBER': 4,
            'SAT': 3
        }
        internet_score = internet_scores.get(self.internet_type, 0) / 4

        # Device score (0-1 points)
        devices_per_person = (self.number_of_computers + 
                            self.number_of_smartphones) / self.household_size
        device_score = min(devices_per_person, 1.0)

        # Infrastructure score (0-1 points)
        infrastructure_score = 1.0 if self.has_electricity else 0.0

        # Calculate weighted average
        self.digital_access_index = (
            (internet_score * 0.4) +
            (device_score * 0.3) +
            (infrastructure_score * 0.3)
        )
        return self.digital_access_index

    def save(self, *args, **kwargs):
        """
        Override save method to calculate digital access index before saving
        """
        self.calculate_digital_access_index()
        super().save(*args, **kwargs)