from tkinter import *  # Developed by Fredrik Lundh
from functools import partial
import pickle
from webbrowser import get
root = Tk()
root.title(" Game Stash by leromango ")
# Setting all popular genres
genres = [
    "action",
    "rpg",
    "retro",
    "horror",
    "jrpg",
    "dungeon-crawler",
    "roguelite",
    "survival",
    "sandbox",
    "puzzle",
    "rts",
    "turn-based strategy",
    "racing",
    "simulator",
    "co-op",
    "multiplayer",
    "adventure",
    "open world",
    "metroidvania",
    "hack-n-slash",
    "platformer",
    "fps",
    "moba",
    "third person shooter",
    "mmorpg",
    "rhytm games",
    "fighting",
    "beat 'em up",
    "experiences",
    "narrative"
]

genres.sort()
# Setting all main main gaming platforms
platform = [
    "Xbox",
    "Playstation",
    "Nintendo",
    "PC",
    "Mobile",
    "VR"
]
gameList = []  # List, which later will store all games
with open('myGames.pickle', 'rb') as f:
    gameList = pickle.load(f)  # Saving games into a files
playlists = []  # List, which later will store all playlists
with open('playlists.pickle', 'rb') as f:
    playlists = pickle.load(f)  # Saving playlists into a files


def widget_removal():  # Function, that clears the screen
    for widget in root.winfo_children():
        widget.destroy()


def main_menu():  # Function, that creates main menu layout
    widget_removal()
    buttonAddDel = Button(root, text="Add/Delete",
                          command=lambda: [widget_removal(), addDelFunc()])
    buttonAddDel.grid(column=0, row=0)
    buttonEdit = Button(root, text="Add Score/Mark Played",
                        command=lambda: [widget_removal(), gameEdit()])
    buttonEdit.grid(column=1, row=0)
    buttonAll = Button(root, text="Show All", command=lambda: [
        widget_removal(), displayAll()])
    buttonAll.grid(column=2, row=0)
    buttonPlay = Button(root, text="Playlists", command=lambda: [
        widget_removal(), playlistMenu()])
    buttonPlay.grid(column=3, row=0)
    buttonSearch = Button(root, text="Search", command=lambda: [
                          widget_removal(), gameSearch()])
    buttonSearch.grid(column=4, row=0)


def playlistMenu():
    if playlists:
        for i in range(len(playlists)):
            x = Button(root, text=playlists[i]["Name"], command=partial(
                # Ekaterina Medvedeva helped me with understanding of how partial() function works
                displayPlaylist, playlists[i]["Name"])).grid(column=0, row=i)
    buttonCreate = Button(root, text="Create",
                          command=lambda: [widget_removal(), playlistCreate()])
    buttonCreate.grid(column=0, row=100)
    buttonDelete = Button(root, text="Delete",
                          command=lambda: [widget_removal(), playlistDelete()])
    buttonDelete.grid(column=1, row=100)
    back = Button(root, text="Back", command=lambda: [main_menu()])
    back.grid(column=2, row=0)


def displayPlaylist(name):  # Function to display all games in a playlist
    widget_removal()
    title = Label(root, text=playlists[next((index for (index, d) in enumerate(
        playlists) if d["Name"] == name), None)]["Name"]).grid(column=0, row=0)
    x = next((index for (index, d) in enumerate(
        playlists) if d["Name"] == name), None)
    for g in range(len(playlists[x]["Games"])):
        globals()["FUCK"+str(g)] = Button(root, text=playlists[x]["Games"][g],
                                          command=partial(gameSearchF, playlists[x]["Games"][g])).grid(column=0, row=g+1)
    back = Button(root, text="Back", command=lambda: [main_menu()])
    back.grid(column=2, row=0)
    addButton = Button(root, text="Add", command=lambda: [
                       playlistGameAdd(next((index for (index, d) in enumerate(playlists) if d["Name"] == name), None))])
    addButton.grid(column=1, row=0)
    delButton = Button(root, text="Delete", command=partial(playlistGameDel, next((index for (
        index, d) in enumerate(playlists) if d["Name"] == name), None))).grid(column=1, row=1)


def playlistGameDel(playlistname):  # Function to delete games from playlist
    widget_removal()
    for i in range(len(playlists[playlistname]["Games"])):
        btn = Button(root, text=playlists[playlistname]["Games"][i], command=partial(
            playlistGameDel2, playlistname, playlists[playlistname]["Games"][i])).grid(column=0, row=i)
    back = Button(root, text="Back", command=lambda: [main_menu()])
    back.grid(column=2, row=0)


