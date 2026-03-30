import { useState, type CSSProperties } from "react"
import { useUpload } from "../hooks/useUpload"
import Input from "../../../components/ui/Input"
import Button from "../../../components/ui/Button"

const cardStyle: CSSProperties = {
  marginTop: "24px",
  padding: "20px",
  borderRadius: "16px",
  border: "1px solid #e5e7eb",
  background: "#ffffff",
  boxShadow: "0 10px 15px -3px rgba(0,0,0,0.08)",
  maxWidth: "480px",
}

const labelStyle: CSSProperties = {
  fontSize: "0.85rem",
  fontWeight: 500,
  color: "#6b7280",
  marginBottom: "6px",
}

const UploadVideo = () => {
  const [file, setFile] = useState<File | null>(null)
  const [title, setTitle] = useState("")
  const { upload, loading } = useUpload()

  const handleUpload = async () => {
    if (!file || !title.trim()) {
      alert("Please select a video and enter a title.")
      return
    }

    try {
      await upload(file, title.trim())
      setTitle("")
      setFile(null)
      alert("Upload successful!")
    } catch (err) {
      console.error(err)
      alert("Upload failed")
    }
  }

  return (
    <div style={cardStyle}>
      <h3 style={{ marginBottom: "12px" }}>Upload Video</h3>

      <div style={{ display: "flex", flexDirection: "column", gap: "12px" }}>
        <div>
          <div style={labelStyle}>Title</div>
          <Input
            placeholder="Enter video title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
          />
        </div>

        <div>
          <div style={labelStyle}>Video file (MP4)</div>
          <input
            type="file"
            accept="video/mp4"
            onChange={(e) => setFile(e.target.files?.[0] || null)}
          />
        </div>

        <div style={{ marginTop: "4px" }}>
          <Button onClick={handleUpload} disabled={loading || !file}>
            {loading ? "Uploading..." : "Upload"}
          </Button>
        </div>
      </div>
    </div>
  )
}

export default UploadVideo