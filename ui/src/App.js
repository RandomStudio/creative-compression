import './App.css';
import React, { useState } from 'react';
import Uploader from './Uploader/Uploader';
import Sidebar from './Sidebar/Sidebar';
import Canvas from './Canvas/Canvas';


function App() {
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
      {isLoading && <div className="loader" />}
      <div className="main">
        <Canvas imageFilename={imageFilename} savedShapes={savedShapes} shapeVisibilities={shapeVisibilities} setIsLoading={setIsLoading} setSavedShapes={setSavedShapes} setShapeVisibilities={setShapeVisibilities} />
      </div>
      <div className="sidebar">
        <Uploader resetState={resetState} setImageFilename={setImageFilename} setIsLoading={setIsLoading} />
        <Sidebar shapeVisibilities={shapeVisibilities} setShapeVisibilities={setShapeVisibilities} savedShapes={savedShapes} /> 
      </div>
    </div>
  );
}

export default App;
