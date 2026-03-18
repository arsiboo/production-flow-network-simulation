from base_controller import BaseController
from read import capacity_by_vertex


class AdaptiveSimulationController(BaseController):
    # Here I reuse the shared controller constructor and initialize the extra variables needed for adaptive bottleneck control
    def __init__(self, queue_network, controller_df):
        super().__init__(queue_network, controller_df)
        self.capacity_by_vertex = capacity_by_vertex
        self.adaptive_bottleneck_threshold = int(controller_df[controller_df["Controller_agent"] == "Bottleneck_manager"].iloc[0]["threshold"])

    # Here I override the controller rule so the bottleneck manager uses the adaptive threshold instead of the fixed one
    def get_controller_rule(self, controller_name):
        monitored_item, controlled_vertex, threshold, action, slowdown_factor = super().get_controller_rule(controller_name)
        if controller_name == "Bottleneck_manager":
            threshold = self.adaptive_bottleneck_threshold

        return monitored_item, controlled_vertex, threshold, action, slowdown_factor

    # Here I update the adaptive bottleneck threshold according to the current number of products in the buffer
    def update_adaptive_threshold(self):
        monitored_item, _, base_threshold, _, _ = super().get_controller_rule("Bottleneck_manager")
        buffer_products = self.observe_state("Bottleneck_manager")
        buffer_capacity = int(self.capacity_by_vertex[monitored_item])
        base_threshold = int(base_threshold)

        if buffer_products > base_threshold:
            self.adaptive_bottleneck_threshold = max(1, self.adaptive_bottleneck_threshold - 1)
        elif buffer_products < base_threshold:
            self.adaptive_bottleneck_threshold = min(buffer_capacity, self.adaptive_bottleneck_threshold + 1)