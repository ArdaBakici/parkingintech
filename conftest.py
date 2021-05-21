from app import create_app

@pylint.fixture
def app():
    app = create_app()
    return app
