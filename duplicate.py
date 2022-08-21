from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener
import win32api
import time


intervals=[]

events=[]
clicks=[]
cleaned_clicks=[]
presses=[]
cleaned_presses=[]
movements=[]

def on_click(x, y, button, pressed):

    if pressed:
        # print(f'Mouse clicked at ({x}, {y}) with {button}')
        if str(button)=='Button.left':
            events.append('click')
            # if(clicks):
            #     interval=time.time()-clicks[-1]['time']
            #     clicks.append({'rest':interval})
            clicks.append({'event':"left_click",'coords':(x,y),'time':time.time()})

        elif str(button)=='Button.right':
            events.append('click')
            # if(clicks):
            #     interval=time.time()-clicks[-1]['time']
            #     clicks.append({'rest':interval})
            clicks.append({'event':"right_click",'coords':(x,y),'time':time.time()})
    else:
        clicks.append({'event':'mouse_release'})



def clean_clicks(clicks):
    for i in range(len(clicks)-1):
        if(clicks[i]['event']=='left_click'):

            if(clicks[i+1]['event']=='mouse_release'):
                cleaned_clicks.append({
                    "event":'left_click',"coords":clicks[i]['coords']
                    })
            elif(clicks[i+1]['event']=='move'):
                cleaned_clicks.append({
                    "event":'left_drag',"coords":clicks[i]['coords']
                    })


        if(clicks[i]['event']=='right_click'):

            if(clicks[i+1]['event']=='mouse_release'):
                cleaned_clicks.append({
                    "event":'right_click',"coords":clicks[i]['coords']
                    })
                
                
            elif(clicks[i+1]['event']=='move'):
                cleaned_clicks.append({
                    "event":'right_drag',"coords":clicks[i]['coords']
                    })


def on_press(key):
    keyer=str(key)
    keyer=keyer.replace("'","")

    presses.append({"event":"key_press",'value':keyer})
    if str(key)=='Key.esc':
        # print(f'actual_moves...{actual_moves}')
        # print(f'actual_l_drags...{actual_l_drags}')
        # print(f'actual_r_drags...{actual_r_drags}')
        # print(ordered_events)
        clean_clicks(clicks)
        wording(presses)

        # print(cleaned_presses)
        # print(cleaned_clicks)
        print(events)
        keyboard_listener.stop()
        mouse_listener.stop()


def wording(presses):
    word=''
    for i in presses:
        if(i['event']=='key_press'):
            if(i['value'].isalpha()):
                word+=str(i['value'])
            elif(i['value']=='Key.space'):
                word+=' '
            else:
                
                if(word):
                    cleaned_presses.append({'event':"type","value":word})
                    events.append('type')
                    word=''
                cleaned_presses.append(i)
                events.append('press')
                    







def on_release(key):
    keyer=str(key)
    keyer=keyer.replace("'","")

    presses.append({"event":"key_release",'value':keyer})





def on_move(x, y):
    movements.append({"event":'move','coords':(x,y)})
    # events.append('move')





# Setup the listener threads
keyboard_listener = KeyboardListener(on_press=on_press,on_release=on_release)
mouse_listener = MouseListener(on_move=on_move, on_click=on_click)


# Start the threads and join them so the script doesn't end early
keyboard_listener.start()
mouse_listener.start()
keyboard_listener.join()
mouse_listener.join()