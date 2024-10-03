from django.db import models

from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.admin.panels import FieldPanel


class CodeBlock(blocks.StructBlock):
    language = blocks.ChoiceBlock(
        choices=[
            ("python", "Python"),
            ("shell", "Shell"),
        ],
        label="Language code",
    )
    code = blocks.TextBlock(label="Source code")

    class Meta:
        template = "blocks/code_block.html"
        icon = "code_block"
        label = "Code block"


class ResultBlock(blocks.TextBlock):
    class Meta:
        template = "blocks/result_block.html"
        icon = "doc-full-inverse"
        label = "Result block"


class MiscPage(Page):

    html_subtitle = models.TextField(
        max_length=2000,
        blank=True,
        help_text="This can include Raw HTML. Be careful!",
    )

    body = StreamField(
        [
            (
                "content",
                blocks.RichTextBlock(
                    features=[
                        "bold",
                        "italic",
                        "link",
                        "ol",
                        "ul",
                        "hr",
                        "h1",
                        "h2",
                        "h3",
                    ],
                    template="blocks/richtext.html",
                ),
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
                        ("author", blocks.CharBlock()),
                    ],
                    template="blocks/twitter_block.html",
                ),
            ),
            (
                "code_block",
                CodeBlock(),
            ),
            (
                "result_block",
                ResultBlock(),
            ),
        ]
    )

    content_panels = Page.content_panels + [
        FieldPanel("html_subtitle"),
        FieldPanel("body"),
    ]
