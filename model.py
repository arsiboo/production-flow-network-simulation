import queueing_tool as qt
from read import *
import numpy as np

def build_queue_network():
    # Here I build the adjacency structure for the network, edges' types and transition probabilities
    adjacency = {v: [] for v in vertices_df["vertex_id"]}
    edge_type = {v: {} for v in vertices_df["vertex_id"]}
    transitions = {}
    for _, row in edges_df.iterrows():
        adjacency[name_to_id[row["from_vertex"]]].append(name_to_id[row["to_vertex"]])
        edge_type[name_to_id[row["from_vertex"]]][name_to_id[row["to_vertex"]]] = int(row["edge_id"])
        transitions.setdefault(name_to_id[row["from_vertex"]], {})[name_to_id[row["to_vertex"]]] = float(row["probability"])

    # Here I build the directed network
    DG = qt.adjacency2graph(adjacency=adjacency, edge_type=edge_type)

    # Here I define the queue disciplines
    q_classes = {0: qt.NullQueue}
    for _, row in edges_df.iterrows():
        label = int(row["edge_id"])
        target_vertex = row["to_vertex"]
        target_type = type_by_vertex[target_vertex]
        if target_type == "repository":
            q_classes[label] = qt.LossQueue
        else:
            q_classes[label] = qt.QueueServer

    # Here I define the queue arguments
    q_args = {}
    for _, row in edges_df.iterrows():
        label = int(row["edge_id"])
        target_vertex = row["to_vertex"]
        target_type = type_by_vertex[target_vertex]
        q_args[label] = {"collect_data": True}
        if target_type == "processor":
            if pd.notna(server_by_vertex[target_vertex]):
                q_args[label]["num_servers"] = int(server_by_vertex[target_vertex])
            if pd.notna(service_time_by_vertex[target_vertex]):
                service_time = float(service_time_by_vertex[target_vertex])
                q_args[label]["service_f"] = lambda t, s=service_time: t + s
        elif target_type == "repository":
            if pd.notna(capacity_by_vertex[target_vertex]):
                q_args[label]["qbuffer"] = int(capacity_by_vertex[target_vertex])
    q_args[1]["arrival_f"] = lambda t: t + np.random.uniform(float(arrival_min_by_vertex["Source"]),float(arrival_max_by_vertex["Source"]))

    # Here I connect the network to queues disciplines and arguments as well as define the maximum products require entering the production line
    queue_network = qt.QueueNetwork(DG, q_classes=q_classes, q_args=q_args, max_agents=5000)

    return queue_network, DG