import simpleBDB as db

db.createEnvWithDir('db')

class TestResource(db.Resource):
    keys = ('first', 'second')

    pass

