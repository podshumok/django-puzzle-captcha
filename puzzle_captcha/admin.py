from django.contrib import admin
from puzzle_captcha.models import Puzzle, PuzzlePiece

class PuzzlePieceInline(admin.StackedInline):
    model = PuzzlePiece
    readonly_fields = ('admin_preview', 'key', 'image', 'order')
    can_delete = False
    extra = 0

class PuzzleAdmin(admin.ModelAdmin):
    list_display = ('admin_preview', 'ready', 'key', 'rows', 'cols')
    readonly_fields = ('key', 'rows', 'cols', 'thumb', 'ready')
    class Meta:
        model = Puzzle
    inlines = [
        PuzzlePieceInline,
    ]
    
admin.site.register(Puzzle, PuzzleAdmin)

