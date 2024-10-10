from django.db import models
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.core.exceptions import ValidationError

from wagtail import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.models import Page
from wagtail.images.blocks import ImageChooserBlock
from datetime import datetime

from utils.models import (
    UtilsCodeBlock,
    UtilsResultBlock,
    UtilsCustomRichTextBlock,
)


def validate_year(value):
    current_year = datetime.now().year
    if value < 1980 or value > current_year:
        raise ValidationError(
            f"L'année doit être comprise entre 1980 et {current_year}."
        )


class ExperienceIndexPage(Page):
    subpage_types = ["experience.ExperiencePage"]
    parent_page_types = ["home.HomePage"]

    summary = models.TextField(blank=True, max_length=500)

    content_panels = Page.content_panels + [
        FieldPanel("summary"),
    ]

    def get_context(self, request):
        context = super().get_context(request)

        posts = (
            ExperiencePage.objects.live()
            .public()
            .order_by("-first_published_at")
        )
        page = request.GET.get("page", 1)

        paginator = Paginator(posts, 6)
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        context["posts"] = posts
        return context


class ExperiencePage(Page):
    parent_page_types = ["experience.ExperienceIndexPage"]
    logo = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    date_in = models.IntegerField(
        "Date d'entrée", blank=True, null=True, validators=[validate_year]
    )
    date_out = models.IntegerField(
        "Date de sortie", blank=True, null=True, validators=[validate_year]
    )
    summary = models.TextField(blank=True, max_length=500)
    body = StreamField(
        [
            (
                "content",
                UtilsCustomRichTextBlock(),
            ),
            (
                "image",
                ImageChooserBlock(
                    template="blocks/image.html",
                ),
            ),
            (
                "quote",
                blocks.BlockQuoteBlock(
                    template="blocks/quote.html",
                ),
            ),
            (
                "twitter_block",
                blocks.StructBlock(
                    [
                        ("text", blocks.CharBlock()),
                    ],
                    template="blocks/twitter_block.html",
                ),
            ),
            (
                "code_block",
                UtilsCodeBlock(),
            ),
            (
                "result_block",
                UtilsResultBlock(),
            ),
        ]
    )

    content_panels = Page.content_panels + [
        FieldPanel("summary"),
        FieldPanel("logo"),
        FieldPanel("date_in"),
        FieldPanel("date_out"),
        FieldPanel("body"),
    ]
