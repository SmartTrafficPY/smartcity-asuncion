import decimal
import json
import sys

import ijson
from django.contrib.gis.geos import GEOSGeometry
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from splots.models import ParkingLot, ParkingSpot


class JSONEncoderWithDecimal(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super().default(o)


class Command(BaseCommand):
    help = "Load parking spots from a GeoJSON file"

    def add_arguments(self, parser):
        parser.add_argument(
            "lot_pk", metavar="LOT_PK", type=int, help="the primary key of the parking lot these spots correspond to"
        )
        parser.add_argument(
            "--ifile", metavar="INPUT_FILE", default=None, type=str, help="the GeoJSON input file (STDIN if ommitted)"
        )

    def read(self, fd, lot):
        lot_pk = lot.pk

        num_created = 0
        features = ijson.items(fd, "features.item")

        with transaction.atomic():
            ParkingSpot.objects.filter(lot=lot_pk).delete()

            for i, feature in enumerate(features):
                geom = GEOSGeometry(json.dumps(feature["geometry"], cls=JSONEncoderWithDecimal))

                if geom.geom_type == "MultiPolygon":
                    if geom.empty:
                        self.stdout.write(self.style.WARNING(f"{i}: ignoring empty multipolygon"))
                        continue
                    polygon = geom[0]

                elif geom.geom_type == "Polygon":
                    polygon = geom

                else:
                    self.stdout.write(self.style.WARNING(f"{i}: ignoring type: {geom.geom_type} feature"))
                    continue

                spot = ParkingSpot(lot=lot, polygon=polygon)
                spot.save()

                num_created += 1

        return num_created

    def handle(self, *args, **options):
        ifile = options["ifile"]
        lot_pk = options["lot_pk"]

        try:
            lot = ParkingLot.objects.get(pk=lot_pk)
        except ParkingLot.DoesNotExist:
            raise CommandError(f"ParkingLot(pk={lot_pk}) doesn't exist")

        if ifile is None:
            num_created = self.read(sys.stdin, lot)
        else:
            with open(ifile) as fd:
                num_created = self.read(fd, lot)

        self.stdout.write(self.style.SUCCESS(f"Successfully created {num_created} spots for ParkingLot(pk={lot_pk})"))
