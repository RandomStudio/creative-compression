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
  const [hasVisibleBorders, setHasVisibleBorders] = useState(false);

  const [steps, setSteps] = useState([]);
  const [distances, setDistances] = useState([]);

  const resetState = async event => {
    setImageFilename(null);
    setSavedShapes([]);
    setSteps([]);
    setDistances([]);
  };

  const addShape = shape => {
    setSavedShapes([...savedShapes, shape]);
    setDistances([...distances, 5]);
    setSteps([...steps, 5]);
  }

  const removeFromArray = (array, index) => array.map((value, i) => index === i ? false : value).filter(exists => exists)
  const deleteShape = index => {
    setDistances(removeFromArray(distances, index));
    setSteps(removeFromArray(steps, index));
    setSavedShapes(removeFromArray(savedShapes, index));
  }

  const imageUrl = (isPreview = true) => savedShapes.length > 0 
    ? `${API_URL}/composition/${isPreview ? 'preview_' : ''}${imageFilename}?boxes=${JSON.stringify(savedShapes)}&width=${canvasRef.current.width}&showBorders=${hasVisibleBorders}&steps=${JSON.stringify(steps)}&distances=${JSON.stringify(distances)}`
    : `${API_URL}/static/uploads/preview_${imageFilename}`;

  return (
    <div className="page">
      <div className="main">
        <Canvas
          addShape={addShape}
          canvasRef={canvasRef}
          imageUrl={imageFilename ? imageUrl() : null}
          savedShapes={savedShapes}
          setIsLoading={setIsLoading}
        />
        {isLoading && <div className="loader" />}
      </div>
      <div className="sidebar">
        <Sidebar
          deleteShape={deleteShape}
          distances={distances}
          hasVisibleBorders={hasVisibleBorders}
          savedShapes={savedShapes}
          setDistances={setDistances}
          setHasVisibleBorders={setHasVisibleBorders}
          setSteps={setSteps}
          steps={steps}
        /> 
        <Uploader API_URL={API_URL} resetState={resetState} setImageFilename={setImageFilename} setIsLoading={setIsLoading} />
        <button className="finder" disabled>Find objects in image</button>
        <a href={imageUrl(false)} target="_blank" className="downloader">Save high quality</a>
      </div>
    </div>
  );
}

export default App;
