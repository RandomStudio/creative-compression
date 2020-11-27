import React from 'react';

const Sidebar = ({ savedShapes, shapeVisibilities, setSavedShapes, setShapeVisibilities }) => {
  const toggleShapeVisibility = index => {
    const updatedState = shapeVisibilities.map((state, i) => i === index ? !state : state)
    setShapeVisibilities(updatedState);
  }

  const deleteShape = index => {
    setSavedShapes(savedShapes.map((shape, i) => index === i ? false : shape).filter(exists => exists));
    setShapeVisibilities(shapeVisibilities.map((visibility, i) => index === i ? null : visibility).filter(state => state !== null));
  }

  const areLayersVisible = shapeVisibilities.some(visible => visible !== false);

  const toggleAllBorders = () => {
    setShapeVisibilities(shapeVisibilities.map(entry => !areLayersVisible));
  }


  return (
    <>
      {shapeVisibilities.map((isShapeVisible, index) => (
        <div className="row">
          <p className="row-title">Box {index}</p>
          <button onClick={() => deleteShape(index)}>Delete</button>
        </div>
      ))}
      <div className="row options">
        <input type="checkbox" checked={areLayersVisible} onChange={toggleAllBorders} />
        Toggle guides
      </div>
    </>
  );
}

export default Sidebar;
