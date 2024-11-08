import { useEffect, useState } from 'react';

export default function EndPage() {
    const [finished, setFinished] = useState(false);
    const [points, setPoints] = useState(null);

    useEffect(() => {
        // Função assíncrona para realizar o fetch e obter os pontos
        const fetchPoints = async () => {
            try {
                // Obtém o valor de 'category' do localStorage
                const category = localStorage.getItem('foundType');

                // Faz a requisição para a API
                const response = await fetch('http://localhost:8000/livelo_points/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ category }), // Envia a categoria como body
                });

                const data = await response.json();
                setPoints(data.points); // Define os pontos com o valor retornado pelo backend
            } catch (error) {
                console.error("Erro ao buscar pontos:", error);
            }
        };

        fetchPoints();

        const timer = setTimeout(() => {
            setFinished(true);
        }, 5000); // 5 segundos

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
                        Sua ajuda ao planeta acumulou <span className="text-yellow-400">{points ?? '...'}</span> pontos livelo.
                    </p>
                </>
            )}
        </div>
    );
}
