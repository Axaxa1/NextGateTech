from firebase_admin import credentials, firestore
import firebase_admin

def hello_world(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    request_json = request.get_json()
    if request.args and 'message' in request.args:
        return request.args.get('message')
    elif request_json and 'message' in request_json:
        return request_json['message']
    else:
        app = firebase_admin.initialize_app()
        datab = firestore.client(app=app)
        testsref = datab.collection(u'tests')
        docs = testsref.stream()
        ret = ""
        for doc in docs:
            # ret += ('{} : {}'.format(doc.id, doc.to_dict()))
            a, b = doc.id, doc.to_dict()
            check = True
            for key in b.keys():
                check = b[key] and check
            ret += "Result for " + str(a) + " : " + str(check) + "\n"

        return ret

