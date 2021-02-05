import React from 'react';

const Sidebar = ({
  deleteShape,
  distances,
  hasVisibleBorders,
  savedShapes,
  setDistances,
  setHasVisibleBorders,
  setSteps,
  steps
}) => {
  const updateSetting = (value, index, func) => {
    if (!value) {
      return;
    }
    func(v => {
      v[index] = Math.max(1, parseInt(value));
      return [...v];
    })
  }

  return (
    <>
    <div className="boxes">
      {savedShapes.map((shape, index) => (
        <div className="row" key={`${index}_${shape.join('-')}`}>
          <p className="row-title">Box {index}</p>
          <div className="input-row">
            Number of steps
            <input type="number" value={steps[index]} onChange={e => updateSetting(e.target.value, index, setSteps)} />
          </div>
          <div className="input-row">
            Step width divisor
            <input type="number" value={distances[index]} onChange={e => updateSetting(e.target.value, index, setDistances)} />
          </div>
          <button onClick={() => deleteShape(index)}>Delete</button>
        </div>
      ))}
      </div>
      <div className="row options">
        <input type="checkbox" checked={hasVisibleBorders} onChange={() => setHasVisibleBorders(!hasVisibleBorders)} />
        Display debug borders
      </div>
    </>
  );
}

export default Sidebar;
