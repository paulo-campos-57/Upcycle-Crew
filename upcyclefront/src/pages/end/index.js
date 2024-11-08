import { useEffect, useState } from 'react';

export default function EndPage() {
    const [finished, setFinished] = useState(false);

    useEffect(() => {
        const timer = setTimeout(() => {
            setFinished(true);
        }, 5000); // 5 seconds

        // Cleanup the timer if the component unmounts
        return () => clearTimeout(timer);
    }, []);

    return (
        <div className="bg-white flex flex-col items-center justify-center gap-8 h-screen w-full">
            {finished ? (
                <h1 className="text-blue-600 text-4xl">Operação Finalizada</h1>
            ) : (
                <>
                    <img src="/images/logo.svg" alt="Logo" />
                    <h1 className="text-blue-600 w-1/2 text-center text-6xl font-bold">
                        <span className="text-yellow-400">Obrigado</span> pela sua contribuição!
                    </h1>
                    <p className="text-blue-600 text-center text-2xl">
                        Sua ajuda ao planeta acumulou <span className="text-yellow-400">xxx</span> pontos livelo.
                    </p>
                </>
            )}
        </div>
    );
}
