from ui.base_algorithm_ui.base_algorithm_controller import BaseAlgorithmController
from ui.heuristic_miner_ui.heuristic_miner_view import HeuristicMinerView
import streamlit as st
from mining_algorithms.heuristic_mining import HeuristicMining


class HeuristicMinerController(BaseAlgorithmController):
    def __init__(self, views=None, model=None):
        if views is None:
            views = [HeuristicMinerView()]
        super().__init__(views, model)

    def process_session_state(self):
        super().process_session_state()
        # read values from session state
        if "threshold" not in st.session_state:
            st.session_state.threshold = self.mining_model.get_threshold()

        if "frequency" not in st.session_state:
            st.session_state.frequency = self.mining_model.get_min_frequency()
        # set instance variables from session state
        if "threshold" in st.session_state:
            self.threshold = st.session_state.threshold

        if "frequency" in st.session_state:
            self.frequency = st.session_state.frequency

    def perform_mining(self) -> None:
        self.mining_model.create_dependency_graph_with_graphviz(
            self.threshold, self.frequency
        )

    def create_empty_model(self, *log_data):
        return HeuristicMining(*log_data)

    def have_parameters_changed(self) -> bool:
        return (
            self.mining_model.get_threshold() != self.threshold
            or self.mining_model.get_min_frequency() != self.frequency
        )

    def is_correct_model_type(self, model) -> bool:
        return isinstance(model, HeuristicMining)

    def get_sidebar_values(self) -> dict[str, tuple[int | float, int | float]]:
        sidebar_values = {
            "frequency": (1, self.mining_model.get_max_frequency()),
            "threshold": (0.0, 1.0),
        }

        return sidebar_values