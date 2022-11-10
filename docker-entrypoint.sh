#!/bin/sh

flask db upgrade

exec gunicorn "app:create_app()"