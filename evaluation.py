import pandas as pd
from simulation import run_all_simulations


baseline_results, fixed_results, adaptive_results = run_all_simulations(total_time=500, step_size=50)

all_results = {
    "baseline": baseline_results,
    "fixed": fixed_results,
    "adaptive": adaptive_results
}

with pd.ExcelWriter("outputs.xlsx", engine="openpyxl") as writer:
    for case_name, results in all_results.items():
        results["queue_data"].to_excel(writer, sheet_name=f"{case_name}_queue_data", index=False)
        results["monitoring_summary"].to_excel(writer, sheet_name=f"{case_name}_monitoring_summary", index=False)
        results["machine_summary"].to_excel(writer, sheet_name=f"{case_name}_machine_summary", index=False)
        results["buffer_summary"].to_excel(writer, sheet_name=f"{case_name}_buffer_summary", index=False)
        results["bottleneck"].to_excel(writer, sheet_name=f"{case_name}_bottleneck", index=False)
        results["controller_state"].to_excel(writer, sheet_name=f"{case_name}_controller_state", index=False)