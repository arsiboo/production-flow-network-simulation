from read import *
import numpy as np


class BaseController:
    # Here I store the queue network and input data needed by the controller
    def __init__(self, queue_network, controller_df):
        self.queue_network = queue_network
        self.controller_df = controller_df
        self.edges_df = edges_df
        self.name_to_id = name_to_id
        self.arrival_min_by_vertex = arrival_min_by_vertex
        self.arrival_max_by_vertex = arrival_max_by_vertex
        self.current_time = 0

    # Here I update the current simulation time so time dependent rules can be evaluated
    def set_current_time(self, current_time):
        self.current_time = current_time

    # Here I extract the rule parameters of the selected controller from the controller data
    def get_controller_rule(self, controller_name):
        rule = self.controller_df[self.controller_df["Controller_agent"] == controller_name].iloc[0]
        return rule["monitored_item"], rule["controlled_vertex"], float(rule["threshold"]), rule["action"], float(rule["slowdown_factor"])

    # Here I read from the controller rule which system variable should be checked and return its current value
    def observe_state(self, controller_name):
        monitored_item, _, _, _, _ = self.get_controller_rule(controller_name)
        return getattr(self, f"get_{str(monitored_item).lower()}_state")()

    # Here I return the current number of products in the buffer queue so it can be compared with the controller threshold
    def get_buffer_state(self):
        buffer_queue_data = self.queue_network.get_queue_data(
            edge=(
                self.name_to_id[self.edges_df[self.edges_df["to_vertex"] == "Buffer"].iloc[0]["from_vertex"]],
                self.name_to_id[self.edges_df[self.edges_df["to_vertex"] == "Buffer"].iloc[0]["to_vertex"]],
            )
        )
        if len(buffer_queue_data) == 0:
            return 0
        _, _, _, _, num_total, _ = buffer_queue_data[-1]

        return num_total

    # Here I return the electricity price based on the current simulation time (This one I hardcoded due to time limitation)
    def get_electricity_price_state(self):
        if self.current_time < 200:
            return 1.0
        if self.current_time < 350:
            return 2.0
        return 1.2


    # Here I compare the observed state with the controller threshold to decide if an action should be taken
    def should_trigger(self, controller_name):
        observed_value = self.observe_state(controller_name)
        threshold = self.get_controller_rule(controller_name)[2]
        return observed_value >= threshold


    # Here I adjust the source arrival process using the selected scaling factor
    def set_source_arrival(self, factor):
        for q in self.queue_network.edge2queue:
            if q.edge[0] == self.name_to_id[self.edges_df[self.edges_df["from_vertex"] == "Source"].iloc[0]["from_vertex"]] and q.edge[1] == self.name_to_id[self.edges_df[self.edges_df["from_vertex"] == "Source"].iloc[0]["to_vertex"]]:
                q.arrival_f = lambda t: t + np.random.uniform(float(self.arrival_min_by_vertex["Source"]) * factor,float(self.arrival_max_by_vertex["Source"]) * factor)
                return


    # Here I either keep the normal arrival rate or reduce it according to the controller rule
    def apply_action(self, controller_name):
        _, controlled_vertex, _, action, slowdown_factor = self.get_controller_rule(controller_name)

        if not self.should_trigger(controller_name):
            self.set_source_arrival(1)
            return "normal_arrival_rate"

        if action == "reduce_arrival_rate" and controlled_vertex == "Source":
            self.set_source_arrival(slowdown_factor)
            return "reduce_arrival_rate"

        return "no_action"


