import type { CSSProperties } from "react"
import Input from "../../../components/ui/Input"

type Props = {
  query: string
  onQueryChange: (value: string) => void
}

const inputStyle: CSSProperties = {
  background: "#0b1220",
  color: "#e5e7eb",
  border: "1px solid #334155",
}

const SearchBar = ({ query, onQueryChange }: Props) => {
  return (
    <div>
      <Input
        value={query}
        onChange={(e) => onQueryChange(e.target.value)}
        placeholder="Search videos by title..."
        style={inputStyle}
      />
    </div>
  )
}

export default SearchBar
