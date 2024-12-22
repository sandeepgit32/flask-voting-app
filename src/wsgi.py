from app import app, initialize_candidates, initialize_voters

# Initialize on module import, before workers start
try:
    initialize_candidates()
    initialize_voters()
except Exception as e:
    print(f"Error initializing application: {e}")
    raise

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
