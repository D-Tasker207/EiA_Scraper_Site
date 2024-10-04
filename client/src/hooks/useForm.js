import { useState } from 'react';
import { submitForm } from '../services/api';
import { connectSocket, getSocketId, disconnectSocket } from '../services/websocket';

const useForm = () => {
    const [data, setData] = useState('');
    const [message, setMessage] = useState('');
    const [progress, setProgress] = useState(0);
    const [error, setError] = useState('');
    const [downloadLink, setDownloadLink] = useState('');

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
        return true;
    }

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');

        if(!validate()) return;

        try {
            await connectSocket(setProgress, setMessage, setDownloadLink);
            const sid = getSocketId();
            setDownloadLink('');

            if(!sid) {
                throw new Error('Failed to connect to websocket');
            }
            
            const result = await submitForm({ data, sid });
            // setMessage(result.message);
        } catch (err) {
            setError(err.message || 'An error occurred');
            disconnectSocket();
        }
    };

    return {
        data,
        setData,
        message,
        progress,
        downloadLink,
        error,
        handleSubmit
    };
};

export default useForm;