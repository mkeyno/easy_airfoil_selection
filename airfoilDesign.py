#!/usr/bin/env python
__version__=.03

from layout import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt

AllFig=[plt.figure(i) for i in range(6)]

from bs4 import BeautifulSoup  
import requests ,os,pickle,urllib,re,sys,json,math
from urllib.parse import urlparse
import numpy as np

DoCompare=False
Reynolds=10000
max_camber   =16.4#('cp-180-050-gn', 16.4)
min_camber   =0#('ys900-il'     , 0.0)
max_thick=66.4#('fx79w660a-il', 66.4)
min_thick=2.0#('sc20402-il'  , 2.0)
cruise_cl     =0 
cruise_cd     =0 
cruise_alfa   =0
cruise_cm     =0
max_lift_cl           =0
drag_in_max_lift      =0
alfa_in_max_lift      =0
cm_in_max_lift        =0

WingLenght=1
Chord=1
taper_angle=90
A_ref=WingLenght*(Chord-.5*WingLenght*math.tan(taper_angle * math.pi / 180))
Velocity=0

v_scale=[1,1.60934]
l_scale=[1,.00254]
w_scale=[1,0.3048]
        
currentPath, filename = os.path.split(os.path.abspath(__file__))
defultFolder=currentPath+'\AirfoilData'
alpha=[];CL=[];CD=[];CDp=[];CM=[];Top_Xtr=[];Bot_Xtr=[]
sound_speed={-10:325.18,0:331.30,10:337.31,20:343.21}
Mach_num=0
Viscosity={-10:1.2462E-5,0:1.3324E-5,10:1.4207E-5,20:1.5111E-5}
Air      ={-10:1.3413   ,0:1.2922   ,10:1.2466   ,20:1.2041   }
AirDencity                                         = 1.2041
ReynoldSeries=[50000,100000,200000,500000,1000000]
folder_icon = b'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAACXBIWXMAAAsSAAALEgHS3X78AAABnUlEQVQ4y8WSv2rUQRSFv7vZgJFFsQg2EkWb4AvEJ8hqKVilSmFn3iNvIAp21oIW9haihBRKiqwElMVsIJjNrprsOr/5dyzml3UhEQIWHhjmcpn7zblw4B9lJ8Xag9mlmQb3AJzX3tOX8Tngzg349q7t5xcfzpKGhOFHnjx+9qLTzW8wsmFTL2Gzk7Y2O/k9kCbtwUZbV+Zvo8Md3PALrjoiqsKSR9ljpAJpwOsNtlfXfRvoNU8Arr/NsVo0ry5z4dZN5hoGqEzYDChBOoKwS/vSq0XW3y5NAI/uN1cvLqzQur4MCpBGEEd1PQDfQ74HYR+LfeQOAOYAmgAmbly+dgfid5CHPIKqC74L8RDyGPIYy7+QQjFWa7ICsQ8SpB/IfcJSDVMAJUwJkYDMNOEPIBxA/gnuMyYPijXAI3lMse7FGnIKsIuqrxgRSeXOoYZUCI8pIKW/OHA7kD2YYcpAKgM5ABXk4qSsdJaDOMCsgTIYAlL5TQFTyUIZDmev0N/bnwqnylEBQS45UKnHx/lUlFvA3fo+jwR8ALb47/oNma38cuqiJ9AAAAAASUVORK5CYII='
file_icon   = b'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAACXBIWXMAAAsSAAALEgHS3X78AAABU0lEQVQ4y52TzStEURiHn/ecc6XG54JSdlMkNhYWsiILS0lsJaUsLW2Mv8CfIDtr2VtbY4GUEvmIZnKbZsY977Uwt2HcyW1+dTZvt6fn9557BGB+aaNQKBR2ifkbgWR+cX13ubO1svz++niVTA1ArDHDg91UahHFsMxbKWycYsjze4muTsP64vT43v7hSf/A0FgdjQPQWAmco68nB+T+SFSqNUQgcIbN1bn8Z3RwvL22MAvcu8TACFgrpMVZ4aUYcn77BMDkxGgemAGOHIBXxRjBWZMKoCPA2h6qEUSRR2MF6GxUUMUaIUgBCNTnAcm3H2G5YQfgvccYIXAtDH7FoKq/AaqKlbrBj2trFVXfBPAea4SOIIsBeN9kkCwxsNkAqRWy7+B7Z00G3xVc2wZeMSI4S7sVYkSk5Z/4PyBWROqvox3A28PN2cjUwinQC9QyckKALxj4kv2auK0xAAAAAElFTkSuQmCC'

