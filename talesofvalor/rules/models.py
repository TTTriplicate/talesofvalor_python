"""
Describes special rules for skills, headers, origins.
"""
from django.contrib.contenttypes.fields import GenericForeignKey,\
    GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext as _

from djangocms_text_ckeditor.fields import HTMLField

from talesofvalor.origins.models import Origin
from talesofvalor.skills.models import Header, HeaderSkill, Skill


class Rule(models.Model):
    """
    Rules that change what skills/headers cost.

    Origins or other attributes may change what a skill costs.

    Rules track those changes and should be run when adding up
    character point changes/totals.

    Grant skills are skills that have the Boolean "free" field set to true:
    When a character fulfills the requirement,
    they get the skill automatically without having to buy it.

    Prerequisites are things that have to happen before something can be
    purchased and are attached to that thing.
    """

    SKILL_RULE = 'SkillRule'
    HEADER_RULE = 'HeaderRule'
    ORIGIN_RULE = 'OriginRule'
    GRANT_RULE = 'GrantRule'  # happens without having to purchase the skill:  The skill is given automatically.
    RULE_REQUIREMENT_CHOICES = (
        (SKILL_RULE, 'Skill Rule'),
        (HEADER_RULE, 'Header Rule'),
        (ORIGIN_RULE, 'Origin Rule'),
        (GRANT_RULE, 'Grant Rule')
    )
    name = models.CharField(max_length=100)
    description = HTMLField(blank=True)
    # the origin, header, skill, grant that invokes this rule.
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to=models.Q(
            app_label='origins', model='Origin'
        ) | models.Q(
            app_label='skills', model='Header'
        ) | models.Q(
            app_label='skills', model='Skill'
        )

    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    # the skill that this will effect
    skill = models.ForeignKey(
        HeaderSkill,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    # the new cost of the skill
    new_cost = models.PositiveIntegerField(default=0, blank=True, null=True)
    # The character just gets this skill for free, without having to buy it at all.
    free = models.BooleanField(
        default=False,
        blank=True,
        help_text=_("This is granted for free if the requirements are met.")
    )
    # Universal.  Everybody gets this no matter what.
    universal_flag = models.BooleanField(
        _("Universal"),
        default=False,
        help_text=_("All characters get this.")
    )
    # There are a limited number of times that the user can choose this skill
    # as a result of fulfilling
    # The requirement.  Defaults to infinite.
    picks_remaining = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        """General display of model."""
        return "{}".format(
            self.name
        )

    @property
    def type(self):
        if self.free:
            return self.GRANT_RULE
        return "{} Rule".format(self.content_type.name.capitalize())


class Prerequisite(models.Model):
    """
    Indicates something that must be true before an item can be purchased.
    That Item can be an a header, a skill (ie, a capstone)

    there are different "types" but that is mostly for UI sake

    Any of these can be attached ot any object.
    """
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to=models.Q(
            app_label='origins', model='Origin'
        ) | models.Q(
            app_label='skills', model='Header'
        ) | models.Q(
            app_label='skills', model='Skill'
        )

    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    origin = models.ForeignKey(
        Origin,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    number_of_purchases = models.PositiveIntegerField(
        help_text=_("How many you must purchase to meet the requirement"),
        blank=True,
        null=True
    )
    skill = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE,
        help_text=_("What skill must be purchased"),
        blank=True,
        null=True
    )
    points = models.PositiveIntegerField(
        help_text=_("how many character points"),
        blank=True,
        null=True
    )
    number_of_different_skills = models.PositiveIntegerField(
        help_text=_("how many different skills must be purchased"),
        blank=True,
        null=True
    )
    header = models.ForeignKey(
        Header,
        on_delete=models.CASCADE,
        help_text=_("What header the skills must be in."),
        blank=True,
        null=True
    )
    additional_header = models.ForeignKey(
        Header,
        on_delete=models.CASCADE,
        help_text=_("Additional header before you can purchase this."),
        blank=True,
        null=True,
        related_name="additional_headers"
    )

    def __str__(self):
        """General display of model."""
        if self.origin:
            return f"{self.id}: Requires {self.origin}"
        if self.number_of_purchases:
            return f"{self.id}: Requires {self.number_of_purchases} of {self.skill}"
        if self.number_of_different_skills:
            return f"{self.id}: Requires {self.points} point in {self.number_of_different_skills} in {self.header}"
        if self.additional_header:
            return f"{self.id}: Requires additional header, {self.additional_header}"
        if self.skill:
            return f"{self.id}: Requires {self.skill}"

class PrerequisiteGroup(models.Model):
    """
    A grouping of prerequisites that can be combined with "AND" or "OR"
    """
    OR = 'OR'
    AND = 'AND'
    OPERATOR_CHOICES = [
        (OR, 'or'),
        (AND, 'and'),
    ]
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to=models.Q(
            app_label='origins', model='Origin'
        ) | models.Q(
            app_label='skills', model='Header'
        ) | models.Q(
            app_label='skills', model='Skill'
        )

    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    operator = models.CharField(
        max_length=3,
        choices=OPERATOR_CHOICES,
        default=OR,
    )
    # done like the to prevent circular imports
    prerequisites = GenericRelation('rules.Prerequisite')
