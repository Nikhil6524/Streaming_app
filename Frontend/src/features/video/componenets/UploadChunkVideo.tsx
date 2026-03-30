import { useState } from "react"
import { useChunkUpload } from "../hooks/useChunkUpload"

const UploadChunkVideo = () => {
  const [file, setFile] = useState<File | null>(null)
  const [title, setTitle] = useState("")
  const { upload, progress, loading } = useChunkUpload()

  const handleUpload = async () => {
    if (!file || !title.trim()) {
      alert("Please select a video and enter a title.")
      return
    }

    try {
      const res = await upload(file, title.trim())
      console.log("Final URL:", res.url)
      alert("Chunk upload complete!")
      setFile(null)
      setTitle("")
    } catch (err) {
      console.error(err)
      alert("Upload failed")
    }
  }

  return (
    <div
      style={{
        marginTop: "20px",
        padding: "20px",
        borderRadius: "12px",
        border: "1px solid #e5e7eb",
        background: "#f9fafb",
        boxShadow: "0 8px 20px rgba(15,23,42,0.04)",
        maxWidth: "480px",
      }}
    >
      <h3 style={{ marginBottom: "12px", fontSize: "20px" }}>Chunk Upload Video</h3>

      <div style={{ display: "flex", flexDirection: "column", gap: "10px" }}>
        <input
          type="text"
          placeholder="Video title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          style={{
            padding: "8px 12px",
            borderRadius: "8px",
            border: "1px solid #d1d5db",
          }}
        />

        <input
          type="file"
          accept="video/mp4"
          onChange={(e) => setFile(e.target.files?.[0] || null)}
          style={{
            padding: "8px 0",
          }}
        />

        <button
          onClick={handleUpload}
          disabled={loading}
          style={{
            marginTop: "6px",
            padding: "8px 16px",
            borderRadius: "999px",
            border: "none",
            background: loading ? "#9ca3af" : "#10b981",
            color: "white",
            cursor: loading ? "default" : "pointer",
            fontWeight: 500,
          }}
        >
          {loading ? "Uploading..." : "Upload in Chunks"}
        </button>

        <p style={{ margin: 0, fontSize: "14px", color: "#4b5563" }}>
          Progress: <strong>{progress}%</strong>
        </p>
      </div>
    </div>
  )
}

export default UploadChunkVideo