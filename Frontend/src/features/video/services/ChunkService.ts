import api from "../../../lib/api/axios"

export const initUpload = async () => {
  const res = await api.post("/chunk/init")
  return res.data.upload_id
}

export const uploadChunk = async (
  uploadId: string,
  chunkIndex: number,
  chunk: Blob
) => {
  const formData = new FormData()
  formData.append("upload_id", uploadId)
  formData.append("chunk_index", chunkIndex.toString())
  formData.append("file", chunk)

  await api.post("/chunk/upload", formData)
}

export const completeUpload = async (
  uploadId: string,
  totalChunks: number,
  title: string
) => {
  const formData = new FormData()
  formData.append("upload_id", uploadId)
  formData.append("total_chunks", totalChunks.toString())
  formData.append("title", title)

  const res = await api.post("/chunk/complete", formData)
  return res.data
}