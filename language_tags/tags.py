# -*- coding: utf-8 -*-
from language_tags.Subtag import Subtag
from language_tags.Tag import Tag

def check(tag):
    return Tag(tag).valid()