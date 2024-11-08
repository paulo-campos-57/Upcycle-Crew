import Footer from "../../components/Footer";
import styles from "./Home.module.css";

function Home() {

    return (
        <>
            <img src="/images/pexels.jpg" className={styles.image} alt="Ilustração digital aconchegante de uma família em um ambiente de oficina ou laboratório caseiro. Uma família de quatro pessoas - pai, mãe e dois filhos pequenos - estão debruçados sobre uma mesa de trabalho repleta de dispositivos eletrônicos desmontados. O pai usa óculos e uma camisa azul marinho, enquanto a mãe e as crianças vestem blusas verdes. Todos estão concentrados em um projeto que emite uma luz verde brilhante no centro da mesa. Há um laptop aberto ao lado e várias caixas organizadoras com peças eletrônicas nas prateleiras ao fundo. A cena é iluminada por uma grande janela industrial que cria uma atmosfera azulada e nostálgica." />
            <Footer />
        </>
    );
}

export default Home;