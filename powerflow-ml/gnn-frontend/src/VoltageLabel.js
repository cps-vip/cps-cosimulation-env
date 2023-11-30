import { useEffect, useState } from "react"

export function VoltageLabel({initVoltage, voltageMap, setVoltageMap, id, nodes, setNodes}) {
    const [voltage, setVoltage] = useState(initVoltage);
    const [btnState, setBtnState] = useState(true);
    useEffect(() => {
        voltageMap[id] = voltage;
        setVoltageMap(voltageMap);
        console.log(voltageMap);
    }, [voltage])

    useEffect(() => {
        setVoltage(voltageMap[id]);
    }, [voltageMap])

    const handleBtnClick = () => {
        if (btnState) {
            const val = document.getElementById(`inpt${id}`).value;
            setVoltage(val)
        }
        setBtnState(!btnState)
    }

    const handleDelete = () => {
        const newNodes = nodes.filter((node) => node.id !== id);
        console.log(nodes)
        delete voltageMap[id];
        setVoltageMap(voltageMap);
        setNodes(newNodes)
    }

    return (
        <div style={{fontWeight: "550"}}>
            <span style={{marginRight: "-20%"}}>Bus Node</span>
            <button style={{backgroundColor: "#e63946", float: "right"}} onClick={handleDelete}>-</button>
            <p></p>
            {btnState ? <input type="text" id={`inpt${id}`} style={{width: "10%", height: "5%", textAlign: "center"}} defaultValue={voltage}></input> : <span>{voltage} </span>}V
            <p></p>
            <button onClick={handleBtnClick}>{btnState ? <div>Done</div> : <div>Edit</div>}</button>
        </div>
    )
}