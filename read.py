import pandas as pd

#Here I access the input data from the Excel file
file_path = "production-line.xlsx"

#Here I read the data from the Excel file which are the vertices, edges and controllers
vertices_df = pd.read_excel(file_path, sheet_name="Vertices")
edges_df = pd.read_excel(file_path, sheet_name="Edges")
controller_df = pd.read_excel(file_path, sheet_name="Controllers")

# Here I create dictionaries that assign attributes to each vertex
name_to_id = dict(zip(vertices_df["vertex"], vertices_df["vertex_id"]))
id_to_name = dict(zip(vertices_df["vertex_id"], vertices_df["vertex"]))
type_by_vertex = dict(zip(vertices_df["vertex"], vertices_df["type"]))
server_by_vertex = dict(zip(vertices_df["vertex"], vertices_df["server"]))
capacity_by_vertex = dict(zip(vertices_df["vertex"], vertices_df["capacity"]))
service_time_by_vertex = dict(zip(vertices_df["vertex"], vertices_df["service_time"]))
arrival_min_by_vertex = dict(zip(vertices_df["vertex"], vertices_df["arrival_rate_min"]))
arrival_max_by_vertex = dict(zip(vertices_df["vertex"], vertices_df["arrival_rate_max"]))
energy_by_vertex = dict(zip(vertices_df["vertex"], vertices_df["energy_per_time_unit"]))