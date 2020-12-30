function generateGraph() {
    var text_url = document.querySelector('#url').value;

    // text_url = text_url.replace(/\//g, "&");
    // console.log(text_url);

    // var link = "http://127.0.0.1:5000/textAnalyser/"+ text_url;
    var textAnalyserURL = "https://us-central1-manisha-suresh.cloudfunctions.net/textAnalyzer";
        // graphURL = "https://us-central1-manisha-suresh.cloudfunctions.net/graph";

    const main = document.getElementById('target');
    while (main.firstChild) main.firstChild.remove();
    const urlShow = document.getElementById('showURL');
    while (urlShow.firstChild) urlShow.firstChild.remove();
    console.log("Tiggering cloud function");
    var xmlHttp = new XMLHttpRequest(); // creates 'ajax' object
        xmlHttp.onreadystatechange = function() //monitors and waits for response from the server
        {
           if(xmlHttp.readyState === 4 && xmlHttp.status === 200) //checks if response was with status -> "OK"
           {
               var re = JSON.parse(xmlHttp.responseText); //gets data and parses it, in this case we know that data type is JSON.

               if(re)
               {
                    console.log("received response!");
                    var src = re["graph_as_string"];
                    var a = document.createElement('a');
                    var link = document.createTextNode("Click to go to text file");
                    a.appendChild(link);
                    a.title = "This is Link";
                    a.href = text_url;
                    urlShow.appendChild(a);
                    var img = document.createElement('img');
                    // image.src = 'data:image/png;base64,iVBORw0K...';
                    img.src = 'data:image/png;base64,' + src;
                    img.id = "::img"
                    img.style.cssText = 'width:100%;height:70%;'
                    main.appendChild(img);
               }
               else{
                    console.log("ERROR")
               }
           }
    
        }
        xmlHttp.open("POST", textAnalyserURL); //set method and address
        xmlHttp.send(JSON.stringify({"url":text_url})); //send data
    
    
    
    }
    
