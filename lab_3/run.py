from app import create_app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=8700, host='0.0.0.0')
    