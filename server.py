import flask
from flask import Flask, send_from_directory, request, send_file, url_for
import sqlite3
import json
import os

from werkzeug.utils import redirect, secure_filename

app = Flask(__name__)
myConnection = sqlite3.connect('data.sqlite', check_same_thread=False)

myCursor = myConnection.cursor()

# userList table
myCursor.execute("""CREATE TABLE IF NOT EXISTS userList (
    username TEXT,
    email TEXT,
    password TEXT,
    userType INT
)""")

# add admin if not exists
myCursor.execute("""
    INSERT INTO userList (username, email, password, userType)
    SELECT 'Admin', 'admin', 'admin', 2
    WHERE NOT EXISTS(SELECT 1 FROM userList WHERE LOWER(username) = 'admin');
""")


# themes table
myCursor.execute("""CREATE TABLE IF NOT EXISTS themes (
    preset TEXT,
    mainColor TEXT,
    secondColor TEXT,
    mainBackground TEXT,
    secondBackground TEXT,
    newsBorder TEXT,
    font TEXT,
    selected INT
)""")

# add presets if not exists
myCursor.execute("""
    INSERT INTO themes (preset, mainColor, secondColor, mainBackground, secondBackground, newsBorder, font, selected)
    SELECT 'light', '#000000', '#000000', '#ffffff', '#cccccc', '#444444', 'Arial', 1
    WHERE NOT EXISTS(SELECT 1 FROM themes WHERE preset = 'light');
""")
myCursor.execute("""
    INSERT INTO themes (preset, mainColor, secondColor, mainBackground, secondBackground, newsBorder, font, selected)
    SELECT 'dark', '#ffffff', '#ffffff', '#222222', '#333333', '#111111', 'Arial', 0
    WHERE NOT EXISTS(SELECT 1 FROM themes WHERE preset = 'dark');
""")
myCursor.execute("""
    INSERT INTO themes (preset, mainColor, secondColor, mainBackground, secondBackground, newsBorder, font, selected)
    SELECT 'custom', '#000000', '#000000', '#ffffff', '#ffffff', '#cccccc', 'Arial', 0
    WHERE NOT EXISTS(SELECT 1 FROM themes WHERE preset = 'custom');
""")


# blocks table
myCursor.execute("""CREATE TABLE IF NOT EXISTS blocks (
    name TEXT,
    active TEXT,
    orderIndex INT
)""")

# add themes if not exists
myCursor.execute("""
    INSERT INTO blocks (name, active, orderIndex)
    SELECT 'navbar', 'true', '0'
    WHERE NOT EXISTS(SELECT 1 FROM blocks WHERE name = 'navbar');
""")
myCursor.execute("""
    INSERT INTO blocks (name, active, orderIndex)
    SELECT 'slider', 'true', '1'
    WHERE NOT EXISTS(SELECT 1 FROM blocks WHERE name = 'slider');
""")
myCursor.execute("""
    INSERT INTO blocks (name, active, orderIndex)
    SELECT 'news', 'true', '2'
    WHERE NOT EXISTS(SELECT 1 FROM blocks WHERE name = 'news');
""")
myCursor.execute("""
    INSERT INTO blocks (name, active, orderIndex)
    SELECT 'content', 'true', '3'
    WHERE NOT EXISTS(SELECT 1 FROM blocks WHERE name = 'content');
""")
myCursor.execute("""
    INSERT INTO blocks (name, active, orderIndex)
    SELECT 'footer', 'true', '4'
    WHERE NOT EXISTS(SELECT 1 FROM blocks WHERE name = 'footer');
""")


# news table
myCursor.execute("""CREATE TABLE IF NOT EXISTS news (
    title TEXT,
    description TEXT,
    category TEXT,
    images TEXT,
    authors TEXT,
    comments TEXT,
    id INTEGER PRIMARY KEY AUTOINCREMENT
)""")


# menu table
myCursor.execute("""CREATE TABLE IF NOT EXISTS menu (
    text TEXT,
    link TEXT,
    id INTEGER PRIMARY KEY AUTOINCREMENT
)""")


# menuType table
myCursor.execute("""CREATE TABLE IF NOT EXISTS menuType (
    type TEXT
)""")
myCursor.execute("""
    INSERT INTO menuType (type)
    SELECT 'horizontal'
    WHERE NOT EXISTS(SELECT 1 FROM menuType);
""")


