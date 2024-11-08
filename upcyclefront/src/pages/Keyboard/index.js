import React, { useState, useEffect } from 'react';

function Keyboard() {
    const [cpf, setCpf] = useState('');

    useEffect(() => {
        localStorage.setItem('cpf', formatCpf(cpf));
    }, [cpf]);

    const handleNumberClick = (number) => {
        if (cpf.length < 11) {
            setCpf(prevCpf => prevCpf + number);
        }
    };

    const handleDelete = () => {
        setCpf(prevCpf => prevCpf.slice(0, -1));
    };

    const formatCpf = (value) => {
        return value.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, "$1.$2.$3-$4");
    };

    return (
        <div className="h-screen flex flex-col items-center justify-center">
            <div className='w-11/12 flex flex-col items-center justify-center h-5/6 justify-between'>
                <div className='flex flex-col gap-6 w-[49%] items-center justify-center'>
                    <h1 className='text-blue-600 text-4xl '>Digite aqui seu CPF</h1>
                    <input 
                        className='w-full h-16 rounded-lg text-center text-2xl bg-gray-200'
                        type='text'
                        value={cpf.length > 0 ? formatCpf(cpf) : ''}
                        readOnly
                        placeholder='000.000.000-00'
                    />
                </div>
                
                <div className='grid grid-cols-3 grid-rows-4 h-5/6 w-1/2 mt-8 gap-4'>
                    {[1, 2, 3, 4, 5, 6, 7, 8, 9, 0].map((number, index) => (
                        <button
                            key={index}
                            className={`w-full h-full bg-[#0047B6] rounded-lg text-2xl font-semibold`}
                            onClick={() => handleNumberClick(number)}
                            style={{
                                transition: 'transform 0.2s ease',
                            }}
                            onMouseEnter={(e) => (e.currentTarget.style.transform = 'scale(1.05)')}
                            onMouseLeave={(e) => (e.currentTarget.style.transform = 'scale(1)')}
                        >
                            {number}
                        </button>
                    ))}
                    {cpf.length > 0 && (
                        <button
                            className='w-full h-full bg-red-600 rounded-lg text-2xl font-semibold'
                            onClick={handleDelete}
                            style={{
                                transition: 'transform 0.2s ease',
                            }}
                            onMouseEnter={(e) => (e.currentTarget.style.transform = 'scale(1.05)')}
                            onMouseLeave={(e) => (e.currentTarget.style.transform = 'scale(1)')}
                        >
                            Apagar
                        </button>
                    )}
                </div>
            </div>
        </div>
    );
}

export default Keyboard;