def playlistGameDel2(name, i):  # Supporting function to delete games from playlist
    playlists[name]["Games"].remove(i),
    main_menu()
    pickleList()


def playlistGameAdd(playlistname):  # Function to add games to playlist
    widget_removal()
    for i in range(len(gameList)):
        if not(any(gameList[i]["Name"] in sublist.get("Games") for sublist in playlists)):
            btn = Button(root, text=gameList[i]["Name"], command=partial(
                playlistGameAdd2, playlistname, i)).grid(column=0, row=i)
    back = Button(root, text="Back", command=lambda: [main_menu()])
    back.grid(column=2, row=0)


def playlistGameAdd2(name, i):  # Supporting function to add games to playlist
    playlists[name]["Games"].append(gameList[i]["Name"])
    main_menu()
    pickleList()


def pickleList():  # Function that pickles playlists
    with open('playlists.pickle', 'wb') as f:
        pickle.dump(playlists, f)


def playlistCreate():  # Function to create playlists
    print(playlists)
    playlistName = Text(root, height=1, width=8)
    playlistName.grid(column=0, row=0)
    buttonAccept = Button(root, text="Create",
                          command=lambda: [playlistAdd(playlistName.get("1.0", "end-1c"))])
    buttonAccept.grid(column=1, row=0)
    back = Button(root, text="Back", command=lambda: [main_menu()])
    back.grid(column=2, row=0)


def playlistAdd(name):  # Function to create a dictionary with info about game
    if name != "" and not(any(name in sublist.get("Name") for sublist in playlists)):
        x = {
            "Name": name,
            "Games": []
        }
        playlists.append(x)
        with open('playlists.pickle', 'wb') as f:
            pickle.dump(playlists, f)
        main_menu()
    else:
        error = Label(
            root, text="Empty name/Already exist").grid(column=0, row=999)


def playlistDelete():  # Function to delete a dictionary with info about game from playlists
    if playlists:
        for i in range(len(playlists)):
            x = Button(root, text=playlists[i]["Name"], command=partial(
                playlistPop, playlists[i]["Name"])).grid(column=0, row=i)
    back = Button(root, text="Back", command=lambda: [main_menu()])
    back.grid(column=2, row=0)


def playlistPop(name):  # Supporting function for deletion
    x = next((index for (index, d) in enumerate(
        playlists) if d["Name"] == name), None)
    playlists.pop(x)
    with open('playlists.pickle', 'wb') as f:
        pickle.dump(playlists, f)
    main_menu()


def displayAll():  # Function to display all games
    for i in range(len(gameList)):
        btn = Button(root, text=gameList[i]["Name"], command=partial(  # Ekaterina Medvedeva helped me with understanding of how partial() function works
            gameSearchF, gameList[i]["Name"])).grid(column=0, row=i)
    back = Button(root, text="Back", command=lambda: [main_menu()])
    back.grid(column=2, row=0)


def gameSearch():  # Function, that creates search menu layout
    inputSearch = Text(root, height=1, width=8)
    inputSearch.grid(column=0, row=0)
    inputAccept = Button(root, text="Name", command=lambda: [
        gameSearchF(inputSearch.get("1.0", "end-1c"))])
    inputAccept.grid(column=0, row=1)
    inputYear = Button(root, text="Year", command=lambda: [
        gameSearchProperties("Year", inputSearch.get("1.0", "end-1c"))])
    inputYear.grid(column=0, row=2)
    inputScore = Button(root, text="Metascore", command=lambda: [
        gameSearchProperties("Score", inputSearch.get("1.0", "end-1c"))])
    inputScore.grid(column=1, row=2)
    inputUserscore = Button(root, text="Userscore", command=lambda: [
        gameSearchProperties("Userscore", inputSearch.get("1.0", "end-1c"))])
    inputUserscore.grid(column=0, row=3)
    inputPlatform = Button(root, text="Platform", command=lambda: [
        gameSearchProperties("Platform", inputSearch.get("1.0", "end-1c"))])
    inputPlatform.grid(column=1, row=3)
    inputGenre = Button(root, text="Genre", command=lambda: [
        gameSearchProperties("Genre", inputSearch.get("1.0", "end-1c"))])
    inputGenre.grid(column=0, row=4)
    inputPlayed = Button(root, text="Played", command=lambda: [
        gameSearchProperties("Played", inputSearch.get("1.0", "end-1c"))])
    inputPlayed.grid(column=1, row=4)
    back = Button(root, text="Back", command=lambda: [main_menu()])
    back.grid(column=1, row=0)


