import axios from 'axios'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:5000'

async function getCourses() {
  try {
    const res = await axios.get(`${API_BASE}/calificar`, { withCredentials: true })
    return res.data
  } catch (err) {
    const msg = err.response?.data?.message || err.response?.data || err.message || 'Error de conexión'
    throw new Error(msg)
  }
}

async function getStudentsByCourse(courseId) {
  try {
    const res = await axios.get(`${API_BASE}/api/students-by-course`, {
      params: { course_id: courseId },
      withCredentials: true
    })
    return res.data
  } catch (err) {
    const msg = err.response?.data?.message || err.response?.data || err.message || 'Error de conexión'
    throw new Error(msg)
  }
}

async function submitQualification(payload) {
  try {
    const res = await axios.post(`${API_BASE}/calificar`, payload, { withCredentials: true })
    return res.data
  } catch (err) {
    const msg = err.response?.data?.message || err.response?.data || err.message || 'Error de conexión'
    throw new Error(msg)
  }
}

export default {
  getCourses,
  getStudentsByCourse,
  submitQualification,
}
