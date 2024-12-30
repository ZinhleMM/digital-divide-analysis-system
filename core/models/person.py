"""
person.py - Person Model for Digital Divide Analysis System

This module defines the Person model representing individuals within South African households,
focusing on their educational and technology usage characteristics.

References:
Department of Basic Education SA. "Education Statistics 2019." 2020,
www.education.gov.za/EMIS/StatisticalPublications.

Statistics South Africa. "General Household Survey 2021." Stats SA, 2022,
www.statssa.gov.za/publications/P0318/P03182021.pdf.
"""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from .household import Household


class Person(models.Model):
    """
    Represents an individual within a South African household, capturing their
    demographic information, educational status, and technology usage patterns.
    """

    # Educational level choices based on South African education system
    EDUCATION_LEVEL_CHOICES = [
        ('NONE', 'No Formal Education'),
        ('PRIM', 'Primary School'),
        ('SECO', 'Secondary School'),
        ('MATR', 'Matric Completed'),
        ('DIPL', 'Diploma/Certificate'),
        ('DEGR', 'University Degree'),
        ('POST', 'Postgraduate Degree'),
    ]

    SCHOOL_TYPE_CHOICES = [
        ('PUB', 'Public School'),
        ('PRI', 'Private School'),
        ('TVET', 'TVET College'),
        ('UNI', 'University'),
        ('NONE', 'Not Enrolled'),
    ]

    # Basic Information
    person_id = models.CharField(
        max_length=20,
        primary_key=True,
        help_text=_("Unique identifier for the person")
    )

    household = models.ForeignKey(
        Household,
        on_delete=models.CASCADE,
        related_name='household_members',
        help_text=_("Associated household")
    )

    # Demographic Information
    age = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(120)],
        help_text=_("Age in years")
    )

    gender = models.CharField(
        max_length=1,
        choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')],
        help_text=_("Gender of the person")
    )

    # Educational Information
    education_level = models.CharField(
        max_length=4,
        choices=EDUCATION_LEVEL_CHOICES,
        help_text=_("Highest level of education completed")
    )

    currently_studying = models.BooleanField(
        default=False,
        help_text=_("Whether the person is currently enrolled in education")
    )

    school_type = models.CharField(
        max_length=4,
        choices=SCHOOL_TYPE_CHOICES,
        default='NONE',
        help_text=_("Type of educational institution currently attending")
    )

    # Technology Usage
    has_own_device = models.BooleanField(
        default=False,
        help_text=_("Whether the person has their own computing device")
    )

    device_type = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text=_("Type of personal computing device owned")
    )

    internet_usage_hours = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(24.0)],
        default=0.0,
        help_text=_("Average daily internet usage in hours")
    )

    uses_internet_for_education = models.BooleanField(
        default=False,
        help_text=_("Whether internet is used for educational purposes")
    )

    # Educational Performance (for students)
    average_academic_score = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
        null=True,
        blank=True,
        help_text=_("Average academic score (percentage)")
    )

    # Digital Literacy Score
    digital_literacy_score = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(1.0)],
        null=True,
        blank=True,
        help_text=_("Calculated digital literacy score (0-1)")
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
        verbose_name = _("Person")
        verbose_name_plural = _("People")
        ordering = ['household', 'age']
        indexes = [
            models.Index(fields=['household', 'education_level']),
            models.Index(fields=['digital_literacy_score']),
            models.Index(fields=['age', 'education_level']),
        ]

    def __str__(self):
        """
        String representation of the Person model
        """
        return f"Person {self.person_id} - {self.age} years old"

    def calculate_digital_literacy_score(self):
        """
        Calculates digital literacy score based on device ownership,
        internet usage, and educational technology adoption.

        Returns:
            float: Digital literacy score between 0 and 1
        """
        # Base score from device ownership (0-0.3)
        device_score = 0.3 if self.has_own_device else 0.0

        # Internet usage score (0-0.4)
        usage_score = min(self.internet_usage_hours / 8.0, 1.0) * 0.4

        # Educational technology adoption score (0-0.3)
        edu_tech_score = 0.3 if self.uses_internet_for_education else 0.0

        # Calculate total score
        self.digital_literacy_score = device_score + usage_score + edu_tech_score
        return self.digital_literacy_score

    def save(self, *args, **kwargs):
        """
        Override save method to calculate digital literacy score before saving
        """
        self.calculate_digital_literacy_score()
        super().save(*args, **kwargs)

    @property
    def is_student(self):
        """
        Determines if the person is currently a student
        """
        return self.currently_studying and self.school_type != 'NONE'

    @property
    def has_digital_access(self):
        """
        Determines if the person has adequate digital access
        """
        return (self.has_own_device and 
                self.household.has_internet and 
                self.internet_usage_hours > 0)