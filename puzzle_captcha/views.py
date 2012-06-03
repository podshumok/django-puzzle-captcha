from django.shortcuts import get_object_or_404

from filetransfers.api import serve_file

from puzzle_captcha.models import Puzzle, PuzzlePiece

def download_handler(request, pk):
    piece = get_object_or_404(PuzzlePiece, pk=pk)
    return serve_file(request, piece.image, save_as=False)
