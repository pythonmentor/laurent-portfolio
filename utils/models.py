from django.db import models
from wagtail import blocks
from wagtail.snippets.models import register_snippet


class UtilsCodeBlock(blocks.StructBlock):
    language = blocks.ChoiceBlock(
        choices=[
            ("python", "Python"),
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
class Category(models.Model):
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
