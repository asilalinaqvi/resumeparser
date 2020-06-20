from __future__ import unicode_literals# -*- coding: utf-8 -*-

from django.db import models

class CV(models.Model):
    name=models.CharField(max_length=250)
    father_name=models.CharField(max_length=250)

