#!/bin/sh

exec gunicorn "app:create_app()"