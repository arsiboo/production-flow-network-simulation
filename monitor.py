from model import *
import pandas as pd
import numpy as np

# Here I monitor the queue network and collect data on the queue information, machine and buffer performance as well as the bottleneck vertex
def run_monitoring(queue_network, DG, simulation_time=1):
    rows = []

    for source in DG.nodes():
        for target in DG.nodes():
            if source != target and DG.has_edge(source, target):
                for arrival, service, departure, num_queued, num_total, q_id in queue_network.get_queue_data(edge=(source, target)):
                    occupied_servers = num_total - num_queued

                    rows.append([
                        arrival,
                        service,
                        departure,
                        num_queued,
                        num_total,
                        q_id,
                        id_to_name[source],
                        id_to_name[target],
                        occupied_servers,
                        occupied_servers / float(server_by_vertex[id_to_name[target]])
                        if pd.notna(server_by_vertex.get(id_to_name[target], np.nan)) and float(server_by_vertex[id_to_name[target]]) > 0
                        else np.nan,
                        capacity_by_vertex.get(id_to_name[target], np.nan)
                    ])

    queue_df = pd.DataFrame(
        rows,
        columns=[
            "arrival",
            "service",
            "departure",
            "num_queued",
            "num_total",
            "q_id",
            "source",
            "target",
            "occupied_servers",
            "machine_utilization",
            "buffer_capacity"
        ]
    )

    simulation_start = pd.Timestamp("2026-01-01 08:00:00")
    queue_df["event_time"] = queue_df["arrival"]
    queue_df["event_timestamp"] = (
        simulation_start + pd.to_timedelta(queue_df["event_time"], unit="m")
    ).dt.strftime("%H:%M:%S")

    queue_df["waiting_time"] = queue_df["service"] - queue_df["arrival"]
    queue_df.loc[queue_df["waiting_time"] < 0, "waiting_time"] = np.nan

    throughput_count = queue_df[
        (queue_df["target"] == "Sink") & (queue_df["departure"] > 0)
    ].shape[0]
    throughput_rate = throughput_count / simulation_time

    machine_summary = (
        queue_df[queue_df["target"].isin(vertices_df[vertices_df["type"] == "processor"]["vertex"].tolist())]
        .groupby("target", as_index=False)
        .agg(
            avg_waiting_time=("waiting_time", "mean"),
            avg_machine_utilization=("machine_utilization", "mean"),
            avg_queue_length=("num_queued", "mean"),
            avg_num_total=("num_total", "mean"),
            completed_products=("departure", lambda x: (x > 0).sum())
        )
    )

    buffer_summary = (
        queue_df[queue_df["target"] == "Buffer"]
        .groupby("target", as_index=False)
        .agg(
            avg_waiting_time=("waiting_time", "mean"),
            avg_queue_length=("num_queued", "mean"),
            avg_num_total=("num_total", "mean"),
            buffer_capacity=("buffer_capacity", "max"),
            max_queue_length=("num_queued", "max"),
            max_num_total=("num_total", "max")
        )
    )

    monitoring_summary = pd.DataFrame({
        "metric": [
            "throughput_count",
            "throughput_rate_per_time_unit",
            "overall_avg_waiting_time"
        ],
        "value": [
            throughput_count,
            throughput_rate,
            queue_df["waiting_time"].mean()
        ]
    })

    bottleneck_by_wait = machine_summary.loc[machine_summary["avg_waiting_time"].idxmax(), "target"]
    bottleneck_by_util = machine_summary.loc[machine_summary["avg_machine_utilization"].idxmax(), "target"]

    return queue_df, monitoring_summary, machine_summary, buffer_summary, bottleneck_by_wait, bottleneck_by_util