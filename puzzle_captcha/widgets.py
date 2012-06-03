import random
from django.forms import widgets
from django.template import Context
from django.template.loader import render_to_string

from models import Puzzle

class PuzzleCaptchaInput(widgets.Widget):
    def render(self, name, value, attrs = None):
        puzzle = random.choice(Puzzle.objects.all())
        width = puzzle.puzzlepiece_set.all()[0].image.width
        width = puzzle.cols * (4+width)

        return render_to_string('puzzle/widget.html',
            Context({'name':name, 'puzzle':puzzle, 'width':width}))

    class Media:
        css = {'puzzle':('captcha/puzzle.css',)}
        js = {'puzzle':('captcha/puzzle.js',)}