airfoilJson={}
totalList=[]
totalListMcMt=[]
linkDET='http://www.airfoiltools.com/airfoil/details?airfoil='#clarkw-il
linkTXT='http://www.airfoiltools.com/polar/text?polar='#wb13535sm-il-50000
AirfoilList     =currentPath+'/airfoillist.txt'
AirfoilListMcMt =currentPath+'/AirfoilListMcMt.txt'
AirfoilJson     =currentPath+'/airfoiljson.json'


print(defultFolder)
Imperial=False
#loadPickle()
starting_path=''
# starting_path = sg.popup_get_folder('Folder to display')
if not starting_path:
       starting_path=defultFolder  #sys.exit(0)


#                        '', E:\Github\Airplane\AirfoilData
def add_files_in_folder(parent, dirname):
    #T = sg.TreeData()
    files = os.listdir(dirname)

    for f in files:
        fullname = os.path.join(dirname, f)
        if os.path.isdir(fullname):            # if it's a folder, add folder and recurse
            treedata.Insert(parent, fullname, f, values=[],                          icon=folder_icon)
            add_files_in_folder(fullname, fullname)
        else:              #parent, key     , text, values, icon=None)
            treedata.Insert(parent, fullname, f   , values=[os.stat(fullname).st_size], icon=file_icon)
    return treedata

def load_airfoil_dic(data):
    T = sg.TreeData()
    for airfoil in data :
        #print(name, len(airfoil.AllAirfoilsPage))
        T.Insert('', airfoil, airfoil, values=[], icon=folder_icon)
        # print(data[airfoil]['AllAirfoilsPage'])
        for i in range(len(data[airfoil]['AllAirfoilsPage'])):
            #treedata.Insert(name, i, name, values=airfoil.show(), icon=file_icon)
           #print(data[airfoil]['AllAirfoilsPage'][i]['filename'])
           T.Insert(airfoil, data[airfoil]['AllAirfoilsPage'][i]['filename'], f"Rey:{data[airfoil]['AllAirfoilsPage'][i]['Reynolds']:,},Max cl/Cd", values=[data[airfoil]['AllAirfoilsPage'][i]['max_clOnCd']], icon=file_icon) 
    return T

class Toolbar(NavigationToolbar2Tk):
    def __init__(self, *args, **kwargs):
        super(Toolbar, self).__init__(*args, **kwargs)

def draw_figure_w_toolbar(x,y,Title,TX,TY,num,canvas,  canvas_toolbar):
    #print(canvas.children,canvas_toolbar.children)
    plt.figure(num)
    fig = plt.gcf()
    if not(DoCompare): fig.clear()
    DPI = fig.get_dpi()
    #print('DPI=',DPI,fig)
    # ------------------------------- you have to play with this size to reduce the movement error when the mouse hovers over the figure, it's close to canvas size
    fig.set_size_inches(404 * 2 / float(DPI), 404 / float(DPI))
    plt.plot(x, y)
    plt.title(Title)
    plt.xlabel(TX)
    plt.ylabel(TY)
    plt.grid()
    if canvas.children:
        for child in canvas.winfo_children():
            child.destroy()
    if canvas_toolbar.children:
        for child in canvas_toolbar.winfo_children():
            child.destroy()
    f = FigureCanvasTkAgg(fig, master=canvas)
    f.draw()
    toolbar = Toolbar(f, canvas_toolbar)
    toolbar.update()
    f.get_tk_widget().pack(side='right', fill='both', expand=1)

