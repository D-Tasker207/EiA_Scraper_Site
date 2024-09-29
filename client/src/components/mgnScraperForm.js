import React from 'react';

const MgnScraperForm = ({ handleSubmit, data, setData, error }) => {
    return (
        <form onSubmit={handleSubmit}>
            <div>
                <input
                    type="text"
                    name="image_ids"
                    value={image_ids}
                    onChange={(e) => setData(e.target.value)}
                    placeholder="Enter URL"
                    required
                />
            </div>
            <button type="submit">Submit</button>
            {error && <p style={{color: 'red'}}>{error}</p>}
        </form>
    );
};

export default MgnScraperForm;