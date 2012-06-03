from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.forms import fields, ValidationError

from puzzle_captcha.models import Puzzle
from puzzle_captcha.widgets import PuzzleCaptchaInput

class PuzzleCaptchaField(fields.Field):
    widget = PuzzleCaptchaInput
    default_error_messages = {
        'invalid': _('You did not get the puzzle right.'),
    }

    def to_python(self, value):
        return value.split(',')

    def validate(self, values):
        try:
            puzzle = Puzzle.objects.get(key=values[0])
            pieces = dict(puzzle.puzzlepiece_set.values_list('key', 'order'))
            for order,key in enumerate(values[1:]):
                if pieces[key] != order+1:
                    raise ValidationError(self.default_error_messages['invalid'])
            return True
        except Puzzle.DoesNotExist:
            raise ValidationError(self.default_error_messages['invalid'])
