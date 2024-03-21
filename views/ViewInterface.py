from abc import ABC, abstractmethod
import streamlit as st


class ViewInterface(ABC):

    @abstractmethod
    def render(self):
        raise NotImplementedError("render() method not implemented")

    def navigte_to(self, page: str, clean_up: bool = False):
        if clean_up:
            self.clear()
        st.session_state.page = page

    @abstractmethod
    def clear(self):
        raise NotImplementedError("clear() method not implemented")
