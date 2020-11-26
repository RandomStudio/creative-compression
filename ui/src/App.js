import './App.css';
import React, { useCallback, useEffect, useRef, useState } from 'react';

const API_URL = process.env.NODE_ENV === 'development' ? 'http://127.0.0.1:5000' : '';

function App() {
  const canvasRef = useRef();
  const [image, setImage] = useState(null);
  const [imageFilename, setImageFilename] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const [drawRectContext, setDrawRectContext] = useState(null);
  const [savedShapes, setSavedShapes] = useState([]);
  const [shapeVisibility, setShapeVisibility] = useState([]);

  const onUpload = async event => {
    setIsLoading(true);
    const response = await fetch(API_URL + '/upload', {
      method: 'POST',
      body: event.target.files[0]
    });
    const { filename } = await response.json();
    console.log('has filename', filename)
    setIsLoading(false);
    setImageFilename(filename);
    event.preventDefault();
  };

  useEffect(() => {
    if (!imageFilename) {
      return;
    }
    setIsLoading(true);
    const img = new Image();
    img.src = savedShapes.length > 0 ? `${API_URL}/composition/${imageFilename}?boxes=${JSON.stringify(savedShapes)}&width=${canvasRef.current.width}` : `${API_URL}/static/uploads/${imageFilename}`;
    img.decoding = 'async';
    img.decode().then(() => {
      setImage(img);
      setIsLoading(false);
    });
  }, [imageFilename, savedShapes]);

  const getCanvasCoords = function (clientX, clientY) {
    var rect = canvasRef.current.getBoundingClientRect();

    return {
      x: clientX - rect.left,
      y: clientY - rect.top
    };
  };

  const refreshImage = useCallback(async (context) => {
    canvasRef.current.width = canvasRef.current.clientWidth;
    canvasRef.current.height = (canvasRef.current.clientWidth / image.width) * image.height
    context.drawImage(image, 0, 0, canvasRef.current.clientWidth, canvasRef.current.clientHeight);
  }, [image]);

  const refreshShapes = useCallback((context) => {
    savedShapes.map(([startX, startY, width, height], i) => {
      if (!shapeVisibility[i]) {
        return false;
      }
      context.strokeStyle = 'blue'
      context.strokeRect(startX, startY, width, height);
      return true;
    })
  }, [savedShapes, shapeVisibility]);


  const redrawCanvas = useCallback(async (sharedContext) => {
    if (!sharedContext && !canvasRef.current) {
      return;
    }
    const context = sharedContext ?? canvasRef.current.getContext('2d');
    context.clearRect(0, 0, canvasRef.current.width, canvasRef.current.height);
    refreshImage(context, image);
    refreshShapes(context);
  }, [image, refreshImage, refreshShapes]);

  useEffect(() => {
    redrawCanvas();
  }, [redrawCanvas, savedShapes, shapeVisibility]);

  const currentShapeRef = useRef([0, 0, 0, 0]);

  const onMouseDown = event => {
    const context = canvasRef.current.getContext('2d');
    setDrawRectContext(context);
    const coords = getCanvasCoords(event.clientX, event.clientY);
    currentShapeRef.current = [coords.x, coords.y, 0, 0];
  };

  const onMouseUp = event => {
    setDrawRectContext(null);
    setSavedShapes(state => [...state, currentShapeRef.current]);
    setShapeVisibility(state => [...state, true]);
  }

  const onMouseMove = event => {
    if (!drawRectContext) {
      return;
    }

    redrawCanvas(drawRectContext);

    const [startX, startY] = currentShapeRef.current;
    const coords = getCanvasCoords(event.clientX, event.clientY);
    const width = coords.x - startX;
    const height = coords.y - startY;

    drawRectContext.strokeStyle = 'blue'
    drawRectContext.strokeRect(startX, startY, width, height);
    currentShapeRef.current = [startX, startY, width, height]
  };

  const toggleShapeVisibility = index => {
    const updatedState = shapeVisibility.map((state, i) => i === index ? !state : state)
    setShapeVisibility(updatedState);
    redrawCanvas();
  }

  const deleteShape = index => {
    setSavedShapes(savedShapes.map((shape, i) => index === i ? false : shape).filter(exists => exists));
    setShapeVisibility(shapeVisibility.map((visibility, i) => index === i ? null : visibility).filter(state => state !== null));
  }

  return (
    <div className="page">
      <input id="upload" onChange={onUpload} type="file" />
      {isLoading && <div className="loader" />}
      {image && <canvas className="canvas" onMouseDown={onMouseDown} onMouseUp={onMouseUp} onMouseMove={onMouseMove} ref={canvasRef} />}
      <div className="sidebar">
        {shapeVisibility.map((isShapeVisible, index) => (
          <div className="row">
            <p>Box {index}</p>
          Enabled?
            <input type="checkbox" checked={isShapeVisible} onChange={() => toggleShapeVisibility(index)} />
            <button onClick={() => deleteShape(index)}>Delete</button>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
