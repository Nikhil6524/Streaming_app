import { useState } from "react"
import { useChunkUpload } from "../hooks/useChunkUpload"

const UploadChunkVideo = () => {
  const [file, setFile] = useState<File | null>(null)
  const { upload, progress, loading } = useChunkUpload()

  const handleUpload = async () => {
    if (!file) return

    try {
      const res = await upload(file)
      console.log("Final URL:", res.url)
      alert("Chunk upload complete!")
    } catch (err) {
      console.error(err)
      alert("Upload failed")
    }
  }

  return (
    <div style={{ marginTop: "30px" }}>
      <h3>Chunk Upload Video</h3>

      <input
        type="file"
        accept="video/mp4"
        onChange={(e) => setFile(e.target.files?.[0] || null)}
      />

      <button onClick={handleUpload} disabled={loading}>
        {loading ? "Uploading..." : "Upload in Chunks"}
      </button>

      <p>Progress: {progress}%</p>
    </div>
  )
}

export default UploadChunkVideo