import './App.css';
import React, { useRef, useState } from 'react';
import Uploader from './Uploader/Uploader';
import Sidebar from './Sidebar/Sidebar';
import Canvas from './Canvas/Canvas';

const API_URL = process.env.NODE_ENV === 'development' ? 'http://127.0.0.1:5000' : '';

function App() {
  const canvasRef = useRef();
  const [imageFilename, setImageFilename] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const [savedShapes, setSavedShapes] = useState([]);
  const [shapeVisibilities, setShapeVisibilities] = useState([]);

  const resetState = async event => {
    setImageFilename(null);
    setSavedShapes([]);
    setShapeVisibilities([]);
  };

  return (
    <div className="page">
      <div className="main">
        <Canvas canvasRef={canvasRef} imageFilename={imageFilename} savedShapes={savedShapes} shapeVisibilities={shapeVisibilities} setIsLoading={setIsLoading} setSavedShapes={setSavedShapes} setShapeVisibilities={setShapeVisibilities} />
        {isLoading && <div className="loader" />}
      </div>
      <div className="sidebar">
        <Sidebar shapeVisibilities={shapeVisibilities} setShapeVisibilities={setShapeVisibilities} savedShapes={savedShapes} setSavedShapes={setSavedShapes} /> 
        <Uploader API_URL={API_URL} resetState={resetState} setImageFilename={setImageFilename} setIsLoading={setIsLoading} />
        <a href={`${API_URL}/composition/${imageFilename}?boxes=${JSON.stringify(savedShapes)}&width=${canvasRef?.current?.width}`} target="_blank" className="downloader">Save high quality</a>
      </div>
    </div>
  );
}

export default App;
