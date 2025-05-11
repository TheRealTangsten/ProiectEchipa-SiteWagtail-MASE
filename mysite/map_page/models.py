from django.db import models

from wagtail.models import Page
from wagtail.fields import RichTextField

from wagtail.embeds.blocks import EmbedBlock

class MapPage(Page):
    body = RichTextField(blank=True)
    field2 = RichTextField(blank=True)     
    content_panels = Page.content_panels + ["body","field2"]




