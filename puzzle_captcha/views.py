from django.shortcuts import get_object_or_404

from filetransfers.api import serve_file

from puzzle_captcha.models import Puzzle, PuzzlePiece

def download_handler_piece(request, pk):
    piece = get_object_or_404(PuzzlePiece, pk=pk)
    return serve_file(request, piece.image, save_as=False)

def download_handler_thumb(request, key):
    puzzle = get_object_or_404(Puzzle, key=key)
    return serve_file(request, puzzle.thumb, save_as=False)
