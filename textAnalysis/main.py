import urllib
import urllib.request
import collections
import requests
import json
from google.cloud import storage
from flask import jsonify


def textAnalyser(request):

    # Get URL of text file
    text_url = json.loads(request.get_data())
    if text_url:
        url = text_url['url']
    else:
        return format("Undone")
    
    b64string = ''
    
    # *****Get Bucket to check if graph for url exists
    storage_client = storage.Client()
    bucket_name = "gcf-sources-353018688455-us-central1"
    bucket = storage_client.bucket(bucket_name)
    destination_blob_name = url

    blob = bucket.blob(destination_blob_name)
    file_exists =  blob.exists()
    if file_exists:
        b64string = json.loads(blob.download_as_string())[destination_blob_name]

    else:
        # *****Code for hitting url and performing text analysis STARTS*****
        file = urllib.request.urlopen(url)

        text_lines = ''
        for line in file:
            text_lines = text_lines + line.decode("utf-8") + ' '

        if not text_lines:
            return format("Undone")

        distribution_json = collections.defaultdict(int)
        text_lines = text_lines.split('.')

        for i,sentence in enumerate(text_lines):
            text_lines[i] = sentence.split()
            sentence_len = len(text_lines[i])
            if sentence_len:
                distribution_json[sentence_len] += 1
        # *****Code for hitting url and performing text analysis STOPS*****


        # ******Code to cache results in cloud storage***********
        

        # Upload distribution json to storage
        destination_blob_name = url
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_string(json.dumps(distribution_json))

        # Now trigger graph function
        graph_url = "https://us-central1-manisha-suresh.cloudfunctions.net/graph"
        response = requests.post(graph_url, json = {"file_name": destination_blob_name})
        b64string = json.loads(response.json())["graph_as_string"]

        # Update json file in storage
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_string(json.dumps({destination_blob_name : b64string}))

    # Return graph in string form in response
    response = jsonify({"graph_as_string" : b64string})
    response.headers.add('Access-Control-Allow-Origin', '*')
    # return json.dumps({"fig_name" : distribution_json_file_name + ".png"})
    return response

    # return format(destination_blob_name)

