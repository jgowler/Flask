import json
from flask import Flask, jsonify, request

# Create the Flask application:
app = Flask(__name__)

# Example data:
employees = [
    {"id": 1, "name": "Ashley"},
    {"id": 2, "name": "Kate"},
    {"id": 3, "name": "Joe"},
]


# Define the API endpoint(GET). The above list of employees will be located at "/employees". The function will run returning the employees info:
@app.route("/employees", methods=["GET"])
def get_employees():
    return jsonify(employees)


def get_employee(id):
    return next((e for e in employees if e["id"] == id), None)


def employee_is_valid(employee):
    for key in employee.keys():
        if key != "name":
            return False
    return True


# Get a specific employee using their Id:
@app.route("/employees/<int:id>", methods=["GET"])
def get_emplyee_by_id(id: int):
    employee = get_employee(id)
    if employee is None:
        return jsonify({"error": "Employee does not exist."}), 404
    return jsonify(employee)


# POST api endpoint for employees data:
@app.route("/employees", methods=["POST"])
def create_employee():
    global nextEmployeeId
    employee = json.loads(request.data)
    if not employee_is_valid(employee):
        return jsonify({"error": "Invalid employee properties"}), 400

    employee["id"] = nextEmployeeId
    nextEmployeeId += 1
    employees.append(employee)

    return "", 201, {"location": f"/employees/{employee['id']}"}


# Update (PUT) employee data:
@app.route("/employees", methods=["PUT"])
def update_employee(id: int):
    employee = get_employees(id)
    if employee is None:
        return jsonify({"error": "Employee does not exist."}), 404

    updated_employee = json.loads(request.data)
    if not employee_is_valid(updated_employee):
        return jsonify({"error": "Invalid employee properties"}), 400

    employee.update(updated_employee)


# Delet a user from the employees data:
@app.route("/employees/<int:id>", methods=["DELETE"])
def delete_employee(id):
    global employees
    employee = get_employee(id)
    if employee is None:
        return jsonify({"error": "Employee does not exist."}), 404
    employees = [e for e in employees if e["id"] != id]
    return jsonify(employee), 200


if __name__ == "__main__":
    app.run(port=5000)
