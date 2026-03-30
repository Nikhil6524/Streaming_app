import { createContext, useContext, useEffect } from "react"
import { useAuth } from "../hooks/useAuth"

const AuthContext = createContext<any>(null)

export const AuthProvider = ({ children }: any) => {
  const auth = useAuth()

  useEffect(() => {
    auth.fetchUser() // auto-login using cookie
  }, [])

  return (
    <AuthContext.Provider value={auth}>
      {children}
    </AuthContext.Provider>
  )
}

export const useAuthContext = () => useContext(AuthContext)