import { useState, useEffect } from "react"
import { uploadVideo, getVideos } from "../services/VideoService"

export const useUpload = () => {
  const [loading, setLoading] = useState(false)
  const [progress] = useState(0)

  const upload = async (file: File, title: string) => {
    setLoading(true)

    try {
      const data = await uploadVideo(file, title)
      console.log("Uploaded:", data)
      return data
    } finally {
      setLoading(false)
    }
  }

  return { upload, loading, progress }
}

export const useVideos = (refreshKey = 0) => {
  const [videos, setVideos] = useState<any[]>([])
  const [refreshIndex, setRefreshIndex] = useState(0)

  const refresh = () => setRefreshIndex((prev) => prev + 1)

  useEffect(() => {
    getVideos().then(setVideos)
  }, [refreshIndex, refreshKey])

  return { videos, refresh }
}