# footer table
myCursor.execute("""CREATE TABLE IF NOT EXISTS footer (
    text TEXT,
    link TEXT,
    id INTEGER PRIMARY KEY AUTOINCREMENT
)""")

# slider table
myCursor.execute("""CREATE TABLE IF NOT EXISTS slider (
    text TEXT,
    image TEXT,
    orderIndex TEXT,
    id INTEGER PRIMARY KEY AUTOINCREMENT
)""")

# sliderDuration table
myCursor.execute("""CREATE TABLE IF NOT EXISTS sliderDuration (
    duration TEXT
)""")
myCursor.execute("""
    INSERT INTO sliderDuration (duration)
    SELECT "200"
    WHERE NOT EXISTS(SELECT 1 FROM sliderDuration);
""")

# content table
myCursor.execute("""CREATE TABLE IF NOT EXISTS content (
    title TEXT,
    description TEXT,
    image TEXT
)""")
myCursor.execute("""
    INSERT INTO content (title, description, image)
    SELECT "", "", ""
    WHERE NOT EXISTS(SELECT 1 FROM content);
""")

# comments table

myCursor.execute("""CREATE TABLE IF NOT EXISTS comments (
    author TEXT,
    content TEXT,
    newsIndex INT
)""")

myConnection.commit()


###################################################################################################


def userExist(username):
    myCursor = myConnection.cursor()
    myCursor.execute(
        f'SELECT EXISTS(SELECT 1 FROM userList WHERE LOWER(username)=LOWER("{username}"))')
    row = myCursor.fetchall()
    if row[0][0] == 1:
        return True
    return False


def newsTitleExist(title):
    myCursor = myConnection.cursor()
    myCursor.execute(
        f'SELECT EXISTS(SELECT 1 FROM news WHERE LOWER(title)=LOWER("{title}"))')
    row = myCursor.fetchall()
    if row[0][0] == 1:
        return True
    return False


###################################################################################################


@app.route("/")
def base():
    return send_from_directory('client/public', 'index.html')


@app.route("/<path:path>")
def home(path):
    return send_from_directory('client/public', path)


@app.route("/register", methods=['POST'])
def register():
    data = request.json
    username = data["username"]
    password = data["password"]
    email = data["email"]

    if userExist(username):
        return '0'

    myCursor = myConnection.cursor()
    myCursor.execute(f"""INSERT INTO userList
        (username, email, password, userType)
        VALUES
        ('{username}','{email}','{password}',0)""")
    myConnection.commit()
    return '1'


@app.route("/login", methods=['POST'])
def login():
    data = request.json
    username = data["username"]
    password = data["password"]

    myCursor = myConnection.cursor()
    myCursor.execute(
        f'SELECT EXISTS(SELECT 1 FROM userList WHERE LOWER(username)=LOWER("{username}") AND password="{password}")')
    row = myCursor.fetchall()
    if (row[0][0] == 1):
        return '1'
    return '0'


@app.route("/getPermission", methods=['POST'])
def getPermission():
    username = request.data.decode("utf-8")
    myCursor = myConnection.cursor()
    myCursor.execute(
        f'SELECT userType FROM userList WHERE LOWER(userName) = LOWER("{username}");')
    permission = myCursor.fetchall()[0][0]
    return str(permission)


@app.route("/getProperUsername", methods=['POST'])
def getProperUsername():
    username = request.data.decode("utf-8")
    myCursor = myConnection.cursor()
    myCursor.execute(
        f'SELECT userName FROM userList WHERE LOWER(userName) = LOWER("{username}");')
    userName = myCursor.fetchall()[0][0]
    return str(userName)


@app.route("/getUserList", methods=['POST'])
def getUserList():
    myCursor = myConnection.cursor()
    permissionLevel = request.json['permissionLevel']
    username = request.json['username']
    print(username)
    if permissionLevel == '2':
        myCursor.execute(
            f'SELECT * FROM userList ORDER BY userType DESC, username ASC')
    else:
        myCursor.execute(
            f'SELECT * FROM userList WHERE LOWER(username)=LOWER("{username}")')
    userList = json.dumps(myCursor.fetchall())
    return userList


@app.route("/deleteUser", methods=['POST'])
def deleteUser():
    username = request.data.decode("utf-8")
    myCursor = myConnection.cursor()
    myCursor.execute(
        f'DELETE FROM userList WHERE LOWER(username)=LOWER("{username}");')
    myConnection.commit()
    return "success"


