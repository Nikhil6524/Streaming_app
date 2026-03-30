import LoginButton from "./features/auth/components/LoginButton"
import { useAuthContext } from "./features/auth/context/AuthContext"
import UploadVideo from "./features/video/componenets/UploadVideo"
import VideoList from "./features/video/componenets/VideoList"
import UploadChunkVideo from "./features/video/componenets/UploadChunkVideo"

const App = () => {
  const { user } = useAuthContext()

  return (
    <div
      style={{
        padding: "40px",
        minHeight: "100vh",
        background: "linear-gradient(135deg,#0f172a,#020617)",
        color: "#f9fafb",
      }}
    >
      {!user ? (
        <>
          <h2>Login</h2>
          <LoginButton />
        </>
      ) : (
        <>
          <h2 style={{ fontSize: "26px", marginBottom: "20px" }}>
            Welcome {user.name}
          </h2>

          {/* 🔼 Upload Section */}
          <div
            style={{
              display: "flex",
              flexWrap: "wrap",
              gap: "20px",
              alignItems: "flex-start",
            }}
          >
            <UploadVideo />
            <UploadChunkVideo />
          </div>

          {/* 🎥 Video Feed */}
          <div
            style={{
              marginTop: "40px",
              padding: "20px",
              borderRadius: "16px",
              background: "rgba(15,23,42,0.7)",
              border: "1px solid rgba(148,163,184,0.4)",
            }}
          >
            <VideoList />
          </div>
        </>
      )}
    </div>
  )
}

export default App