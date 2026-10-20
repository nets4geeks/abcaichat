

import logging
import sys

import utl
import llm
import conf
import ver
import inf



def menu():
    llm.init(config)

    while True:
        inf.show("",config['hintTemplate'], config)
        i = input(">>> ")

        if (i == '/exit') or (i == '/e'):
           exit(0)

        if (i == '/models') or (i == '/m'):
           models = llm.models(config)
           inf.show(models,config['extraTemplate'],config)
           continue

        if (i == '/image') or (i == '/i'):
           fname = input(" image file: ")
           if utl.exists(fname):
               config['image'] = utl.encode(fname)
               print(f"... attached image from {fname}")
           else:
               print(f"\n... :(( image {fname} wasn't found \n")
           continue

        if (i == '/save') or (i == '/s'):
           fname = llm.saveContext(config)
           print(f"\n... saving context as {fname}")
           continue

        if (i == '/load') or (i == '/l'):
           arr = utl.getFolder(config['saves'])
           sn = ""
           for index, value in enumerate(arr):
               sn = sn + "["+str(index)+"] "+str(value)+"\n"

           inf.show(sn, config['extraTemplate'],config)
           i = int(input("enter save's number ('9999' to exit): "))
           if (i == 9999):
               continue
           llm.loadContext(arr[i],config)
           print(f"\n... context from {arr[i]} has been loaded")
           continue

        if (i == '/help') or (i == '/h'):
           inf.show("",config['helpTemplate'],config)
           continue

        if (i == '/talk') or (i == '/t'):
           llm.say(config)
           continue


        if (i == '/file') or (i == '/f'):
           fname = input(" file name: ")
           if utl.exists(fname):
               i = utl.readFile(fname)
               inf.show(i, config['sendTemplate'], config)               
           else:
               print(f"\n... :(( file {fname} wasn't found\n")
               continue

        llm.chat(config,i)
        inf.show("", config['chatTemplate'], config)


config = conf.get(sys.argv[1])


inf.show("",config['infoTemplate'], config)

menu()