@app.route("/editUser", methods=['POST'])
def editUser():
    print('editUser')
    originalUsername = request.json['originalUsername']
    username = str(request.json['username'])
    email = request.json['email']
    password = request.json['password']
    permissionLevel = str(request.json['permissionLevel'])

    if originalUsername.lower() != username.lower():
        if userExist(username):
            return {'type': "error", 'message': "This username is already taken"}

    print(permissionLevel)
    if permissionLevel != '0' and permissionLevel != '1' and permissionLevel != '2':
        return {'type': "error", 'message': "Wrong permission level"}

    myCursor = myConnection.cursor()
    myCursor.execute(f"""
        UPDATE userList 
        SET username="{username}", email="{email}", password="{password}", userType="{permissionLevel}" 
        WHERE LOWER(username)=LOWER("{originalUsername}");
    """)
    myConnection.commit()
    return {'type': "success", 'message': "msg"}


@app.route("/getPresets", methods=['POST'])
def getPresets():
    myCursor = myConnection.cursor()
    myCursor.execute(f'SELECT * FROM themes')
    themes = json.dumps(myCursor.fetchall())
    return themes


@app.route("/savePreset", methods=['POST'])
def savePreset():
    myCursor = myConnection.cursor()
    myCursor.execute(f"""
                UPDATE themes 
                SET selected=0
                WHERE selected=1;
            """)
    myConnection.commit()
    selectedPreset = request.json['selectedPreset']
    preset = request.json['preset']
    myCursor.execute(f"""
            UPDATE themes 
            SET mainColor="{preset[0]}", secondColor="{preset[1]}", mainBackground="{preset[2]}" , secondBackground="{preset[3]}", newsBorder="{preset[4]}", font="{preset[5]}", selected=1
            WHERE LOWER(preset)=LOWER("{selectedPreset}");
        """)
    myConnection.commit()
    return 'success'


@app.route("/getBlocks", methods=['POST'])
def getBlocks():
    myCursor = myConnection.cursor()
    myCursor.execute(f'SELECT * FROM blocks')
    blocks = json.dumps(myCursor.fetchall())
    return blocks


@app.route("/saveBlocks", methods=['POST'])
def saveBlocks():
    blocks = request.json
    i = 0
    for block in blocks:
        myCursor = myConnection.cursor()
        myCursor.execute(f"""
                UPDATE blocks
                SET active="{block['active']}", orderIndex="{i}"
                WHERE LOWER(name)=LOWER("{block['name']}");
            """)
        i += 1
    myConnection.commit()
    return 'success'


@app.route("/getNews", methods=['POST'])
def getNews():
    myCursor = myConnection.cursor()
    myCursor.execute(f'SELECT * FROM news')
    news = json.dumps(myCursor.fetchall())
    return news


@app.route("/saveNews", methods=['POST'])
def saveNews():
    news = request.json
    if newsTitleExist(news['title']):
        return {"type": "error", "message": "News title already exists"}

    myCursor = myConnection.cursor()
    myCursor.execute(f"""
        INSERT INTO news (title, description, category, images)
        VALUES ('{news['title']}','{news['description']}','{news['category']}','{news['images']}')
    """)
    myConnection.commit()
    return {"type": "success"}


@app.route("/updateNews", methods=['POST'])
def updateNews():
    news = request.json
    if news['title'].lower() == 'title':
        return {"type": "error", "message": "c'mon can't you think about a better title?"}
    if newsTitleExist(news['title']):
        if news['originalTitle'].lower() != news['title'].lower():
            return {"type": "error", "message": "News title already exists"}
    myCursor = myConnection.cursor()
    myCursor.execute(f"""
        UPDATE news 
        SET title="{news['title']}", description="{news['description']}", category="{news['category']}", images="{news['images']}" 
        WHERE LOWER(title)=LOWER("{news['originalTitle']}");
    """)
    myConnection.commit()
    return {"type": "success"}


@app.route("/deleteNews", methods=['POST'])
def deleteNews():
    title = request.data.decode("utf-8")
    myCursor.execute(
        f'DELETE FROM news WHERE LOWER(title)=LOWER("{title}");')
    myConnection.commit()

    return {"type": "success"}


@app.route("/getMenu", methods=['POST'])
def getMenu():
    myCursor = myConnection.cursor()
    myCursor.execute(f'SELECT * FROM menu')
    menu = json.dumps(myCursor.fetchall())
    return menu


