import streamlit as st
from base_ui.base_view import BaseView
from components.buttons import home_button, navigation_button
from components.interactiveGraph import interactiveGraph
from abc import abstractmethod


class BaseAlgorithmView(BaseView):

    def create_layout(self):
        super().create_layout()
        self.sidebar = st.sidebar()
        self.graph_container = st.container()
        self.button_container = st.container()
        self.node_data_container = st.container()

    @abstractmethod
    def render_sidebar(self):
        raise NotImplementedError("render_sidebar() method not implemented")

    def display_sidebar(self):
        with self.sidebar:
            self.render_sidebar()

    def display_navigation_buttons(self):
        with self.back_button_column:
            back_button_column, _, export_button_column = st.columns([1, 1, 1])

        with back_button_column:
            home_button("Back", use_container_width=True)

        with export_button_column:
            navigation_button(
                "Export",
                "Export",
                use_container_width=True,
            )

    def display_graph(self, graph):
        with self.graph_container:
            if graph is not None:
                interactiveGraph(graph, onNodeClick=self.display_node_data)

    def display_node_info(self, node_name: str, node_description: str):
        with self.node_data_container:
            with st.expander(f"Node: {node_name}"):
                for line in node_description.split("\n"):
                    st.write(line)

    def display_page_title(self, title):
        from config import docs_path_mappings

        with self.title_container:

            if st.session_state.algorithm not in docs_path_mappings:
                st.title(title)

            else:
                title_column, button_column = st.columns([3, 1])
                with title_column:
                    st.title(title)
                with button_column:
                    navigation_button(
                        "Algorithm Explanation",
                        "Documentation",
                        use_container_width=True,
                    )
