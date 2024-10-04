import React from 'react';

const MgnScraperForm = ({ handleSubmit, data, setData, error }) => {
    return (
        <form onSubmit={handleSubmit}>
            <div>
                <textarea
                    type="text"
                    name="image_ids"
                    value={data}
                    onChange={(e) => setData(e.target.value)}
                    placeholder="Enter Image IDs"
                    required
                    rows="4"
                    cols="40"
                />
            </div>
            <button type="submit">Submit</button>
            {error && <p style={{color: 'red'}}>{error}</p>}
        </form>
    );
};

export default MgnScraperForm;