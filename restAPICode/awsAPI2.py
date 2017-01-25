import json
import bottle
from bottle import route, run, request, abort
from pymongo import Connection
 
connection = Connection('ec2-54-144-216-55.compute-1.amazonaws.com', 27017)
db = connection.test
 
@route('/news', method='PUT')
def put_document():
    data = request.body.readline()
    if not data:
        abort(400, 'No data received')
    entity = json.loads(data)
    if not entity.has_key('_id'):
        abort(400, 'No _id specified')
    try:
        db['news'].save(entity)
    except ValidationError as ve:
        abort(400, str(ve))
     
@route('/news/:id', method='GET')
def get_document(id):
    entity = db['news'].find_one({"name":{"$regex": id}})
    if not entity:
        abort(404, 'No document with id %s' % id)
    return entity
 
run(host='ec2-54-144-216-55.compute-1.amazonaws.com', port=8081)