from supabase import create_client, Client
from flask import Flask, request
from dotenv import load_dotenv
import os
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

load_dotenv()

url = os.environ.get('SUPABASE_URL')
key = os.environ.get('SUPABASE_KEY')

def get_db_connection():
    if not url or not key:
        raise ValueError("missing url or key")
    supabase: Client = create_client(url, key)
    return supabase

def handle_update(srn, column):
    supabase = get_db_connection()
    data2 = supabase.table('participant').select(column).eq('srn',srn).execute()
    if data2.data is None :
        return {"srn":srn,"status":"error","response":"Given SRN not in database"}
    elif data2.data and data2.data[0].get(column) is not None :
        return {"srn":srn, "status":"has already done", "response":data2.data}
    else :
        try :
            response = supabase.table('participant').update({column:"done"}).eq("srn",srn).execute()
            return {"srn":srn,"status":"not done before","response":response.data}
        except Exception as e:
            return {"srn":srn,"status":"error","error":str(e)}

def show_all_data():
    try :
        supabase = get_db_connection()
        data2 = supabase.table('participant').select('*').execute()
        return {"status":"done",'data':data2.data}
    except Exception as e :
        return {"status":"error","error":str(e)}
    
@app.route('/')
def hello():
    return {"status":"its working"}

# ENTRY
@app.route('/entry', methods = ['GET','POST'])
def entry():
    data = request.json
    srn = data.get('srn')
    return handle_update(srn,"entry")

# DINNER
@app.route('/dinner', methods = ['GET','POST'])
def dinner():
    data = request.json
    srn = data.get('srn')
    return handle_update(srn,"dinner")

# SNACKS
@app.route('/snacks', methods = ['GET','POST'])
def snacks():
    data = request.json
    srn = data.get('srn')
    return handle_update(srn,"snacks")


# BREAKFAST
@app.route('/breakfast', methods = ['GET','POST'])
def breakfast():
    data = request.json
    srn = data.get('srn')
    return handle_update(srn,"breakfast")

@app.route('/database' , methods = ['GET'])
def database():
    return show_all_data()


app.debug = True
if __name__ == "__main__" :
    app.run()