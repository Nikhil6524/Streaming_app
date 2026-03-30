import { useState } from "react"
import LoginButton from "./features/auth/components/LoginButton"
import { useAuthContext } from "./features/auth/context/AuthContext"
import VideoList from "./features/video/componenets/VideoList"
import UploadChunkVideo from "./features/video/componenets/UploadChunkVideo"

const App = () => {
  const { user } = useAuthContext()
  const [videoRefreshKey, setVideoRefreshKey] = useState(0)

  const handleUploadSuccess = () => {
    setVideoRefreshKey((prev) => prev + 1)
  }

  return (
    <div
      style={{
        minHeight: "100vh",
        background:
          "radial-gradient(circle at top left, #1f2937 0, #020617 55%, #000000 100%)",
        color: "#e5e7eb",
        padding: "32px 16px",
        boxSizing: "border-box",
      }}
    >
      <div
        style={{
          maxWidth: "1040px",
          margin: "0 auto",
        }}
      >
      {!user ? (
        <>
          <h2 style={{ marginBottom: "16px" }}>Login</h2>
          <LoginButton />
        </>
      ) : (
        <>
          <h2 style={{ marginBottom: "8px" }}>Welcome {user.name}</h2>
          <p style={{ marginBottom: "24px", color: "#9ca3af" }}>
            Upload your videos and see them appear instantly in your feed.
          </p>

          {/*  Upload Section */}
          <div
            style={{
              display: "flex",
              flexWrap: "wrap",
              gap: "16px",
            }}
          >
            {/* <UploadVideo /> */}
            <UploadChunkVideo onUploadSuccess={handleUploadSuccess} />
          </div>

          {/*  Video Feed */}
          <div style={{ marginTop: "32px" }}>
            <VideoList refreshKey={videoRefreshKey} />
          </div>
        </>
      )}
      </div>
    </div>
  )
}

export default App