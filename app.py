from flask import Flask   
from flask import request
from flask import render_template
import mysql.connector as mc

app = Flask(__name__)

@app.route('/process',methods=['POST'])
def process_order():
    qty = request.form['qty']
    product = request.form['itemOrdered']
    connection = get_connection()
    sql = 'insert into orders (quantity,product_id) values ('+qty+','+product+')'
    # i.e insert into orders (quantity, product_id) values (8000,2)
    result = connection.cmd_query(sql)
    connection.commit()
    connection.close()
    return "Order processed"
  

@app.route('/viewOrders')
def view_orders():
  connection = get_connection()
  sql = "select * from orders"
  result = connection.cmd.query(sql)
  rows = connection.get_rows()
  connection.close()
  return render_template('candystore_orders.html',orders=rows[0])


@app.route('/')
def candystore_main():
    products = get_products()
    return render_template('candystore_main.html',stuff=products,more_stuff=5)

@app.route("/hello")
def hello():
  return render_template('index.html')

@app.route('/orders/<orderid>')
def show_orders(orderid=None):
  calc = int(orderid) * 5 
  stuff = "<b>Hello" + str(calc)+ "</b>"
  return stuff

@app.route('/query')
def query():
  name = request.args.get('name')
  color = request.args.get('color')
  combined = name + ' ' + color
  return combined

def get_products():
    connection = get_connection()
    result = connection.cmd_query("select * from products")
    rows = connection.get_rows()
    connection.close()
    return rows[0]


def get_connection():
  return mc.connect(user='root',
  password= 'jigru8MySQL',
  host ='127.0.0.1',
  database= 'Candystore',
  auth_plugin='mysql_native_password')





if __name__ == "__main__":
  app.run(debug=True)