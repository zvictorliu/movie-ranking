#!/usr/bin/env python3
"""Backfill small WebP thumbnails for existing actor covers."""

import argparse
import os
import sys

BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO_ROOT = os.path.dirname(BACKEND_DIR)
sys.path.insert(0, BACKEND_DIR)

from cover_thumbs import (  # noqa: E402
    ACTOR_THUMB_SIZES,
    generate_thumbs,
    iter_original_covers,
    thumb_path,
)


def parse_args():
    parser = argparse.ArgumentParser(description='Generate actor-cover thumbnails')
    parser.add_argument(
        '--content-dir',
        default=os.path.join(REPO_ROOT, 'content'),
        help='Path to the content directory (default: <repo>/content)',
    )
    parser.add_argument(
        '--force',
        action='store_true',
        help='Regenerate thumbs even if they already exist',
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='List work without writing files',
    )
    return parser.parse_args()


def main():
    args = parse_args()
    cover_dir = os.path.join(args.content_dir, 'covers', 'actor-cover')
    if not os.path.isdir(cover_dir):
        print(f'Cover directory not found: {cover_dir}')
        return 1

    created = 0
    skipped = 0
    failed = 0
    originals = list(iter_original_covers(cover_dir))
    print(f'Found {len(originals)} original covers in {cover_dir}')

    for original_path in originals:
        name = os.path.basename(original_path)
        missing = [
            size
            for size in ACTOR_THUMB_SIZES
            if args.force or not os.path.exists(thumb_path(original_path, size))
        ]
        if not missing:
            skipped += 1
            continue
        try:
            generate_thumbs(
                original_path,
                force=args.force,
                dry_run=args.dry_run,
                sizes=ACTOR_THUMB_SIZES,
            )
            created += 1
            action = 'would generate' if args.dry_run else 'generated'
            print(f'  {action} {", ".join(missing)} for {name}')
        except Exception as exc:
            failed += 1
            print(f'  failed {name}: {exc}')

    print(
        f'Done. generated={created} skipped={skipped} failed={failed}'
        + (' (dry-run)' if args.dry_run else '')
    )
    return 1 if failed else 0


if __name__ == '__main__':
    raise SystemExit(main())
