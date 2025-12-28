import axios from 'axios'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:5000'

async function login(email, password) {
  try {
    const res = await axios.post(
      `${API_BASE}/api/auth/login`,
      { email, password },
      { withCredentials: true }
    )
    return res.data
  } catch (err) {
    // normalize error message
    const msg = err.response?.data?.message || err.response?.data || err.message || 'Error de conexión'
    throw new Error(msg)
  }
}

async function register(full_name, email, password, confirm_password) {
  try {
    const res = await axios.post(`${API_BASE}/api/auth/register`, {
      full_name,
      email,
      password,
      confirm_password
    })
    return res.data
  } catch (err) {
    const msg = err.response?.data?.message || err.response?.data || err.message || 'Error de conexión'
    throw new Error(msg)
  }
}

async function logout() {
  try {
    const res = await axios.post(`${API_BASE}/api/auth/logout`, {}, { withCredentials: true })
    return res.data
  } catch (err) {
    const msg = err.response?.data?.message || err.response?.data || err.message || 'Error de conexión'
    throw new Error(msg)
  }
}

export default {
  login,
  register,
  logout
}