def check_number(str):
    v=0
    try:
       v= float(  re.findall(r'[-+]?\d*\.\d+|\d+', str)[0]  )       
    except Exception as e:    
       pass;#window['rey_rezalt'].update(e)
    return v

def find_max(L):
    i=0;max=0;j=0
    for l in L:
        if l>max:
            max=l;j=i
        i+=1
    return max,j
    
def find_min(L):
    i=0;min=1000;j=0
    for l in L:
        if l<min:
            min=l;j=i
        i+=1
    return min,j

def find_max_div(L,D):
    i=0;max=0;j=0
    for (l,d )in zip(L,D):
        if (l/d)>max:
            max=round((l/d),2);j=i
        i+=1
    return max,j
  

def getXYcordinate(path):
    x=[];y=[]
    with open(path, 'r') as input:
       content=''
       for L in input:
            #print(L,end='')                    
            s = [float(s) for s in re.findall(r'[-+]?\d*\.\d+|\d+', L)]
            if len(s)==2 and s[0]<=1 and s[1]<=1:
                x.append(s[0])
                y.append(s[1])
                #print('   ',s,end='')
    #print(x);print(y)
    np_x = np.array(x)
    np_y = np.array(y)
    return np_x,np_y


def loadInfoOfAirfoilPage(path):
    with open(os.path.join(path), 'r') as f:
      alpha=[];CL=[];CD=[];CDp=[];CM=[];Top_Xtr=[];Bot_Xtr=[];
      content=''  
      for i, line in enumerate(f):
          content+=line;
          if i==8: 
            # Mach =   0.000     Re =     0.100 e 6     Ncrit =   5.000
            s = [float(s) for s in re.findall(r'[-+]?\d*\.\d+|\d+', line)]
            #print(line,f'reynolds={int(s[1]*1000000)} Ncrit={int(s[-1])}')
            Reynolds=int(s[ 1]*1000000)
            Ncrit   =int(s[-1])
          if i>11:            
            ss = ''.join((ch if ch in '0123456789.-e' else ' ') for ch in line)
            series = [float(i) for i in ss.split()]
            #print(line)
            #print(i-12,series[1])
            alpha.insert(  i-12,series[0])
            CL.insert(     i-12,series[1])
            CD.insert(     i-12,series[2])
            CDp.insert(    i-12,series[3])
            CM.insert(     i-12,series[4])
            Top_Xtr.insert(i-12,series[5])
            Bot_Xtr.insert(i-12,series[6])
            
      return content,Reynolds,Ncrit,alpha,CL,CD,CDp,CM,Top_Xtr,Bot_Xtr
      
#######################################################
class Airfoil():
  def __init__(self,name,FolderLocation,airfoilLink,AllAirfoilsPage,Max_camber,Max_camber_L,Max_thickness,Max_thickness_L):
    self.name     =name
    self.FolderLocation         =FolderLocation
    self.name                   =name
    self.AllAirfoilsPage        =AllAirfoilsPage
    self.Max_camber             =Max_camber
    self.Max_camber_L           =Max_camber_L
    self.Max_thickness          =Max_thickness
    self.Max_thickness_L        =Max_thickness_L

  def summary(self): # not appreat in print( )     
    s=f"Max camber={self.Max_camber} at {self.Max_camber_L}, "
    return s
  
  def page(self,index): # not appreat in print( )     
    s=''
    p=self.AllAirfoilsPage[index]
    s=f"Re:{p['Reynolds']} max cl={p['max_cl']},at {p['max_cl_alfa']:>5},max Cl/Cd={p['max_clOnCd']} at {p['max_clOnCd_alfa'] }" 
    return s
  
  def show(self): # not appreat in print( )     
    s=''
    for p in self.AllAirfoilsPage:
        s+=f"\nReynolds={p['Reynolds']:>10} max cl={p['max_cl']},at {p['max_cl_alfa']:>5},max Cl/Cd={p['max_clOnCd']} at {p['max_clOnCd_alfa'] }" 
    return s#f"Airfoil({self.name}), Max camber={self.Max_camber}{s}"

  def __str__(self): #print(t)  or print(str(t))
    s=''
    for p in self.AllAirfoilsPage:
        s+=f"\n\tReynolds={p['Reynolds']:>10} max cl={p['max_cl']},at {p['max_cl_alfa']:>5},max Cl/Cd={p['max_clOnCd']} at {p['max_clOnCd_alfa'] }" 
    return f"Airfoil({self.name}), Max camber={self.Max_camber}{s}"

