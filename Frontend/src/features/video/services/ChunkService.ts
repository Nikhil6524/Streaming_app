import api from "../../../lib/api/axios"

// Initialize an upload session on the backend.
// The backend expects a JSON body with { filename: string }
// and responds with { message, filename }.
export const initUpload = async (filename: string) => {
  const res = await api.post("/chunk/init", { filename })
  return res.data.filename as string
}

// Upload a single chunk.
// The backend expects multipart/form-data with
// fields: file (UploadFile), filename (str), chunk_index (int).
export const uploadChunk = async (
  filename: string,
  chunkIndex: number,
  chunk: Blob
) => {
  const formData = new FormData()
  formData.append("filename", filename)
  formData.append("chunk_index", chunkIndex.toString())
  formData.append("file", chunk)

  await api.post("/chunk/upload", formData)
}

// Complete the upload.
// The backend expects multipart/form-data with
// fields: filename (str), total_chunks (int).
// We also send title, which the backend currently ignores but may be useful later.
export const completeUpload = async (
  filename: string,
  totalChunks: number,
  title: string
) => {
  const formData = new FormData()
  formData.append("filename", filename)
  formData.append("total_chunks", totalChunks.toString())
  formData.append("title", title)

  const res = await api.post("/chunk/complete", formData)
  return res.data
}