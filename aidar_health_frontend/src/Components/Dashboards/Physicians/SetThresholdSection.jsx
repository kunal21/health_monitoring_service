import React, { useState } from 'react';
import { healthMetrics } from '../../../healthMetrics';
import { useNavigate } from 'react-router-dom';

const Modal = ({ message, onClose }) => {
    return (
        <div className="modal-overlay">
            <div className="modal">
                <p>{message}</p>
                <button onClick={onClose}>Close</button>
            </div>
        </div>
    );
};

const SetThresholdSection = ({ addThresholdToState }) => {
    // State for form input
    const [metricName, setMetricName] = useState('');
    const [minValue, setMinValue] = useState('');
    const [maxValue, setMaxValue] = useState('');

    // State for loader, modal, and messages
    const [modalMessage, setModalMessage] = useState(''); 
    const [showModal, setShowModal] = useState(false); 

    const navigate = useNavigate();


    // Handle form submission
    const handleSubmit = (e) => {
        e.preventDefault(); 

        fetch('http://localhost:5000/api/threshold', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include',
            body: JSON.stringify({
                metric_name: metricName,
                min_value: parseFloat(minValue),
                max_value: parseFloat(maxValue)
            })
        })
        .then(response => {
            if (response.status === 401) {
                alert('Session Expired. Login Again');
                navigate('/login');
            }
            if (!response.ok) {
                return response.json().then(errorData => {
                    throw new Error(errorData.error || 'Failed to set threshold');
                });
            }
            return response.json();
        })
        .then(result => {
            setModalMessage(result.message);
            setShowModal(true); 
            addThresholdToState(
                {
                    metric_name: metricName,
                    min_value: parseFloat(minValue),
                    max_value: parseFloat(maxValue)
                }
            );
            setMetricName('');
            setMinValue('');
            setMaxValue('');
        })
        .catch(error => {
            setModalMessage(error || 'Error setting threshold.');
            setShowModal(true); 
        });
    };

    const closeModal = () => {
        setShowModal(false);
        setModalMessage('');
    };

    return (
        <div className="sub-section">
            <h2>Set Thresholds for Health Metrics</h2>
            <form onSubmit={handleSubmit}>
                <div className="form-group">
                    <label>Metric Name:</label>
                    <select
                        value={metricName}
                        onChange={(e) => setMetricName(e.target.value)}
                        required
                    >
                        {healthMetrics.map((metric) => (
                            <option key={metric.value} value={metric.value}>
                                {metric.label}
                            </option>
                        ))}
                    </select>
                </div>
                <div className="form-group">
                    <label>Min Value:</label>
                    <input
                        type="number"
                        value={minValue}
                        onChange={(e) => setMinValue(e.target.value)}
                        required
                    />
                </div>
                <div className="form-group">
                    <label>Max Value:</label>
                    <input
                        type="number"
                        value={maxValue}
                        onChange={(e) => setMaxValue(e.target.value)}
                        required
                    />
                </div>
                <button type="submit">Submit</button>
            </form>

            {showModal && <Modal message={modalMessage} onClose={closeModal} />}
        </div>
    );
};

export default SetThresholdSection;
