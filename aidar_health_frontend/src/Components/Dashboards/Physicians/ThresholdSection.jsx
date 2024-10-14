import React from 'react';
import SetThresholdSection from './SetThresholdSection';
import DisplayThresholdSection from './DisplayThresholdSection';

const ThresholdSection = ({ thresholds, setThresholds }) => {

    // Updates the thresholds useState hook with the newly added threshold 
    const addThresholdToState = (newThreshold) => {
        setThresholds((prevThresholds) => {
        
        const index = prevThresholds.findIndex(threshold => threshold.metric_name === newThreshold.metric_name);

        if (index !== -1) {
            // If it exists, replace the existing threshold with the updated one
            const updatedThresholds = [...prevThresholds];
            updatedThresholds[index] = newThreshold;
            return updatedThresholds;
        } else {
            // If it doesn't exist, add the new threshold
            return [...prevThresholds, newThreshold];
        }
        });
    };

    return (
        <div>
            <h1>Threshold Management</h1>
                <div>
                    <SetThresholdSection addThresholdToState={addThresholdToState} /> 
                    <DisplayThresholdSection thresholds={thresholds} /> 
                </div>
        </div>
    );
}

export default ThresholdSection;