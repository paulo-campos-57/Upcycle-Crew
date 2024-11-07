import React, { useState } from 'react';
import Footer from '../../components/Footer';

function ImageUpload() {
    const [selectedImage, setSelectedImage] = useState(null);
    const [responseMessage, setResponseMessage] = useState('');

    const handleImageChange = (e) => {
        setSelectedImage(e.target.files[0]);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!selectedImage) {
            setResponseMessage('Please select an image first.');
            return;
        }

        const formData = new FormData();
        formData.append('image', selectedImage);

        try {
            const response = await fetch('http://localhost:8000/receive_image/', {
                method: 'POST',
                body: formData,
                headers: {
                    'Accept': 'application/json',
                },
            });

            if (response.ok) {
                const data = await response.json();
                setResponseMessage(`Response: ${JSON.stringify(data)}`);
            } else {
                const errorData = await response.json();
                setResponseMessage(`Error: ${errorData.error}`);
            }
        } catch (error) {
            setResponseMessage(`Error: ${error.message}`);
        }
    };

    return (
        <div>
            <h1>Upload an Image</h1>
            <form onSubmit={handleSubmit}>
                <input type="file" onChange={handleImageChange} accept="image/*" />
                <button type="submit">Upload</button>
            </form>
            {responseMessage && <p>{responseMessage}</p>}
            <Footer />
        </div>
    );
}

export default ImageUpload;
