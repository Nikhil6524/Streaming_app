import { useState, useEffect } from "react"
import { uploadVideo } from "../services/videoservice"

export const useUpload = () => {
  const [loading, setLoading] = useState(false)
  const [progress, setProgress] = useState(0)

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

import { getVideos } from "../services/videoservice"

export const useVideos = () => {
  const [videos, setVideos] = useState<any[]>([])

  useEffect(() => {
    getVideos().then(setVideos)
  }, [])

  return { videos }
}