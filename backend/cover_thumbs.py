"""Movie-cover thumbnail generation (small / medium WebP)."""

import os

from PIL import Image, ImageOps

DEFAULT_COVER_URL = '/imgs/default_cover.jpg'
THUMBS_DIRNAME = 'thumbs'
THUMB_EXT = '.webp'
THUMB_FORMAT = 'WEBP'
IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif', '.webp'}

THUMB_SIZES = {
    'small': {'max_edge': 480, 'quality': 75},
    'medium': {'max_edge': 960, 'quality': 82},
}


def thumb_filename(original_filename):
    stem, _ = os.path.splitext(original_filename)
    return f'{stem}{THUMB_EXT}'


def thumb_path(original_path, size):
    cover_dir = os.path.dirname(original_path)
    filename = os.path.basename(original_path)
    return os.path.join(cover_dir, THUMBS_DIRNAME, size, thumb_filename(filename))


def is_default_cover(url):
    return not url or 'default_cover' in url


def thumb_url(original_url, size):
    if is_default_cover(original_url) or size == 'original':
        return original_url
    if f'/{THUMBS_DIRNAME}/' in original_url:
        return original_url
    dirname, filename = original_url.rsplit('/', 1)
    return f'{dirname}/{THUMBS_DIRNAME}/{size}/{thumb_filename(filename)}'


def cover_variant_urls(original_url):
    if is_default_cover(original_url):
        url = original_url or DEFAULT_COVER_URL
        return {'original': url, 'small': url, 'medium': url}
    return {
        'original': original_url,
        'small': thumb_url(original_url, 'small'),
        'medium': thumb_url(original_url, 'medium'),
    }


def _to_rgb(img):
    if img.mode == 'RGB':
        return img
    if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
        rgba = img.convert('RGBA')
        background = Image.new('RGB', rgba.size, (255, 255, 255))
        background.paste(rgba, mask=rgba.split()[-1])
        return background
    return img.convert('RGB')


def _load_still(path):
    with Image.open(path) as img:
        img = ImageOps.exif_transpose(img) or img
        if getattr(img, 'n_frames', 1) > 1:
            img.seek(0)
        return _to_rgb(img).copy()


def generate_thumbs(original_path, force=False, dry_run=False):
    """Create small/medium WebP thumbs beside an original cover.

    Returns a dict of {size: dest_path} for written or already-present files.
    """
    results = {}
    img = None
    for size, spec in THUMB_SIZES.items():
        dest = thumb_path(original_path, size)
        if not force and os.path.exists(dest):
            results[size] = dest
            continue
        if dry_run:
            results[size] = dest
            continue
        if img is None:
            img = _load_still(original_path)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        thumb = img.copy()
        thumb.thumbnail((spec['max_edge'], spec['max_edge']), Image.Resampling.LANCZOS)
        thumb.save(
            dest,
            format=THUMB_FORMAT,
            quality=spec['quality'],
            method=4,
        )
        results[size] = dest
    return results


def save_movie_cover(file_storage, dest_dir, filename):
    """Persist the original cover, then generate both thumbnail grades."""
    os.makedirs(dest_dir, exist_ok=True)
    original_path = os.path.join(dest_dir, filename)
    file_storage.save(original_path)
    generate_thumbs(original_path, force=True)
    return original_path


def iter_original_covers(cover_dir):
    if not os.path.isdir(cover_dir):
        return
    for name in sorted(os.listdir(cover_dir)):
        if name == THUMBS_DIRNAME:
            continue
        path = os.path.join(cover_dir, name)
        if not os.path.isfile(path):
            continue
        ext = os.path.splitext(name)[1].lower()
        if ext not in IMAGE_EXTENSIONS:
            continue
        yield path