# make airfoilJson parameter
def grabAirfoilDataFromFile3(index):
  airfoil={}
  name,Max_camber,Max_camber_L,Max_thickness,Max_thickness_L=totalListMcMt[index].split(',')
  print('Num:',index,name,Max_camber,Max_camber_L,Max_thickness,Max_thickness_L)
  FolderLocation=ProjectPath+'/AirfoilData/'+name
  if not os.path.isdir(FolderLocation): return
  airfoilLink=linkDET+name
  ListOfFiles=[f for f in os.listdir(FolderLocation) if f.endswith('.txt')]
  
  ''' we dont need these 
  
  datFile    =[f for f in os.listdir(FolderLocation) if f.endswith('.dat')]
  datFilePath=FolderLocation+"\\"+datFile[0]
  X_cor,Y_cor=getXYcordinate(datFilePath)
  #print(list(zip(X_cor,Y_cor)))
  #maxCord=Max_Distance(X_cor,Y_cor)
  #print(maxCord)
  '''
  AllAirfoilsPage=[] #list of dictionary 
  for filename in ListOfFiles:
    Page={}
    Reynolds,Ncrit,alpha,CL,CD,CDp,CM,Top_Xtr,Bot_Xtr=loadInfoOfAirfoilPage(FolderLocation,filename)
    #print(f'{filename:40},Reynolds={Reynolds:>10}, Ncrit={Ncrit}')
    max_cl,i        =find_max(CL)
    max_cl_alfa     =alpha[i]
    max_cl_cm       =CM[i]
    
    max_clOnCd,i    =find_max_div(CL,CD)
    max_clOnCd_alfa =alpha[i]
    max_clOnCd_cm   =CM[i]
    cl_cruise       =CL[i]
    
    delta_alfa=max_cl_alfa-max_clOnCd_alfa
    
    min_cm,i        =find_min(CM)
    min_cm_alfa     =alpha[i]
    max_cm_clcd     =CL[i]/CD[i]
    
    Page['filename']        =filename
    Page['Reynolds']        =Reynolds
    Page['Ncrit']           =Ncrit
    
    Page['max_cl']          =max_cl
    Page['max_cl_alfa']     =max_cl_alfa
    Page['max_cl_cm']       =max_cl_cm
    
    Page['max_clOnCd']      =max_clOnCd
    Page['max_clOnCd_alfa'] =max_clOnCd_alfa
    Page['max_clOnCd_cm']   =max_clOnCd_cm
    Page['cl_cruise']       =cl_cruise
    
    Page['delta_alfa']       =delta_alfa
    
    Page['min_cm']          =min_cm
    Page['min_cm_alfa']     =min_cm_alfa
    Page['max_cm_clcd']     =max_cm_clcd
    
    #print(f' Rey {Page["filename"] }- Ncrit {Page["Reynolds"]} ')
            # max Cl ={max_cl} at a={max_cl_alfa:.1f}` cm={max_cl_cm:.3f},\
            # max Cl/Cd={max_clOnCd} a={max_clOnCd_alfa:.1f} cm={max_clOnCd_cm:.3f}` \
            # min cm{min_cm:.3f} at a={min_cm_alfa:.1f} with Cl/Cd {max_cm_clcd:.3f}')
    AllAirfoilsPage.append(Page)
  
  #airfoil=Airfoil(name,FolderLocation,airfoilLink,AllAirfoilsPage,Max_camber,Max_camber_L,Max_thickness,Max_thickness_L)
  airfoil['Max_camber']=Max_camber
  airfoil['Max_camber_L']=Max_camber_L
  airfoil['Max_thickness']=Max_thickness
  airfoil['Max_thickness_L']=Max_thickness_L
  airfoil['FolderLocation']=FolderLocation
  airfoil['airfoilLink']=airfoilLink
  airfoil['AllAirfoilsPage']=AllAirfoilsPage
   
  airfoilJson[name]=airfoil#airfoilObjects[name]=airfoil
  print(name)

  
