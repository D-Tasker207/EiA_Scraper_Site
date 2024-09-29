export const submitForm = async ({ data }) => {
    const response = await fetch('/api/mgn-scraper', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ data })
    });

    if(!response.ok) {
        const errorReponse = await response.json();
        throw new Error(errorResponse.message || "Failed to submit form");
    };

    return await response.json();
};