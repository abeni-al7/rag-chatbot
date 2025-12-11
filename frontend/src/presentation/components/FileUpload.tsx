import React, { useState, useRef } from 'react';
import { Upload, File, X, CheckCircle, AlertCircle } from 'lucide-react';
import { Button } from './Button';
import { uploadDocument } from '../../data/api';

export const FileUpload: React.FC = () => {
    const [selectedFile, setSelectedFile] = useState<File | null>(null);
    const [isUploading, setIsUploading] = useState(false);
    const [status, setStatus] = useState<'idle' | 'success' | 'error'>('idle');
    const [errorMessage, setErrorMessage] = useState<string>('');
    const fileInputRef = useRef<HTMLInputElement>(null);

    const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
        const file = event.target.files?.[0];
        if (file) {
            if (file.type !== 'application/pdf') {
                setStatus('error');
                setErrorMessage('Please select a PDF file.');
                return;
            }
            setSelectedFile(file);
            setStatus('idle');
            setErrorMessage('');
        }
    };

    const handleUpload = async () => {
        if (!selectedFile) return;

        setIsUploading(true);
        setStatus('idle');
        setErrorMessage('');

        try {
            await uploadDocument(selectedFile);
            setStatus('success');
            setSelectedFile(null);
            if (fileInputRef.current) {
                fileInputRef.current.value = '';
            }
        } catch (error: any) {
            setStatus('error');
            const msg = error.response?.data?.detail || 'Failed to upload document. Please try again.';
            setErrorMessage(msg);
            console.error('Upload error:', error);
        } finally {
            setIsUploading(false);
        }
    };

    const clearSelection = () => {
        setSelectedFile(null);
        setStatus('idle');
        setErrorMessage('');
        if (fileInputRef.current) {
            fileInputRef.current.value = '';
        }
    };

    return (
        <div className="w-full max-w-md p-6 bg-white rounded-xl shadow-sm border border-gray-100">
            <h3 className="text-lg font-semibold text-gray-800 mb-4">Upload Document</h3>
            
            <div className="space-y-4">
                <input
                    type="file"
                    ref={fileInputRef}
                    onChange={handleFileSelect}
                    accept=".pdf"
                    className="hidden"
                />

                {!selectedFile ? (
                    <div 
                        onClick={() => fileInputRef.current?.click()}
                        className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center cursor-pointer hover:border-blue-500 hover:bg-blue-50 transition-colors duration-200"
                    >
                        <div className="flex flex-col items-center space-y-2">
                            <div className="p-3 bg-blue-100 rounded-full text-blue-600">
                                <Upload size={24} />
                            </div>
                            <p className="text-sm font-medium text-gray-700">
                                Click to upload PDF
                            </p>
                            <p className="text-xs text-gray-500">
                                PDF files only
                            </p>
                        </div>
                    </div>
                ) : (
                    <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg border border-gray-200">
                        <div className="flex items-center space-x-3 overflow-hidden">
                            <div className="p-2 bg-white rounded-lg border border-gray-200 text-red-500">
                                <File size={20} />
                            </div>
                            <span className="text-sm font-medium text-gray-700 truncate">
                                {selectedFile.name}
                            </span>
                        </div>
                        <button 
                            onClick={clearSelection}
                            className="p-1 hover:bg-gray-200 rounded-full text-gray-500 transition-colors"
                            disabled={isUploading}
                        >
                            <X size={18} />
                        </button>
                    </div>
                )}

                {selectedFile && (
                    <Button 
                        onClick={handleUpload} 
                        isLoading={isUploading}
                        className="w-full"
                    >
                        Upload Document
                    </Button>
                )}

                {status === 'success' && (
                    <div className="flex items-center space-x-2 text-green-600 bg-green-50 p-3 rounded-lg text-sm">
                        <CheckCircle size={18} />
                        <span>Document uploaded successfully!</span>
                    </div>
                )}

                {status === 'error' && (
                    <div className="flex items-center space-x-2 text-red-600 bg-red-50 p-3 rounded-lg text-sm">
                        <AlertCircle size={18} />
                        <span>{errorMessage}</span>
                    </div>
                )}
            </div>
        </div>
    );
};