def loadNameMcMt(): #load all name of arifoils from file
  with open (AirfoilListMcMt, 'r') as f:
    for line in f.readlines():
      totalListMcMt.append(line.strip())
  #print(len(totalListMcMt),' item has been loaded')

def loadList(): #load all name of arifoils from file
  with open (AirfoilList, 'r') as f:
    for line in f.readlines():
      totalList.append(line.strip())
  print(len(totalList),' item has been loaded')


def saveJson():
  with open(AirfoilJson, 'wb') as fp:
    s = json.dumps(airfoilJson)#json.dump(airfoilJson, fp)
    fp.write(s)
  print(len(airfoilJson),' Airfoil opject has been saved')

  # s = json.dumps(airfoilJson)
  # open(AirfoilJson,"w").write(s)

def loadJson():
    #global airfoilJson
    with open(AirfoilJson) as json_file:
        d = json.load(json_file)
    return  d    
    #print(id(airfoilJson),len(airfoilJson),' loadJson()')

def find_reynolds_location(rey):
    j=0
    for num in ReynoldSeries:
        if rey >= num: j+=1

    if   j==0:    
        s=f'{rey:,} < {ReynoldSeries[0]:,}'
        v=ReynoldSeries[0]
    elif j==5:    
        s=f'{ReynoldSeries[4]:,} < {rey:,}'
        v=ReynoldSeries[4]
    else     :    
        s=f'{ReynoldSeries[j-1]:,} < {rey:,} < {ReynoldSeries[j]:,}'
        v=ReynoldSeries[j]
    #ss=f'{s:>60}'
    return v, s
    
    
def find_max_thinckness_in_database():
    ss=''
    max_tic=0
    for name,airfoil in airfoilObjects.items():
        #print(f'{name}, max thinckness={airfoil.Max_camber}, max chamber={airfoil.Max_thickness}')
        if float(airfoil.Max_thickness)>=max_tic:
            max_tic=float(airfoil.Max_thickness)
            ss=name
    return ss,max_tic
def find_max_chamber_in_database():
    ss=''
    max_cham=0
    for name,airfoil in airfoilObjects.items():
        #print(f'{name}, max thinckness={airfoil.Max_camber}, max chamber={airfoil.Max_thickness}')
        if float(airfoil.Max_camber)>=max_cham:
            max_cham=float(airfoil.Max_camber)
            ss=name
    return ss,max_cham  

def find_min_thinckness_in_database():
    ss=''
    max_tic=100
    for name,airfoil in airfoilObjects.items():
        #print(f'{name}, max thinckness={airfoil.Max_camber}, max chamber={airfoil.Max_thickness}')
        if float(airfoil.Max_thickness)<=max_tic:
            max_tic=float(airfoil.Max_thickness)
            ss=name
    return ss,max_tic
def find_min_chamber_in_database():
    ss=''
    max_cham=100
    for name,airfoil in airfoilObjects.items():
        #print(f'{name}, max thinckness={airfoil.Max_camber}, max chamber={airfoil.Max_thickness}')
        if float(airfoil.Max_camber)<=max_cham:
            max_cham=float(airfoil.Max_camber)
            ss=name
    return ss,max_cham  



