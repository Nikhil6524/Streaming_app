import { useState, type CSSProperties } from "react"
import { useChunkUpload } from "../hooks/useChunkUpload"
import Input from "../../../components/ui/Input"
import Button from "../../../components/ui/Button"

type Props = {
  onUploadSuccess?: () => void
}

const cardStyle: CSSProperties = {
  marginTop: "16px",
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

const progressBarOuter: CSSProperties = {
  width: "100%",
  height: "8px",
  borderRadius: "9999px",
  background: "#e5e7eb",
  overflow: "hidden",
}

const UploadChunkVideo = ({ onUploadSuccess }: Props) => {
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
      setTitle("")
      setFile(null)
      onUploadSuccess?.()
      alert("Chunk upload complete!")
    } catch (err) {
      console.error(err)
      alert("Upload failed")
    }
  }

  return (
    <div style={cardStyle}>
      <h3 style={{ marginBottom: "12px" }}>Chunk Upload Video</h3>

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
            {loading ? "Uploading..." : "Upload in Chunks"}
          </Button>
        </div>

        <div style={{ marginTop: "8px" }}>
          <div style={labelStyle}>Progress</div>
          <div style={progressBarOuter}>
            <div
              style={{
                width: `${progress}%`,
                height: "100%",
                background:
                  "linear-gradient(135deg, #4ade80, #22c55e)",
              }}
            />
          </div>
          <div style={{ fontSize: "0.8rem", color: "#6b7280", marginTop: "4px" }}>
            {progress}%
          </div>
        </div>
      </div>
    </div>
  )
}

export default UploadChunkVideo