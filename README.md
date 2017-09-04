# eyetoai

git checkout -b ai_ranking 

Make sure that you are running Python 3.6.0 or later 
Open shell, go to eyetoai/database/

If using Windows:
1. In the shell:
$pip install curl 
$pip install pymongo
$pip install numpy
$pip install Flask
$python predict_upd.py

This will download dependencies and run your code, localhost will listen to everything. Don't be afraid of browser message.

2. Open  another cmd, and send test POST request via curl:

$curl -X POST -H "Content-Type: application/json" -d "{ \"condition\": \"Fibroadenoma\",\"findings\": [\"Mass\"] }" http://localhost:8000/

Where condition can be any condition from database and findings is an array of findings (can be unlimited size).
Make sure using escaping quotes - Windows is sensitive.

If everything is ok, you will receive a fraction as a result in your shell. 
For example request, correct result is 5.90636393769

TODO:
You have to send result back to your server and coordinate everything with UI, so ranking (see Workflow) will work as is.
Please sort everything by DESC order.
