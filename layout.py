WindowsSize=(1100,670)
import PySimpleGUI as sg

treedata = sg.TreeData()

tab_lift = [
                 [sg.Text('Download Airfoil Data from AirfoilTools.com'),],
                 [sg.Button('Download',size=(10, 1))],
                 [sg.Text('Progress')],
                 [sg.ProgressBar(max_value=1636, size=(70, 25), orientation='h', key='ProgressBar')],
                 [sg.Text('downloading...'),sg.Text(' '*150,key='fileDown'),],
                 [sg.Text('\u0394  \u03A9  \u03C0  \u03F4  \u03BB  \u03B8 	 \u03B1 \u03B1 \u03B2 \u03B3  \u03B4  \u03B5  \u03B6  \u03B7  \u03B8  \u03B9 	 \u03BA 	 \u03BB 	 \u03BC  \u03BD  \u03BE  \u03BF  \u03C0  \u03C1  \u03C2  \u03C3  \u03C4  \u03C5  \u03C6  \u03C7  \u03C8  \u03C9  ')],
                 [sg.Text(' Ξ Θ Λ Π Φ Ψ ϴ Ω')],
 ]

tab_select = [
                 [sg.Text('Load All Airfoil Data'),sg.Button('Load',size=(10, 1),key='loadObject'),sg.Text('              '*5),sg.Radio('metric', "RADIO1",key='metric', enable_events=True,default=True, size=(5, 1)),sg.Radio('imperial ', "RADIO1",key='imperial',enable_events=True)],
                 [sg.Text('     Search the 1638 airfoils in the databases filtering by name, thickness and camber')],
                 [sg.Text('Maximum thickness(%)'),sg.Input(default_text='66.4', size=(5, 1), key='max_thick') ,sg.Text('      Minimum  thickness(%)   '),sg.Input(default_text='2', size=(5, 1), key='min_thick') ,sg.Text('(66.4 - 2.0)            ' ),sg.Button('Geometry Set',size=(13, 1))],
                 [sg.Text('Maximum    camber(%)'),sg.Input(default_text='16.4', size=(5, 1), key='max_camber'),sg.Text('      Minimum     camber(%)   '),sg.Input(default_text='0', size=(5, 1), key='min_camber'),sg.Text('(16.4 - 0.0)' )],
                 [sg.Text('Wing Lenght                '),sg.Input(default_text='1', size=(5, 1), key='wing'),sg.Text('m',key='wing_unit'),sg.Text('Minimum thickness        ' ),sg.Input(default_text='16', size=(5, 1), key='minThick'),sg.Text('cm',key='thick_unit')],
                 
                 [sg.Text('Velocity'),sg.Input(default_text='180', size=(4, 1), key='velocity'),sg.Text('km/h',key='vel_unit'),sg.Text('Chord width'),sg.Input(default_text='60', size=(3, 1), key='chord'),sg.Text('cm',key='cord_unit'),sg.Text('temperatures'),sg.Combo((-10,0,10,20),change_submits=True,default_value=20,key='temp'), sg.Text('Kinematic Viscosity, Air Dencity'),sg.Text('1.5111E-5, 1.2041 ',key='Viscosity')],
                 [sg.Text('Reynolds Num Re=(v l) /\u03BD'),sg.Input(default_text='--',justification='center',size=(25, 1),disabled=True,key='rey_rezalt'),sg.Text('Mach Num:'),sg.Input(default_text='-',size=(4, 1),disabled=True,key='mach_num'),sg.Button('Calculate',size=(10, 1),key='rey_cal'),  ],
                 [sg.Text(' '*150,key='cruise_info')],
                 [sg.Text(' '*150,key='max_lift_info')],
                 [sg.Text(' '*150,key='delta_alfa')],
                 [sg.Text('Find nominated Airfoil'),sg.Button('Find',size=(10, 1),key='findAirfols') ],
                 [sg.Text('Shell output')],
                 [sg.Output(size=(100, 14))],
                 # [sg.Listbox(values=[], size=(3, 10), change_submits=True,key='listbox4')],
]

tab_draw = [
                [sg.T('Airfoil Geometry:')],
                [sg.Canvas(              key='controls_draw')],
                [sg.T('Figure:'),sg.T(' '*100,   key='text_draw')],
                [sg.Column(layout=[[sg.Canvas(key='fig_draw', size=(400 * 2, 400)  )]  ], background_color='#DAE0E6', pad=(0, 0) )],                   # it's important that you set this size  
                [sg.Text(f'Save file as DXF'),sg.Button('Save',size=(10, 1),key='saveDXF'),sg.Text('Cord Lengh:'),sg.Text('     ',key='cordLengh')]
]
tab_Cmalfa = [
                [sg.T('Controls Cm vs alfa:')],
                [sg.Canvas(key='controls_Cmalfa')],
                [sg.T('Figure:'),sg.T(' '*100,key='text_Cmalfa')],
                [sg.Column(layout=[[sg.Canvas(key='fig_Cmalfa', size=(400 * 2, 400)  )]  ], background_color='#DAE0E6', pad=(0, 0) )],                   # it's important that you set this size
   
]

