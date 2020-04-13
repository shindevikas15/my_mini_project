

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import sys
import PySimpleGUI as sg
import csv


df=pd.DataFrame()
temp_df=pd.DataFrame()
fname=""
temp_id=[]
temp_cat=[]

def loaddataset(filename):
    global df
    #filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
    #messagebox.showwarning("warning","Please Wait Loading Process take a while...!") 
    #print("Dataset Loaded Successfully from Location :- "+filename)
    df = pd.read_csv(str(filename),engine="python")
    # drop duplicate rows using res_id as it is unique for each restaurant
    sg.Popup("Dataset Loaded Successfully...!\nLocation :- "+fname,title="Loaded Successfully",text_color='Green',auto_close_duration=5)
    
    
def preprocess():
    global df
    print('preprocessing Output :-')
    df["description"] = df["description"].fillna(value="")
    
    print(df.info())
    
    print("Now we Replace Null Values with '' blank String")
    #df.drop_duplicates(subset='res_id',inplace=True)
    #df = df.sort_values('city')
    sg.PopupTimed("Preprocessing Completed")
    #print(df.info())

def featch_json():
    import json
    with open("C:\\Users\\LENOVO\\Desktop\\yt\\IN_category_id.json") as f:
        categories = json.load(f)["items"]
        
    global temp_cat
    global temp_id
    cat_dict = {}  #this is use to store the select category

    temp_id=[]
    temp_cat=[]

    for cat in categories:
        cat_dict[int(cat["id"])] = cat["snippet"]["title"]
        temp_id.append(cat["id"])
        temp_cat.append(cat["snippet"]["title"])
    df['category_name'] = df['category_id'].map(cat_dict)

    
def main_fun(category):
    global temp_df
    #json_featchure()
    sel_cat=category
    loc=temp_cat.index(sel_cat)
    #print(temp_id)
    #print("Location "+str(loc))
    sel_id=temp_id[loc]
    #print("ID "+str(sel_id))
    #print(type(df['category_id']))

    #temp_df=df[df['category_id']==sel_id]



    temp_df=df[df['category_id']==int(sel_id)]
    #temp_df=temp_df.groupby('channel_title').head(30)

    temp_df=temp_df.sort_values("likes", ascending=False).head(200)


    #print(temp_df['channel_title'].unique())

    temp_df=temp_df[temp_df['channel_title'].isin(temp_df['channel_title'].unique())]


    #plt.barh(temp_df['channel_title'],temp_df['likes'])
    #plt.show()
    


def maincaller():
    global fname
    global temp_cat
    global temp_id
    #Main Function [Read Dataset File] 
    import PySimpleGUI as sg
    import sys

    sg.ChangeLookAndFeel('BlueMono') 



    event, values = sg.Window('Select DataSet').Layout([[sg.Text('Browse Dataset File :')],
                                                        [sg.In(), sg.FileBrowse()],
                                                       [sg.CloseButton('Load'), sg.CloseButton('Cancel')]]).Read()
    fname = values[0]

    if not fname:
        sg.Popup("Cancel", "No filename supplied")
        raise SystemExit("Cancelling: no filename supplied")
    else:
        #----------------------------------Display Progress Bar for Load dataset window
        # layout the Window
        layout = [[sg.Text('Loading your File...')],
                  [sg.ProgressBar(1000, orientation='h', size=(20, 20), key='progbar')],
                  [sg.Cancel()]]


        # create the Window
        window = sg.Window('Loading...', layout)
        # loop that would normally do something useful
        for i in range(1000):
            # check to see if the cancel button was clicked and exit loop if clicked
            event, values = window.Read(timeout=6)
            if event == 'Cancel' or event is None:
                fname=""
                break
                # update bar with loop value +1 so that bar eventually reaches the maximum
            window.Element('progbar').UpdateBar(i + 1)
        # done with loop... need to destroy the window as it's still open
        loaddataset(fname)
        window.Close()
        #UserPanel()
        #-------------------------------Display Progress bar for Preprocessing Window
        # layout the Window
        event=sg.PopupYesNo('Can we Preprocess Data',title="Permissions")
        if event == 'Yes':
            layout = [[sg.Text('We are Analysing your Dataset')],
                      [sg.ProgressBar(1000, orientation='h', size=(30, 20), key='progbar')],
                      [sg.Cancel()]]


            # create the Window
            window = sg.Window('Please Wait...!', layout)
            # loop that would normally do something useful
            for i in range(1000):
                # check to see if the cancel button was clicked and exit loop if clicked
                event, values = window.Read(timeout=5)
                if event == 'Cancel' or event is None:
                    fname=""
                    break
                    # update bar with loop value +1 so that bar eventually reaches the maximum
                window.Element('progbar').UpdateBar(i + 1)
            # done with loop... need to destroy the window as it's still open
            preprocess() #this is call the function

        else :
            sg.PopupError('Please Preprocess Dataset',title="Error")


        window.Close()
    


