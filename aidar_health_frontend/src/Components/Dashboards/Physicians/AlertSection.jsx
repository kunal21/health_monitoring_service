import React from 'react';
import './Dashboard.css';

function AlertSection({ alerts, setAlerts }) {

    // Acknowledge alert
    const acknowledgeAlert = async (alertId) => {
        await fetch('http://localhost:5000/api/acknowledge-alert', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ alert_id: alertId }),
        });
        setAlerts(alerts.filter(alert => alert.id !== alertId));
    };

    return (
        <div>
            <h1>Alerts Management</h1>
            <h4>(Unacknowledged Alerts: {alerts.length})</h4>
            <div className='sub-section'>
                { alerts.length === 0 ? (
                    <p>No Alerts</p>
                ) : (
                    <table className='sub-section-table-alert'>
                        <tr>
                            <th>Patient Name</th>
                            <th>Patient Age</th>
                            <th>Metric Name</th>
                            <th>Metric Value</th>
                            <th>Time</th>
                            <th>Action</th>
                        </tr>
                            {
                            alerts.map((alert) => (
                                <tr>
                                    <td>{alert.patient_name}</td>
                                    <td>{alert.patient_age}</td>
                                    <td>{alert.metric_name_label}</td>
                                    <td>{alert.value}</td>
                                    <td>{alert.timestamp}</td>
                                    <td>
                                        <button 
                                            onClick={() => acknowledgeAlert(alert.id)}>Acknowledge
                                        </button>
                                    </td>
                                </tr>
                        ))}
                    </table>
                ) }
            </div>
        </div>
    );
}

export default AlertSection;