@app.route("/saveMenu", methods=['POST'])
def saveMenu():
    text = request.json['text']
    link = request.json['link']
    myCursor = myConnection.cursor()
    myCursor.execute(f"""
        INSERT INTO menu (text, link)
        VALUES ('{text}','{link}')
    """)
    myConnection.commit()
    myCursor = myConnection.cursor()
    myCursor.execute("select seq from sqlite_sequence WHERE name = 'menu'")
    lastId = myCursor.fetchall()
    return {"type": "success", 'message': lastId[0][0]}


@app.route("/updateMenu", methods=['POST'])
def updateMenu():
    menu = request.json
    myCursor = myConnection.cursor()
    myCursor.execute(f"""
        UPDATE menu 
        SET text="{menu['text']}", link="{menu['link']}"
        WHERE id={menu['id']};
    """)
    myConnection.commit()
    return {"type": "success"}


@app.route("/deleteMenu", methods=['POST'])
def deleteMenu():
    id = request.data.decode("utf-8")
    myCursor = myConnection.cursor()
    myCursor.execute(
        f'DELETE FROM menu WHERE id={id};')
    myConnection.commit()
    return {"type": "success"}


@app.route("/getMenuType", methods=['POST'])
def getMenuType():
    myCursor = myConnection.cursor()
    myCursor.execute(f'SELECT * FROM menuType')
    menu = myCursor.fetchall()
    return menu[0][0]


@app.route("/changeMenuType", methods=['POST'])
def changeMenuType():
    menuType = request.data.decode("utf-8")
    lastType = ''
    if menuType == 'horizontal':
        lastType = 'hamburger'
    else:
        lastType = 'horizontal'

    myCursor = myConnection.cursor()
    myCursor.execute(f"""
        UPDATE menuType
        SET type="{menuType}"
        WHERE type="{lastType}";
    """)
    myConnection.commit()
    return {"type": "success"}


@app.route("/getFooter", methods=['POST'])
def getFooter():
    myCursor = myConnection.cursor()
    myCursor.execute(f'SELECT * FROM footer')
    footer = json.dumps(myCursor.fetchall())
    return footer


@app.route("/saveFooter", methods=['POST'])
def saveFooter():
    text = request.json['text']
    link = request.json['link']
    myCursor = myConnection.cursor()
    myCursor.execute(f"""
        INSERT INTO footer (text, link)
        VALUES ('{text}','{link}')
    """)
    myConnection.commit()
    myCursor.execute("select seq from sqlite_sequence WHERE name = 'footer'")
    lastId = myCursor.fetchall()
    return {"type": "success", 'message': lastId[0][0]}


@app.route("/updateFooter", methods=['POST'])
def updateFooter():
    footer = request.json
    myCursor = myConnection.cursor()
    myCursor.execute(f"""
        UPDATE footer 
        SET text="{footer['text']}", link="{footer['link']}"
        WHERE id={footer['id']};
    """)
    myConnection.commit()
    return {"type": "success"}


@app.route("/deleteFooter", methods=['POST'])
def deleteFooter():
    id = request.data.decode("utf-8")
    myCursor = myConnection.cursor()
    myCursor.execute(
        f'DELETE FROM footer WHERE id={id};')
    myConnection.commit()
    return {"type": "success"}


@app.route("/getSlider", methods=['POST'])
def getSlider():
    myCursor = myConnection.cursor()
    myCursor.execute(f'SELECT * FROM slider')
    slider = json.dumps(myCursor.fetchall())
    return slider


@app.route("/saveSlide", methods=['POST'])
def saveSlide():
    text = request.json['text']
    image = request.json['image']
    order = request.json['order']
    myCursor = myConnection.cursor()
    myCursor.execute(f"""
        INSERT INTO slider (text, image, orderIndex)
        VALUES ('{text}','{image}', '{order}')
    """)
    myConnection.commit()
    myCursor = myConnection.cursor()
    myCursor.execute("select seq from sqlite_sequence WHERE name = 'slider'")
    lastId = myCursor.fetchall()
    return {"type": "success", 'message': lastId[0][0]}


@app.route("/updateSlide", methods=['POST'])
def updateSlide():
    slider = request.json
    myCursor = myConnection.cursor()
    myCursor.execute(f"""
        UPDATE slider 
        SET text="{slider['text']}", image="{slider['image']}"
        WHERE id={slider['id']};
    """)
    myConnection.commit()
    return {"type": "success"}


@app.route("/deleteSlide", methods=['POST'])
def deleteSlide():
    id = request.data.decode("utf-8")
    myCursor = myConnection.cursor()
    myCursor.execute(
        f'DELETE FROM slider WHERE id={id};')
    myConnection.commit()
    return {"type": "success"}


