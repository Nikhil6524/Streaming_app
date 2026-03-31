import { useEffect } from "react"
import { useAuthContext } from "../context/AuthContext"

declare global {
  interface Window {
    google: any
  }
}

const LoginButton = () => {
  const { loginWithGoogle } = useAuthContext()

  useEffect(() => {
    window.google.accounts.id.initialize({
      client_id: import.meta.env.VITE_GOOGLE_CLIENT_ID,
      callback: async (response: any) => {
        try {
          await loginWithGoogle(response.credential)
        } catch (error) {
          console.error("Google login failed", error)
          alert("Login failed. Please try again.")
        }
      },
    })

    window.google.accounts.id.renderButton(
      document.getElementById("googleBtn"),
      { theme: "outline", size: "large" }
    )
  }, [])

  return <div id="googleBtn"></div>
}

export default LoginButton