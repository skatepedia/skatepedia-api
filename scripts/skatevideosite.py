#!/usr/bin/python3
"""Parse skatevideosite.com API to get all the skate videos info

Usage:

>>> python skatevideosite.py --pages 11 12 13
>>> python skatevideosite.py --from_page 50
>>> python skatevideosite.py  # fetch all

- Page videos API, in a synchronous manner otherwise the server refuses some connections.
- Get details for each video in the page (asynchronously)
- Dump each page videos in JSON (videos_{page_number}.json)
"""
import json
import time
import asyncio
import os.path
import argparse
from datetime import datetime
from dataclasses import dataclass

import aiohttp
import requests

VIDEOS_API_URL = (
    "https://www.skatevideosite.com/api/videos?sort=date-descending&page={page}"
)


async def get_video_details(client, slug: str, videos: list):
    url = f"https://www.skatevideosite.com/api/videos/{slug}"
    async with client.get(url) as resp:
        content = await resp.json()
        try:
            video = content["data"]
            videos.append(video)
        except Exception as exc:
            print(f"Error processing video page {slug}", exc)


async def get_videos(page: int):
    start = time.time()
    videos = []
    async with aiohttp.ClientSession() as session:
        async with session.get(VIDEOS_API_URL.format(page=page)) as resp:
            content = await resp.json()
            video_tasks = (
                get_video_details(session, video["slug"], videos)
                for video in content.get("data", [])
            )
            await asyncio.gather(*video_tasks)

    with open(f"videos_{page}.json", "w") as _f:
        json.dump(videos, _f)

    print(
        f"Page {page} with {len(videos)} processed in {time.time() - start}s",
    )


def get_page_count():
    response = requests.get(VIDEOS_API_URL.format(page=1))
    page_count = response.json()["meta"]["page_count"] + 1
    return page_count


async def main(from_page=1, pages=None, archive=False):
    start = time.time()
    if pages is None:
        page_count = get_page_count()
        pages = range(from_page, page_count)

    print(f"Pages to process: {pages}")
    for page in pages:
        await get_videos(page)

    print("Total processing time  {time.time() - start}s")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Dump skatevideosite API videos.")
    parser.add_argument(
        "--pages",
        type=int,
        nargs="+",
        help="Get specific page results. Specify page numbers",
    )
    parser.add_argument(
        "--from_page",
        type=int,
        nargs="?",
        default=1,
        help="Start getting data from a specific page. Specify page number",
    )

    args = parser.parse_args()
    asyncio.run(main(from_page=args.from_page, pages=args.pages, archive=args.archive))