# Searching games by properties, it calls gameSearchF to display info about a found game
def gameSearchProperties(type, property):
    widget_removal()
    back = Button(root, text="Back", command=lambda: [main_menu()])
    back.grid(column=1, row=0)
    for i in range(len(gameList)):
        if type == "Year" or "Score" or "Userscore":
            if gameList[i][type] == property:
                gameName = gameList[i]["Name"]

                btn = Button(root, text=gameName,
                             command=partial(gameSearchF, gameName))
                btn.grid(column=0, row=i)
        if type == "Platform" or type == "Genre":
            for g in range(len(gameList[i][type])):
                if gameList[i][type][g] == property:
                    gameName = gameList[i]["Name"]
                    btn = Button(root, text=gameName,
                                 command=partial(gameSearchF, gameName))
                    btn.grid(column=0, row=i)
        if type == "Played":
            choice = property.upper()
            if choice == "PLAYED" or choice == "FINISHED":
                if gameList[i][type] == True:
                    gameName = gameList[i]["Name"]
                    btn = Button(root, text=gameName,
                                 command=partial(gameSearchF, gameName))
                    btn.grid(column=0, row=i)
            elif choice == "NOT PLAYED" or choice == "NO PLAY":
                if gameList[i][type] == False:
                    gameName = gameList[i]["Name"]
                    btn = Button(root, text=gameName,
                                 command=partial(gameSearchF, gameName))
                    btn.grid(column=0, row=i)


# Function that takes name of the game as an input and displays all data about it
def gameSearchF(name):
    if (any(name in sublist.get("Name") for sublist in gameList)) and name != "":
        widget_removal()
        x = next((index for (index, d) in enumerate(
            gameList) if d["Name"] == name), None)
        nameLabel = Label(root, text=gameList[x]["Name"]).grid(column=0, row=1)
        platformLabel = Label(
            root, text=gameList[x]["Platform"]) .grid(column=0, row=2)
        yearLabel = Label(root, text=gameList[x]["Year"]).grid(column=0, row=3)
        scoreLabel = Label(root, text=gameList[x]["Score"]).grid(
            column=0, row=4)
        userscoreLabel = Label(
            root, text=gameList[x]["Userscore"]).grid(column=0, row=5)
        for i in range(len(gameList[x]["Genre"])):
            genreLabel = Label(root, text=gameList[x]["Genre"][i]).grid(
                column=0, row=6+i)
        if gameList[x]["Played"]:
            playedLabel = Label(root, text="Played").grid(column=0, row=100)
        else:
            playedLabel = Label(
                root, text="Haven't Played").grid(column=0, row=100)
        back = Button(root, text="Back", command=lambda: [main_menu()])
        back.grid(column=1, row=0)
    else:
        noLabel = Label(root, text="Not Found")
        noLabel.grid(column=1, row=1)


def findGame(name):  # Funtion, that allows user to chose what he wants to do with the found game & creates a layout of the page
    if (any(name in sublist.get("Name") for sublist in gameList)) and name != "":
        widget_removal()
        choiceLabel = Label(root, text="What do you want to do?")
        choiceLabel.grid(column=0, row=0)
        scoreButton = Button(root, text="Add score",
                             command=lambda: [widget_removal(), addScore(name)])
        scoreButton.grid(column=0, row=1)
        playedButton = Button(root, text="Mark played",
                              command=lambda: [widget_removal(), markPlayed(name)])
        playedButton.grid(column=1, row=1)
        back = Button(root, text="Back", command=lambda: [main_menu()])
        back.grid(column=2, row=0)
    else:
        noLabel = Label(root, text="Not Found")
        noLabel.grid(column=1, row=2)


def gameEdit():  # Function, that allows user to search game by title & creates a layout of the page
    labelName = Label(root, text="Game Title")
    labelName.grid(column=0, row=0)
    inputName = Text(root, width=8, height=1)
    inputName.grid(column=1, row=0)
    back = Button(root, text="Search", command=lambda: [
        findGame(inputName.get("1.0", "end-1c"))])
    back.grid(column=1, row=1)
    back = Button(root, text="Back", command=lambda: [main_menu()])
    back.grid(column=2, row=0)


