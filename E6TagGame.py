tempPath = '/directory/to/folder
#Add the temp folder directory here please merci thank you
#make sure it doesn't end with a /

tempPath += '/e6tagimage'

import json
import requests
import random
import urllib.request
import PySimpleGUI as sg
import os
from PIL import Image
import tkinter

def download_progress_hook(count, blockSize, totalSize):
    sg.OneLineProgressMeter('Image Loading Now...',  count*blockSize, totalSize, 'key')

root = tkinter.Tk()
root.withdraw()
WIDTH, HEIGHT = root.winfo_screenwidth(), root.winfo_screenheight()

print('N.B. If the program skips some letters while revealing them, it\'s because the file associated to them is either a gif, video, or some flash file thing')

#sg.theme(random.choice(sg.ListOfLookAndFeelValues()))

#print('N.B. Only General Tags will be included')

headers = {"User-agent" : "TagHangman/1.0 (By WibbleTime on e621)"}
again = True
while again == True:
    e621String = "https://e621.net/posts.json?tags=order:random&limit=1"
    response = requests.get(e621String, headers = headers)
    response = response.json()

    text = json.dumps(response, indent = 4)
    tag_list = response['posts'][0]['tags']['general']
    chosen_tag = random.choice(tag_list)
    #print(chosen_tag)

    #input()

    e621String2 = "https://e621.net/posts.json?tags=order:random {0}&limit={1}".format(chosen_tag, str(len(chosen_tag)-1))
    response2 = requests.get(e621String2, headers = headers)
    response2 = response2.json()
    text2 = json.dumps(response2, indent = 4)
    #print(text2)

    file_list = []

    for i in range(len(response2['posts'])):
        tag_url = response2['posts'][i]['sample']['url']
        file_list.append(tag_url)
    #input()

    opener = urllib.request.build_opener()
    opener.addheaders = [("User-agent", "MyProject/1.0 (By WibbleTime on e621)")]
    urllib.request.install_opener(opener)

    get_correct = False
    for n in range(len(file_list)):
        sg.theme(random.choice(sg.ListOfLookAndFeelValues()))
        cannot_convert_list = [
            'swf',
            'webm',
            'gif'
        ]
        
        OGextension = response2['posts'][n]['file']['ext']
        
        if file_list[n] is None or OGextension in cannot_convert_list:
            continue
        
        actualfile = urllib.request.urlretrieve(file_list[n], ((tempPath)), reporthook=download_progress_hook)
        
        #convert jpeg to png
        im = Image.open(tempPath)
        width, height = im.size
        buffer = 0.6
        ratio = height/width
        if ratio > HEIGHT/WIDTH:
            newW = round(width / height * HEIGHT*buffer)
            newH = round(height / height * HEIGHT*buffer)
        else:
            newW = round(width / width * WIDTH*buffer)
            newH = round(height / width * WIDTH*buffer)

        im = im.resize(((newW,newH)))

        im.save(tempPath + '.png')
        
        im_new = Image.open(tempPath + '.png')
        width_pic, height_pic = im.size
        
        #print('done!')

        layout = [
            [sg.Text("+".join(response2['posts'][n]['tags']['artist'])), sg.Text(response2['posts'][n]['id'])],
            [sg.Image(tempPath + '.png', key='-IMAGE-')]
        ]
        
        clue = chosen_tag[:n+1-len(chosen_tag)] + '?'*(len(chosen_tag)-n-1) 
        
        #print(HEIGHT, WIDTH, height_pic, width_pic)
        answer_layout = [
            [sg.Text(clue, font='ANY 20')],
            [sg.Input(font='ANY 20', key='-GUESS-'), sg.Submit()]
            ]
        
        window = sg.Window('Image', layout, location = ((WIDTH/2)-width_pic/2,0))
        window.read(timeout=1)
        
        answer_window = sg.Window('Answer', answer_layout, location =(150, (HEIGHT+height_pic*buffer)/2))
        event, values = answer_window.read()
        
        if values['-GUESS-'].lower() == chosen_tag:
            score = round((len(chosen_tag)-(n+1))/len(chosen_tag)*100)
            get_correct = True
            window.close()
            answer_window.close()
            
            correct_layout = [
                [sg.Text('Well done, you got it right!', font = 'ANY 20')],
                [sg.Text('The mystery tag was ' + chosen_tag + '!', font = 'ANY 20')],
                [sg.Text('Your score is ' + str(score) + ' out of 100!', font = 'ANY 20')]

            ]
            
            correct_window = sg.Window('Correct!', correct_layout, return_keyboard_events = True)
            correct_window.read()
            correct_window.close()
            break
        window.close()
        answer_window.close()
    window.close()
    answer_window.close()
    if get_correct == False:
        incorrect_layout = [
                [sg.Text('Better luck next time,', font = 'ANY 20')],
                [sg.Text('The mystery tag was ' + chosen_tag + '!', font = 'ANY 20')],
                [sg.Text('Your score is 0 out of 100 :(', font = 'ANY 20')]
            ]
            
        incorrect_window = sg.Window('Sadly!', incorrect_layout, return_keyboard_events = True)
        incorrect_window.read()
        incorrect_window.close()
    again_layout = [
        [sg.Text('Play again?', font = 'ANY 20')],
        [sg.Yes(), sg.No()]
    ]
    
    again_window = sg.Window('Again?', again_layout, return_keyboard_events = True)
    event, values = again_window.read()
    if event in ['Yes', 'y', 'Y' 'y:29', 'Y:29', 'Enter', 'Return', 'Return:36']:
        again = True
    elif event in ['No', 'n', 'N', 'n:57', 'N:57', 'Escape:9', 'Escape'] :
        again = False
    
    again_window.close()
