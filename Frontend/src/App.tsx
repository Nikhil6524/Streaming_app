import LoginButton from "./features/auth/components/LoginButton"
import { useAuthContext } from "./features/auth/context/AuthContext"
import UploadVideo from "./features/video/componenets/UploadVideo"
import VideoList from "./features/video/componenets/VideoList"
import UploadChunkVideo from "./features/video/componenets/UploadChunkVideo"

const App = () => {
  const { user } = useAuthContext()

  return (
    <div style={{ padding: "40px" }}>
      {!user ? (
        <>
          <h2>Login</h2>
          <LoginButton />
        </>
      ) : (
        <>
          <h2>Welcome {user.name}</h2>

          {/* 🔼 Upload Section */}
          <UploadVideo />
          <UploadChunkVideo />

          {/* 🎥 Video Feed */}
          <div style={{ marginTop: "40px" }}>
            <VideoList />
          </div>
        </>
      )}
    </div>
  )
}

export default App