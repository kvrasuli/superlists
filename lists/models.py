from django.db import models

class List(models.Model):
    '''список'''
    pass

class Item(models.Model):
    '''элемент списка'''
    text = models.TextField(default='')
    list = models.ForeignKey(List, on_delete=models.DO_NOTHING, default=None)
    # list = models.TextField(default='')


