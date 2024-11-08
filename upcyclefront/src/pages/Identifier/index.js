import styles from './Identifier.module.css';

function Identifier() {
    return(
        <>
            <div className={styles['identifier-body']}>
                <h1 className={styles.question}>
                    ?
                </h1>
                <h2 className={styles.subtitle}>
                    Gostaria de se identificar?
                </h2>
                <div className={styles['button-container']}>
                    <button className={styles['yes-button']}>SIM</button>
                    <button className={styles['no-button']}>NÃO</button>
                </div>
            </div>
        </>
    );
}

export default Identifier;