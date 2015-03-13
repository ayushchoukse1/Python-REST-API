import json
import pymongo
import pymysql
import collections
import bottle
from bottle import route, run, request, abort
from pymongo import Connection,MongoClient
from bson import json_util
connection = MongoClient("127.0.0.1",27017 )
db = connection["test"]


db1 = pymysql.connect(host ='0.0.0.0', port=3306,user='root', password='toor', db='test')

@route('/shirts', method='POST')
def put_document():
    data = request.body.readline()
    if not data:
        abort(400, 'No data received')
    entity = json.loads(data)
    if not entity.has_key('shirtId'):
        abort(400, 'No shirtId specified')
    try:
        db['shirts'].save(entity)
    except ValidationError as ve:
        abort(400, str(ve))

@route('/shirt/:id', method='GET')
def get_document(id):
    entity = db['shirts'].find_one({'shirtId':id})
    print entity
#    if not entity:
#        abort(404, 'No document with id %s' % id)
    return json.dumps(entity, sort_keys=True, indent=4, default=json_util.default)


@route('/shirts',method='DELETE')
def delete_document():
        shirt = request.json
        if not shirt:
                abort(400, 'No data received')

#       if not entity.has_key('shirtId'):
#               abort(400, 'No shirtId specified')
#       try:
        db.shirts.remove({'shirtId':shirt['shirtId']})
#       except ValidationError as ve:
#               abort(400, str(ve))

@route('/shirts',method='PUT')
def updateShirtInfo():
        shirt = request.json
        db.shirts.update({'shirtId':shirt['shirtId']},{"$set":shirt},upsert=False)
        msg='UPDATE '+shirt['shirtName']
        return msg


@route('/shoe/:id', method='GET')
def get_mysql(id):
        cur= db1.cursor()
        objects_list=[]
        result =cur.execute("select * from shoes where shoeId='"+id+"'")
        row= cur.fetchone()
        json_results= {'shoeId': row[0],'shoeName': row[1],'shoeQuantity': row[2],'createdBy' : row[3]}
        cur.close()
        return json_results

@route('/shoes', method='POST')
def post_mysql():
        cursor2=db1.cursor()
        shoeId=request.json['shoeId']
        shoeName=request.json['shoeName']
        shoeQuantity=request.json['shoeQuantity']
        createdBy=request.json['createdBy']
        cursor2.execute("insert into shoes values ('"+shoeId+"','"+shoeName+"','"+shoeQuantity+"','"+createdBy+"')")
        cursor2.close()
        db1.commit()
@route('/shoes', method='DELETE')
def delete_mysql():
        shoeId=request.json['shoeId']
        shoeName=request.json['shoeName']
        cursor=db1.cursor()
        cursor.execute("delete from shoes where shoeId='"+shoeId+"'")
        cursor.close()
        msg= 'DELETE '+ shoeName
        return msg

@route('/shoes',method='PUT')
def put_mysql():
        cursor1=db1.cursor()
        shoeId=request.json['shoeId']
        shoeName=request.json['shoeName']
        shoeQuantity=request.json['shoeQuantity']
        createdBy=request.json['createdBy']
        cursor1.execute("update shoes set shoeName='"+shoeName+"',shoeQuantity='"+shoeQuantity+"',createdBy='"+createdBy+"' where shoeId='"+shoeId+"'")
        cursor1.close()
        db1.commit()
        msg='UPDATE :'+ shoeName
        return msg

run(host='0.0.0.0', port=8081)


