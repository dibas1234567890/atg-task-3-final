import React, { useState, useEffect } from 'react';
import axios from 'axios';

const ConfirmedAppointments = () => {
    const [appointments, setAppointments] = useState([]);
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchAppointments = async () => {
            const token = localStorage.getItem('access_token');
            try {
                const response = await axios.get('http://127.0.0.1:8000/api/myappointments', {
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json',
                    }
                });
                setAppointments(response.data || []);
            } catch (error) {
                setError('Failed to fetch appointments');
                console.error('Error fetching appointments:', error.response || error.message);
            } finally {
                setLoading(false);
            }
        };

        fetchAppointments();
    }, []);

    return (
        <div className="container">
            <h2>Confirmed Appointments</h2>
            {loading && <p>Loading appointments...</p>}
            {error && <div className="alert alert-danger">{error}</div>}
            {!loading && appointments.length === 0 ? (
                <p>No confirmed appointments.</p>
            ) : (
                <div className="accordion">
                    {appointments.map((appointment) => (
                        <div key={appointment.id} className="accordion-item">
                            <h2 className="accordion-header" id={`heading-${appointment.id}`}>
                                <button 
                                    className="accordion-button" 
                                    type="button" 
                                    data-bs-toggle="collapse" 
                                    data-bs-target={`#collapse-${appointment.id}`} 
                                    aria-expanded="true" 
                                    aria-controls={`collapse-${appointment.id}`}
                                >
                                    Appointment on {appointment.date}
                                </button>
                            </h2>
                            <div 
                                id={`collapse-${appointment.id}`} 
                                className="accordion-collapse collapse show" 
                                aria-labelledby={`heading-${appointment.id}`}
                            >
                                <div className="accordion-body">
                                    <ul className="list-group">
                                        <li className="list-group-item">
                                            <h3>
                                                Specialty: 
                                                <small className="text-muted">{appointment.speciality}</small>
                                            </h3>
                                            <p>Date: {appointment.date}</p>
                                            <p>Start Time: {appointment.start_time}</p>
                                            <p>End Time: {appointment.end_time || 'Not specified'}</p>
                                            <p>Doctor: <strong>{appointment.doctor_name}</strong></p>
                                        </li>
                                    </ul>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};

export default ConfirmedAppointments;
