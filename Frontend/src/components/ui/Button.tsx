import React from "react"

type ButtonProps = React.ButtonHTMLAttributes<HTMLButtonElement> & {
	variant?: "primary" | "secondary"
}

const baseStyle: React.CSSProperties = {
	padding: "10px 16px",
	borderRadius: "9999px",
	border: "none",
	fontWeight: 600,
	cursor: "pointer",
	fontSize: "0.95rem",
	display: "inline-flex",
	alignItems: "center",
	justifyContent: "center",
	gap: "8px",
}

const variants: Record<string, React.CSSProperties> = {
	primary: {
		background: "linear-gradient(135deg, #ff4b2b, #ff416c)",
		color: "#ffffff",
	},
	secondary: {
		background: "#ffffff",
		color: "#111827",
		border: "1px solid #e5e7eb",
	},
}

export const Button: React.FC<ButtonProps> = ({
	variant = "primary",
	style,
	children,
	...props
}) => {
	return (
		<button
			style={{
				...baseStyle,
				...variants[variant],
				opacity: props.disabled ? 0.6 : 1,
				...(style || {}),
			}}
			{...props}
		>
			{children}
		</button>
	)
}

export default Button

