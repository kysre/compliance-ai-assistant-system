from django.db import models
from django.utils.translation import gettext_lazy as _


class Regulation(models.Model):
    """
    Model representing a regulation or law.

    A regulation can have multiple articles and can reference other regulations.
    """

    title = models.CharField(max_length=255, help_text=_("Regulation Title"))
    description = models.TextField(help_text=_("Description"), blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.number}" if self.number else self.title

    class Meta:
        verbose_name = _("Regulation")
        verbose_name_plural = _("Regulations")
        ordering = ["-created_at", "title"]


class Article(models.Model):
    """
    Model representing an article within a regulation.

    Each article belongs to a regulation and can have multiple clauses.
    """

    regulation = models.ForeignKey(
        Regulation,
        on_delete=models.CASCADE,
        related_name="articles",
        help_text=_("Related Regulation"),
    )
    number = models.CharField(max_length=50, help_text=_("Article Number"))
    text = models.TextField(help_text=_("Article Text"))

    def __str__(self):
        return f"{self.regulation.title} - {_('Article')} {self.number}"

    class Meta:
        verbose_name = _("Article")
        verbose_name_plural = _("Articles")
        ordering = ["regulation", "number"]
        unique_together = ["regulation", "number"]


class Clause(models.Model):
    """
    Model representing a clause within an article.

    Each clause belongs to an article.
    """

    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name="clauses",
        help_text=_("Related Article"),
    )
    number = models.CharField(max_length=50, help_text=_("Clause Number"))
    text = models.TextField(help_text=_("Clause Text"))

    def __str__(self):
        return f"{self.article} - {_('Clause')} {self.number}"

    class Meta:
        verbose_name = _("Clause")
        verbose_name_plural = _("Clauses")
        ordering = ["article", "number"]
        unique_together = ["article", "number"]
