import os

from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Creates ctags file for all js and py files"

    requires_model_validation = False
    can_import_settings = False

    def handle(self, *args, **options):
        ctags = None
        for ct in ('ctags', 'ctags-exuberant'):
            if os.system('which %s' % ct) == 0:
                ctags = ct
                break

        if ctags == None:
            raise Exception("Ctags not found")

        opts = "--language-force=python -L -"

        os.system('find ./ -regextype posix-extended -iregex ".*py$" | %s %s' % \
                (ctags, opts))

