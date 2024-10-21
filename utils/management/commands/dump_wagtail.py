import sys
from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Dump the database into a JSON file with UTF-8 encoding and specific options'

    def handle(self, *args, **kwargs):
        # Ouvrir un fichier de sortie avec l'encodage UTF-8
        with open('data.json', 'w', encoding='utf-8') as outfile:
            # Rediriger la sortie standard vers ce fichier
            sys.stdout = outfile
            # Exécuter la commande dumpdata avec les options spécifiques
            call_command(
                'dumpdata',
                '--natural-foreign', 
                '--indent', '2', 
                '-e', 'contenttypes', 
                '-e', 'sessions', 
                '-e', 'auth.permission', 
                '-e', 'wagtailsearch', 
                '-e', 'wagtailcore.groupcollectionpermission', 
                '-e', 'wagtailcore.grouppagepermission', 
                '-e', 'wagtailimages.rendition'
            )
        # Réinitialiser sys.stdout pour éviter tout conflit avec d'autres commandes
        sys.stdout = sys.__stdout__
        self.stdout.write(self.style.SUCCESS('Data successfully dumped to data.json in UTF-8 encoding.'))