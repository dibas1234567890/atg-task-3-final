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
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        const token = localStorage.getItem('access_token');
        setIsLoggedIn(!!token);

        const fetchUserType = async () => {
            if (token) {
                const type = await getUserType();
                console.log(type);
                setUserType(type);
            }
            setIsLoading(false);
        };

        fetchUserType();
    }, []);

    const handleLogout = () => {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        setIsLoggedIn(false);
        setUserType(null);
        return (<Navigate to ='/app/login'/>)
    };


    return (
        <div className="App">
            <BrowserRouter>
                <Navbar isLoggedIn={isLoggedIn} handleLogout={handleLogout} userType={userType} />
                <Routes>
                    <Route path="/app/register" element={<RegisterForm />} />
                    <Route path="/app/login" element={isLoggedIn ? null : <LoginForm />} />
                    <Route path="/app/blogpost" element={isLoggedIn ? <BlogForm /> : <Navigate to="/app/login" />} />
                    <Route path="/app/categories" element={isLoggedIn ? <CategoryForm /> : <Navigate to="/app/login" />} />
                    <Route path="/app/blogosphere" element={<BlogList />} />
                    {userType === 'patient' && <Route path="/app/patient_dashboard" element={<Dashboard />} />}
                    {userType === 'doctor' && <Route path="/app/myappointments" element={<ConfirmedAppointments />} />}
                    <Route path="/app/blogs_by_category/:category_id" element={<BlogsByCategory />} />
                   
                   
                </Routes>
            </BrowserRouter>
        </div>
    );
}

export default App;