def markPlayed(name):  # Function, that takes a name of the game and allows user to set its played value to True or False & creates a layout of the page
    # https://stackoverflow.com/questions/4391697/find-the-index-of-a-dict-within-a-list-by-matching-the-dicts-value
    x = next((index for (index, d) in enumerate(
        gameList) if d["Name"] == name), None)
    play = BooleanVar(False)
    inputPlayed = Checkbutton(root, text="Played!",
                              variable=play, onvalue=True, offvalue=False)
    inputPlayed.grid(column=0, row=0)
    inputAccept = Button(root, text="Accept", command=lambda: [
        markPlayedF(x, play.get()), main_menu()])
    inputAccept.grid(column=0, row=1)
    back = Button(root, text="Back", command=lambda: [main_menu()])
    back.grid(column=2, row=0)


# Function, that assigns value received from the checkbox from markPlayed(name) to Played in dictionary of game
def markPlayedF(index, value):
    gameList[index]["Played"] = value
    print(gameList)
    with open('myGames.pickle', 'wb') as f:
        pickle.dump(gameList, f)


def addScore(name):  # Function, that takes a name of the game and allows user to set its userscore value & creates a layout of the page
    x = next((index for (index, d) in enumerate(
        gameList) if d["Name"] == name), None)
    labelScore = Label(root, text="Enter you score")
    labelScore.grid(column=0, row=0)
    inputScore = Text(root, width=8, height=1)
    inputScore.grid(column=1, row=0)
    back = Button(root, text="Back", command=lambda: [main_menu()])
    back.grid(column=2, row=0)
    buttonAccept = Button(root, text="Accept", command=lambda: [
        addScoreF(x, inputScore.get("1.0", "end-1c"))])
    buttonAccept.grid(column=0, row=1)


def addScoreF(index, value):  # Function, that checks if user-entered score is below 100 and is not string, then assigns value received from the checkbox from addScore(name) to Usersocre in dictionary of game
    if intCheck(value):
        if int(value) <= 100:
            gameList[index]["Userscore"] = value
            main_menu()
        else:
            errorLabel = Label(root, text="Error, needs to be lower than 100").grid(
                column=2, row=2)
    else:
        errorLabel = Label(root, text="Error, not int value").grid(
            column=2, row=2)
    with open('myGames.pickle', 'wb') as f:
        pickle.dump(gameList, f)


def addDelFunc():  # Function, that allows user to choose users if they want to add or delete a game from Stash & creates a layout of the page
    add = Button(root, text="Add", command=lambda: [widget_removal(),
                                                    gameNew()])
    add.grid(column=0, row=0)
    delete = Button(root, text="Delete", command=lambda: [
        widget_removal(), gameDel()])
    delete.grid(column=1, row=0)
    back = Button(root, text="Back", command=lambda: main_menu())
    back.grid(column=2, row=0)


def intCheck(var):  # Function, that checks if a certain variale is an integer
    if not(var.isnumeric()):
        return False
    else:
        return True


def deleteGame(gameName):  # Deletes a game
    for i in range(len(gameList)):
        if gameName == gameList[i].get("Name"):
            gameList.pop(i)
            print(i, "deleted")
    with open('myGames.pickle', 'wb') as f:
        pickle.dump(gameList, f)


def gameDel():  # Function, that allows user to enter title of the game to delete and accept the deletion & creates a layout of the page
    deleteLabel = Label(root, text="Title")
    deleteLabel.grid(column=0, row=0)
    deleteField = Text(root, height=1, width=8)
    deleteField.grid(column=1, row=0)
    back = Button(root, text="Back", command=lambda: main_menu())
    back.grid(column=2, row=1)
    back = Button(root, text="Delete", command=lambda: [
        deleteGame(deleteField.get("1.0", "end-1c")), main_menu()])
    back.grid(column=2, row=0)


# Function, that takes all the required data about the game assembles it into a dictonary and puts it in gameList
def saveGame(name, platform, year, score, userscore, genre, playedBol):
    game = {
        "Name": name,
        "Platform": platform,
        "Year": year,
        "Score": score,
        "Userscore": userscore,
        "Genre": genre,
        "Played": playedBol
    }
    gameList.insert(int(len(gameList)-1), game)
    with open('myGames.pickle', 'wb') as f:
        pickle.dump(gameList, f)


def createListPlatforms():  # Function, that takes data from all platform-related checkboxes in gameNew and returns respective platforms of a game
    gamePlatforms = []
    for i in range(len(platform)):
        if (globals()["value" + str(i)].get()) and not(platform[i] in gamePlatforms):
            gamePlatforms.append(platform[i])
    return gamePlatforms