def find_nominate_sorted_airfoil():
    r_scop,s=find_reynolds_location(Reynolds)
    T = sg.TreeData()
    list_unsorted={}
    for airfoil in airfoilJson:
       A_Mc=float(airfoilJson[airfoil]['Max_camber'])
       A_Mt=float(airfoilJson[airfoil]['Max_thickness'])       
       if A_Mc <= max_camber and A_Mc >= min_camber and A_Mt <= max_thick and A_Mt >= min_thick :             
            for i in range(len(airfoilJson[airfoil]['AllAirfoilsPage'])):
                A_rey  =int(airfoilJson[airfoil]['AllAirfoilsPage'][i]['Reynolds'])               
                if r_scop==A_rey:
                    dicc={}
                    dicc['name']=airfoil
                    dicc['file']=airfoilJson[airfoil]['AllAirfoilsPage'][i]['filename']
                    dicc['i']=i
                    dicc['delta']=float(airfoilJson[airfoil]['AllAirfoilsPage'][i]['delta_alfa'])
                    cl_cruise=float(airfoilJson[airfoil]['AllAirfoilsPage'][i]['cl_cruise'])
                    list_unsorted[cl_cruise]=dicc       
    #print(list_unsorted)
    #f=sorted(list_unsorted)
    dic_sorted=dict(reversed(sorted(list_unsorted.items())))
    #f=json.dumps(list_unsorted, sort_keys = True)
    for clCruise,v in dic_sorted.items() :
        #print(k,v)        
        # 117.83 {'name': 'e379-il', 'file': 'xf-e379-il-200000.txt', 'i': 4}
        # 91.16 {'name': 'e379-il', 'file': 'xf-e379-il-200000-n5.txt', 'i': 3}
        # 40.11 {'name': 'sc20402-il', 'file': 'xf-sc20402-il-200000-n5.txt', 'i': 3}
        # 20.14 {'name': 'sc20402-il', 'file': 'xf-sc20402-il-200000.txt', 'i': 4}
        # Insert(parent, key      , text     , values   , icon=None       )
        T.Insert(''       , v['name'], v['name'], values=[]       ,  icon=folder_icon)
        T.Insert(v['name'], v['file'], v['file'], values=[clCruise,v['delta']], icon=file_icon)
        
    window['Tree'].update(T  )
    
    
    
      
loadList()
loadNameMcMt()





