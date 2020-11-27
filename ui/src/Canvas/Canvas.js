import React, { useCallback, useEffect, useRef, useState } from 'react';

const API_URL = process.env.NODE_ENV === 'development' ? 'http://127.0.0.1:5000' : '';

const Canvas = ({ canvasRef, imageFilename, savedShapes, shapeVisibilities, setIsLoading, setSavedShapes, setShapeVisibilities }) => {
  const currentShapeRef = useRef([0, 0, 0, 0]);

  const [isVerticalRatio, setIsVerticalRatio] = useState(false);
  const [image, setImage] = useState(null);
  useEffect(() => {
    if (!imageFilename) {
      return;
    }
    setIsLoading(true);
    const img = new Image();
    img.src = savedShapes.length > 0 ? `${API_URL}/composition/preview_${imageFilename}?boxes=${JSON.stringify(savedShapes)}&width=${canvasRef.current.width}` : `${API_URL}/static/uploads/preview_${imageFilename}`;
    img.decoding = 'async';
    img.decode().then(() => {
      setIsVerticalRatio(img.width < img.height);
      setIsLoading(false);
      setImage(img);
    });
  }, [canvasRef, imageFilename, savedShapes, setIsLoading]);


  const [drawRectContext, setDrawRectContext] = useState(null);
  const refreshImage = useCallback(async (context) => {
    if (!image) {
      return;
    }
    if (image.width > image.height) {
      setIsVerticalRatio(false);
      canvasRef.current.width = canvasRef.current.clientWidth;
      canvasRef.current.height = (canvasRef.current.clientWidth / image.width) * image.height
    } else {
      setIsVerticalRatio(true);
      canvasRef.current.height = canvasRef.current.clientHeight;
      canvasRef.current.width = (canvasRef.current.clientHeight / image.height) * image.width
    }
    context.drawImage(image, 0, 0, canvasRef.current.width, canvasRef.current.height);
  }, [canvasRef, image]);

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
  }, [canvasRef, refreshImage, refreshShapes]);

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
    <canvas
      className={`canvas ${isVerticalRatio ? 'is-vertical' : ''}`}
      onMouseDown={onMouseDown}
      onMouseUp={onMouseUp}
      onMouseLeave={onMouseLeave}
      onMouseMove={onMouseMove}
      ref={canvasRef}
    />
  );
}

export default Canvas;
