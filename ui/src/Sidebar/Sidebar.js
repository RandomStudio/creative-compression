import React from 'react';

const Sidebar = ({
  deleteShape,
  distances,
  hasVisibleBorders,
  savedShapes,
  setDistances,
  setHasVisibleBorders,
  setSteps,
  setSpeeds,
  speeds,
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
            Degradation speed
            <input type="number" value={speeds[index]} onChange={e => updateSetting(e.target.value, index, setSpeeds)} />
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
        Display borders
      </div>
      <div className="row options">
        <input type="number" value={steps} onChange={e => setSteps(e.target.value)} />
        Number of steps
      </div>
    </>
  );
}

export default Sidebar;
