from abc import ABC, abstractmethod
from views.ViewInterface import ViewInterface
import streamlit as st
from graphs.visualization.base_graph import BaseGraph
from components.interactiveGraph import interactiveGraph
from components.buttons import home_button


class AlgorithmViewInterface(ViewInterface, ABC):

    controller = None

    @abstractmethod
    def initialize_values(self):
        raise NotImplementedError("initialize_values() method not implemented")

    @abstractmethod
    def is_correct_model_type(self, model) -> bool:
        raise NotImplementedError("is_correct_model_type() method not implemented")

    @abstractmethod
    def render_sidebar(self):
        raise NotImplementedError("render_sidebar() method not implemented")

    @abstractmethod
    def get_page_title(self) -> str:
        return "Algorithm View Interface"

    def read_values_from_session_state(self):
        if "model" in st.session_state:
            if not self.is_correct_model_type(st.session_state.model):
                st.session_state.error = "Invalid model type"
                self.navigte_to("Home", True)
                st.rerun()
            self.controller.set_model(st.session_state.model)
        else:
            if (
                "df" not in st.session_state
                or "time_column" not in st.session_state
                or "case_column" not in st.session_state
                or "activity_column" not in st.session_state
            ):
                self.navigte_to("Home", True)

            self.controller.create_model(
                st.session_state.df,
                st.session_state.time_column,
                st.session_state.activity_column,
                st.session_state.case_column,
            )

            del st.session_state.df
            st.session_state.model = self.controller.get_model()

    def render(self):
        self.read_values_from_session_state()
        self.initialize_values()

        st.title(self.get_page_title())
        with st.sidebar:
            self.render_sidebar()

        self.controller.perform_mining()

        graph_container = st.container(border=True)

        button_container = st.container()

        self.node_info_container = st.container()

        with graph_container:
            interactiveGraph(
                self.controller.get_graph(), onNodeClick=self.display_node_info
            )
        with button_container:
            columns = st.columns([1, 1, 1])
            with columns[0]:
                home_button("Back", use_container_width=True)
            with columns[2]:
                st.button(
                    "Export",
                    on_click=self.navigte_to,
                    args=("Export",),
                    type="primary",
                    use_container_width=True,
                )

    def display_node_info(self, node_name: str, node_description: str):
        with self.node_info_container:
            with st.expander(f"Node: {node_name}"):
                for line in node_description.split("\n"):
                    st.write(line)

    def clear(self):
        return
