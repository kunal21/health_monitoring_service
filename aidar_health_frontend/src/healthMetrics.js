// src/constants/healthMetrics.js

export const healthMetrics = [
    { value: '', label: 'Select a health metric' },
    { value: 'heart_rate', label: 'Heart Rate' },
    { value: 'blood_pressure_systolic', label: 'Blood Pressure (Systolic)' },
    { value: 'blood_pressure_diastolic', label: 'Blood Pressure (Diastolic)' },
    { value: 'respiratory_rate', label: 'Respiratory Rate' },
    { value: 'oxygen_saturation', label: 'Oxygen Saturation' },
    { value: 'body_temperature', label: 'Body Temperature' },
    { value: 'blood_glucose', label: 'Blood Glucose' },
    { value: 'cholesterol_total', label: 'Total Cholesterol' },
    { value: 'cholesterol_hdl', label: 'HDL Cholesterol' },
    { value: 'cholesterol_ldl', label: 'LDL Cholesterol' },
    { value: 'triglycerides', label: 'Triglycerides' },
    { value: 'body_mass_index', label: 'Body Mass Index (BMI)' },
    { value: 'hemoglobin', label: 'Hemoglobin' },
    { value: 'white_blood_cell_count', label: 'White Blood Cell Count' },
    { value: 'red_blood_cell_count', label: 'Red Blood Cell Count' },
];

// Helper function to get label by value
export const getMetricLabel = (metricValue) => {
    const metric = healthMetrics.find(item => item.value === metricValue);
    return metric ? metric.label : metricValue;
};
