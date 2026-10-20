

from jinja2 import Template
import requests

import yaml
import logging
import sys
import re
import json

import utl
import tts

def init(config):
    config['context'] = []
    config['currentResponseNum'] =  0
    config['image'] = None
    config['promptTokens'] = 0
    config['tokens'] = 0

    path = "./templates/"+config['init']
    logging.info("creating chat from "+path)

    with open(path, 'r') as f:
        prompt = Template(f.read()).render(config)

    chat(config,prompt)


def get(config):
    return config['currentResponse']

def models(config):

    headers = {}
    if config['key'] != None:
       headers['X-API-Key'] = config['key']

    thelist = requests.get(config['tags'],headers=headers)
    jsondata = thelist.json()
    result = ""

    for model in jsondata["models"]:
        result = result + model['model']+ "\n"
    return result


def chat(config, msg):

    if config['image'] != None:
        config['context'].append({"role": "user", "content": msg, "images": [config['image']]})
        config['image'] = None
    else:
        config['context'].append({"role": "user", "content": msg})

    payload = {
       "model":  config['model'],
       "messages": config['context'],
       "think": config['think'],
       "stream": False
    }

    if config['temperature'] != None:
        payload["temperature"]=config['temperature']

    logging.info("asking "+config['model']+" via "+config['chat'])

    print("\n... asking llm, please wait")
#    print(payload)

    headers = {}
    if config['key'] != None:
       headers['X-API-Key'] = config['key']

    response = requests.post(config['chat'], headers=headers, json=payload)    

#    print (response.json())
    assistant_message = response.json()['message']
    config['context'].append(assistant_message)

    config['prompt_eval_count'] = response.json()['prompt_eval_count']
    config['promptTokens'] = config['promptTokens']+config['prompt_eval_count']

    config['eval_count'] = response.json()['eval_count']
    config['tokens'] = config['tokens']+config['eval_count']
    config['eval_duration'] = "{:.2f}".format(response.json()['eval_duration']/1000000000)
    config['speed'] = "{:.2f}".format(response.json()['eval_count'] / ( response.json()['eval_duration']/1000000000))

    config['total_duration'] = "{:.2f}".format(response.json()['total_duration']/1000000000)


    config['currentResponse'] = assistant_message['content']
    config['currentResponseNum'] = config['currentResponseNum']+1


    if config['think']:
        if config['thinkShow']:
           if 'thinking' in assistant_message:
               config['currentThinking'] = assistant_message['thinking']
           else:
               config['currentThinking'] = None
               del config['currentThinking']

#    return assistant_message['content']



def saveContext(config):    
    utl.prepareFolder(config['saves'])
    fname = config['saves']+"/"+utl.tf() + ".json"
    utl.saveFile(fname,  json.dumps(config['context'], indent=4))
    return fname


def loadContext(fname,config):
    config['context'] = json.loads(utl.readFile(config['saves']+"/"+fname))
    

def say (config):
    tts.say(config['currentResponse'],config)
