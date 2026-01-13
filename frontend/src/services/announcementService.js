import axios from 'axios'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:5000'

async function createAnnouncement(payload) {
  try {
    const res = await axios.post(`${API_BASE}/api/anuncios/admin`, payload, { withCredentials: true })
    return res.data
  } catch (err) {
    const msg = err.response?.data?.message || err.response?.data || err.message || 'Error de conexión'
    throw new Error(msg)
  }
}

async function fetchCourses() {
  try {
    const res = await axios.get(`${API_BASE}/admin/courses`, { withCredentials: true })
    return res.data
  } catch (err) {
    const msg = err.response?.data?.message || err.response?.data || err.message || 'Error de conexión'
    throw new Error(msg)
  }
}


export default {
  createAnnouncement,
  fetchCourses
}
