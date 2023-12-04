from flask import Flask, request, jsonify
import torch
import torch.nn.functional as F
from gnn import PowerFlowGCN
from json import loads
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
gcn_model = PowerFlowGCN()


@app.route("/", methods=["POST", "GET"])
@cross_origin()
def callModel():
    if (request.method == "GET"):
        return dumps({
            "hello": "world"
        })
    json = loads(request.data.decode("utf-8"))
    print(json)
    edge_index = torch.tensor([json["src"],json["dest"]], dtype=torch.long)
    initialVoltage = torch.tensor(json["voltages"], dtype=torch.float).view(-1, 1)
    x = initialVoltage.clone()

    for i in range(json["steps"]):
        # Forward pass through the GCN model
        x = gcn_model(x, edge_index)
        
        # Clamp voltage magnitudes to ensure they remain positive
        x = F.relu(x)
    print(x.tolist())
    return {
        "voltages": x.tolist()
    }

if (__name__ == "__main__"):
    app.run(port=8000)