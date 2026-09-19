from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

print("Loading official NeuraX dataset...")

traffic = pd.read_csv(DATA / "traffic_train.csv")
network = pd.read_csv(DATA / "network.csv")
incidents = pd.read_csv(DATA / "incidents_train.csv")

print("Traffic rows:", len(traffic))
print("Network rows:", len(network))
print("Incident rows:", len(incidents))

agg = traffic.groupby("segment_id").agg(
    vehicle_count=("flow_vph", "mean"),
    avg_speed=("speed_kmh", "mean"),
    occupancy=("occupancy_pct", "mean"),
    congestion=("congestion_index", "mean"),
    delay=("delay_min", "mean"),
    queue=("queue_length_veh", "mean"),
).reset_index()

agg = agg.merge(
    network[["segment_id", "capacity_vph"]],
    on="segment_id",
    how="left"
)

agg["incident_flag"] = agg["segment_id"].astype(str).isin(
    incidents["segment_id"].astype(str)
).astype(int)

capacity_ratio = (
    agg["vehicle_count"] / agg["capacity_vph"]
).clip(0, 1.5)

q95 = max(
    float(agg["congestion"].quantile(0.95)),
    1e-6
)

cong_score = (
    agg["congestion"] / q95
).clip(0, 1)

speed_score = (
    1 - agg["avg_speed"] /
    max(float(agg["avg_speed"].max()), 1e-6)
).clip(0, 1)

agg["risk_score"] = (
    100 * (
        0.45 * cong_score +
        0.30 * capacity_ratio.clip(0, 1) +
        0.15 * speed_score +
        0.10 * (agg["incident_flag"] * 0.20)
    )
).round(2)


def level(score):
    if score >= 70:
        return "CRITICAL"
    elif score >= 50:
        return "HIGH"
    elif score >= 30:
        return "MODERATE"
    else:
        return "NORMAL"


def action(priority):
    if priority == "CRITICAL":
        return "Deploy traffic control + suggest alternate route"
    elif priority == "HIGH":
        return "Increase monitoring + evaluate signal timing"
    elif priority == "MODERATE":
        return "Monitor traffic conditions"
    else:
        return "No immediate action"


agg["congestion_level"] = agg["risk_score"].apply(level)
agg["priority"] = agg["risk_score"].apply(level)
agg["recommended_action"] = agg["priority"].apply(action)

out = agg.sort_values(
    ["risk_score", "congestion"],
    ascending=False
).head(20).copy()

out["normal_traffic"] = (
    out["capacity_vph"] * 0.60
).round(0)
out["occupancy"] = out["occupancy"].round(0)
out["occupancy"] = out["occupancy"].round(1)
out["vehicle_count"] = out["vehicle_count"].round(0)
out["avg_speed"] = out["avg_speed"].round(1)
out["road_capacity"] = out["capacity_vph"].round(0)

out = out[
    [
        "segment_id",
        "vehicle_count",
        "avg_speed",
        "road_capacity",
        "normal_traffic",
        "occupancy",
        "incident_flag",
        "congestion_level",
        "risk_score",
        "priority",
        "recommended_action"
    ]
]

out = out.rename(
    columns={"segment_id": "road"}
)

output = DATA / "traffic_analysis.csv"

out.to_csv(output, index=False)

print()
print("SUCCESS!")
print("Created:", output)
print("Rows:", len(out))
print()
print(out.head(10).to_string(index=False))