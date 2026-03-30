import { useState } from "react"
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
                    onChange={(e) =>
                      setSelectedQualityById((prev) => ({
                        ...prev,
                        [video.id]: e.target.value,
                      }))
                    }
                  >
                    <option value="360p">360p</option>
                    <option value="480p">480p</option>
                    <option value="720p">720p</option>
                  </select>
                </label>

                <video key={sourceUrl} width="400" controls>
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