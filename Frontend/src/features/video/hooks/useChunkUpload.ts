import { useState } from "react"
import { initUpload, uploadChunk, completeUpload } from "../services/chunkService"

const CHUNK_SIZE = 5 * 1024 * 1024 // 5MB

export const useChunkUpload = () => {
  const [progress, setProgress] = useState(0)
  const [loading, setLoading] = useState(false)

  const upload = async (file: File, title: string) => {
    setLoading(true)

    try {
      // Use the original file name as the logical "filename" key
      // for the backend chunking API.
      const filename = file.name

      // Initialize upload session on the backend
      const uploadKey = await initUpload(filename)

      const totalChunks = Math.ceil(file.size / CHUNK_SIZE)

      for (let i = 0; i < totalChunks; i++) {
        const start = i * CHUNK_SIZE
        const end = Math.min(start + CHUNK_SIZE, file.size)

        const chunk = file.slice(start, end)

  await uploadChunk(uploadKey, i, chunk)

        // 🔥 update progress
        setProgress(Math.round(((i + 1) / totalChunks) * 100))
      }

      const result = await completeUpload(uploadKey, totalChunks, title)

      return result
    } finally {
      setLoading(false)
    }
  }

  return { upload, progress, loading }
}