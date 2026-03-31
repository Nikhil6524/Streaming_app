import { useRef, useState } from "react"
import { useVideos } from "../hooks/useUpload"

type Props = {
  refreshKey?: number
}

type VideoItem = {
  id: string
  title: string
  url: string
  quality_urls?: Record<string, string>
}

const VideoList = ({ refreshKey = 0 }: Props) => {
  const { videos } = useVideos(refreshKey)
  const [selectedQualityById, setSelectedQualityById] = useState<Record<string, string>>({})
  const [loadedResolutionById, setLoadedResolutionById] = useState<Record<string, string>>({})
  const seekTimeByIdRef = useRef<Record<string, number>>({})

  const getVideoSource = (video: VideoItem, quality: string) => {
    if (video.quality_urls && video.quality_urls[quality]) {
      return video.quality_urls[quality]
    }

    return video.url
  }

  return (
    <div>
      <h2>Videos</h2>

      {videos.map((video: VideoItem) => (
        <div key={video.id} style={{ marginBottom: "20px" }}>
          <p>{video.title}</p>

          {(() => {
            const selectedQuality = selectedQualityById[video.id] || "720p"
            const sourceUrl = getVideoSource(video, selectedQuality)

            return (
              <>
                <label style={{ display: "block", marginBottom: "8px" }}>
                  Quality:&nbsp;
                  <select
                    value={selectedQuality}
                    onChange={(e) => {
                      const videoEl = document.getElementById(`video-${video.id}`) as HTMLVideoElement | null
                      if (videoEl) {
                        seekTimeByIdRef.current[video.id] = videoEl.currentTime || 0
                      }

                      setSelectedQualityById((prev) => ({
                        ...prev,
                        [video.id]: e.target.value,
                      }))
                    }}
                  >
                    <option value="360p">360p</option>
                    <option value="480p">480p</option>
                    <option value="720p">720p</option>
                  </select>
                </label>

                <div style={{ fontSize: "0.82rem", color: "#9ca3af", marginBottom: "8px" }}>
                  Selected: {selectedQuality} | Loaded: {loadedResolutionById[video.id] || "loading..."}
                </div>

                <video
                  key={sourceUrl}
                  id={`video-${video.id}`}
                  width="760"
                  style={{ maxWidth: "100%", borderRadius: "10px", background: "#000" }}
                  controls
                  onLoadedMetadata={(e) => {
                    const el = e.currentTarget
                    setLoadedResolutionById((prev) => ({
                      ...prev,
                      [video.id]: `${el.videoWidth}x${el.videoHeight}`,
                    }))

                    const seekTo = seekTimeByIdRef.current[video.id]
                    if (typeof seekTo === "number" && seekTo > 0 && !Number.isNaN(seekTo)) {
                      try {
                        el.currentTime = seekTo
                      } catch {
                        // Ignore if browser blocks seek at this stage.
                      }
                    }
                  }}
                >
                  <source src={sourceUrl} type="video/mp4" />
                </video>
              </>
            )
          })()}
        </div>
      ))}
    </div>
  )
}

export default VideoList