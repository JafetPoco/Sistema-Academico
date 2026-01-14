import axios from 'axios'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:5000'

export async function fetchParentGrades() {
  try {
    const res = await axios.get(`${API_BASE}/parent_query_grades`, { withCredentials: true })
    return res.data
  } catch (err) {
    const msg = err.response?.data?.message || err.response?.data || err.message || 'Error de conexión'
    throw new Error(msg)
  }
}

export default { fetchParentGrades }
