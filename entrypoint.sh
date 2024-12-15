#!/bin/sh
set -e

echo "Replacing supervisord.conf"
cp setup/main_supervisord.conf /etc/supervisor/supervisord.conf || exit 1

echo "Copying supervisor gunicorn conf"
cp setup/gunicorn.conf /etc/supervisor/conf.d/ || exit 1

exec supervisord -c /etc/supervisor/supervisord.conf
