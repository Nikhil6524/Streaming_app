import { useState } from "react"
import { googleLogin, getCurrentUser, logout } from "../services/authService"
import type { User } from "../types/auth.types"

const AUTH_USER_KEY = "yt_clone_user"

export const useAuth = () => {
  const [user, setUser] = useState<User | null>(null)
  const [isLoadingUser, setIsLoadingUser] = useState(true)

  const loginWithGoogle = async (token: string) => {
    const data = await googleLogin(token)

    // Support both { user: {...} } and direct user payload shapes.
    const nextUser = (data?.user ?? data) as User | null

    if (nextUser?.id) {
      setUser(nextUser)
      localStorage.setItem(AUTH_USER_KEY, JSON.stringify(nextUser))
    }

    // Refresh from cookie-backed /user/me when available.
    await fetchUser()

    return nextUser
  }

  const logoutUser = async () => {
    try {
      await logout()
    } catch (error) {
      console.error("Logout error:", error)
    } finally {
      setUser(null)
      localStorage.removeItem(AUTH_USER_KEY)
    }
  }

  const fetchUser = async () => {
    setIsLoadingUser(true)

    try {
      const data = await getCurrentUser()
      setUser(data)
      localStorage.setItem(AUTH_USER_KEY, JSON.stringify(data))
    } catch {
      // Fallback lets UI redirect into app immediately after successful login
      // even if cookie propagation is delayed in development.
      const saved = localStorage.getItem(AUTH_USER_KEY)
      if (saved) {
        try {
          setUser(JSON.parse(saved) as User)
        } catch {
          localStorage.removeItem(AUTH_USER_KEY)
          setUser(null)
        }
      } else {
        setUser(null)
      }
    } finally {
      setIsLoadingUser(false)
    }
  }

  return { user, loginWithGoogle, logoutUser, fetchUser, isLoadingUser }
}