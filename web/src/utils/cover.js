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

export function movieCover(movie, size = 'original') {
  if (!movie) {
    return DEFAULT_COVER
  }
  if (movie.covers?.[size]) {
    return movie.covers[size]
  }
  if (size === 'original') {
    return movie.cover || DEFAULT_COVER
  }
  if (movie.cover) {
    return deriveThumbUrl(movie.cover, size)
  }
  return DEFAULT_COVER
}
