import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import styles from "./Recieved.module.css";

function Recieved() {
    const navigate = useNavigate();

    const [foundType, setFoundType] = useState('item');

    useEffect(() => {
        const type = localStorage.getItem('foundType');
        if (type) {
            setFoundType(type);
        }
    }, []);

    const goBack = () => {
        navigate('/camera')
    }

    return (
        <>
            <div className={styles['recieved-container']}>
                <img className={styles['recieved-logo']} src='/images/logo.svg' alt='Logo do Banco do Brasil' />
                <p className='text-6xl w-1/2 text-center text-blue-600'>
                    Você está descartando um: <strong>{foundType}</strong>
                </p>
                <p className={styles.text}>
                    Você confirma?
                </p>
                <div className={styles['button-container']}>
                    <button className={styles['yes-button']}>Sim</button>
                    <button className={styles['no-button']} onClick={() => goBack()}>Não</button>
                </div>
            </div>
        </>
    );
}

export default Recieved;