def graph_plotter():
    #total likes count
    def t_l_c():
        plt.barh(temp_df['channel_title'],temp_df['dislikes'])
        plt.xlabel('No of likes')
        plt.ylabel('Channel Title')

        plt.title("Top liked Channels")
        plt.show()
        
        #total dislike count
    def t_d_c():
        plt.barh(temp_df['channel_title'],temp_df['dislikes'])
        plt.xlabel('No of Dislikes')
        plt.ylabel('Channel Title')

        plt.title("Top Disliked Channels")
        plt.show()
        
        #total views count
    def t_v_c():
        plt.clf()
        plt.barh(temp_df['channel_title'],temp_df['views'])

        plt.xlabel('No of Views')
        plt.ylabel('Channel Title')

        plt.title("Top Viewed Channels")

        plt.show()
        
        #views vs likes
    def v_vs_l():
        plt.clf()
        plt.scatter(temp_df['views'],temp_df['likes'])
        plt.xlabel('Views')
        plt.ylabel('Likse')

        plt.title("Views VS Likes")
        plt.show()
        
        #dislike vs likes
    def d_vs_l():
        plt.clf()
        plt.scatter(temp_df['dislikes'],temp_df['likes'])
        plt.xlabel('Dislikes')
        plt.ylabel('Likse')

        plt.title("Dislikes VS Likes")
        plt.show()
        
    #===================================================================================================
     
    tab1_layout =  [[sg.Button('Top liked Channels')],[sg.Button('Top Viewed Channels')],[sg.Button('Top Disliked Channels')]]


    tab2_layout =  [[sg.Button('Views VS Likes')],[sg.Button('Dislikes VS Likes')]]
    
    temp_sort_view=temp_df.sort_values("views", ascending=False).head(200)
    
    tab3_layout =  [[sg.Text("Our Recommended Channel for You:-")],[sg.Button(temp_sort_view.iloc[0,3])]]

    layout=[]

    layout = [[sg.TabGroup([[sg.Tab('Bar Graph', tab1_layout), sg.Tab('Scatter Plot', tab2_layout),sg.Tab('Result', tab3_layout)]],theme=sg.THEME_XPNATIVE)],    
              ]

    print(temp_df.head(5))
    window = sg.Window('Dataset Analysis', layout, default_element_size=(30,50))    

    while True:    
        event, values = window.Read()    
        print(event)
        if event == 'Close':
            window.Close()
            break
        if event is None:           # always,  always give a way out!    
            window.Close()
            break 
        if event == "Top liked Channels":
            t_l_c()
        if event == "Top Viewed Channels":
            t_v_c()
        if event == "Top Disliked Channels":
            t_d_c()
        if event == "Views VS Likes":
            v_vs_l()
        if event == "Dislikes VS Likes":
            d_vs_l()
        


def cat_selector():
    layout = [[sg.Text('Select Channel Type')],
                  [sg.Listbox(values=temp_cat,size=(50,10), select_mode=sg.LISTBOX_SELECT_MODE_SINGLE)],
                  [sg.Button('Select'),sg.Cancel()]]

    selected_cat=""
    window1 = sg.Window('Please Select Channel Category', layout)
    while True:     # Event Loop
        event, value = window1.Read()
        if event in (None,'Cancel'):
            window1.Close()
            break
        selected_cat=value[0]
        break
    window1.close()
    #print(selected_cat[0])

    main_fun(selected_cat[0])




maincaller()
featch_json()

cat_selector()
graph_plotter()






