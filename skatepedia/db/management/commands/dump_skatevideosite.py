#!/usr/bin/python
"""See scripts/skatevideosite.py"""
import json
import asyncio
import os.path
from dataclasses import dataclass

import aiohttp
import requests

from django.core.management.base import BaseCommand, CommandError

from skatepedia.db.models import (
    Clip,
    Track,
    Video,
    Skater,
    Company,
    Filmmaker,
    Soundtrack
)


class Command(BaseCommand):
    help = "Dump Skatevideosite JSONs into SQL"

    def add_arguments(self, parser):
        parser.add_argument(
            "--source",
            type=int,
            nargs="+",
            help="Folder containing JSON files for each skatevideosite videos API page",
        )

    def handle(self, *args, **options):
        pass
