import { useEffect, useState } from "react"
import { searchVideos, type SearchVideo } from "../services/searchService"

export const useVideoSearch = (query: string, refreshKey = 0) => {
  const [results, setResults] = useState<SearchVideo[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const trimmed = query.trim()

    if (!trimmed) {
      setResults([])
      setLoading(false)
      setError(null)
      return
    }

    const timer = setTimeout(async () => {
      setLoading(true)
      setError(null)

      try {
        const data = await searchVideos(trimmed)
        setResults(data)
      } catch {
        setError("Search failed. Please try again.")
      } finally {
        setLoading(false)
      }
    }, 350)

    return () => clearTimeout(timer)
  }, [query, refreshKey])

  return { results, loading, error }
}