@app.route("/previousOrder", methods=['POST'])
def previousOrder():
    id = request.json["id"]
    lastId = request.json["lastId"]
    order = int(request.json["order"])
    nextOrder = order - 1
    myCursor = myConnection.cursor()
    myCursor.execute(f"""
        UPDATE slider 
        SET orderIndex="{nextOrder}"
        WHERE id={id};
    """)
    myCursor = myConnection.cursor()
    myCursor.execute(f"""
        UPDATE slider 
        SET orderIndex="{order}"
        WHERE id={lastId};
    """)
    myConnection.commit()
    return {"type": "success"}


@app.route("/nextOrder", methods=['POST'])
def nextOrder():
    id = request.json["id"]
    lastId = request.json["lastId"]
    order = int(request.json["order"])
    nextOrder = order + 1
    myCursor = myConnection.cursor()
    myCursor.execute(f"""
        UPDATE slider 
        SET orderIndex="{nextOrder}"
        WHERE id={id};
    """)
    myCursor = myConnection.cursor()
    myCursor.execute(f"""
        UPDATE slider 
        SET orderIndex="{order}"
        WHERE id={lastId};
    """)
    myConnection.commit()
    return {"type": "success"}


@app.route("/getSliderDuration", methods=['POST'])
def getSliderDuration():
    myCursor = myConnection.cursor()
    myCursor.execute(f'SELECT * FROM sliderDuration')
    duration = myCursor.fetchall()
    return duration[0][0]


@app.route("/changeSliderDuration", methods=['POST'])
def changeSliderDuration():
    duration = request.data.decode("utf-8")

    myCursor.execute(f"""
        UPDATE sliderDuration
        SET duration="{duration}";
    """)
    myConnection.commit()
    return {"type": "success"}


@app.route("/getContent", methods=['POST'])
def getContent():
    myCursor = myConnection.cursor()
    myCursor.execute(f'SELECT * FROM content')
    content = json.dumps(myCursor.fetchall())
    return content


@app.route("/saveContent", methods=['POST'])
def saveContent():
    title = request.json['title']
    description = request.json['description']
    image = request.json['image']
    myCursor = myConnection.cursor()
    myCursor.execute(f"""
        UPDATE content 
        SET title="{title}", description="{description}", image="{image}"
    """)
    myConnection.commit()
    return {"type": "success"}


@app.route("/exportSettings")
def exportSettings():
    with open('./data.sql', 'w') as f:
        for line in myConnection.iterdump():
            f.write('%s\n' % line)
        print(f)
    return send_file('./data.sql', as_attachment=True)


@app.route("/importSettings", methods=['POST'])
def importSettings():
    if 'file' not in request.files:
        return redirect('/#/Settings')
    file = request.files['file']
    file.filename = 'data.sql'
    print(file)
    filename = secure_filename(file.filename)
    file.save(os.path.join('./', filename))

    myCursor.execute("DROP TABLE IF EXISTS themes")
    myCursor.execute("DROP TABLE IF EXISTS blocks")
    myCursor.execute("DROP TABLE IF EXISTS menu")
    myCursor.execute("DROP TABLE IF EXISTS menuType")
    myCursor.execute("DROP TABLE IF EXISTS slider")
    myCursor.execute("DROP TABLE IF EXISTS sliderDuration")
    myCursor.execute("DROP TABLE IF EXISTS news")
    myCursor.execute("DROP TABLE IF EXISTS content")
    myCursor.execute("DROP TABLE IF EXISTS footer")
    myCursor.execute("DROP TABLE IF EXISTS userList")
    myCursor.execute("DROP TABLE IF EXISTS comments")
    myConnection.commit()

    f = open('./data.sql', 'r')
    sql = f.read()
    myConnection.executescript(sql)
    return redirect('/#/Settings')


