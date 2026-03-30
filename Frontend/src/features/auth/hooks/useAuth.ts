import { useState } from "react"
import { googleLogin, getCurrentUser } from "../services/authService"
import type { User } from "../types/auth.types"

export const useAuth = () => {
  const [user, setUser] = useState<User | null>(null)

  const loginWithGoogle = async (token: string) => {
    const data = await googleLogin(token)
    setUser(data.user)
  }

  const fetchUser = async () => {
    try {
      const data = await getCurrentUser()
      setUser(data)
    } catch {
      setUser(null)
    }
  }

  return { user, loginWithGoogle, fetchUser }
}