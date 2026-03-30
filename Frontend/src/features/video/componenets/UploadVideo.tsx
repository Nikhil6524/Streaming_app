import { useState } from "react"
import { useUpload } from "../hooks/useUpload"

const UploadVideo = () => {
  const [file, setFile] = useState<File | null>(null)
  const { upload, loading } = useUpload()

  const handleUpload = async () => {
    if (!file) return

    try {
      await upload(file)
      alert("Upload successful!")
    } catch (err) {
      console.error(err)
      alert("Upload failed")
    }
  }

  return (
    <div style={{ marginTop: "30px" }}>
      <h3>Upload Video</h3>

      <input
        type="file"
        accept="video/mp4"
        onChange={(e) => setFile(e.target.files?.[0] || null)}
      />

      <button onClick={handleUpload} disabled={loading}>
        {loading ? "Uploading..." : "Upload"}
      </button>
    </div>
  )
}

export default UploadVideo