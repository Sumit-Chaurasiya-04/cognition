from streamlit.testing.v1 import AppTest

def test_ui_loads():
    """Smoke test to ensure the Streamlit app loads without error."""
    at = AppTest.from_file("app/main.py")
    at.run()
    assert not at.exception