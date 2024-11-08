'use client';

import React, { useEffect, useRef, useState } from 'react';
import { Camera, X, Camera as CameraIcon } from "lucide-react";

export default function Component() {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [isStreaming, setIsStreaming] = useState(false);
  const [error, setError] = useState('');
  const [isCaptureDisabled, setIsCaptureDisabled] = useState(true);

  const startCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: {
          aspectRatio: 16 / 9,
          facingMode: 'user',
        },
      });

      if (videoRef.current) {
        videoRef.current.srcObject = stream;
        setIsStreaming(true);
        setError('');
        setIsCaptureDisabled(false);
      }
    } catch (err) {
      setError('Não foi possível acessar a câmera. Por favor, verifique se você concedeu permissão.');
      console.error('Erro ao acessar a câmera:', err);
    }
  };

  const stopCamera = () => {
    if (videoRef.current && videoRef.current.srcObject) {
      const tracks = videoRef.current.srcObject.getTracks();
      tracks.forEach((track) => track.stop());
      videoRef.current.srcObject = null;
      setIsStreaming(false);
      setIsCaptureDisabled(true);
    }
  };

  const captureImage = async () => {
    if (videoRef.current && canvasRef.current) {
      const video = videoRef.current;
      const canvas = canvasRef.current;
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      const context = canvas.getContext('2d');
      if (context) {
        context.drawImage(video, 0, 0, canvas.width, canvas.height);
      }

      canvas.toBlob(async (blob) => {
        if (blob) {
          const cpf = localStorage.getItem('cpf');
          const unitId = localStorage.getItem('unitId');

          if (!cpf || !unitId) {
            setError('CPF ou unitId não encontrados no localStorage.');
            return;
          }

          const url = `http://localhost:8000/receive_image/5/`;

          const formData = new FormData();
          formData.append('cpf', cpf);
          formData.append('image', blob, 'photo.jpg');
          console.log('Tamanho do blob:', blob.size);


          try {
            const response = await fetch(url, {
              method: 'POST',
              body: formData,
            });

            if (response.ok) {
              console.log('Imagem enviada com sucesso');
            } else {
              console.error('Falha ao enviar a imagem');
            }
          } catch (error) {
            console.error('Erro ao enviar a imagem:', error);
          }
        } else {
          console.error('Erro ao capturar a imagem.');
        }
      }, 'image/jpeg');
    }
  };

  useEffect(() => {
    return () => {
      stopCamera();
    };
  }, []);

  return (
    <div className="min-h-screen w-full flex flex-col items-center justify-center p-4">
      <div className="w-[75%] h-[95%]">
        <div className="aspect-video rounded-lg overflow-hidden border-2 border-blue-500">
          <video
            ref={videoRef}
            autoPlay
            playsInline
            className="w-full h-full object-cover bg-black"
          />
          {error && (
            <div className="absolute inset-0 flex items-center justify-center bg-black/80 text-white p-4 text-center">
              {error}
            </div>
          )}
        </div>
        <div className="flex justify-center gap-2 mt-4">
          {!isStreaming ? (
            <button
              onClick={startCamera}
              className="flex items-center gap-2 px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50 transition-colors"
            >
              <Camera className="w-4 h-4" />
              Iniciar câmera
            </button>
          ) : (
            <button
              onClick={stopCamera}
              className="flex items-center gap-2 px-4 py-2 bg-red-500 text-white rounded-md hover:bg-red-600 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-opacity-50 transition-colors"
            >
              <X className="w-4 h-4" />
              Parar câmera
            </button>
          )}
          <button
            onClick={captureImage}
            disabled={isCaptureDisabled}
            className="flex items-center gap-2 px-6 py-3 bg-green-500 text-white text-lg font-semibold rounded-md hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-opacity-50 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <CameraIcon className="w-6 h-6" />
            Tirar foto
          </button>
        </div>
      </div>
      <canvas ref={canvasRef} style={{ display: 'none' }} />
    </div>
  );
}
