from base_controller import BaseController
from read import capacity_by_vertex


class AdaptiveSimulationController(BaseController):
    # Here I reuse the shared controller constructor and initialize the extra variables needed for adaptive bottleneck control
    def __init__(self, queue_network, controller_df):
        super().__init__(queue_network, controller_df)
        self.capacity_by_vertex = capacity_by_vertex
        self.adaptive_controller_name = self.get_adaptive_controller_name()
        self.adaptive_bottleneck_threshold = int(
            controller_df[controller_df["Controller_agent"] == self.adaptive_controller_name].iloc[0]["threshold"]
        )

    # Here I identify the controller that monitors a network vertex instead of an external variable such as electricity price
    def get_adaptive_controller_name(self):
        adaptive_rows = self.controller_df[self.controller_df["monitored_item"] != "electricity_price"]

        if adaptive_rows.empty:
            raise ValueError("No adaptive bottleneck controller rule was found.")

        return adaptive_rows.iloc[0]["Controller_agent"]

    # Here I override the controller rule so the adaptive bottleneck controller uses the adaptive threshold instead of the fixed one
    def get_controller_rule(self, controller_name):
        monitored_item, controlled_vertex, threshold, action, slowdown_factor = super().get_controller_rule(controller_name)

        if controller_name == self.adaptive_controller_name:
            threshold = self.adaptive_bottleneck_threshold

        return monitored_item, controlled_vertex, threshold, action, slowdown_factor

    # Here I update the adaptive bottleneck threshold according to the current number of products in the monitored vertex
    def update_adaptive_threshold(self):
        monitored_item, _, base_threshold, _, _ = super().get_controller_rule(self.adaptive_controller_name)
        monitored_products = self.observe_state(self.adaptive_controller_name)
        monitored_capacity = int(self.capacity_by_vertex[monitored_item])
        base_threshold = int(base_threshold)

        if monitored_products > base_threshold:
            self.adaptive_bottleneck_threshold = max(1, self.adaptive_bottleneck_threshold - 1)
        elif monitored_products < base_threshold:
            self.adaptive_bottleneck_threshold = min(monitored_capacity, self.adaptive_bottleneck_threshold + 1)