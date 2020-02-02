import webapp2
from google.cloud import datastore

client = datastore.Client()


class ValueNode:
    def __init__(self, name=None, value=None, prev=None, next=None):
        self.name = name
        self.value = value
        self.prev = prev
        self.next = next

    def __repr__(self):
        return repr(self.name), repr(self.value)


class ValueNodeList:
    def __init__(self):
        self.head = None

    # Adding from head  - to handle case that all of operations must be O(1) TC
    def add_to_head(self, name, value):
        possible_head = ValueNode(name=name, value=value, next=self.head)
        if self.head:
            self.head.prev = possible_head
        self.head = possible_head


# entity_name = self.request.get('name').strip()
# entity_value = self.request.get('value').strip()
#    strip() is used to handle wrong user input

class GetHandler(webapp2.RequestHandler):
    def get(self):
        name = self.request.get('name').strip()
        entity_value = client.get(name)
        self.response.write(entity_value)


class SetHandler(webapp2.RequestHandler):
    def get(self):
        entity_name = self.request.get('name').strip()
        entity_value = self.request.get('value').strip()
        key = client.key('Value', entity_name)
        entity_to_store = datastore.Entity(key=key)
        entity_to_store.update({
            'name': entity_name,
            'value': entity_value
        })
        client.put(entity_to_store)
        res = client.get(key)
        self.response.write(res)


class UnsetHandler(webapp2.RequestHandler):
    def get(self):
        entity_name = self.request.get('name').strip()
        key = client.key('Value', entity_name)
        entity_to_update = datastore.Entity(key=key)
        entity_to_update.update({
            'name': entity_name,
            'value': None
        })
        client.put(entity_to_update)
        res = client.get(key)
        self.response.write(res)


class NumEqualToHandler(webapp2.RequestHandler):
    def get(self):
        entity_value = self.request.get('value').strip()
        query = client.query(kind='Value')
        query.add_filter('value', '=', entity_value)
        entities = list(query.fetch())
        self.response.write(len(entities))


# class UndoHandler(webapp2.RequestHandler):
#     def undo(self):
#
#
# class RedoHandler(webapp2.RequestHandler):
#     def redo(self):


class EndHandler(webapp2.RequestHandler):
    def get(self):
        query = client.query(kind='Value')
        results = query.fetch()
        for res in results:
            client.delete(res.key)
        check_results = list(query.fetch())
        if len(check_results) == 0:
            self.response.write('CLEANED')
        else:
            self.response.write('Something went wrong')


app = webapp2.WSGIApplication([ \
    ('/get', GetHandler),
    ('/set', SetHandler),
    ('/unset', UnsetHandler),
    ('/numequalto', NumEqualToHandler),
    # ('/undo', UndoHandler),
    # ('/redo', RedoHandler),
    ('/end', EndHandler),
], debug=True)
