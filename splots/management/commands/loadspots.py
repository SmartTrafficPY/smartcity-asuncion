import decimal
import json

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
        parser.add_argument("in_file", metavar="IN_FILE", type=str, help="the GeoJSON input file")
        parser.add_argument(
            "lot_pk", metavar="LOT_PK", type=int, help="the primary key of the parking lot these spots correspond to"
        )

    def handle(self, *args, **options):
        in_file = options["in_file"]
        lot_pk = options["lot_pk"]

        try:
            lot = ParkingLot.objects.get(pk=lot_pk)
        except ParkingLot.DoesNotExist:
            raise CommandError(f"ParkingLot(pk={lot_pk}) doesn't exist")

        num_created = 0

        with open(in_file) as fd:
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

        self.stdout.write(self.style.SUCCESS(f"Successfully created {num_created} spots for ParkingLot(pk={lot_pk})"))
