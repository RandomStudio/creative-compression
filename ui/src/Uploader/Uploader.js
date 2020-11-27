import React from 'react';

const API_URL = process.env.NODE_ENV === 'development' ? 'http://127.0.0.1:5000' : '';

const Uploader = ({ resetState, setImageFilename, setIsLoading }) => {
  const onUpload = async event => {
    setIsLoading(true);
    resetState();
    try {
      const response = await fetch(API_URL + '/upload', {
        method: 'POST',
        body: event.target.files[0]
      });
      const { filename } = await response.json();
      setImageFilename(filename);
    } catch(error) {
      console.error(error);
    }
    setIsLoading(false);
    event.preventDefault();
  };

  return (
      <input id="upload" onChange={onUpload} type="file" />
  );
}

export default Uploader;
