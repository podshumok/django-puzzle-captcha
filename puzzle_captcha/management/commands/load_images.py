import os
from django.core.management.base import BaseCommand, CommandError
from django.core.files import File
from puzzle_captcha.models import Puzzle

class Command(BaseCommand):
    args = '<path_to_images_folder ...>'
    help = 'Loads all the images from the folder specified into the Puzzle Captcha library'

    def handle(self, *args, **options):
        if args:
            path = args[0]
            files = os.listdir(path)
            for filename in files:
                print "Loading %s..." % filename
                create_puzzle(path, filename)
  
        else:
            raise CommandError('Please provide a valid path to the folder that contains your images.')    
        
        
                    
def create_puzzle(directory, filename):
    puzzle = Puzzle(key='')
    try:
        full_file_path = os.path.join(directory, filename)
        image = open(full_file_path, 'rb')
        puzzle = Puzzle(image=File(image))
        puzzle.save()

    except Exception as ex:
        if puzzle.id:
            puzzle.delete()
        print ex

