import api from "../../../lib/api/axios"

export const uploadVideo = async (file: File, title: string) => {
  const formData = new FormData()
  formData.append("file", file)
  formData.append("title", title)

  const res = await api.post("/upload/", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  })
  return res.data
}

export const getVideos = async () => {
  const res = await api.get("/videos/")
  return res.data
}