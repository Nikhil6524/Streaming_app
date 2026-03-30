import React from "react"

type InputProps = React.InputHTMLAttributes<HTMLInputElement>

const baseStyle: React.CSSProperties = {
	width: "100%",
	padding: "8px 12px",
	borderRadius: "9999px",
	border: "1px solid #e5e7eb",
	fontSize: "0.95rem",
	outline: "none",
	boxSizing: "border-box",
}

export const Input: React.FC<InputProps> = ({ style, ...props }) => {
	return (
		<input
			style={{
				...baseStyle,
				...(style || {}),
			}}
			{...props}
		/>
	)
}

export default Input

