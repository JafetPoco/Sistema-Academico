import axios from 'axios'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:5000'

async function fetchUsers() {
  try {
    const res = await axios.get(`${API_BASE}/admin/users`, { withCredentials: true })
    return res.data
  } catch (err) {
    const msg = err.response?.data?.message || err.response?.data || err.message || 'Error de conexión'
    throw new Error(msg)
  }
}

async function updateUserRole(userId, role) {
  try {
    const form = new URLSearchParams()
    form.append('role', role)
    await axios.post(`${API_BASE}/admin/users/${userId}`, form, {
      withCredentials: true,
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    })
  } catch (err) {
    const msg = err.response?.data?.message || err.response?.data || err.message || 'Error de conexión'
    throw new Error(msg)
  }
}

export default {
  fetchUsers,
  updateUserRole,
}
