import styles from './Register.module.css';

function Register() {
    return (
        <div className={styles['register-container']}>
            <div className={styles['register-body']}>
                <img className={styles['register-logo']} src='/images/logo.svg' alt='Logo do Banco do Brasil' />
                <h1 className={styles.title}>
                    Compartimento de reciclagem de resíduos eletrônicos
                </h1>
                <form className={styles['register-form']}>
                    <div className={styles['form-input']}>
                        <label>Cidade</label>
                        <input type='text' />
                    </div>
                    <div className={styles['form-input']}>
                        <label>Bairro</label>
                        <input type='text' />
                    </div>
                    <div className={styles['form-input']}>
                        <label>Rua</label>
                        <input type='text' />
                    </div>
                    <div className={styles['form-input']}>
                        <label>Número</label>
                        <input type='text' />
                    </div>
                </form>
            </div>
            <div className={styles['register-image']}><img src='./images/eletronic.png' alt='Imagens de eletrônicos envelhecidos'/></div>
        </div>
    );
}

export default Register;
