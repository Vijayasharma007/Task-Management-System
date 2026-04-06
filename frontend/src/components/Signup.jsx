import React, { useState } from 'react'
import { ENDPOINTS, instance } from './api'
import { useNavigate, Link } from 'react-router-dom'
import { toast } from 'react-toastify'

const Signup = () => {
    const [username, setUsername] = useState("")
    const [password, setPassword] = useState("")
    const navigate = useNavigate()

    const handleOnSubmit = async(e) => {
        e.preventDefault()
        try {
            await instance.post(ENDPOINTS.REGISTER(), { username, password })
            toast.success("Registration successful! Please login.")
            navigate("/")
        } catch (error) {
            toast.error(error.response?.data?.detail || "Registration failed")
        }
    }

    return (
        <div className='auth-container'>
            <form onSubmit={handleOnSubmit} className='auth-form glass-panel'>
                <h2>Create Account</h2>
                <div className='input-group'>
                    <input type="text"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        placeholder='Username'
                        required
                    />
                </div>
                <div className='input-group'>
                    <input type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        placeholder='Password'
                        required
                    />
                </div>
                <button type="submit" className='btn-primary'>Sign Up</button>
                <p className='auth-link'>
                    Already have an account? <Link to="/">Login here</Link>
                </p>
            </form>
        </div>
    )
}

export default Signup
