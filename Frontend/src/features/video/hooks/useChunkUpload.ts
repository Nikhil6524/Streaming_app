import { useState } from "react"
import { initUpload, uploadChunk, completeUpload } from "../services/chunkService"

const CHUNK_SIZE = 5 * 1024 * 1024 // 5MB

export const useChunkUpload = () => {
  const [progress, setProgress] = useState(0)
  const [loading, setLoading] = useState(false)

  const upload = async (file: File, title: string) => {
    setLoading(true)

    try {
      const uploadId = await initUpload()

      const totalChunks = Math.ceil(file.size / CHUNK_SIZE)

      for (let i = 0; i < totalChunks; i++) {
        const start = i * CHUNK_SIZE
        const end = Math.min(start + CHUNK_SIZE, file.size)

        const chunk = file.slice(start, end)

        await uploadChunk(uploadId, i, chunk)

        // 🔥 update progress
        setProgress(Math.round(((i + 1) / totalChunks) * 100))
      }

      const result = await completeUpload(uploadId, totalChunks, title)

      return result
    } finally {
      setLoading(false)
    }
  }

  return { upload, progress, loading }
}