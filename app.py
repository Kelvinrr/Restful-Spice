from flask import Flask, jsonify, request

from kernel_manager import create_kernel_listing
from create_isd import isd_from_json
from utils import NumpyAwareJSONEncoder

# Configure the app
app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')

@app.route('/')
def index():
    data = {'status':'success',
            'apis':{1.0:'api/1.0'}}

    return jsonify(data)


@app.route('/api/1.0/csm_isd', methods=['GET', 'POST'])
def generate_isd():
    resp = {'success':True,
                'data':{}}
    if request.method == 'POST':
        data = request.get_json(force=True)
        isd = isd_from_json(data, app.meta_kernels)
        resp['data']['isd'] = isd
        resp['data']['loaded_kernels'] = None
    else:
        resp['data'] = 'Describe this end point'
    return jsonify(resp)

@app.route('/api/1.0')
def api_description():
    resp = {'success':True, 'data':{}}
    data = resp['data']
    data['available_missions'] = app.config['AVAILABLE_MISSIONS']
    return jsonify(resp)

@app.route('/api/1.0/socet_set', methods=['GET', 'POST'])
def socet_set():
    resp = {'success':True,
                'data':{}}
    if request.method == 'POST':
        data = request.get_json(force=True)
        #sset = my_func_to_create_a_set_as_json()
        sset = None
        resp['data']['set'] = sset
        resp['data']['loaded_kernels'] = None
    else:
        resp['data'] = 'POSTing to this endpoint will return a SOCET compliant .set file.'
    return jsonify(resp)

@app.route('/api/1.0/<body>')
def available_missions_by_body(body):
    resp = {'success':True, 'data':{}}
    data = resp['data']
    body = body.lower()
    missions = list(app.meta_kernels[body].keys())
    data['links'] = []

    for i in missions:
        data['links'].append({'name':i,
                   'href':'/api/1.0/{}/{}'.format(body, i)})
    return jsonify(resp)

@app.route('/api/1.0/<body>/<mission>')
def available_kernels(body, mission):
    resp = {'success':True, 'data':{}}
    data = resp['data']
    body = body.lower()
    mission = mission.lower()
    kernels = app.meta_kernels[body][mission]
    data['kernels'] = kernels
    data['description'] = "All available meta kernels for a given body and mission in sorted order.  The first meta kernel in the list will be loaded unless a different metakernel is specified."
    return  jsonify(resp)

@app.route('/api/1.0/<body>/<mission>/<year>')
def available_kernels_by_year(body, mission, year):
    resp = {'success':True, 'data':{}}
    data = resp['data']
    body = body.lower()
    mission = mission.lower()
    kernels = app.meta_kernels[body][mission][year]
    data['kernels'] = kernels
    data['description'] = "All available meta kernels for a given body and mission in sorted order.  The first meta kernel in the list will be loaded unless a different metakernel is specified."
    return  jsonify(resp)

if __name__ == '__main__':
    app.meta_kernels = create_kernel_listing(app.config['AVAILABLE_MISSIONS'])
    app.json_encoder = NumpyAwareJSONEncoder
    app.response_failure = {'success':False, 'error_msg':""}
    app.run()