def createListGenres():  # Function, that takes data from all genre-related checkboxes in gameNew and returns respective genres of a game
    gameGenres = []
    for i in range(len(genres)):
        if (globals()["Uvalue" + str(i)].get()) and not(genres[i] in gameGenres):
            gameGenres.append(genres[i])
    return gameGenres


def gameNew():  # Function, that allows users to choose all properties of the game they want to add & creates a layout of the page
    labelName = Label(root, text="Game Title")
    labelName.grid(column=0, row=0)
    inputName = Text(root, height=1, width=8)
    inputName.grid(column=1, row=0)

    def name():  # Function, that takes info from text field and checks if game with the same name already in gameList, if it is returns a number of the game, if it isn't returns a name
        if not(any(inputName.get("1.0", "end-1c") in sublist.get("Name") for sublist in gameList)):
            return inputName.get("1.0", "end-1c")
        else:
            return str(len(gameList)+1)

    labelYear = Label(root, text="Release Year")
    labelYear.grid(column=0, row=1)
    inputYear = Text(root, height=1, width=8)
    inputYear.grid(column=1, row=1)

    def year():  # Function, that takes info from text field and checks if year is entered as an integer
        if intCheck(inputYear.get("1.0", "end-1c")):
            return inputYear.get("1.0", "end-1c")
        else:
            return 0000

    labelPlatform = Label(root, text="Platforms")
    labelPlatform.grid(column=0, row=2)
    c = 0
    r = 3
    for i in range(len(platform)):
        # Function, that allows user to choose platforms of the added game
        globals()["value"+str(i)] = BooleanVar(False)
        globals()["checkbutton" + str(i)] = Checkbutton(root,
                                                        text=platform[i], variable=globals()["value"+str(i)], onvalue=True, offvalue=False)
        if(c == 3):
            c = 0
            r = r + 1
        globals()["checkbutton" + str(i)].grid(column=c, row=r)
        c = c + 1

    labelScore = Label(root, text="Metascore")
    labelScore.grid(column=0, row=5)
    inputScore = Text(root, height=1, width=8)
    inputScore.grid(column=1, row=5)

    def score():  # Function, that takes info from text field and checks if score is entered as an integer and if it is below 100
        if intCheck(inputScore.get("1.0", "end-1c")):
            if int(inputScore.get("1.0", "end-1c")) <= 100:
                return inputScore.get("1.0", "end-1c")
            else:
                return 0000
        else:
            return 0000

    labelUserScore = Label(root, text="Your score")
    labelUserScore.grid(column=0, row=6)
    inputUserScore = Text(root, height=1, width=8)
    inputUserScore.grid(column=1, row=6)

    def userscore():  # Function, that takes info from text field and checks if userscore is entered as an integer and if it is below 100
        if intCheck(inputUserScore.get("1.0", "end-1c")):
            if int(inputUserScore.get("1.0", "end-1c")) <= 100:
                return inputUserScore.get("1.0", "end-1c")
            else:
                return 0000
        else:
            return 0000

    labelGenre = Label(root, text="Genres")
    labelGenre.grid(column=0, row=7)
    c = 0
    r = 8
    for i in range(len(genres)):  # Function, that allows user to choose genres of the added game
        globals()["Uvalue"+str(i)] = BooleanVar(False)
        globals()["check2button" + str(i)] = Checkbutton(root,
                                                         text=genres[i], variable=globals()["Uvalue"+str(i)], onvalue=True, offvalue=False)
        if(c == 3):
            c = 0
            r = r + 1
        globals()["check2button" + str(i)].grid(column=c, row=r)
        c = c + 1

    labelPlayed = Label(root, text="Have you played it?")
    labelPlayed.grid(column=0, row=45)
    playedButton = BooleanVar(False)
    played = Checkbutton(root, text="Played!",
                         variable=playedButton, onvalue=True, offvalue=False)
    played.grid(column=1, row=45)
    # Button, that executes all functions and gathers all data for saveGame function
    accept = Button(root, text="Accept",
                    command=lambda: [saveGame(name(), createListPlatforms(), year(), score(), userscore(), createListGenres(), playedButton.get()), print(gameList), main_menu()])
    accept.grid(column=1, row=50)
    goBack = Button(root, text="Back", command=lambda: main_menu())
    goBack.grid(column=2, row=0)


main_menu()
root.mainloop()
