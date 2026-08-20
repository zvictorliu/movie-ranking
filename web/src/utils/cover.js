const DEFAULT_COVER = '/imgs/default_cover.jpg'

export function deriveThumbUrl(originalUrl, size) {
  if (!originalUrl || size === 'original') {
    return originalUrl || DEFAULT_COVER
  }
  if (originalUrl.includes('default_cover') || originalUrl.includes('/thumbs/')) {
    return originalUrl
  }
  const lastSlash = originalUrl.lastIndexOf('/')
  if (lastSlash < 0) {
    return originalUrl
  }
  const dir = originalUrl.slice(0, lastSlash)
  const filename = originalUrl.slice(lastSlash + 1)
  const stem = filename.replace(/\.[^.]+$/, '')
  return `${dir}/thumbs/${size}/${stem}.webp`
}

function pickCover(item, size) {
  if (!item) {
    return DEFAULT_COVER
  }
  if (item.covers?.[size]) {
    return item.covers[size]
  }
  if (size === 'original') {
    return item.cover || DEFAULT_COVER
  }
  if (item.cover) {
    return deriveThumbUrl(item.cover, size)
  }
  return DEFAULT_COVER
}

export function movieCover(movie, size = 'original') {
  return pickCover(movie, size)
}

export function actorCover(actor, size = 'small') {
  return pickCover(actor, size)
}
