from django.db import models
from wagtail import blocks
from wagtail.snippets.models import register_snippet
from wagtail.embeds.blocks import EmbedBlock
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.images.blocks import ImageChooserBlock


class UtilsCodeBlock(blocks.StructBlock):
    language = blocks.ChoiceBlock(
        choices=[
            ("python", "Python"),
            ("css", "CSS"),
            ("html", "HTML"),
            ("javascript", "Javascript"),
            ("shell", "Shell"),
        ],
        label="Language code",
        default="python",
    )
    code = blocks.TextBlock(label="Source code")

    class Meta:
        template = "blocks/code_block.html"
        icon = "code_block"
        label = "Code block"


class UtilsResultBlock(blocks.TextBlock):
    class Meta:
        template = "blocks/result_block.html"
        icon = "doc-full-inverse"
        label = "Result block"


@register_snippet
class UtilsCategory(models.Model):
    name = models.CharField(max_length=255)
    color = models.CharField(
        choices=[
            ("blue", "Blue"),
            ("green", "Green"),
            ("yellow", "Yellow"),
            ("grey", "Grey"),
            ("red", "Red"),
            ("purple", "Purple"),
            ("orange", "Orange"),
            ("pink", "Pink"),
            ("black", "Black"),
            ("white", "White"),
            ("brown", "Brown"),
            ("teal", "Teal"),
            ("cyan", "Cyan"),
            ("lime", "Lime"),
            ("amber", "Amber"),
        ],
        help_text="Background color",
        default="grey",
        max_length=6,
    )

    @property
    def text_color(self):
        if self.color == "grey":
            return "blue-dark"
        elif self.color == "yellow":
            return "yellow-dark"
        return self.color

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class UtilsVideoBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=False)
    video_url = EmbedBlock(required=False)
    video_file = DocumentChooserBlock(required=False)
    poster_image = ImageChooserBlock(required=False)

    class Meta:
        template = "blocks/video_block.html"
        icon = "media"
        label = "Vidéo"


class UtilsCustomRichTextBlock(blocks.RichTextBlock):
    def __init__(self, **kwargs):
        default_features = [
            "bold",
            "italic",
            "link",
            "document-link",
            "ol",
            "ul",
            "hr",
            "h1",
            "h2",
            "h3",
            "center",
            "justify",
        ]
        kwargs.setdefault("features", default_features)
        kwargs.setdefault("template", "blocks/richtext.html")
        super().__init__(**kwargs)
