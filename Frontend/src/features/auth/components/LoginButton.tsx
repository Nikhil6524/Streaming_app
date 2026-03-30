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
        console.log("TOKEN:", response.credential)
        await loginWithGoogle(response.credential)
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