from flask import Flask, request
from flask_restful import Api, Resource
import pandas as pd
import sqlite3
from itertools import groupby
import json

app = Flask(__name__)
api = Api(app)

class v2(Resource):
    def get(self):
        args = request.args
        value1 = args["report_type"]
        value2 = args["search_phrase"]

        cnx = sqlite3.connect('all.db')
        final2 = pd.read_sql_query("SELECT * FROM lost_documents", cnx)

        value = value2.split()
        res = [''.join(j).strip() for sub in value for k, j in groupby(sub, str.isdigit)]
        final2 = final2[(final2['doc_seria'] == res[0]) & (final2['doc_num'] == res[1])]
        data = final2.reset_index().to_json(orient='records', lines=True)

        data = json.dumps(json.loads(data), indent=2, sort_keys=True, ensure_ascii=False)

        print(data)


        if value1 == 'full':
            return data
        else:
            if final2.shape[0]>0:
                data = {"result":1}
            else:
                data = {"result":0}
            return data

api.add_resource(v2, '/api/v2/', endpoint='v2/')


if __name__ == '__main__':
    app.run(debug=True)