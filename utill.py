import os,re,math,threading
import numpy as np



from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt

AllFig=[plt.figure(i) for i in range(6)]


totalList=[]

sound_speed={-10:325.18,0:331.30,10:337.31,20:343.21}
Mach_num=0
Viscosity={-10:1.2462E-5,0:1.3324E-5,10:1.4207E-5,20:1.5111E-5}
Air      ={-10:1.3413   ,0:1.2922   ,10:1.2466   ,20:1.2041   }
AirDencity                                         = 1.2041
ReynoldSeries=[50000,100000,200000,500000,1000000]
folder_icon = b'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAACXBIWXMAAAsSAAALEgHS3X78AAABnUlEQVQ4y8WSv2rUQRSFv7vZgJFFsQg2EkWb4AvEJ8hqKVilSmFn3iNvIAp21oIW9haihBRKiqwElMVsIJjNrprsOr/5dyzml3UhEQIWHhjmcpn7zblw4B9lJ8Xag9mlmQb3AJzX3tOX8Tngzg349q7t5xcfzpKGhOFHnjx+9qLTzW8wsmFTL2Gzk7Y2O/k9kCbtwUZbV+Zvo8Md3PALrjoiqsKSR9ljpAJpwOsNtlfXfRvoNU8Arr/NsVo0ry5z4dZN5hoGqEzYDChBOoKwS/vSq0XW3y5NAI/uN1cvLqzQur4MCpBGEEd1PQDfQ74HYR+LfeQOAOYAmgAmbly+dgfid5CHPIKqC74L8RDyGPIYy7+QQjFWa7ICsQ8SpB/IfcJSDVMAJUwJkYDMNOEPIBxA/gnuMyYPijXAI3lMse7FGnIKsIuqrxgRSeXOoYZUCI8pIKW/OHA7kD2YYcpAKgM5ABXk4qSsdJaDOMCsgTIYAlL5TQFTyUIZDmev0N/bnwqnylEBQS45UKnHx/lUlFvA3fo+jwR8ALb47/oNma38cuqiJ9AAAAAASUVORK5CYII='
file_icon   = b'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAACXBIWXMAAAsSAAALEgHS3X78AAABU0lEQVQ4y52TzStEURiHn/ecc6XG54JSdlMkNhYWsiILS0lsJaUsLW2Mv8CfIDtr2VtbY4GUEvmIZnKbZsY977Uwt2HcyW1+dTZvt6fn9557BGB+aaNQKBR2ifkbgWR+cX13ubO1svz++niVTA1ArDHDg91UahHFsMxbKWycYsjze4muTsP64vT43v7hSf/A0FgdjQPQWAmco68nB+T+SFSqNUQgcIbN1bn8Z3RwvL22MAvcu8TACFgrpMVZ4aUYcn77BMDkxGgemAGOHIBXxRjBWZMKoCPA2h6qEUSRR2MF6GxUUMUaIUgBCNTnAcm3H2G5YQfgvccYIXAtDH7FoKq/AaqKlbrBj2trFVXfBPAea4SOIIsBeN9kkCwxsNkAqRWy7+B7Z00G3xVc2wZeMSI4S7sVYkSk5Z/4PyBWROqvox3A28PN2cjUwinQC9QyckKALxj4kv2auK0xAAAAAElFTkSuQmCC'

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

DoCompare=False


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
  
def airfoilDataDowload():
#978,979,980,981,982,983
  for i in range(0,len(totalList)):#len(totalList)49,102,141,142,143,144,145,146,147,155,175,176,924,930,931,932,933,948
    name=airfoilObjects[i].name
    if not os.path.isdir(ProjectPath+'/AirfoilData/'+name):
       print('create----',ProjectPath+'/AirfoilData/'+name)
       os.makedirs(ProjectPath+'/AirfoilData/'+name)
    print('getting... ',i,name[:-3],'from: ',linkDat+name[:-3]+".dat")  
    urllib.request.urlretrieve(linkDat+name[:-3]+".dat", ProjectPath+"/AirfoilData/"+name+"/"+name[:-3]+".dat")


class Download(threading.Thread):
    def __init__(self):
        #super(Download, self).__init__()
        super().__init__()
        #Thread.__init__(self)
        self.daemon = True  # Allow main to exit even if still running.
        self.paused = True  # Start out paused.
        self.state = threading.Condition()
        self.stop_event = threading.Event()

    def run(self):
        self.resume()
        while True:
            with self.state:
                if self.paused:
                    self.state.wait()  # Block execution until notified.
            # Do stuff...
            airfoilDataDowload()


    def stop(self):
        self.stop_event.set() 
        
    def pause(self):
        with self.state:
            self.paused = True  # Block self.

    def resume(self):
        with self.state:
            self.paused = False
            self.state.notify()  # Unblock self if waiting.    
    

downloader=Download()    
    
    
    
    
    
    