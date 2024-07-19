import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const AppointmentForm = ({ doctorId, onClose }) => {
    const [formData, setFormData] = useState({
        doctor: doctorId,
        speciality: '',
        date: '',
        start_time: '',
    });
    const [error, setError] = useState(null);
    const [success, setSuccess] = useState(null);
    const [availableDates, setAvailableDates] = useState({});
    const [timeSlots, setTimeSlots] = useState([]);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchAvailableDates = async () => {
            const token = localStorage.getItem('access_token');
            try {
                const response = await axios.get(`http://127.0.0.1:8000/api/fetch-available-slots/${doctorId}`, {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    },
                });
                setAvailableDates(response.data.available_dates);
            } catch (error) {
                setError('Failed to fetch available dates');
            }
        };

        fetchAvailableDates();
    }, [doctorId]);

    useEffect(() => {
        if (formData.date && availableDates[formData.date]) {
            setTimeSlots(availableDates[formData.date]);
        } else {
            setTimeSlots([]);
        }
    }, [formData.date, availableDates]);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({
            ...formData,
            [name]: value,
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await axios.post(`http://127.0.0.1:8000/api/fetch-available-slots/${doctorId}`, {
                summary: formData.speciality,
                start_time: `${formData.date}T${formData.start_time}:00`,
                doctor: formData.doctor,
            }, {
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${localStorage.getItem('access_token')}`
                },
            });
            setSuccess('Appointment booked successfully');
            setFormData({
                doctor: doctorId,
                speciality: '',
                date: '',
                start_time: '',
            });
            navigate('/app/myappointments');
        } catch (error) {
            setError('Failed to book appointment');
        }
    };
    

    return (
        <div className="container">
            <h2>Book an Appointment</h2>
            {success && <div className="alert alert-success">{success}</div>}
            {error && <div className="alert alert-danger">{error}</div>}
            <form onSubmit={handleSubmit}>
                <div className="form-group">
                    <label htmlFor="speciality">Speciality</label>
                    <input
                        id="speciality"
                        name="speciality"
                        type="text"
                        className="form-control"
                        value={formData.speciality}
                        onChange={handleChange}
                        required
                    />
                </div>

                <div className="form-group">
                    <label htmlFor="date">Date</label>
                    <select
                        id="date"
                        name="date"
                        className="form-control"
                        value={formData.date}
                        onChange={handleChange}
                        required
                    >
                        <option value="">Select a date</option>
                        {Object.keys(availableDates).map(date => (
                            <option key={date} value={date}>{date}</option>
                        ))}
                    </select>
                </div>

                <div className="form-group">
                    <label htmlFor="start_time">Start Time</label>
                    <select
                        id="start_time"
                        name="start_time"
                        className="form-control"
                        value={formData.start_time}
                        onChange={handleChange}
                        required
                    >
                        <option value="">Select a time</option>
                        {timeSlots.map(slot => (
                            <option key={slot.start_time} value={slot.start_time}>
                                {slot.start_time} - {slot.end_time}
                            </option>
                        ))}
                    </select>
                </div>

                <div className="mt-2">
                    <button type="submit" className="btn mx-2 btn-primary">Confirm</button>
                    <button type="button" className="btn btn-secondary" onClick={onClose}>Cancel</button>
                </div>
            </form>
        </div>
    );
};

export default AppointmentForm;
