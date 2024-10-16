from django.db import models
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from wagtail import blocks
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.fields import StreamField
from wagtail.models import Page, Orderable

from wagtail.images.blocks import ImageChooserBlock

from modelcluster.fields import ParentalKey
from utils.models import (
    UtilsCodeBlock,
    UtilsResultBlock,
    UtilsCustomRichTextBlock,
    UtilsVideoBlock,
)


class ProjectPageCategories(Orderable):
    page = ParentalKey("project.ProjectPage", related_name="categories")
    project = models.ForeignKey(
        "utils.UtilsCategory",
        on_delete=models.CASCADE,
    )

    panels = [
        FieldPanel("project"),
    ]


class ProjectIndexPage(Page):
    max_count = 1
    subpage_types = ["project.ProjectPage"]
    parent_page_types = ["home.HomePage"]

    summary = models.TextField(blank=True, max_length=500)

    content_panels = Page.content_panels + [
        FieldPanel("summary"),
    ]

    def get_context(self, request):
        context = super().get_context(request)

        posts = (
            ProjectPage.objects.live().public().order_by("-first_published_at")
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


class ProjectPage(Page):
    parent_page_types = ["project.ProjectIndexPage"]

    summary = models.TextField(blank=True, max_length=500)
    reading_time_in_minutes = models.IntegerField()
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
                "video_block",
                UtilsVideoBlock(
                    template="blocks/video_block.html",
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
        InlinePanel("categories", label="Categories"),
        FieldPanel("reading_time_in_minutes"),
        FieldPanel("summary"),
        FieldPanel("body"),
    ]
