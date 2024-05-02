import json
import time
import pytz
import requests
from flasgger import Swagger

from flask import Flask, request, jsonify, make_response, render_template, abort

from DBHelper import *

app = Flask(__name__)
Session = sessionmaker(bind=engine)

@app.route("/api/v1")
def index():
    return "Home page" 

@app.route("/api/v1/clients", methods = ["GET"])
def getClients():
    username = request.args.get("username")
    email = request.args.get("email")
    with Session() as session:
        query = session.query(Client)
        if username:
            query = query.filter(Client.username.like(f"%{username}%"))
        if email:
            query = query.filter(Client.email.like(f"%{email}%"))
        clients = query.all()
        clients_json = []
        for client in clients:
            clients_json.append(client.to_json())
        return clients_json

@app.route("/api/v1/clients/<int:client_id>", methods = ["GET"])
def getClientById(client_id):
    with Session() as session:
        client = session.query(Client).get(client_id)
        if not client:
            abort(404)
        return client.to_json()

@app.route("/api/v1/clients", methods = ["POST"])
def addClient():
    if not request.json or not "username" in request.json or not "email" in request.json:
        abort(400)
    username = request.json.get("username")
    email = request.json.get("email")
    with Session() as session:
        client = Client(username=username, email=email)
        session.add(client)
        session.commit()
        return client.to_json(), 201

@app.route("/api/v1/clients/<int:client_id>", methods = ["PUT"])
def updateClientById(client_id):
    with Session() as session:
        client = session.query(Client).get(client_id)
        if not client:
            abort(404)
        if not request.json:
            abort(400)
        client.username = request.json.get("username", client.username)
        client.email = request.json.get("email", client.email)
        session.commit()
        return client.to_json()

@app.route("/api/v1/clients/<int:client_id>", methods = ["DELETE"])
def removeClientById(client_id):
    with Session() as session:
        client = session.query(Client).get(client_id)
        if not client:
            abort(404)
        session.delete(client)
        session.commit()
        return jsonify({"result" : True})
    
@app.route("/api/v1/employees", methods = ["GET"])
def getEmployees():
    with Session() as session:
        employees = session.query(Employee).all()
        employees_json = []
        for employee in employees:
            employees_json.append(employee.to_json())
        return employees_json

@app.route("/api/v1/employees/<int:employee_id>", methods = ["GET"])
def getEmployeeById(employee_id):
    with Session() as session:
        employee = session.query(Employee).get(employee_id)
        if not employee:
            abort(404)
        return employee.to_json()

@app.route("/api/v1/employees", methods = ["POST"])
def addEmployee():
    if not request.json or not "username" in request.json:
        abort(400)
    employee_name = request.json.get("username")
    post = request.json.get("post")
    salary = request.json.get("salary")
    start_date = request.json.get("start_date")
    with Session() as session:
        employee = Employee(employee_name=employee_name, post=post, salary=salary, start_date=start_date)
        session.add(employee)
        session.commit()
        return employee.to_json(), 201

@app.route("/api/v1/employees/<int:employee_id>", methods = ["PUT"])
def updateEmployeeById(employee_id):
    with Session() as session:
        employee = session.query(Employee).get(employee_id)
        if not employee:
            abort(404)
        if not request.json:
            abort(400)
        employee.employee_name = request.json.get("username", employee.employee_name)
        employee.post = request.json.get("post", employee.post)
        employee.salary = request.json.get("salary", employee.salary)
        employee.start_date = request.json.get("start_date", employee.start_date)
        session.commit()
        return employee.to_json()

@app.route("/api/v1/employees/<int:employee_id>", methods = ["DELETE"])
def removeEmployeeById(employee_id):
    with Session() as session:
        employee = session.query(Employee).get(employee_id)
        if not employee:
            abort(404)
        session.delete(employee)
        session.commit()
        return jsonify({"result" : True})
    
@app.route("/api/v1/orders", methods = ["GET"])
def getOrders():
    with Session() as session:
        orders = session.query(Order).all()
        orders_json = []
        for order in orders:
            orders_json.append(order.to_json())
        return orders_json
    
@app.route("/api/v1/orders/<int:order_id>", methods = ["GET"])
def getOrderById(order_id):
    with Session() as session:
        order = session.query(Order).get(order_id)
        if not order:
            abort(404)
        return order.to_json()
    
@app.route("/api/v1/orders", methods = ["POST"])
def addOrder():
    if not request.json or not "description" in request.json or not "client_id" in request.json:
        abort(400)
    description = request.json.get("description")
    client_id = request.json.get("client_id")
    with Session() as session:
        client = session.query(Client).get(client_id)
        if not client:
            abort(400)
        order = Order(description=description)
        client.orders.append(order)
        session.commit()
        return order.to_json(), 201
    
@app.route("/api/v1/orders/<int:order_id>", methods = ["PUT"])
def updateOrderById(order_id):
    with Session() as session:
        order = session.query(Order).get(order_id)
        if not order:
            abort(404)
        if not request.json:
            abort(400)
        order.description = request.json.get("description", order.description)
        session.commit()
        return order.to_json()
    
@app.route("/api/v1/orders/<int:order_id>", methods = ["DELETE"])
def removeOrderById(order_id):
    with Session() as session:
        order = session.query(Order).get(order_id)
        if not order:
            abort(404)
        session.delete(order)
        session.commit()
        return jsonify({"result" : True})
    
@app.route("/api/v1/clients/<int:client_id>/add-employee", methods=["POST"])
def addEmployeeToClient(client_id):
    if not request.json or not "employee_id" in request.json:
        abort(400)
    employee_id = request.json.get("employee_id")
    with Session() as session:
        client = session.query(Client).get(client_id)
        employee = session.query(Employee).get(employee_id)
        if not client or not employee:
            abort(404)
        client.employees.append(employee)
        session.commit()
        return jsonify({"result": True})
    
@app.route("/api/v1/employees/<int:employee_id>/add-client", methods=["POST"])
def addClientToEmployee(employee_id):
    if not request.json or not "client_id" in request.json:
        abort(400)
    client_id = request.json.get("client_id")
    with Session() as session:
        employee = session.query(Employee).get(employee_id)
        client = session.query(Client).get(client_id)
        if not employee or not client:
            abort(404)
        employee.clients.append(client)
        session.commit()
        return jsonify({"result": True})

@app.route("/api/v1/clients", methods=["GET"])
def getClientsByNameAndEmail():
    username = request.args.get("username")
    email = request.args.get("email")
    print(EMADLSKDJALKjDL)
    print(email)
    print(username)
    with Session() as session:
        query = se
        if username:
            query = query.filter(Client.username.like(f"%{username}%"))
        if email:
            query = query.filter(Client.email.like(f"%{email}%"))
        clients = query.all()
        clients_json = []
        for client in clients:
            clients_json.append(client.to_json())
        return clients_json

if __name__ == "__main__":
    app.run()
