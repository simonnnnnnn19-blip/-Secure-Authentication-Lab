from app import create_app

app = create_app()

if __name__ == "__main__":
    # debug=False on purpose: the debugger allows remote code execution.
    app.run(host="127.0.0.1", port=5000, debug=False)
