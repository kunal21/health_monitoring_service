// src/Components/Dashboards/Physician/MainDashboard.jsx
import React, { useState, useEffect, useRef } from 'react';
import AlertSection from './AlertSection';
import ThresholdSection from './ThresholdSection'
import './Dashboard.css'; // Import CSS
import { useNavigate } from 'react-router-dom';
import { getMetricLabel } from '../../../healthMetrics'; 
import io from 'socket.io-client';

function MainDashboard() {
    const [alerts, setAlerts] = useState([]);
    const [thresholds, setThresholds] = useState([]);
    const navigate = useNavigate();
    const sessionExpiredRef = useRef(false);

    const fetchWithSessionCheck = (url, options, navigate) => {
        return fetch(url, options)
            .then(response => {
                if (response.status === 401 && !sessionExpiredRef.current) {
                    // Redirect to login only once
                    sessionExpiredRef.current = true;
                    alert('Session Expired. Login Again');
                    navigate('/login');
                    throw new Error('Session Expired');
                }
                if (!response.ok) {
                    return response.json().then(errorData => {
                        throw new Error(errorData.error || 'Failed to fetch data');
                    });
                }
                return response.json();
            });
    };
    

    // Fetch unacknowledged alerts from the DB
    const fetchAlerts = () => {
        fetchWithSessionCheck('http://localhost:5000/api/alerts', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include',
        }, navigate)
        .then(data => {
            const alertWithLabels = data.map(alert => ({
                ...alert, 
                metric_name_label: getMetricLabel(alert.metric_name)
            }));
            setAlerts(alertWithLabels);
        })
        .catch(error => {
            console.error('Error fetching alerts:', error);
        });
    };

    // Fetch already set threshold values
    const fetchThresholds = () => {
        fetchWithSessionCheck('http://localhost:5000/api/threshold/', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include',
        }, navigate)
        .then(data => setThresholds(data))
        .catch(error => {
            console.error('Error fetching thresholds:', error);
        });
    };

    useEffect(() => {
        fetchAlerts();
        fetchThresholds();
    
        const socket = io('http://localhost:5000', {
            withCredentials: true, 
        });

        // Join WebSocket room for this physician
        socket.emit('join');
        
        // Listen for new alerts
        socket.on('new_alert', (alertData) => {
            if (alertData.alert) {
                const mergedAlert = {
                    ...alertData.alert,
                    metric_name_label: getMetricLabel(alertData.alert.metric_name),
                    patient_age: alertData.patient_age,
                    patient_name: alertData.patient_name
                };
                setAlerts((prevAlerts) => [mergedAlert, ...prevAlerts]);
            }
        });

        // Handle session expiration
        socket.on('connect_error', (error) => {
            if (error.message === 'Unauthorized' && !sessionExpiredRef.current) {
                sessionExpiredRef.current = true;
                alert('Session Expired in Socket. Login Again');
                navigate('/login');
            }
        });

        // Cleanup socket connection when the component unmounts
        return () => {
            socket.off('new_alert');
            socket.close();
        };
    }, [navigate]);

    return (
        <div className="dashboard-container">
            <div className="section-wrapper">
                <ThresholdSection thresholds={thresholds} setThresholds={setThresholds}/>
            </div>
            <div className="section-wrapper">
                <AlertSection alerts={alerts} setAlerts={setAlerts} />
            </div>
        </div>
    );
}

export default MainDashboard;
