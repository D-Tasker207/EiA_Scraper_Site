import { useState } from 'react';
import { submitForm } from '../services/api';

const useForm = () => {
    const [data, setData] = useState('');
    const [error, setError] = useState('');

    const validate = () => {
        if(!data) {
            setError('Please Enter comma separated image ids');
            return false;
        } else if(!data.match(/^[0-9, ]+$/)) {
            setError('Invalid characters found in input: Please enter comma separated numbers only');
            return false;
        } else if(!data.match(/([0-9]{6}, ?)*[0-9]{6}$/)) {
            setError('Invalid ID sequence: please entered comma separated 6 digit ID numbers');
            return false;
        }
    }

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');

        if(!validate()) return;

        try {
            const result = await submitForm({ data });
            setMessage(result.message);
        } catch (error) {
            setError(err.message || 'An error occurred');
        }
    };

    return {
        data,
        setData,
        error,
        handleSubmit
    };
};

export default useForm;