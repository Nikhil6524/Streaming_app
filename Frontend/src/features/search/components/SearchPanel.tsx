import { useState } from "react"
import SearchBar from "./SearchBar"
import SearchResults from "./SearchResults"
import { useVideoSearch } from "../hooks/useVideoSearch"

type Props = {
  refreshKey?: number
}

const SearchPanel = ({ refreshKey = 0 }: Props) => {
  const [query, setQuery] = useState("")
  const { results, loading, error } = useVideoSearch(query, refreshKey)

  return (
    <section
      style={{
        border: "1px solid #1f2937",
        borderRadius: "16px",
        padding: "16px",
        background: "rgba(15, 23, 42, 0.45)",
      }}
    >
      <h3 style={{ marginBottom: "10px" }}>Search Videos</h3>
      <SearchBar query={query} onQueryChange={setQuery} />
      <SearchResults results={results} loading={loading} error={error} query={query} />
    </section>
  )
}

export default SearchPanel
