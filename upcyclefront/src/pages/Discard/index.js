import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

function Discard() {
    const navigate = useNavigate();

    useEffect(() => {
        const timer = setTimeout(() => {
            navigate('/end');
        }, 5000);

        return () => clearTimeout(timer);
    }, [navigate]);

    return (
        <div className='h-screen w-full px-[64px] py-[36px] flex flex-col gap-28'>
            <img src='/images/logo.svg' className="w-[85px]" alt="Logo" />
            <p className="text-blue-600 text-5xl w-1/2">Deposite seus descartes abaixo!</p>
            <p className="text-gray-600 text-3xl">Aguardando depósito...</p>
            <img src='/images/Arrow.png' className="absolute right-0 top-0" alt="Arrow" />
        </div>
    );
}

export default Discard;
