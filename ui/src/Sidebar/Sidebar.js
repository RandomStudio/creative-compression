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

  return (
    <>
      {shapeVisibilities.map((isShapeVisible, index) => (
        <div className="row">
          <p>Box {index}</p>
      Enabled?
          <input type="checkbox" checked={isShapeVisible} onChange={() => toggleShapeVisibility(index)} />
          <button onClick={() => deleteShape(index)}>Delete</button>
        </div>
      ))}
    </>
  );
}

export default Sidebar;
