#!/bin/bash

gunicorn --workers=5 --threads=1 -b 0.0.0.0:8050 --log-level=debug app:server --reload