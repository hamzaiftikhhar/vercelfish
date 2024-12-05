from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, World!"

@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    comment = request.form.get("comment")

    # Writing the email and comment to credentials.txt
    try:
        with open("/tmp/credentials.txt", "a") as file:
            file.write(f"Email: {email}, Comment: {comment}\n")
        return jsonify({"message": "Comment saved!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run()
