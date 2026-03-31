import { useState } from "react"
import LoginButton from "./features/auth/components/LoginButton"
import { useAuthContext } from "./features/auth/context/AuthContext"
import VideoList from "./features/video/componenets/VideoList"
import UploadChunkVideo from "./features/video/componenets/UploadChunkVideo"
import SearchPanel from "./features/search/components/SearchPanel"
import { Button } from "./components/ui/Button"

const App = () => {
  const { user, isLoadingUser, logoutUser } = useAuthContext()
  const [videoRefreshKey, setVideoRefreshKey] = useState(0)

  const handleUploadSuccess = () => {
    setVideoRefreshKey((prev) => prev + 1)
  }

  const handleLogout = async () => {
    await logoutUser()
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
      {isLoadingUser ? (
        <p style={{ color: "#93c5fd" }}>Checking session...</p>
      ) : !user ? (
        <>
          <h2 style={{ marginBottom: "16px" }}>Login</h2>
          <LoginButton />
        </>
      ) : (
        <>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "8px" }}>
            <h2>Welcome {user.name}</h2>
            <Button variant="secondary" onClick={handleLogout}>
              Logout
            </Button>
          </div>
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
            <SearchPanel refreshKey={videoRefreshKey} />
          </div>

          <div style={{ marginTop: "24px" }}>
            <VideoList refreshKey={videoRefreshKey} />
          </div>
        </>
      )}
      </div>
    </div>
  )
}

export default App