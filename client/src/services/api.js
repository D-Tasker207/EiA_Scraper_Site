export const submitForm = async ({ data, sid }) => {
    console.log(data);
    console.log(sid);

    const response = await fetch('/api/mgn-scraper', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ data, sid })
    });

    if(!response.ok) {
        const errorReponse = await response.json();
        throw new Error(errorResponse.message || "Failed to submit form");
    };

    return await response.json();
};