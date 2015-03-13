import json
from flask import Flask, request, jsonify
from flask.ext.sqlalchemy import SQLAlchemy
import pymysql

app = Flask(__name__)
db = SQLAlchemy(app)

dbhost = '127.0.0.1:3306'
dbuser = 'root'
dbpass = ''
dbname = 'ecommerce'
 
DB_URI = 'mysql://' + dbuser + ':' + dbpass + '@' + dbhost + '/' +dbname
db1 = pymysql.connect(host = 'localhost', port = 3306, user = 'root', passwd = dbpass, db = 'ecommerce')
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI

class Shoe(db.Model):
  __tablename__ = 'shoes'
  shoeId = db.Column(db.String(100), primary_key = True)
  shoeName = db.Column(db.String(100))
  shoeQuantity = db.Column(db.String(100))
  createdBy = db.Column(db.String(100))
  


@app.route('/shoe', methods=['GET'])
def get_orders():
  if request.method == 'GET':
    results = Shoe.query.all()

    json_results = []
    for result in results:
      d = {'shoeId': result.shoeId,
           'shoeName': result.shoeName,
           'shoeQuantity': result.shoeQuantity,
           'createdBy': result.createdBy,
           }
      json_results.append(d)

    return jsonify(shoes=json_results)


@app.route('/shoe/<int:id>', methods=['GET'])
def get_orders_by_id(id):
  if request.method == 'GET':
    results = Shoe.query.filter_by(shoeId=id).first()

    json_results = {'shoeId': results.shoeId,
           'shoeName': results.shoeName,
           'shoeQuantity': results.shoeQuantity,
           'createdBy': results.createdBy,
           }
   

    return jsonify(shoe=json_results)



@app.route('/shoes', methods=['PUT'])
def update_orders_by_id():
  

   request.get_json(force=True)
   order1='Order Updated!! Please check the Database'
#   cursor = db1.cursor()
   shoeid=request.json['shoeId']
   shoename= request.json['shoeName']
   shoeq= request.json['shoeQuantity']
   create= request.json['createdBy']
   results = results = Shoe.query.filter_by(shoeId=id).first()
#   cursor.execute("update shoes set shoeName='"+shoename+"',shoeQuantity='"+shoeq+"',createdBy='"+create+"' where shoeId="+shoeid+"")
#   cursor.close()
#   db1.commit()
#   db1.close()
    
   return order1




@app.route('/shoes', methods=['POST'])
def post_orders():
    request.get_json(force=True)
    content = request.json
    print content
    shoe = Shoe(shoeId=request.json['shoeId'],shoeName=request.json['shoeName'],shoeQuantity=request.json['shoeQuantity'],createdBy=request.json['createdBy'])
    db.session.add(shoe)
    db.session.commit()

    order1='Order Posted!! Please check the Database'
    return order1




@app.route('/shoes', methods=['DELETE'])
def del_orders_by_id(id):
  request.get_json(force=True)
  shoeid=request.json['shoeId']
  if request.method == 'DELETE':
    results = Order.query.filter_by(orderId=shoeid).first()
    db.session.delete(results)
    db.session.commit()
    order1='Order deleted!! Please check the Database'
    return order1



if __name__ == '__main__':
  app.run(debug=True)