while True:     # Event Loop
    event, values = window.read();#print(event)
    if event in (None, 'Cancel'):
        break
    elif event=='Tree':
      
      #print(values[event][0])
        # E:\Github\Airplane\AirfoilData\ag19-il
        # E:\Github\Airplane\AirfoilData\ag19-il\xf-ag19-il-100000.txt
        # ag36-il
        # xf-ag36-il-100000.txt
      try:
          nameofFile=''
          nameOfAirfoil=''
          pp=values[event][0]
          if pp.find('.txt')>0 :
                ss=pp.split("-")
                if pp.find('\\')>0:  
                    nameOfAirfoil=ss[2]+'-'+ss[3]
                    nameofFile=pp.split("\\")[-1]
                else:                
                    nameOfAirfoil=ss[1]+'-'+ss[2]
                    nameofFile=pp
          #print(nameofFile,'   ',nameOfAirfoil)          
          index=totalList.index(nameOfAirfoil)
          name,Max_camber,Max_camber_L,Max_thickness,Max_thickness_L=totalListMcMt[index].split(',')
            # #print(nameOfAirfoil,index,name,Max_camber,Max_camber_L,Max_thickness,Max_thickness_L)
            
          pathTxtFile=defultFolder+'\\'+nameOfAirfoil+'\\'+nameofFile
          for f in os.listdir(defultFolder+'\\'+nameOfAirfoil):
             if f.endswith(".dat"):
                 datFilePath=os.path.join(defultFolder+'\\'+nameOfAirfoil, f)

          #print(pathTxtFile,datFilePath)
          
          X_cor,Y_cor=getXYcordinate(datFilePath)
          #cc=Chord/1.0
          print('Chord=',Chord)
          #print(X_cor[20],Y_cor[20])
          X_cor=X_cor*Chord*100 ;Y_cor=Y_cor*Chord*100
          #print(X_cor[20],Y_cor[20])
          content,Reynolds,Ncrit,alpha,CL,CD,CDp,CM,Top_Xtr,Bot_Xtr=loadInfoOfAirfoilPage(pathTxtFile)      
          DoCompare=window['doCompare'].Get()
          window['AirfoilInfo'].Update(value=content) #read file then update GUI and lists
          actual_thickness=float(Max_thickness)*Chord  
          infos=f'{nameOfAirfoil}: Max Thickness={actual_thickness:.2f}cm({Max_thickness}%) at {Max_thickness_L}%,   Max Chamber={Max_camber}% at {Max_camber_L}%'
          window['AirFoil_info'].Update(infos)
            
          draw_figure_w_toolbar(CL,CD,'Cl vs Cd','CL','CD'         ,0,window['fig_clcd'].TKCanvas  , window['controls_clcd'].TKCanvas)
          max,j=find_max_div(CL,CD)
          ss=f'Max Cl/Cd ratio=({max}) happen at angle {alpha[j]}'
          window['text_clcd'].Update(value=ss)
          cruise_cl     =CL[j] 
          cruise_cd     =CD[j] 
          cruise_alfa   =alpha[j]
          cruise_cm     =CM[j]          #.5*p*v2*A*cl
          cruise_lift=.5*cruise_cl*AirDencity*Velocity*Velocity*WingLenght*Chord*0.1019
          cruise_drag=.5*cruise_cd*AirDencity*Velocity*Velocity*WingLenght*Chord*0.1019
          cruise_s=f'Cruise Lift/Drag at AOA {cruise_alfa:5.2f} ({cruise_lift:.2f} , {cruise_drag:.2f}) Kg {cruise_cl} {cruise_cd}' 
          window['cruise_info'].Update(cruise_s)
          
          
          draw_figure_w_toolbar(alpha,CL,'Cl vs alpha','CL','alpha',1,window['fig_clalfa'].TKCanvas, window['controls_clalfa'].TKCanvas)
          max,j=find_max(CL)
          ss=f'Max Cl({max}) happen at angle {alpha[j]}'
          window['text_clalfa'].Update(value=ss)
          max_lift_cl           =CL[j]
          drag_in_max_lift      =CD[j]
          alfa_in_max_lift      =alpha[j]
          cm_in_max_lift        =CM[j]
          Max_Lift   =     .5*max_lift_cl*AirDencity*Velocity*Velocity*WingLenght*Chord*0.1019
          Max_Drag   =.5*drag_in_max_lift*AirDencity*Velocity*Velocity*WingLenght*Chord*0.1019
          max_lift_s=f'Max    Lift/Drag at AOA {alfa_in_max_lift:5.2f} ({Max_Lift:.2f} , {Max_Drag:.2f}) Kg,{max_lift_cl} {drag_in_max_lift} '
          window['max_lift_info'].Update(max_lift_s)
          
          delta_alfa=alfa_in_max_lift-cruise_alfa
          delta_alfa_s=f'Scope of AOA(\u0394\u03B1)={delta_alfa}'
          window['delta_alfa'].Update(delta_alfa_s)
          
          draw_figure_w_toolbar(alpha,CD,'Cd vs alpha','CD','alpha',2,window['fig_cdalfa'].TKCanvas, window['controls_cdalfa'].TKCanvas)
          min,j=find_min(CD)
          ss=f'Min Cd({min}) happen at angle {alpha[j]}'
          window['text_cdalfa'].Update(value=ss)
        
        
          draw_figure_w_toolbar(alpha,CM,'Cm vs alpha','CM','alpha',3,window['fig_Cmalfa'].TKCanvas, window['controls_Cmalfa'].TKCanvas)
          min,j=find_min(CM)
          ss=f'Min Cm({min}) happen at angle {alpha[j]}'
          window['text_Cmalfa'].Update(value=ss)    
          
          draw_figure_w_toolbar(alpha,CDp,'CDp vs alpha geometry','CDp','alpha',4,window['fig_Cdpalfa'].TKCanvas, window['controls_Cdpalfa'].TKCanvas)
          
          
          draw_figure_w_toolbar(X_cor,Y_cor,'Drawing','X','Y',5,window['fig_draw'].TKCanvas, window['controls_draw'].TKCanvas)
      
      except Exception as e:
        print(e) 
      
    elif event=='TABGROUP':    
        selectedTab=values[event]
        #if selectedTab=='clcd':
        print(selectedTab)
        
    elif event=='LoadAirfoilDirectory':        
        t=add_files_in_folder('', starting_path)
        #print(starting_path,t)
        window['Tree'].update(t)
    elif event=='doCompare':
        DoCompare=window['doCompare'].Get()
        print('compare multi ',DoCompare)
    
    elif event=='loadObject':
        airfoilJson=loadJson()
        print(len(airfoilJson), 'has loaded ',id(airfoilJson))
        #print(data['fx77w258-il']['AllAirfoilsPage'][0]['filename'])
        t=load_airfoil_dic(airfoilJson)
        #print(starting_path,t)
        window['Tree'].update(t)
               
    elif event=='rey_cal':
        Velocity    =check_number(values['velocity'])/3.6
        Chord       =check_number(values['chord'])/100
        WingLenght  =check_number(values['wing'])
        
        Velocity*=v_scale[Imperial]
        Chord*=l_scale[Imperial]
        WingLenght*=w_scale[Imperial]
        
        temp=values['temp']  
        Reynolds=int((Chord*Velocity)/Viscosity[temp])
        AirDencity=Air[temp]
        
        Mach_num=Velocity/sound_speed[temp]
        print(f'R:{Reynolds},  v:{Velocity:.2f},  c:{Chord},  L:{WingLenght},  m:{Mach_num:.2f}')
        _,s=find_reynolds_location(Reynolds)
        #print(v,L,Viscosity[temp],s,Reynolds)
        window['rey_rezalt'].update(s) 
        window['mach_num'].update(f'{Mach_num:.2f}')
    
    elif event=='temp':
        temp=values['temp']
        st=f'{Viscosity[temp]},{Air[temp]}'
        window['Viscosity'].update(st)

    elif event=='Geometry Set':
        
        max_thick =check_number(values['max_thick'])#66.4
        if max_thick>66.4:max_thick =66.4
        max_camber=check_number(values['max_camber'])#16.4
        if max_camber>16.4:max_camber =16.4
        
        min_camber=check_number(values['min_camber'])#0
        if min_camber<0:min_camber =0
        
        WingLenght=check_number(values['wing'])
        WingLenght*=w_scale[Imperial]
        
        #min_thick =check_number(values['min_thick'])#2      
        minThick=check_number(values['minThick'])
        min_thick=int(minThick/Chord)
        if min_thick<2:min_thick =2
        window['min_thick'].update(min_thick)
        
        print('Wing Lenght=',WingLenght)        
        print(f'{min_thick}<thick<{max_thick} {min_camber}<chamber<{max_camber}')
        #window['Viscosity'].update(Viscosity[temp])

    elif event=='findAirfols':
        find_nominate_sorted_airfoil()

    elif event=='metric':
        Imperial=False
        window['cord_unit'].update('cm')
        window['vel_unit'].update('km/h') 
        window['wing_unit'].update('m')
    elif event=='imperial':
        Imperial=True
        window['cord_unit'].update('in')
        window['vel_unit'].update('mph')
        window['wing_unit'].update('ft')
        window['thick_unit'].update('in')
window.close()
