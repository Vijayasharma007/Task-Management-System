import React, { useState } from 'react'
import { ENDPOINTS, instance } from './api'
import { useNavigate, Link } from 'react-router-dom'
import { toast } from 'react-toastify'

const Login = () => {
    const [username, setUsername] = useState("")
    const [password, setPassword] = useState("")
    const navigate =useNavigate()

    const handleOnSubmit=async(e)=>{
        e.preventDefault()
        try {
            const res = await instance.post(ENDPOINTS.LOGIN(),{username,password})
            if (res && res.data && res.data.token) {
                localStorage.setItem("token", res.data.token)
                toast.success("Login successful")
                navigate("/tasks")
            }
        } catch (error) {
            toast.error(error.response?.data?.detail || "Login failed")
        }
    }

    return (
        <div className='auth-container'>
            <form onSubmit={handleOnSubmit} className='auth-form glass-panel'>
                <h2>Login</h2>
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
                        onChange={(e)=>setPassword(e.target.value)}
                        placeholder='Password'
                        required
                    />
                </div>
                <button type="submit" className='btn-primary'>Login</button>
                <p className='auth-link'>
                    Don't have an account? <Link to="/signup">Sign up here</Link>
                </p>
            </form>
        </div>
    )
}

export default Login