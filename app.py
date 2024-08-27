from flask import Flask, render_template, jsonify, request,send_file
from werkzeug.utils import secure_filename
from src.components.Component import TTS_Components
from src.logging import logger
from flask_cors import CORS
from pydub import AudioSegment
from datetime import datetime
import os


app = Flask(__name__)
CORS(app)


TTS_OBJ = TTS_Components()
logger.info('TTS compnenets class')

@app.route("/")
def index():
    logger.info('Home page')
    return render_template('chat.html')



@app.route("/get", methods=["GET", "POST"])
def get():
    msg = request.form["msg"]
    input = msg
    print(input)
    return input


@app.route("/send", methods=["POST"])
def send():
    try:

        if "audio_file" not in request.files:

            msg = request.form["send_msg"]
            logger.info('User query: ',msg)
        
            print(f"this message is fron send api {msg}")
            print("-"*10)
            response =TTS_OBJ.response_llm(msg)
            print(response)
            print("-"*10)
            
            return response
    
        if request.files['audio_file']:
            print('file get from audio')
            file = request.files["audio_file"]
        
            if file:
                # dt.AUDI_FILE_S2C = file

                print("file get")
                uniqfilename = str(datetime.now().timestamp()).replace(".","")
                file.save(f"{uniqfilename}.wav")
                # path = os.path.join("./Data",f"{uniqfilename}.wav")
                # print(path)
                text_res=TTS_OBJ.voice_to_text(f"{uniqfilename}.wav")
                print("Query-----------")
                print(text_res)
                txt_respone=TTS_OBJ.response_llm(text_res)
                print("Result------------")
                print(txt_respone)
                voice_res_file =TTS_OBJ.text_voice(txt_respone)
                # file.save(f"Data/{file.filename}")
                # with open(f"Data/{file.filename}", 'wb') as f:
                #     f.write(file.read())
                # with open(file, 'r') as f: 
                
            
               
                # print(f"file name from sendfronclientapi is {}")
                return send_file(voice_res_file)
            
       
    except Exception as e:
        raise e    




if __name__ == '__main__':
    app.run(host="0.0.0.0",port=8080,debug=True)