from supabase import create_client, Client
import csv
from flask import Flask, request
from dotenv import load_dotenv
import os


app = Flask(__name__)

load_dotenv()

url = os.environ.get('SUPABASE_URL')
key = os.environ.get('SUPABASE_KEY')

def get_db_connection():
    if not url or not key:
        raise ValueError("missing url or key")
    supabase: Client = create_client(url, key)
    return supabase

# qr_data = ["PES2UG24CS453",'','','','']

# qr_data format - [srn,entry,dinner,snacks,breakfast]
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
    if data2.data[0].get("entry") is not None :
        return {"srn":srn , "status": "has already entered", "response ":data2.data}
    else :
        try:
            supabase.table('participant').update({'entry':"done"}).eq("srn",srn).execute()
            return {"data":"done"}
        except Exception as e:
            return "error occured"

# DINNER
@app.route('/dinner', methods = ['GET','POST'])
def dinner():
    supabase = get_db_connection()
    data = request.json
    srn = data.get('srn')
    data2 = supabase.table('participant').select("dinner").eq("srn",srn).execute()
    if data2.data[0].get("dinner") is not None :
        return {"srn":srn , "status": "has already done dinner", "response ":data2.data}
    else :
        try:
            supabase.table('participant').update({'dinner':"done"}).eq("srn",srn).execute()
            return {"data":"done"}
        except Exception as e:
            return "error occured"

# SNACKS
@app.route('/snacks', methods = ['GET','POST'])
def snacks():
    supabase = get_db_connection()
    data = request.json
    srn = data.get('srn')
    data2 = supabase.table('participant').select("snacks").eq("srn",srn).execute()
    if data2.data[0].get("snacks") is not None :
        return {"srn":srn , "status": " already got snacks", "response ":data2.data}
    else :
        try:
            supabase.table('participant').update({'snacks':"done"}).eq("srn",srn).execute()
            return {"data":"done"}
        except Exception as e:
            return "error occured"

# BREAKFAST
@app.route('/breakfast', methods = ['GET','POST'])
def breakfast():
    supabase = get_db_connection()
    data = request.json
    srn = data.get('srn')
    data2 = supabase.table('participant').select("breakfast").eq("srn",srn).execute()
    if data2.data[0].get("dinner") is not None :
        return {"srn":srn , "status": "has already done breakfast", "response ":data2.data}
    else :
        try:
            supabase.table('participant').update({'breakfast':"done"}).eq("srn",srn).execute()
            return {"data":"done"}
        except Exception as e:
            return "error occured"


if __name__ == "__main__" :
    app.run(debug=True)