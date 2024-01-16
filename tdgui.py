import tkinter as tk 
import ttkbootstrap as ttk
import pyperclip
import teamdetectorgui as scraper
import re

def search():
   b = serverEntryStr.get()
   s =  playerEntryStr.get()

   pattern = r'^7' 
   match = re.search(pattern, s)
   if match: 
      s = f'https://steamcommunity.com/profiles/{s}'

   if b == "" or s == "":
      playersCountStr.set('One of the arguments is empty')
   else: 
      name,steamId,friends,battlemetricsPlayers = scraper.main(b,s)
      playersCountStr.set(f'Players: {len(battlemetricsPlayers)}')

      formattedString = f'Name:'.ljust(34) + 'SteamID:'.ljust(19) + 'Link: \n\n'
      for steamId, name in friends.items():
         formattedString += f'{name}{' '*(34 - len(name))}' + f'{steamId}{' '*(19 - len(steamId))}' + f'https://steamcommunity.com/profiles/{steamId}\n'
         
      playerListStr.set(formattedString)

      copyButton.pack_forget()
      copyButton.pack(pady=10,padx=10)

def copyLabel():
    copyText = playerListStr.get()
    pyperclip.copy("```"+copyText+"```")

# window
window = ttk.Window(themename = 'darkly')
window.title('Team detector')
window.geometry('750x400')

# title
title_label = ttk.Label(
   master = window, 
   text = 'Team detector', 
   font = 'Courier 18 bold',
   width= 100,
   justify="left")
title_label.pack(pady=10, padx=10)

# input fields
input_frame = ttk.Frame(master = window)

# f = open("default.txt", "r")
# server = f.read()

server = "https://www.battlemetrics.com/servers/rust/10274718"

serverEntryStr = tk.StringVar(value = server)
playerEntryStr = tk.StringVar()

serverEntr = ttk.Entry(
   master = input_frame, 
   textvariable = serverEntryStr,
   width= 100)
playerEntry = ttk.Entry(
   master = input_frame, 
   textvariable = playerEntryStr,
   width= 100)
button = ttk.Button(
   master = input_frame,
   text = "Search", 
   command = search,
   width = 89)

# labels % button
serverEntr.pack(padx=10, pady = 5)
playerEntry.pack(padx=10, pady = 5)
button.pack(padx=10, pady = 5)

input_frame.pack(pady = 10)

playersCountStr = tk.StringVar()
playerListStr = tk.StringVar()

playersCountLabel = ttk.Label(
   master = window,
   text= 'Output', 
   font = 'Courier 12', 
   textvariable=playersCountStr,
   width= 100,
   justify="left")
playersCountLabel.pack(padx=10,pady = 5)
playerListLabel = ttk.Label(
   master = window,
   text= 'Output', 
   font = 'Courier 12', 
   textvariable=playerListStr,
   width= 100,
   justify="left")
playerListLabel.pack(padx=10,pady = 5)

copyButton = ttk.Button(window, text="Copy to discord",style='TButton', command=copyLabel, width = 89)

# run
window.mainloop()
