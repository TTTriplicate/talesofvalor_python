"""
Describes the character models.

These models describe a character and its relationship
to players.
"""
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext as _
from djangocms_text_ckeditor.fields import HTMLField

from talesofvalor.players.models import Player
from talesofvalor.rules.models import Prerequisite, Rule
from talesofvalor.skills.models import Header, HeaderSkill, Skill
from talesofvalor.origins.models import Origin


STARTING_POINTS = 30
POINT_CAP = 25


class Character(models.Model):
    """
    Character a player can play.

    Players can have more than one character, but only one can be active at a
    time.
    Staff can have multiple characters who are active at the same time.
    """

    ALIVE = 'alive'
    DEAD = 'dead'
    RETIRED = 'retired'
    STATUS_CHOICES = (
        (ALIVE, 'Alive'),
        (DEAD, 'Dead'),
        (RETIRED, 'Retired'),
    )

    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='alive'
    )
    name = models.CharField(_("Character Name"), max_length=255)
    pronouns = models.CharField('pronouns', max_length=25, default='')
    description = models.TextField(blank=True)
    concept = HTMLField(blank=True)
    history = HTMLField(blank=True)
    picture = models.ImageField(blank=True, null=True, upload_to="characters/")
    player_notes = models.TextField(blank=True)
    staff_notes_visible = models.TextField(blank=True)
    staff_notes_hidden = models.TextField(blank=True)
    staff_attention_flag = models.BooleanField(default=False)
    npc_flag = models.BooleanField(default=False)
    active_flag = models.BooleanField(_("Active"), default=False)
    concept_approved_flag = models.BooleanField(_("Concept Approved"), default=False)
    history_approved_flag = models.BooleanField(_("History Approved"), default=False)
    cp_initial = models.PositiveIntegerField(
        default=STARTING_POINTS, 
        help_text=_("Record of initial points in case a character has to be rebuilt.")
    )
    cp_spent = models.PositiveIntegerField(default=0)
    cp_available = models.PositiveIntegerField(default=STARTING_POINTS)
    cp_transferred = models.PositiveIntegerField(default=0)
    # The headers and skills that a character has.
    headers = models.ManyToManyField(Header)
    skills = models.ManyToManyField(HeaderSkill, through='CharacterSkills')
    # origins.  Should only be as many as there are types.
    origins = models.ManyToManyField(Origin)

    created = models.DateTimeField(
        _('date created'),
        null=True,
        auto_now_add=True,
        editable=False
    )
    modified = models.DateTimeField(
        _('last updated'),
        null=True,
        auto_now=True,
        editable=False
    )
    created_by = models.ForeignKey(
        User,
        editable=False,
        related_name='%(app_label)s_%(class)s_author',
        null=True,
        on_delete=models.SET_NULL
    )
    modified_by = models.ForeignKey(
        User,
        editable=False,
        related_name='%(app_label)s_%(class)s_updater',
        null=True,
        on_delete=models.SET_NULL
    )

    def get_absolute_url(self):
        return reverse('characters:character_detail', kwargs={'pk': self.pk})

    def __str__(self):
        try:
            return "{}::{}".format(
                self.name, self.player)
        except ObjectDoesNotExist:
            return "{}".format(self.name)

    @property
    def tradition(self):
        try:
            return self.origins.get(type=Origin.TRADITION)
        except MultipleObjectsReturned:
            return self.origins.filter(type=Origin.TRADITION).first()

    @property
    def people(self):
        try:
            return self.origins.get(type=Origin.PEOPLE)
        except MultipleObjectsReturned:
            return self.origins.filter(type=Origin.PEOPLE).first()

    @property
    def skillhash(self):
        """
        Get the base skill cost hash and update it based on the character
        """
        skillhash = Skill.skillhash()
        # update skillhash with skills the character has.
        # go through the headers and figure out what headers have had the
        # prerequisites met . . .
        bought_headers = list(self.headers.all().values_list('id', flat=True))
        # go through each of the types of rules
        # - update the costs for for the skills
        # - add any granted headers
        # - add any granted skills without the headers.
        available_skills = {}
        for h, skills in skillhash.items():
            # if the header is open, or if the user bought it.
            header = Header.objects.get(pk=h)
            if h in bought_headers or header.open_flag or not header.hidden_flag:
                available_skills[h] = skills
                # update the has with what has been purchased
                # has the header been purchased?
                available_skills[h]['purchased'] = (h in bought_headers)
                # what skills have we bought?
                for skill_id in available_skills[h]['skills']:
                    try:
                        character_skill = self.characterskills_set.get(
                            skill_id=skill_id
                        )
                        available_skills[h]['skills'][skill_id]['purchased'] = character_skill.count
                    except CharacterSkills.DoesNotExist:
                        # if it doesn't exist, we can leave purchased as default.   
                        pass
                    header_skill = HeaderSkill.objects.get(skill_id=skill_id, header_id=h)
                    available_skills[h]['skills'][skill_id]['cost'] = self.skill_cost(header_skill)
        return available_skills

    def skill_cost(self, header_skill):
        """
        Figure out what this skill should cost for this character, based
        on the Rules model
        """
        # see if there is an updated cost for the skill
        skill_cost_query = Rule.objects.filter(
            skill=header_skill,
            new_cost__gt=0
        )
        if not skill_cost_query.exists():
            return header_skill.cost

        # there are cost updates for that skill.  See if the current
        # character has any of them.
        # just get the new costs and put them in the list and get the lowest.
        people_grants = self.people.rules.filter(
            id__in=skill_cost_query
        ).values_list('new_cost', flat=True)
        tradition_grants = self.tradition.rules.filter(
            id__in=skill_cost_query
        ).values_list('new_cost', flat=True)
        skill_grants = header_skill.skill.rules.filter(
            id__in=skill_cost_query
        ).values_list('new_cost', flat=True)
        header_grants = header_skill.header.rules.filter(
            id__in=skill_cost_query
        ).values_list('new_cost', flat=True)
        found_rules = list(tradition_grants) + list(people_grants) + list(skill_grants) + list(header_grants)
        if not found_rules:
            return header_skill.cost
        return min(found_rules)

    def skill_grants(self):
        """
        skills granted by a specific character grant or as a result of
        of character backgrounds or headers granting skills without the need
        for the player to spend points.
        """
        people_grants = self.people.rules.filter(
            free=True,
            skill__isnull=False
        ).values_list('skill', flat=True)
        tradition_grants = self.tradition.rules.filter(
            free=True,
            skill__isnull=False
        ).values_list('skill', flat=True)
        universal_grants = Rule.objects.filter(
            universal_flag=True
        ).values_list('skill', flat=True)
        skill_grants = list(tradition_grants) + list(people_grants) + list(universal_grants)
        return HeaderSkill.objects.filter(id__in=skill_grants)

    def check_header_prerequisites(self, header):
        """
        Does the sent header meet the prerequisites for that header.
        If there are no prerequisites, it meets them.
        """
        try: 
            header_type = ContentType.objects.get_for_model(Header)
            header_prerequisites = Prerequisite.objects.filter(
                content_type__pk=header_type.id,
                object_id=header.id
            )
            # check for origin requirements
            # print(header_prerequisites)
            for prereq in header_prerequisites:
                if prereq.origin: 
                    if prereq.origin not in self.origins:
                        return False
                # check for header/skill requirements
                # did the user purchase the required header, or is the header open?
                if prereq.header:
                    if (not prereq.header.open_flag and 
                            prereq.header not in self.headers.all()):
                        return False            
                    # check for the number of different skills in the header.
                    purchased_skills = self.skills.filter(header_id=prereq.header.id)
                    if prereq.number_of_different_skills > self.skills.filter(header_id=prereq.header.id).count(): 
                        return False
                    # figure out the total skill points
                    total = 0
                    for skill in purchased_skills:
                        total += skill.header.cost * skill.characterskills_set.get(character=self).count

                # check for skill requirements
            # if we made it this far, we can assume all prerequisites
            # have been met.
            return True
        except Prerequisite.DoesNotExist:
            return True
        return True

    def check_skill_prerequisites(self, skill, header):
        """
        Does the sent skill meet the prerequisites for that header.
        If there are no prerequisites, it meets them.
        """
        try: 
            skill_type = ContentType.objects.get_for_model(Skill)
            skill_prerequisites = Prerequisite.objects.filter(
                content_type__pk=skill_type.id,
                object_id=skill.id
            )
        except Prerequisite.DoesNotExist:
            return True
        return True

    class Meta:
        ordering = ["name"]


