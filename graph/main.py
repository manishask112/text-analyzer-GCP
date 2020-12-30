from google.cloud import storage
from matplotlib import pyplot as plt
import json
import base64
from PIL import Image
import io
from flask import jsonify

def graph(request):

    storage_client = storage.Client()
    bucket_name = "gcf-sources-353018688455-us-central1"
    
    json_name = json.loads(request.get_data())
    source_blob_name = ''
    if json_name:
        source_blob_name = json_name['file_name']
    else:
        return format("Undone")

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)

    distribution_json = json.loads(blob.download_as_string())
    sentence_length = list(distribution_json.keys()) 
    distribution = list(distribution_json.values()) 
    
    fig = plt.figure(figsize = (30, 15)) 
    
    # creating the bar plot 
    plt.bar(sentence_length, distribution, color ='maroon',  
            width = 0.4) 
    
    plt.xlabel("Words per sentence") 
    plt.ylabel("Distribution") 
    plt.title("Sentence Distribution") 

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    b64string = base64.b64encode(buf.getvalue()).decode('utf-8').replace('\n', '')
    buf.close()

    response = jsonify({"graph_as_string" : b64string})

    response.headers.add('Access-Control-Allow-Origin', '*')
    # return json.dumps({"fig_name" : distribution_json_file_name + ".png"})
    return response
    # return format(b64string)