tab_Cdpalfa = [
                [sg.T('Controls CDp vs alfa:')],
                [sg.Canvas(              key='controls_Cdpalfa')],
                [sg.T(f'Figure: '),sg.T(' '*100, key='text_Cdpalfa')],
                [sg.Column(layout=[[sg.Canvas(key='fig_Cdpalfa', size=(400 * 2, 400)  )]  ], background_color='#DAE0E6', pad=(0, 0) )],                   # it's important that you set this size

                  
]
tab_cdalfa = [
                [sg.T('Controls Cd vs alfa:')],
                [sg.Canvas(key='controls_cdalfa')],
                [sg.T('Figure:'),sg.T(' '*100,key='text_cdalfa')],
                [sg.Column(layout=[[sg.Canvas(key='fig_cdalfa', size=(400 * 2, 400)  )]  ], background_color='#DAE0E6', pad=(0, 0) )],                   # it's important that you set this size

]
tab_clalfa = [
                [sg.T('Controls Cl vs alfa:')],
                [sg.Canvas(key='controls_clalfa')],
                [sg.T(f'Figure:'),sg.T(' '*100,key='text_clalfa')],
                [sg.Column(layout=[[sg.Canvas(key='fig_clalfa', size=(400 * 2, 400)  )]  ], background_color='#DAE0E6', pad=(0, 0) )],                   # it's important that you set this size

]

tab_clcd = [
            [sg.T('Controls Cl vs Cd:')],
            [sg.Canvas(key='controls_clcd')],
            [sg.T('Figure:'),sg.T(' '*100,key='text_clcd')],
            [sg.Column(layout=[[sg.Canvas(key='fig_clcd', size=(400 * 2, 400)  )]  ], background_color='#DAE0E6', pad=(0, 0) )],                   # it's important that you set this size
    
]
tab_dataInfo = [
                 [sg.Text('tab1')],
                 [                    
                    sg.Multiline(default_text='airfoil data',key='AirfoilInfo', autoscroll=True,auto_size_text=True,size=(110,32)),#size=(100,90)
                 ],
]
tab_group_layout = [[
                     sg.Tab('Select Airfoil', tab_select, ),
                     sg.Tab('Airfoil Data', tab_dataInfo, ),
                     sg.Tab('Cl vs Cd', tab_clcd, ),
                     sg.Tab('Cl vs alfa', tab_clalfa, ),
                     sg.Tab('Cd vs alfa', tab_cdalfa, ),
                     sg.Tab('CDp vs alpha', tab_Cdpalfa,  ),
                     sg.Tab('Cm vs alfa', tab_Cmalfa, ),                     
                     sg.Tab('Draw', tab_draw, ),
                     sg.Tab('Lift Calculation', tab_lift, ),
                     ]]

layout = [
            [sg.Text('Airfoles and Information Browser')],
            [
                sg.Tree(data=treedata,headings=['Info','\u0394\u03B1' ],auto_size_columns=True,num_rows=27,col0_width=19,key='Tree',show_expanded=False,enable_events=True),
                sg.TabGroup(tab_group_layout,enable_events=True,key='TABGROUP'),
             ],  
             [sg.Button('Ok'), sg.Button('Cancel'), sg.Button('Load Data',key='LoadAirfoilDirectory'),sg.Checkbox('Compare ',enable_events=True,key='doCompare'),
              sg.Text('Author H.R.S'),sg.Text(' '*120,key='AirFoil_info')  
                
                ],
          ]

window = sg.Window('Airfoil Analysis', layout,size=WindowsSize,
                    auto_size_text=True,
                    resizable=False,
                    grab_anywhere=False)

i=0
if __name__ == '__main__':
    
    while True:
            event, values = window.read()
            print(event) if event != sg.TIMEOUT_KEY else None # cur_focus.Type
            
            if    event == 'close' or event is None:
                break
            elif  event == 'saveDXF' :
                text = sg.popup_get_file('Please enter a file name',save_as = True)
                print(text)
            elif  event == 'Download' :
                window['ProgressBar'].UpdateBar(i % 1636)
                i+=10

