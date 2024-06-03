def load_css(file: str) -> str:
    with open(file=file) as f:
        css = f'<style>{f.read()}</style>'
        return css

def load_html(file: str) -> str:
    with open(file=file) as f:
        html = f.read()
        return html