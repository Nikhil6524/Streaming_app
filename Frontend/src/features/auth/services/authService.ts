import api from "../../../lib/api/axios"

export const googleLogin = async (token: string) => {
  const res = await api.post("/auth/google", { token })
  return res.data
}

export const getCurrentUser = async () => {
  const res = await api.get("/user/me")
  return res.data
}