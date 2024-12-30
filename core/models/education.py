from django.db import models
from .person import Person

class Education(models.Model):
    """
    Model to track individual-level education metrics and history.
    """
    person = models.OneToOneField(
        Person,
        on_delete=models.CASCADE,
        related_name='education'
    )

    # Current Education Status
    EDUCATION_LEVEL_CHOICES = [
        ('none', 'No Formal Education'),
        ('primary', 'Primary School'),
        ('secondary', 'Secondary School'),
        ('high_school', 'High School'),
        ('vocational', 'Vocational Training'),
        ('associates', 'Associate\'s Degree'),
        ('bachelors', 'Bachelor\'s Degree'),
        ('masters', 'Master\'s Degree'),
        ('doctorate', 'Doctorate'),
        ('other', 'Other')
    ]

    current_education_level = models.CharField(
        max_length=50,
        choices=EDUCATION_LEVEL_CHOICES,
        default='none'
    )

    is_currently_enrolled = models.BooleanField(default=False)

    # School Information
    school_name = models.CharField(max_length=200, blank=True, null=True)
    school_type = models.CharField(
        max_length=50,
        choices=[
            ('public', 'Public'),
            ('private', 'Private'),
            ('charter', 'Charter'),
            ('homeschool', 'Homeschool'),
            ('other', 'Other')
        ],
        null=True,
        blank=True
    )

    # Academic Performance
    grade_point_average = models.FloatField(null=True, blank=True)

    # Additional Educational Metrics
    years_of_education = models.PositiveIntegerField(default=0)
    has_special_education = models.BooleanField(default=False)
    primary_language = models.CharField(max_length=50, default='English')
    is_bilingual = models.BooleanField(default=False)

    # Scholarships and Financial Aid
    receives_financial_aid = models.BooleanField(default=False)
    scholarship_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00
    )

    # Digital Learning
    has_access_to_computer = models.BooleanField(default=False)
    participates_in_remote_learning = models.BooleanField(default=False)

    # Extracurricular Activities
    participates_in_extracurricular = models.BooleanField(default=False)
    extracurricular_activities = models.TextField(blank=True)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Education"
        db_table = 'education'

    def __str__(self):
        return f"Education Record for {self.person.full_name}"

    def get_education_level_score(self):
        """
        Calculate education level score (0-8).
        """
        level_scores = {
            'none': 0,
            'primary': 1,
            'secondary': 2,
            'high_school': 3,
            'vocational': 4,
            'associates': 5,
            'bachelors': 6,
            'masters': 7,
            'doctorate': 8
        }
        return level_scores.get(self.current_education_level, 0)

    def is_higher_education(self):
        """
        Check if the person is in or has completed higher education.
        """
        higher_ed_levels = ['associates', 'bachelors', 'masters', 'doctorate']
        return self.current_education_level in higher_ed_levels

    def get_academic_status(self):
        """
        Return a summary of the person's academic status.
        """
        status = f"Level: {self.get_education_level_display()}"
        if self.is_currently_enrolled:
            status += " (Currently Enrolled)"
        if self.school_name:
            status += f" at {self.school_name}"
        return status