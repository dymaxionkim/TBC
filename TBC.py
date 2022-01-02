import os
import PySimpleGUI as sg
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def Transform(Xinput,Yinput,Xmove,Ymove):
    Xoutput = Xinput + Xmove
    Youtput = Yinput + Ymove
    return Xoutput,Youtput

def Circle(DIA,SEG_CIRCLE):
    THETA0 = np.linspace(0.0,2*np.pi,SEG_CIRCLE)
    XX = DIA/2*np.sin(THETA0)
    YY = DIA/2*np.cos(THETA0)
    return XX,YY

def BeltLength():
    spec.loc['WorkingDirectory']=[values['-WorkingDirectoty-'],'','Working Directory']
    spec.loc['C']=[float(values['-C-']),'mm','Center Distance']
    spec.loc['D']=[float(values['-D-']),'mm','1st Pulley Dia']
    spec.loc['d']=[float(values['-d-']),'mm','2nd Pulley Dia']
    spec.loc['L']=[2*spec.Content['C']+1.57*(spec.Content['D']+spec.Content['d'])+((spec.Content['D']-spec.Content['d'])**2)/(4*spec.Content['C']),'mm','Belt Length']
    spec.loc['p']=[float(values['-p-']),'mm','Pitch']
    spec.loc['z']=[spec.Content['L']/spec.Content['p'],'ea','Belt Teeth Number']

def CenterDistance():
    spec.loc['WorkingDirectory']=[values['-WorkingDirectoty-'],'','Working Directory']
    spec.loc['D']=[float(values['-D-']),'mm','1st Pulley Dia']
    spec.loc['d']=[float(values['-d-']),'mm','2nd Pulley Dia']
    spec.loc['p']=[float(values['-p-']),'mm','Pitch']
    spec.loc['z']=[float(values['-z-']),'ea','Belt Teeth Number']
    spec.loc['L']=[spec.Content['p']*spec.Content['z'],'mm','Center Length']
    a=8.0
    b=(1.57*4.0)*(spec.Content['D']+spec.Content['d'])-4*spec.Content['L']
    c=(spec.Content['D']-spec.Content['d'])**2
    spec.loc['C']=[(-b+np.sqrt((b**2)-4*a*c))/(2*a),'mm','Center Distance']

def UpdateValues():
    window['-C-'].update(spec.Content['C'])
    window['-D-'].update(spec.Content['D'])
    window['-d-'].update(spec.Content['d'])
    window['-z-'].update(spec.Content['z'])
    window['-p-'].update(spec.Content['p'])

def UpdateDisabled():
    if values['-belt_length-']:
        window['-C-'].update(disabled=False)
        window['-D-'].update(disabled=False)
        window['-d-'].update(disabled=False)
        window['-z-'].update(disabled=True)
        window['-p-'].update(disabled=False)
    elif values['-center_distance-']:
        window['-C-'].update(disabled=True)
        window['-D-'].update(disabled=False)
        window['-d-'].update(disabled=False)
        window['-z-'].update(disabled=False)
        window['-p-'].update(disabled=False)

def TBC_PLOT():
    # Figure
    fig = plt.figure()
    plt.axes().set_aspect('equal')
    plt.title('Timing Belt Cacluator')
    plt.grid(True)
    # D
    XD,YD = Circle(spec.Content['D'],360)
    XD,YD = Transform(XD,YD,0,0)
    plt.plot(XD,YD, '-', linewidth=1.5, color='black')
    # d
    Xd,Yd = Circle(spec.Content['d'],360)
    Xd,Yd = Transform(Xd,Yd,spec.Content['C'],0)
    plt.plot(Xd,Yd, '-', linewidth=1.5, color='black')
    # Figure
    Result = os.path.join(spec.Content['WorkingDirectory'], f'Result.png')
    plt.savefig(Result,dpi=100)
    plt.show()

##############################
# GUI
sg.theme('Default')
col = [[sg.Text('Working Directory :',size=(15,1)),sg.Input('./Result/',key='-WorkingDirectoty-',size=(30,1)), sg.FolderBrowse()],
        [sg.Text('# Input Mode : ',size=(12,1)),sg.Radio('Belt_Length','RADIO2',key='-belt_length-',default=True,enable_events=True,size=(12,1)),sg.Radio('Center_Distance','RADIO2',key='-center_distance-',enable_events=True,size=(12,1)),sg.Button('Update')],
        [sg.Text('Center Distance, C =',size=(32,1)),sg.Input(100.0,key='-C-',size = (10,1)),sg.Text('[mm]')],
        [sg.Text('1st Pulley Dia, D =',size=(32,1)),sg.Input(50.0,key='-D-',size=(10,1),disabled=True),sg.Text('[mm]')],
        [sg.Text('2nd Pulley Dia, d =',size=(32,1)),sg.Input(20.0,key='-d-',size=(10,1)),sg.Text('[mm]')],
        [sg.Text('Belt Teeth Number, z =',size=(32,1)),sg.Input(312.15,key='-z-',size=(10,1),disabled=True),sg.Text('[ea]')],
        [sg.Text('Pitch, p =',size=(32,1)),sg.Input(1.0,key='-p-',size=(10,1),disabled=True),sg.Text('[mm]')],
        [sg.Button('Run'),sg.Button('Exit')]]

layout = [[col]]
window = sg.Window('TBC',layout,icon="TBC.ico")

spec = pd.DataFrame(columns=['Parameter','Content','Unit','Remark'])
spec = spec.set_index('Parameter')

while True:
    event,values=window.read()
    if event in (sg.WIN_CLOSED,'Exit'):
        break
    elif event=='Run':
        if values['-belt_length-']:
            BeltLength()
            UpdateValues()
        elif values['-center_distance-']:
            CenterDistance()
            UpdateValues()
        os.makedirs(spec.Content['WorkingDirectory'],exist_ok=True)
        Result = os.path.join(spec.Content['WorkingDirectory'],f'Result.csv')
        spec.to_csv(Result,header=True,index=True)
        TBC_PLOT()
    elif event=='Update':
        if values['-belt_length-']:
            BeltLength()
            UpdateValues()
        elif values['-Center_Distance-']:
            CenterDistance()
            UpdateValues()
        UpdateValues()
    elif values['-belt_length-']:
        BeltLength()
        UpdateValues()
        UpdateDisabled()
    elif values['-center_distance-']:
        CenterDistance()
        UpdateValues()
        UpdateDisabled()
window.close()