class CharacterSkills(models.Model):
    """
    Links chracters with their skills.

    Indicates what skills a character has and how many of them exist.

    It is important that we are attaching to the HeaderSkill table because
    that contains the cost of the skill for that header.
    """

    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    skill = models.ForeignKey(HeaderSkill, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(null=False, default=0)


class CharacterLog(models.Model):
    """
    Log of changes to character.

    Whenever anyone makes a change to a character, an entry to
    this log should be added so any problems or bad actions can be traced.
    """

    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    message = models.TextField(_("Log Message"))
    created = models.DateTimeField(
        _('date created'),
        auto_now_add=True,
        editable=False
    )
    created_by = models.ForeignKey(
        User,
        editable=False,
        related_name='%(app_label)s_%(class)s_author',
        null=True,
        on_delete=models.SET_NULL
    )


class CharacterGrant(models.Model):
    """
    Tracks special skills and headers granted to a character.

    Some origins or events trigger the granting of headers or skills.
    These do not count against spent character points.

    TODO: I feel like there is a way to do this without grants since the
    system will know what rules have been or should run.

    Grants would then turn into a "special" that could be granted by a
    staff member.
    """

    SKILL_GRANT = 'SkillGrant'
    HEADER_GRANT = 'HeaderGrant'
    TYPE_CHOICES = (
        (SKILL_GRANT, 'Skill Grant'),
        (HEADER_GRANT, 'Header Grant')
    )
    type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        default='SkillGrant'
    )
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    correlated_id = models.PositiveIntegerField()
    reason = models.TextField()
    free = models.BooleanField(default=False)
    picks_remaining = models.PositiveIntegerField(default=10000)

