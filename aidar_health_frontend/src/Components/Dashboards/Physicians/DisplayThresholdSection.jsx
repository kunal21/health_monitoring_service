
import React from 'react';
import { getMetricLabel } from '../../../healthMetrics';

function DisplayThresholdSection({thresholds}) {
    return (
        <div className='sub-section'>
            <h3>Current Threshold Values</h3>
            { thresholds && thresholds.length > 0 ? (
                <table className='sub-section-table'>
                    <tr>
                        <th>Metric Name</th>
                        <th>Min Value</th>
                        <th>Max Value</th>
                    </tr>
                    {thresholds.map((threshold, index) => (
                        <tr>
                            <td>{getMetricLabel(threshold.metric_name)}</td>
                            <td>{threshold.min_value}</td>
                            <td>{threshold.max_value}</td>
                        </tr>
                    ))}
                </table>
            ) : (
                <p>No thresholds set yet</p>
            )}
        </div>
    )
}

export default DisplayThresholdSection;