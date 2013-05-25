from django.core.management.base import BaseCommand, CommandError
from macadjan_ecozoom.models import EcozoomEntity

class Command(BaseCommand):
    args = ''
    help = 'Export basic info of all active entities to entities.csv'

    def handle(self, *args, **options):

        csv_file = open('entities.csv', 'w')

        for entity in EcozoomEntity.objects_active.all():
            line = u'%d,%s,%s,%s,%s\n' % (
                entity.id,
                entity.name,
                entity.email,
                entity.web,
                entity.main_subcategory.name,
            )
            csv_file.write(line.encode('utf-8'))

        csv_file.close()