@app.route("/getData", methods=['POST'])
def getData():
    nav = {
        "type": "navbar",
        "navbarType": "horizontal",
        "navbarItems": []
    }
    theme = []
    blocks = []
    news = []
    slider = []
    myCursor.execute(f'SELECT * FROM blocks')
    bblocks = myCursor.fetchall()
    for i in bblocks:
        if i[1] == 'true':
            blocks.append(i)
    hV = ()
    isSorted = False
    while isSorted == False:
        isSorted = True
        for i in range(1, len(blocks)-1):
            if blocks[i][2] > blocks[i+1][2]:
                hV = blocks[i]
                blocks[i] = blocks[i+1]
                blocks[i+1] = hV
                isSorted = False
    myCursor.execute(f'SELECT * FROM menuType')
    menuType = myCursor.fetchall()
    nav["navbarType"] = menuType[0][0]
    myCursor.execute(f'SELECT * FROM menu')
    links = myCursor.fetchall()
    for i in links:
        link = {
            "navbarText": i[0],
            "navbarLink": i[1]
        }
        nav["navbarItems"].append(link)

    myCursor.execute(f'SELECT * FROM themes')
    themes = myCursor.fetchall()
    for i in themes:
        if i[7] == 1:
            theme = i

    myCursor.execute(f'SELECT * FROM news')
    newsTab = myCursor.fetchall()

    for idx, i in enumerate(newsTab):
        news.append(
            {
                "newsCategory": i[2],
                "newsTitle": i[0],
                "newsText": i[1],
                "newsPhoto": i[3],
                "newsIndex": idx,
                "newsID": i[4]
            }
        )
    myCursor.execute(f'SELECT * FROM slider')
    tabSlider = myCursor.fetchall()
    for i in tabSlider:
        slider.append(
            {
                "sliderPhoto": i[1],
                "sliderText": i[0],
                "index": int(i[2])
            }
        )
    hV = {}
    isSorted = False
    while isSorted == False:
        isSorted = True
        for i in range(0, len(slider) - 1):
            if slider[i]["index"] > slider[i+1]["index"]:
                hV = slider[i]
                slider[i] = slider[i+1]
                slider[i+1] = hV
                isSorted = False
    myCursor.execute(f'SELECT * FROM sliderDuration')
    duration = myCursor.fetchall()
    myCursor.execute(f'SELECT * FROM content')
    objContent = myCursor.fetchall()
    content = {
        "contentTitle": objContent[0][0],
        "contentDesc": objContent[0][1],
        "contentPhoto": objContent[0][2]
    }

    resBlocks = [nav]

    for i in blocks:
        if i[0] == 'slider':
            resBlocks.append(
                {
                    "type": "slider",
                    "sliderDuration": duration,
                    "sliderColor": "white",
                    "sliderItems": slider
                },
            )
        elif i[0] == 'news':
            resBlocks.append({
                "type": "news",
                "newsItems": news
            },)
        elif i[0] == 'content':
            resBlocks.append({
                "type": "content",
                "content": content
            })
    footerItems = []
    myCursor.execute(f'SELECT * FROM footer')
    footer = myCursor.fetchall()
    for i in footer:
        footerItems.append(
            {
                "text": i[0],
                "link": i[1]
            }
        )

    resBlocks.append(
        {
            "type": "footer",
            "footerItems": footerItems,
            "footerText": "Jakub Kowal - Igor Świerczyński CMS 2022"
        }
    )
    finalJSON = {
        "theme": {
            "mainColor": theme[1],
            "secondColor": theme[2],
            "mainBackground": theme[3],
            "newsBorder": theme[5],
            "secondBackground": theme[4],
            "font": theme[6]
        },
        "blocks": resBlocks
    }
    return finalJSON


@app.route("/getComments", methods=['POST'])
def getComments():
    index = request.json['index']
    comments = {"authors": "", "comments": ""}

    myCursor.execute(f'SELECT * FROM comments WHERE newsIndex={index}')
    commentsData = myCursor.fetchall()

    if len(commentsData) < 1:
        myCursor.execute(f"""
            INSERT INTO comments (author, content, newsIndex)
            VALUES ('','',{index})
        """)
        myConnection.commit()
        print("setTable", flush=True)
    if len(commentsData) == 1:
        comments["authors"] = commentsData[0][0]
        comments["comments"] = commentsData[0][1]

    print(comments, flush=True)
    return comments


@app.route("/setComments", methods=['POST'])
def setComments():
    author = request.json['author']
    content = request.json['content']
    index = request.json['index']
    print(author, content, flush=True)

    myCursor.execute(f'SELECT * FROM comments WHERE newsIndex={index}')
    commentsData = myCursor.fetchall()

    finalAuthor = f'{commentsData[0][0]},,,{author}'
    finalContent = f'{commentsData[0][1]},,,{content}'

    myCursor.execute(f"""
        UPDATE comments 
        SET author="{finalAuthor}", content="{finalContent}"
        WHERE newsIndex={index};
    """)
    myConnection.commit()

    return 'success'


if __name__ == "__main__":
    app.run(debug=True)
