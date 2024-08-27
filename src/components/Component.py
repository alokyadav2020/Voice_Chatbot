import whisper
from langchain_community.llms import HuggingFaceHub
from elevenlabs.client import ElevenLabs
from elevenlabs import save
from datetime import datetime
from dotenv import load_dotenv
from src.logging import logger
load_dotenv()
import os

os.environ['HUGGINGFACEHUB_API_TOKEN'] =os.getenv('HUGGINGFACEHUB_API_TOKEN')


class TTS_Components:
    def __init__(self):
        # self.huggingface_key = os.getenv('HUGGINGFACEHUB_API_TOKEN')
        self.hf_llm = HuggingFaceHub(
                                repo_id="mistralai/Mistral-7B-Instruct-v0.2",
                                model_kwargs={"temperature": 0.5, "max_length": 64,"max_new_tokens":512}

                                 )
        self.client = ElevenLabs(api_key=os.getenv('api_key'))
        self.model = whisper.load_model("base")




    def voice_to_text(self,file_path)->str:

        try:
            # model = whisper.load_model("base")
            text_result = self.model.transcribe(file_path)
            print(text_result["text"]) 
            txt_result= text_result["text"]
            logger.info('Text Extracted from audio: ',txt_result)

            return txt_result   
        
        except Exception as e:
            logger.error('In function, voice_to_text',e)
            raise('Error',e)
            
        
        

    def response_llm(self,query_text:str):

        try:
            # hf_llm=HuggingFaceHub(
            #                     repo_id="mistralai/Mistral-7B-Instruct-v0.2",
            #                     model_kwargs={"temperature": 0.5, "max_length": 64,"max_new_tokens":512}

            #                      )
            
            

            prompt = f"""
            <|system|>
            You are an AI assistant that follows instruction extremely well.
            Please be truthful and give direct answers  within two lines.

            </s>
            <|user|>
            {query_text}
            </s>
            <|assistant|>
            """

            respons=self.hf_llm.generate(prompts=[prompt])
            res =respons.generations[0][0].text
            parsed_response = res.split("<|assistant|>")[-1].strip()

            print(parsed_response)
            logger.info("LLM Response: ",parsed_response)

            return parsed_response
        
        except Exception as e:
            raise('Error',e)
        


    def text_voice(self,text_response):
        try:

            audio  = self.client.generate(text=  text_response,voice="Rachel", model="eleven_multilingual_v2")
            uniqfilename = str(datetime.now().timestamp()).replace(".","")
            save(audio,f"Data/{uniqfilename}.mp3")
            logger.info("Saved Audio fle path: ",f"Data/{uniqfilename}.mp3")
            return f"Data/{uniqfilename}.mp3"    
        
        except Exception as e:
            raise e
            
