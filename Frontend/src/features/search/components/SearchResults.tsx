import { useEffect, useRef } from "react"
import Hls from "hls.js"
import type { SearchVideo } from "../services/searchService"

type PlayerProps = {
  hlsUrl?: string | null
  fallbackUrl?: string | null
}

const SearchVideoPlayer = ({ hlsUrl, fallbackUrl }: PlayerProps) => {
  const videoRef = useRef<HTMLVideoElement | null>(null)

  useEffect(() => {
    const video = videoRef.current
    if (!video) return

    let hls: Hls | null = null

    const switchToFallback = () => {
      if (fallbackUrl && video.src !== fallbackUrl) {
        video.src = fallbackUrl
      }
    }

    if (hlsUrl && Hls.isSupported()) {
      hls = new Hls()
      hls.on(Hls.Events.ERROR, (_, data) => {
        if (data.fatal) {
          hls?.destroy()
          hls = null
          switchToFallback()
        }
      })
      hls.loadSource(hlsUrl)
      hls.attachMedia(video)
    } else if (hlsUrl && video.canPlayType("application/vnd.apple.mpegurl")) {
      video.src = hlsUrl
      video.onerror = () => switchToFallback()
    } else if (fallbackUrl) {
      video.src = fallbackUrl
    }

    return () => {
      video.onerror = null
      if (hls) {
        hls.destroy()
      }
    }
  }, [hlsUrl, fallbackUrl])

  return (
    <video
      ref={videoRef}
      controls
      width={760}
      style={{ maxWidth: "100%", borderRadius: "10px", background: "#000" }}
    />
  )
}

type Props = {
  results: SearchVideo[]
  loading: boolean
  error: string | null
  query: string
}

const SearchResults = ({ results, loading, error, query }: Props) => {
  if (!query.trim()) {
    return null
  }

  if (loading) {
    return <p style={{ color: "#93c5fd", marginTop: "10px" }}>Searching...</p>
  }

  if (error) {
    return <p style={{ color: "#fca5a5", marginTop: "10px" }}>{error}</p>
  }

  if (!results.length) {
    return <p style={{ color: "#94a3b8", marginTop: "10px" }}>No videos found.</p>
  }

  return (
    <div style={{ marginTop: "12px", display: "grid", gap: "18px" }}>
      {results.map((video) => (
        <div
          key={video.id}
          style={{
            border: "1px solid #1f2937",
            borderRadius: "14px",
            padding: "12px",
            background: "rgba(2, 6, 23, 0.55)",
          }}
        >
          <p style={{ marginBottom: "8px", fontWeight: 600 }}>{video.title}</p>
          <SearchVideoPlayer hlsUrl={video.hls_url} fallbackUrl={video.url} />
          <p style={{ fontSize: "0.8rem", color: "#94a3b8", marginTop: "8px" }}>
            Source: {video.hls_url ? "HLS" : "MP4"}
          </p>
        </div>
      ))}
    </div>
  )
}

export default SearchResults
