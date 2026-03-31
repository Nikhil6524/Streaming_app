import api from "../../../lib/api/axios"

export type SearchVideo = {
  id: string
  title: string
  hls_url?: string | null
  url?: string | null
}

export const searchVideos = async (query: string) => {
  const res = await api.get<SearchVideo[]>("/search/", {
    params: { query },
  })

  return res.data
}
