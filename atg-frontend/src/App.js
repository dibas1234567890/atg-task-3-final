import React, { useState, useEffect } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import RegisterForm from './register';
import BlogForm from './blogpost';
import LoginForm from './login';
import CategoryForm from './category';
import BlogList from './BlogList';
import BlogsByCategory from './BlogsByCategory';
import Navbar from './NavBar';
import Dashboard from './Dashboard';
// import Appointments from './Appointments'; 
import { getUserType } from './utils';

import ConfirmedAppointments from './AppointmentPatientsSee';

function App() {
    const [userType, setUserType] = useState(null);
    const [isLoggedIn, setIsLoggedIn] = useState(false);

    useEffect(() => {
        const token = localStorage.getItem('access_token');
        setIsLoggedIn(!!token);

        const fetchUserType = async () => {
            if (token) {
                const type = await getUserType();
                setUserType(type);
            }
        };

        fetchUserType();
    }, []);

    const handleLogout = () => {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        setIsLoggedIn(false);
        window.location.href = '/api/login';
    };

 

    return (
        <div className="App">
            <BrowserRouter>
                <Navbar isLoggedIn={isLoggedIn} handleLogout={handleLogout} userType={userType} />
                <Routes>
                    <Route path="/api/register" element={<RegisterForm />} />
                    <Route path="/api/login" element={<LoginForm />} />
                    <Route path="/api/blogpost" element={isLoggedIn ? <BlogForm /> : <Navigate to="/api/login" />} />
                    <Route path="/api/categories" element={isLoggedIn ? <CategoryForm /> : <Navigate to="/api/login" />} />
                    <Route path="/api/blogosphere" element={<BlogList />} />
                    {userType === 'patient' && <Route path="/api/patient_dashboard" element={<Dashboard />} />}
                    {/* {userType === 'doctor' && <Route path="/api/appointments" element={<Appointments />} />} */}
                    <Route path="/api/blogs_by_category/:category_id" element={<BlogsByCategory />} />
                    <Route path='/api/myappointments' element = {<ConfirmedAppointments/>} />
                </Routes>
            </BrowserRouter>
        </div>
    );
}

export default App;
