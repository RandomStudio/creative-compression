import React, { useCallback, useEffect, useRef, useState } from 'react';

const API_URL = process.env.NODE_ENV === 'development' ? 'http://127.0.0.1:5000' : '';

const Canvas = ({ imageFilename, savedShapes, shapeVisibilities, setIsLoading, setSavedShapes, setShapeVisibilities }) => {
  const currentShapeRef = useRef([0, 0, 0, 0]);

  const [image, setImage] = useState(null);
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
  }, [imageFilename, savedShapes, setIsLoading]);


  const [drawRectContext, setDrawRectContext] = useState(null);
  const canvasRef = useRef();
  const refreshImage = useCallback(async (context) => {
    if (!image) {
      return;
    }
    canvasRef.current.width = canvasRef.current.clientWidth;
    canvasRef.current.height = (canvasRef.current.clientWidth / image.width) * image.height
    context.drawImage(image, 0, 0, canvasRef.current.clientWidth, canvasRef.current.clientHeight);
  }, [image]);

  const refreshShapes = useCallback((context) => {
    savedShapes.map(([startX, startY, width, height], i) => {
      if (!shapeVisibilities[i]) {
        return false;
      }
      context.strokeStyle = 'blue'
      context.strokeRect(startX, startY, width, height);
      return true;
    })
  }, [savedShapes, shapeVisibilities]);


  const redrawCanvas = useCallback(async (sharedContext) => {
    if (!sharedContext && !canvasRef.current) {
      return;
    }
    const context = sharedContext ?? canvasRef.current.getContext('2d');
    context.clearRect(0, 0, canvasRef.current.width, canvasRef.current.height);
    refreshImage(context);
    refreshShapes(context);
  }, [refreshImage, refreshShapes]);

  useEffect(() => {
    redrawCanvas();
  }, [redrawCanvas, savedShapes, shapeVisibilities]);

  const getCanvasCoords = function (clientX, clientY) {
    var rect = canvasRef.current.getBoundingClientRect();

    return {
      x: clientX - rect.left,
      y: clientY - rect.top
    };
  };

  const onMouseDown = event => {
    const context = canvasRef.current.getContext('2d');
    setDrawRectContext(context);
    const coords = getCanvasCoords(event.clientX, event.clientY);
    currentShapeRef.current = [coords.x, coords.y, 0, 0];
  };

  const onMouseUp = event => {
    setDrawRectContext(null);
    if (!currentShapeRef.current[2] === 0 || currentShapeRef.current[3] === 0) {
      return;
    }
    setSavedShapes(state => [...state, currentShapeRef.current]);
    setShapeVisibilities(state => [...state, true]);
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

  const onMouseLeave = () => {
    if (drawRectContext) {
      onMouseUp();
      return;
    }
  }

  return (
    <canvas className="canvas" onMouseDown={onMouseDown} onMouseUp={onMouseUp} onMouseLeave={onMouseLeave} onMouseMove={onMouseMove} ref={canvasRef} />
  );
}

export default Canvas;
