import React from 'react';

const Uploader = ({ API_URL, resetState, setImageFilename, setIsLoading }) => {
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
    <div className="uploader">
      <label htmlFor="upload">Load image</label>
      <input id="upload" onChange={onUpload} type="file" />
    </div>
  );
}

export default Uploader;
