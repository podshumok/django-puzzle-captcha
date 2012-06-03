import Image
import hashlib
import datetime
import random
from cStringIO import StringIO

from django.db import models
from django import forms
from django.db.models.fields.files import ImageFieldFile, FileField
from django.core.files import File
from django.core.files.uploadedfile import InMemoryUploadedFile

class Puzzle(models.Model):
    key = models.CharField(max_length=255, default='', unique=True, primary_key=True)
    rows = models.IntegerField(default=0, blank=True)
    cols = models.IntegerField(default=0, blank=True)
    image = models.ImageField(upload_to='originals', null=True)
    
    def save(self, *args, **kwargs):
        super(Puzzle, self).save(*args, **kwargs)
        self.puzzlepiece_set.all().delete()
        self.create_pieces()
        super(Puzzle, self).save(*args, **kwargs)
      
    def create_pieces(self):
        image = Image.open(self.image.file)
        image.thumbnail((400, 400), Image.ANTIALIAS)
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
                #f = piece.image.storage.open(filename)
                f = InMemoryUploadedFile(subimage_io, None, filename, 'image/jpg', 0, None)
                piece.image.save(filename, f, save=True)
                piece.save()

    def delete(self):
        for q in self.puzzlepiece_set.all():
            q.delete()
        self.image.delete(False)
        try:
            super(Puzzle, self).delete()
        except TypeError:
            pass

    def get_random_pieces(self):
        pieces = [piece for piece in self.puzzlepiece_set.all()]
        random.shuffle(pieces)        
        return pieces
        
class PuzzlePiece(models.Model):
    key = models.CharField(max_length=255, primary_key=True)
    image = models.ImageField(upload_to='pieces')
    puzzle = models.ForeignKey(Puzzle)
    order = models.IntegerField()

    def delete(self):
        self.image.delete(False)
        super(PuzzlePiece, self).delete()
