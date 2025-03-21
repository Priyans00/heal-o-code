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

@app.route('/')
def hello():
    return {"status":"its working"}

# ENTRY
@app.route('/entry', methods = ['GET','POST'])
def entry():
    supabase = get_db_connection()
    data = request.json
    srn = data.get('srn')
    data2 = supabase.table('participant').select("entry").eq("srn",srn).execute()
    if data2.data and data2.data[0].get("entry") is not None :
        return {"srn":srn , "status": "has already entered", "response ":data2.data}
    else :
        try:
            response = supabase.table('participant').update({'entry':"done"}).eq("srn",srn).execute()
            return {"status":"done","response":response}
        except Exception as e:
            return {"status":"error","error":str(e)}

# DINNER
@app.route('/dinner', methods = ['GET','POST'])
def dinner():
    supabase = get_db_connection()
    data = request.json
    srn = data.get('srn')
    data2 = supabase.table('participant').select("dinner").eq("srn",srn).execute()
    
    if data2.data and data2.data[0].get("dinner") is not None:
        return {"srn":srn , "status": "has already done dinner", "response ":data2.data}
    else :
        try:
            response = supabase.table('participant').update({'dinner':"done"}).eq("srn",srn).execute()
            return {"status":"done","response":response}
        except Exception as e:
            return {"status":"error","error":str(e)}


# SNACKS
@app.route('/snacks', methods = ['GET','POST'])
def snacks():
    supabase = get_db_connection()
    data = request.json
    srn = data.get('srn')
    data2 = supabase.table('participant').select("snacks").eq("srn",srn).execute()
    if data2.data and data2.data[0].get("snacks") is not None :
        return {"srn":srn , "status": " already got snacks", "response ":data2.data}
    else :
        try:
            response = supabase.table('participant').update({'snacks':"done"}).eq("srn",srn).execute()
            return {"status":"done","response":response}
        except Exception as e:
            return {"status":"error","error":str(e)}


# BREAKFAST
@app.route('/breakfast', methods = ['GET','POST'])
def breakfast():
    supabase = get_db_connection()
    data = request.json
    srn = data.get('srn')
    data2 = supabase.table('participant').select("breakfast").eq("srn",srn).execute()
    
    if data2.data and data2.data[0].get("breakfast") is not None:
        return {"srn":srn , "status": "has already done breakfast", "response ":data2.data}
    else :
        try:
            response = supabase.table('participant').update({'breakfast':"done"}).eq("srn",srn).execute()
            return {"status":"done","response":response}
        except Exception as e:
            return {"status":"error","error":str(e)}


app.debug = True
if __name__ == "__main__" :
    app.run()