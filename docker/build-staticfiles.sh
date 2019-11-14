#!/usr/bin/env bash

set -eu

export DJANGO_SETTINGS_MODULE=smasu.settings.build_staticfiles
python /home/user/code/manage.py collectstatic --noinput -v 0

shopt -s extglob

# cd /staticfiles
# find -name '*.less' -delete
# find -name '*.less.gz' -delete
# rm -rf history.js/vendor jquery/src numeral/!(min)
# rm -rf bootstrap/!(dist) nifty/datatables/extensions/!(Responsive)
# rm -rf nifty/datatables/media/js/jquery.dataTables.js*
# rm -rf ts-test
# rm -f *.ts.js.gz
