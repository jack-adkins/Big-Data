import requests
from bs4 import BeautifulSoup


def books():

    url = 'https://aliceinwonderland.fandom.com/wiki/Welcome_to_Wonderland'
    
    #Using the requests library to send to website using http
    response = requests.get(url)
    
    soup = BeautifulSoup(response.content, 'lxml')
    
    #From the inspected html code, the span tag was used with Canon Books label
    bType = soup.find('span', string='Canon books')
    
    names = []
    if bType:
        #Finds each ul tag containg the list of books we want
        ul = bType.find_next('ul', class_='wds-list')
        if ul:
            #The li tag was used for containing each book of the canon books type
            for li in ul.find_all('li'):
                a_tag = li.find('a')
                if a_tag:
                    bName = a_tag.get_text()
                    names.append({'name': bName})
    
    return names

def poems():
    url = 'https://aliceinwonderland.fandom.com/wiki/Welcome_to_Wonderland'
    
    # Using the requests library to send to website using http
    response = requests.get(url)
    
    soup = BeautifulSoup(response.content, 'lxml')
    
    #From the inspected html code, the span tag was used with Canon Poems label
    pType = soup.find('span', string='Canon poems')
    
    names = []
    if pType:
        # Finds each ul tag containing the list of poems we want
        ul = pType.find_next('ul', class_='wds-list')
        if ul:
            # The li tag was used for containing each poem of the canon poems type
            for li in ul.find_all('li'):
                a_tag = li.find('a')
                if a_tag:
                    pName = a_tag.get_text()
                    pURL = a_tag['href']
                    names.append({'name': pName, 'url': pURL})
    
    return names

def poem_title_text(n):
    all_poems = poems()
    
    # Handling only for Turtle Soup (n = 5) and The Walrus and the Carpenter (n = 2)
    if not (n == 5 or n == 2):
        return ("The structure of the poem at index "+ str(n) + " is not supported"), ""
    else:
        # Get the title that we already know
        pTitle = all_poems[n]['name']

        pText = ""
        
        pURL = all_poems[n]['url']
        
        response = requests.get(pURL)
        soup = BeautifulSoup(response.content, 'lxml')
        
        #from inspected html the header is just labeled as 'Text'
        textArea = soup.find('span', {'id': 'Text'})
        if textArea:
            #Based on the inspected html, all the text is tagged with 'p' after the header
            for p_tag in textArea.find_all_next('p'):
                # within the p tags, i tags and breaks are nested between the lines of text
                paragraph = "".join(i_tag.get_text() for i_tag in p_tag.find_all('i'))
                #Progressively add each paragraph/section to our full text string
                pText += paragraph
            pText += "\n"  
        
        return pTitle, pText


#Actual code to run to use the defined functions
CanonBooks = books()
CanonPoems = poems()
for b in CanonBooks:
    result = f"{b['name']}"
    print(result)
for p in CanonPoems:
    result = f"({p['name']}, {p['url']})"
    print(result)
for i in range(7):
    title, text = poem_title_text(i)
    print(title)
    print(text)