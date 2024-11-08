import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import styles from './Register.module.css';

function Register() {
    const [city, setCity] = useState('');
    const [neighborhood, setNeighborhood] = useState('');
    const [street, setStreet] = useState('');
    const [number, setNumber] = useState('');
    const [postalCode, setPostalCode] = useState('');

    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();

        const formData = {
            city,
            neighbourhood: neighborhood,  
            street,
            number,
            postal_code: postalCode,       
        };

        try {
            const response = await fetch('http://localhost:8000/create_unit/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData),
            });

            if (response.ok) {
                const data = await response.json();
                console.log('Response:', data);
                navigate('/begin');  // Redirect after successful submission
            } else {
                console.error('Error:', response.statusText); 
            }
        } catch (error) {
            console.error('Fetch error:', error);
        }
    };

    return (
        <div className={styles['register-container']}>
            <div className={styles['register-body']}>
                <img className={styles['register-logo']} src='/images/logo.svg' alt='Logo do Banco do Brasil' />
                <h1 className="text-3xl mt-6 text-blue-600">
                    Compartimento de reciclagem de resíduos eletrônicos
                </h1>
                <form className="flex flex-col gap-4 mt-8 w-5/6" onSubmit={handleSubmit}>
                    <div className={styles['form-input']}>
                        <label>Cidade</label>
                        <input
                            type="text"
                            className="w-1/2"
                            value={city}
                            onChange={(e) => setCity(e.target.value)}
                        />
                    </div>
                    <div className={styles['form-input']}>
                        <label>Bairro</label>
                        <input
                            type="text"
                            value={neighborhood}
                            onChange={(e) => setNeighborhood(e.target.value)}
                        />
                    </div>
                    <div className={styles['form-input']}>
                        <label>Rua</label>
                        <input
                            type="text"
                            value={street}
                            onChange={(e) => setStreet(e.target.value)}
                        />
                    </div>
                    <div className={styles['form-input']}>
                        <label>Número</label>
                        <input
                            type="text"
                            value={number}
                            onChange={(e) => setNumber(e.target.value)}
                        />
                    </div>
                    <div className={styles['form-input']}>
                        <label>CEP</label>
                        <input
                            type="text"
                            value={postalCode}
                            onChange={(e) => setPostalCode(e.target.value)}
                        />
                    </div>
                    <button type="submit" className="mt-4 p-2 bg-blue-500 text-white w-1/2 p-4 rounded-lg">
                        Enviar
                    </button>
                </form>
            </div>
            <div className={styles['register-image']}>
                <img className="w-1/2 h-full" src='./images/eletronic.png' alt='Imagens de eletrônicos envelhecidos' />
            </div>
        </div>
    );
}

export default Register;
