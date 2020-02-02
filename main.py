import webapp2
from google.cloud import datastore

client = datastore.Client()


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
    # TODO
    def get(self):
        entity_name = self.request.get('name').strip()
        client.delete(entity_name)


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
    ('/undo', UndoHandler),
    ('/redo', RedoHandler),
    ('/end', EndHandler),
], debug=False)
