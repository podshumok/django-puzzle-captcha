import Image
import hashlib
import datetime
import random
from cStringIO import StringIO

from django.conf import settings
from django.db import models
from django import forms
from django.db.models.fields.files import ImageFieldFile, FileField
from django.core.files import File
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

THUMB_SIZE_PUZZLE = getattr(settings, 'PUZZLE_CAPTCHA_THUMB_PUZZLE', (400,400))
THUMB_SIZE_ADMIN  = getattr(settings, 'PUZZLE_CAPTCHA_THUMB_ADMIN', (100,100))


class Puzzle(models.Model):
    key = models.CharField(max_length=255, blank=True, default='', db_index=True)
    rows = models.IntegerField(default=0, blank=True)
    cols = models.IntegerField(default=0, blank=True)
    image = models.ImageField(upload_to='originals', null=True)
    thumb = models.ImageField(upload_to='thumbs', null=True)
    ready = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        super(Puzzle, self).save(*args, **kwargs)
        self.puzzlepiece_set.all().delete()
        self.create_pieces()
        self.ready = True
        super(Puzzle, self).save(*args, **kwargs)

    def delete(self):
        for q in self.puzzlepiece_set.all():
            q.delete()
        try:
            self.image.delete(False)
        except AttributeError:
            pass
        try:
            self.thumb.delete(False)
        except AttributeError:
            pass
        try:
            if self.id is not None:
                super(Puzzle, self).delete()
        except TypeError:
            pass

    def create_pieces(self):
        image = Image.open(self.image.file)
        image.thumbnail(THUMB_SIZE_PUZZLE, Image.ANTIALIAS)
        self.key = hashlib.sha1(image.tostring()+str(datetime.datetime.now())).hexdigest()
        cols,rows = random.choice(((1,6), (6,1), (2,3), (3,2), (3,3), (2,4), (4,2)))
        self.cols = cols
        self.rows = rows
        horizontal_cell_size = image.size[0]/cols
        vertical_cell_size = image.size[1]/rows
        looper = 0
        for row in range(rows):
            for col in range(cols):
                region = (horizontal_cell_size * col, vertical_cell_size * row,
                    horizontal_cell_size * (col+1), vertical_cell_size * (row+1))
                subimage = image.crop(region)
                subimage_io = StringIO()
                subimage.save(subimage_io, 'JPEG')
                subimage_io.seek(0)
                key = hashlib.sha1(subimage.tostring()+str(datetime.datetime.now())).hexdigest()
                looper += 1
                piece = PuzzlePiece(key=key, order=looper, puzzle=self)
                filename = '%s.jpg' % key
                f = InMemoryUploadedFile(subimage_io, None, filename, 'image/jpg', 0, None)
                piece.image.save(filename, f, save=True)
                piece.save()
        image.thumbnail(THUMB_SIZE_ADMIN, Image.ANTIALIAS)
        filename = '%s.jpg' % self.key
        io = StringIO()
        image.save(io, 'JPEG')
        io.seek(0)
        f = InMemoryUploadedFile(io, None, filename, 'image/jpg', 0, None)
        self.thumb.save(filename, f, save=False)

    def get_random_pieces(self):
        pieces = [piece for piece in self.puzzlepiece_set.all()]
        random.shuffle(pieces)        
        return pieces

    def admin_preview(self):
        if self.thumb:
            return u'<img src="%s" />' % reverse('puzzle-thumb', args=[self.key])
        else:
            piece = random.choice(self.puzzlepiece_set.all())
            return piece.admin_preview();
    admin_preview.short_description = _('Thumb')
    admin_preview.allow_tags = True

class PuzzlePiece(models.Model):
    key = models.CharField(max_length=255, primary_key=True)
    image = models.ImageField(upload_to='pieces')
    puzzle = models.ForeignKey(Puzzle)
    order = models.IntegerField()

    def delete(self):
        self.image.delete(False)
        super(PuzzlePiece, self).delete()

    def admin_preview(self):
        if self.image:
            return u'<img src="%s" />' % reverse('puzzle-piece', args=[self.key])
        else:
            return _('(Picture)')
    admin_preview.short_description = _('Thumb')
    admin_preview.allow_tags = True
