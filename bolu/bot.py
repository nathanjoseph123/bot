from google import genai
import requests
import time
import threading
import json5
import os

class custom_bot:
    def __init__(self,url,api_key,auth,persona,bot_id,timer,specific_id=None):
        
        self.load_file={}
        self.url=url
        self.api_key=api_key
        self.auth={"authorization":auth}
        self.message=[]
        self.to_be_sent=[]
        self.message_reponded_to=[]
        self.power_on=True
        self.move_on=True
        self.timer=timer
        self.counter=0
        self.bot_id=bot_id
        self.start_time=str(time.ctime().split(' ')[3]).replace(':','')
        self.date=time.localtime()
        self.year=str(self.date[0])
        self.month=['0'+str(i) if len(str(i))==1 else str(i) for i in [self.date[1]]][0]
        self.day=['0'+str(i) if len(str(i))==1 else str(i) for i in [self.date[2]]][0]
        self.date=int(self.year+self.month+self.day)
        self.specific_id=specific_id
        self.preson_in=[]
        self.persona=persona
        try:
            if os.path.exists('file.json'):
                with open ('file.json' ,'r') as file:
                    self.load_file=json5.load(file)
                if self.load_file.get(api_key):
                    if self.load_file[api_key]['date'] <self.date:
                        self.load_file[api_key]['date']=self.date
                        self.load_file[api_key]['count']=0
                    else:
                        custom_bot.counter=self.load_file[api_key]['count']

                else:
                    self.load_file[api_key]={'date':self.date,'count':custom_bot.counter}
            else:
                self.load_file[api_key]={'date':self.date,'count':custom_bot.counter}
                with open('file.json','w') as file:
                    json5.dump(self.load_file,file,indent=5)
            custom_bot.counter=self.load_file[api_key]['count']
        except Exception as e:
            self.load_file[api_key].update({api_key:{'date':self.date,'count':custom_bot.counter}})
        threading.Thread(target=self.retrive_message).start()
        threading.Thread(target=self.send_message).start()
    def retrive_message(self):
        while True:
            try:
                if self.move_on:
                    message=requests.get(self.url,headers=self.auth).json()
                    self.message=[mess for mess in message if mess not in self.message and int(mess['timestamp'].split('T')[1].split('.')[0].replace(':',"").split("+")[0])>(int(self.start_time)-10000) and int(mess['timestamp'].split('T')[0].replace('-',''))>=self.date and len(mess['mentions'])>0 and mess['mentions'][0]['id']==self.bot_id and str(mess['author']['id'])!=str(self.bot_id) or str(mess['author']['id'])==str(self.specific_id) and int(mess['timestamp'].split('T')[1].split('.')[0].replace(':',"").split("+")[0])>(int(self.start_time)-10000) and int(mess['timestamp'].split('T')[0].replace('-',''))>=self.date]
                    self.preson_in=[mess for mess in message if mess['author']['id']==self.specific_id and int(mess['timestamp'].split('T')[1].split('.')[0].replace(':',"").split("+")[0])>(int(self.start_time)-10000) and int(mess['timestamp'].split('T')[0].replace('-',''))>=self.date]
    
            except Exception as e:
                pass
    
            time.sleep(2)
    def get_number(self):
        return self.counter

    def send_message(self):
        client = genai.Client(api_key=self.api_key)
        while True:
            try:
                if self.power_on:
                    self.move_on=False
                    for i in self.message:
                        if i not in self.message_reponded_to:
                            remove=i['content'].replace(f'{i['author']['id']}','')
                            response = client.models.generate_content(
                                model="gemini-2.5-flash", contents=f"now you are not a chatbot using this{self.persona} generate a short(real) human like response to {remove} and don't act to clever,you can speak only in english or pidgin english,make no mistake act very human like ,and make the replies be on surface level ,direct answer no fidgetting  for general knowlege or scientific question importantly speak english if spoken to in english or speak pidgin if spoken to in pidgin ",
                            )
                            requests.post(self.url,headers=self.auth,data={'content':f'<@{i['author']['id']}> {response.text}',})
                            self.message_reponded_to.append(i)
                            self.counter+=1
                            self.load_file[self.api_key]['count']=custom_bot.counter
                    for i in self.preson_in:
                        if i not in self.message_reponded_to:
                            remove=i['content'].replace(f'{i['author']['id']}','')
                            response = client.models.generate_content(
                                model="gemini-3-pro-preview", contents=f"“Answer every question in one short line with no extra words. {remove}",
                            )
                            requests.post(self.url,headers=self.auth,data={'content':f'{response.text}'})
                            self.message_reponded_to.append(i)
                            self.counter+=1
                            self.load_file[self.api_key]['count']=custom_bot.counter
                    with open('file.json','w') as file:
                        json5.dump(self.load_file,file,indent=5)
                    self.move_on=True
            
            except Exception as e:
                pass
            time.sleep(self.timer)


if __name__=='__main__':
    custom_bot(url='https://discord.com/api/v9/channels/1205439245465034768/messages',api_key='AIzaSyDDbHpoL3nvdS2sfFnacyafIf5DSYE4LsI',auth='MTQ0NjIwMDYyMzAwNjQ4MjUxMw.GTxWCs.jiiPyypCwAJhm2DRgtFMtbuVk2HvVbSIcRlUhQ',persona='i am john',bot_id='1446200623006482513',specific_id='951487931409911868',timer=2)




