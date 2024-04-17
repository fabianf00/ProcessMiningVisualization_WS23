import streamlit as st
import streamlit.components.v1 as components


def PNGViewer(png_base64: str, height: int = 600):
    html = f"""
    <div style="display: flex; justify-content: center; height:{height}px; width:100%;background-color:white;">
    <img src="data:image/png;base64,{png_base64}" alt="png" style="max-width:99%; max-height:98%;object-fit:contain">
    </div>
    """
    components.html(html, height=height)
