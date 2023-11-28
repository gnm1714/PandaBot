from flask import Flask
from threading import Thread
from waitress import serve

app = Flask('')

@app.route('/')
def home():
  return "Running server..."

def run():
  #serve(app, host='0.0.0.0', port=8080, threads=1) #WAITRESS!
  app.run(host='0.0.0.0',port=8080)

def web_server():
  #run()
  t = Thread(target=run)
  t.start()


#@app.route('/api/v1/')
#def myendpoint():
  #return 'We are computering now'serve(app, host='0.0.0.0', port=8080, threads=1) #WAITRESS!