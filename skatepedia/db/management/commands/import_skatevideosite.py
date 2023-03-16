#!/usr/bin/python
"""See scripts/skatevideosite.py"""
import os
import json
import os.path

from django.core.management.base import BaseCommand

from skatepedia.db.models import (
    Clip,
    Track,
    Video,
    Skater,
    Company,
    Filmmaker,
    Soundtrack,
    VideoCategory
)


def is_dir(path):
    if not os.path.isdir(path):
        raise argparse.ArgumentTypeError(f"{path} is not a valid directory path")
    return os.path.abspath(path)


def get_or_create_video_rels(video):
    rels = {"skaters": [], "filmmakers": [], "companies": []}
    category = video.get("category", {})

    if category:
        cat, created = VideoCategory.objects.get_or_create(
            skatevideosite_id=category["id"], name=category["name"]
        )
        rels["category"] = cat.pk

    for filmmaker in video.get("filmmakers", []):
        filmmaker, created = Filmmaker.objects.get_or_create(
            skatevideosite_id=filmmaker["id"], name=filmmaker["name"]
        )
        rels["filmmakers"].append(filmmaker.pk)

    for skater in video.get("skaters", []):
        skater, created = Skater.objects.get_or_create(
            skatevideosite_id=skater["id"], name=skater["name"]
        )
        rels["skaters"].append(skater.pk)

    for company in video.get("companies", []):
        company, created = Company.objects.get_or_create(
            skatevideosite_id=company["id"], name=company["name"]
        )
        rels["company"] = company.pk

    return rels


def get_or_create(model, skatevideosite_id, data):
    obj = model.objects.filter(skatevideosite_id=skatevideosite_id).first()
    created = False
    if obj is None:
        obj = model.objects.create(skatevideosite_id=skatevideosite_id, **data)
        created = True
    return obj, created


def bulk_video(video):
    relationships = get_or_create_video_rels(video)
    data = {
        "title": video["title"],
        "slug": video["slug"],
        "description": video.get("description"),
        "year": video.get("year"),
        "runtime": video.get("time"),
        "videolink": video.get("videolink"),
        "date": video.get("date"),
        "links": video.get("links"),
        "is_active": video.get("is_active"),
        "external_url": f"https://www.skatevideosite.com/videos/{video['slug']}",
        "image": video.get("image_url"),
        "category_id": relationships.get("category"),
        "company_id": relationships.get("company"),
    }
    obj, created = get_or_create(Video, video["id"], data)

    if skaters := relationships.get("skaters"):
        obj.skaters.add(*skaters)

    if filmmakers := relationships.get("filmmakers"):
        obj.filmmakers.add(*filmmakers)


class Command(BaseCommand):
    help = "Import Skatevideosite JSONs into SQL"

    def add_arguments(self, parser):
        parser.add_argument(
            "source",
            type=is_dir,
            help="Path to the folder containing the skatevideosite videos API paged and stored as JSONs",
        )

    def load_page(self, filename):
        with open(filename, "r") as f:
            videos = json.load(f)

        for video in videos:
            try:
                bulk_video(video)
            except Exception as exc:
                print(f"Error: in file {filename }, bulking video {video['slug']}", exc)
            else:
                print("Bulked video", video["slug"])

    def handle(self, *args, **options):
        files = (
            os.path.join(options["source"], filename)
            for filename in os.listdir(options["source"])
            if filename.endswith(".json")
        )

        for filename in files:
            self.load_page(filename)
