import { useVideos } from "../hooks/useUpload"

const VideoList = () => {
  const { videos } = useVideos()

  return (
    <div>
      <h2>Videos</h2>

      {videos.map((video) => (
        <div key={video.id} style={{ marginBottom: "20px" }}>
          <p>{video.title}</p>

          <video width="400" controls>
            <source src={video.url} type="video/mp4" />
          </video>
        </div>
      ))}
    </div>
  )
}

export default VideoList