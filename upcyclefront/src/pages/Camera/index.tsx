'use client'

import React from 'react'
import { useEffect, useRef, useState } from 'react'
import { Camera, X, Camera as CameraIcon } from "lucide-react"

export default function Component() {
  const videoRef = useRef<HTMLVideoElement>(null)
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const [isStreaming, setIsStreaming] = useState(false)
  const [error, setError] = useState<string>('')
  const [isCaptureDisabled, setIsCaptureDisabled] = useState(true)

  const startCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: {
          aspectRatio: 16/9,
          facingMode: 'user'
        }
      })
      
      if (videoRef.current) {
        videoRef.current.srcObject = stream
        setIsStreaming(true)
        setError('')
        setIsCaptureDisabled(false)
      }
    } catch (err) {
      setError('Unable to access camera. Please ensure you have granted camera permissions.')
      console.error('Error accessing camera:', err)
    }
  }

  const stopCamera = () => {
    if (videoRef.current?.srcObject) {
      const tracks = (videoRef.current.srcObject as MediaStream).getTracks()
      tracks.forEach(track => track.stop())
      videoRef.current.srcObject = null
      setIsStreaming(false)
      setIsCaptureDisabled(true)
    }
  }

  const captureImage = async () => {
    if (videoRef.current && canvasRef.current) {
      const video = videoRef.current
      const canvas = canvasRef.current
      canvas.width = video.videoWidth
      canvas.height = video.videoHeight
      canvas.getContext('2d')?.drawImage(video, 0, 0, canvas.width, canvas.height)
      
      const imageDataUrl = canvas.toDataURL('image/jpeg')
      
      try {
        const response = await fetch('/api/upload-image', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ image: imageDataUrl }),
        })
        
        if (response.ok) {
          console.log('Image uploaded successfully')
        } else {
          console.error('Failed to upload image')
        }
      } catch (error) {
        console.error('Error uploading image:', error)
      }
    }
  }

  useEffect(() => {
    return () => {
      stopCamera()
    }
  }, [])

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
  )
}