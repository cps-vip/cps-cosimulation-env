import React, { useCallback } from 'react';
import ReactFlow, { useNodesState, useEdgesState, addEdge } from 'reactflow';
import { useEffect } from 'react';
import 'reactflow/dist/style.css';
import { VoltageLabel } from './VoltageLabel';
import { useState } from 'react';
 
 
export default function App() {
  const [voltageMap, setVoltageMap] = useState({});
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const [maxId, setMaxId] = useState(3);
  const [invertMap, setInvertMap] = useState({});
  const initialNodes = [
    { id: '1', position: { x: 0, y: 0 }, data: { label: <VoltageLabel voltageMap={voltageMap} setVoltageMap={setVoltageMap} initVoltage={0.0} id={"1"} nodes={nodes} setNodes={setNodes}></VoltageLabel> } },
  ];

  useEffect(() => {
    if (nodes.length < 1) {
      setNodes(initialNodes);
      console.log(initialNodes);
    }
  }, [])

  useEffect(() => {
    console.log("rerendering")
  }, [voltageMap])
  const onConnect = useCallback(
    (params) => setEdges((eds) => addEdge(params, eds)),
    [setEdges],
  );

  const addLoad = () => {
    console.log(nodes)
    nodes.push({ id: maxId.toString(), position: { x: nodes[nodes.length - 1].position.x, y: nodes[nodes.length - 1].position.y }, data: { label: <VoltageLabel voltageMap={voltageMap} setVoltageMap={setVoltageMap} initVoltage={0.0} id={maxId.toString()} nodes={nodes} setNodes={setNodes}></VoltageLabel> } })
    setNodes(nodes);
    voltageMap[maxId.toString()] = 0;
    setVoltageMap(voltageMap);
    setMaxId(maxId + 1);
  }
  const handleSubmit = (e) => {
    const idMap = {};
    e.preventDefault()
    const voltages = [];
    setInvertMap({});
    Object.keys(voltageMap).forEach((key, i) => {
      idMap[key] = i;
      voltages.push(parseInt(voltageMap[key]));
      invertMap[i] = key;
    })
    setInvertMap(invertMap);
    const src = [];
    const dest = [];
    console.log(idMap);
    edges.forEach((edge) => {
      src.push(idMap[edge.source], idMap[edge.target]);
      dest.push(idMap[edge.target], idMap[edge.source]);
    })
    const steps = parseInt(document.getElementById("steps").value)
    const body = {
      src,
      dest,
      steps,
      voltages
    }
    console.log(JSON.stringify(body))
    fetch("http://localhost:8000", {
      method: "POST",
      body: JSON.stringify(body)
    }).then((out) => out.json().then((final) => {
      final.voltages.forEach((voltage, i) => {
        console.log(nodes[0].data.label)
        console.log(nodes.filter((node) => node.data.label.id === voltageMap[invertMap[i]]));
      })

      setVoltageMap(voltageMap);
      console.log(voltageMap)
    }))
  }
    return (
      <div style={{ textAlign: "center" }}>
        <h1>Powerflow ML Visualizer</h1>
        <div style={{ width: '100vw', height: '100vh', borderColor: 'black' }}>
          <ReactFlow
            style={{maxHeight: "75%"}}
            nodes={nodes}
            edges={edges}
            onNodesChange={onNodesChange}
            onEdgesChange={onEdgesChange}
            onConnect={onConnect}
          />
          
          <form onSubmit={handleSubmit}>
            <div style={{ marginRight: "-10%" }}>
            Simulate for <input type="text" style={{width: "2%"}} id="steps"></input> steps
            </div>
            <button style={{width: "5%", height: "5%", fontWeight: "550", marginRight: "-10%"}}>Submit</button>
          </form>
          <button style={{float: "right", height: "5%", width: "5%", marginRight: "10%", backgroundColor: "#adc178", fontSize: "24px"}} onClick={addLoad}>+</button>
        </div>
      </div>
    );
}