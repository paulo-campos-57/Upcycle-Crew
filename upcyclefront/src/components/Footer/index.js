import { useNavigate } from 'react-router-dom';
import styles from './Footer.module.css';

function Footer() {
    const navigate = useNavigate();

    const handleUserClick = () => {
        navigate('/send');
    }

    return (
        <>
            <div className={styles.container}>
                <div className={styles['footer-container']}>
                    <img className={styles.logo} src='/images/logo.svg' alt='Logo do Banco do brasil' />
                    <h2 className={styles.title} onClick={() => handleUserClick()}>Toque para começar</h2>
                </div>
            </div>
        </>
    );
}

export default Footer;
