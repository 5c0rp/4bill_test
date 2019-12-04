#!/bin/sh

gunicorn app:app --bind :5000