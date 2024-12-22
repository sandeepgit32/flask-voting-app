#!/bin/bash

set -e

echo "Starting Gunicorn server..."
gunicorn wsgi:app --bind 0.0.0.0:5000 --timeout 900 || {
    echo "Failed to start Gunicorn server"
    exit 1
}