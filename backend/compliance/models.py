from django.db import models
from django.utils.translation import gettext_lazy as _


class Regulation(models.Model):
    """
    Model representing a regulation or law.
    """

    identifier = models.CharField(max_length=30, help_text=_("Unique Identifier (IDS)"))
    title = models.CharField(max_length=510, help_text=_("Regulation Title"))
    date = models.DateField(help_text=_("Approval Date"))
    authority = models.CharField(max_length=255, help_text=_("Approval Authority"))
    link = models.URLField(help_text=_("Regulation Link"), blank=True)
    text = models.TextField(help_text=_("Regulation Text"), blank=True, default="")

    def __str__(self):
        return f"{self.title} - {self.date}"

    class Meta:
        verbose_name = _("Regulation")
        verbose_name_plural = _("Regulations")
        ordering = ["-date", "title"]
