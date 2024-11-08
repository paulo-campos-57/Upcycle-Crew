import styles from './Identifier.module.css';

function Identifier() {
    return (
        <>
            <div className={styles['identifier-container']}>
                <div className={styles['identifier-body']}>
                    <img className={styles['identifier-logo']} src='/images/logo.svg' alt='Logo do Banco do Brasil' />
                    <p className={styles.subtitle}>
                        <strong>Bem vindo</strong> ao descarte eletrônico do BB!
                    </p>
                    <p className={styles.question}>
                        Você gostria de se identificar?
                    </p>
                    <div className={styles['button-container']}>
                        <button className={styles['yes-button']}>Sim</button>
                        <button className={styles['no-button']}>Não</button>
                    </div>
                </div>
                <div className={styles['identifier-image']}><img src='./images/recycle.png' alt='Símbolo da reciclagem em tons de azul' /></div>
            </div>
        </>
    );
}

export default Identifier;