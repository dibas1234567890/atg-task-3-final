import React from 'react';
import { Link } from 'react-router-dom';

const Navbar = ({ isLoggedIn, handleLogout, userType }) => {
    return (
        <nav className="navbar navbar-expand-lg navbar-light bg-light">
            <div className="container-fluid">
                <Link className="navbar-brand" to="/">My App</Link>
                <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                    <span className="navbar-toggler-icon"></span>
                </button>
                <div className="collapse navbar-collapse" id="navbarNav">
                    <ul className="navbar-nav">
                        {!isLoggedIn && (
                            <>
                                <li className="nav-item">
                                    <Link className="nav-link" to="/api/register">Register</Link>
                                </li>
                                <li className="nav-item">
                                    <Link className="nav-link" to="/api/login">Login</Link>
                                </li>
                            </>
                        )}
                        {isLoggedIn && (
                            <>
                                <li className="nav-item">
                                    <Link className="nav-link" to="/api/blogpost">Create Blog Post</Link>
                                </li>
                                <li className="nav-item">
                                    <Link className="nav-link" to="/api/categories">Categories</Link>
                                </li>
                                {userType === 'patient' && (
                                    <li className="nav-item">
                                        <Link className="nav-link" to="/api/patient_dashboard">Dashboard only shown for patients</Link>
                                    </li>
                                )}
                                {userType === 'doctor' && (
                                    <li className="nav-item">
                                        <Link className="nav-link" to="/api/appointments">Appointments only shown for docs </Link>
                                    </li>
                                )}
                                <li className="nav-item">
                                    <Link className="nav-link" to="/api/blogosphere">Blog List</Link>
                                </li>
                                <li className="nav-item">
                                    <button className="nav-link btn btn-link" onClick={handleLogout}>Logout</button>
                                </li>
                            </>
                        )}
                    </ul>
                </div>
            </div>
        </nav>
    );
};

export default Navbar;
