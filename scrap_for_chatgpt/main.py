import re

from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.chrome.options import Options

# Configurez les options pour Chrome en mode sans tête
chrome_options = Options()
# chrome_options.add_argument("--headless")

# Vous pouvez ensuite utiliser ces options lors de la création d'une instance de WebDriver pour Chrome
driver = webdriver.Chrome(options=chrome_options)

link = "https://docs.ultralytics.com/"

name_txt = "ultralytics"

url_list = [link]

def scrap_page(link):
    """
    Scrap tous les liens interne d'une page dans la liste url_list.
    """
    driver.get(link)
    a = driver.find_elements(by=By.TAG_NAME, value='a')
    for i in a :
        href = i.get_dom_attribute("href")
        # print(href)
        if href != None :
            if not re.search('^http|^\.|#', href) :
                # Obtenez l'URL actuel de la page
                if f"https://docs.ultralytics.com/{href}" in url_list : 
                    continue
                else :
                    url_list.append(f"https://docs.ultralytics.com/{href}")

already_scrap = []

def all_link() :
    """
    scrap tous les liens des sous pages dans url_list jusqu'à ce qu'ils n'y en ai plus.
    """
    init = len(url_list)
    for i in url_list:
        if i not in already_scrap :
            scrap_page(i)
            already_scrap.append(i)
        if len(url_list) == init :
            return 
        else : 
            all_link()

# scrap_page(link) 

# print('len : ',len(url_list))
# print(url_list)
    
all_link()

# print('len : ',len(url_list))

# print(url_list)


# driver.quit()

token_count = 0

for index, i in enumerate(url_list):
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(i) 
    content = driver.find_elements(by = By.CSS_SELECTOR, value="body")
    content = [x for x in content if x.text not in [' ','',None]]

    if index == 0 :
        create_or_add = "w"
    else : 
        create_or_add = "a"

    # Pour redémarrer le scrap où il s'est arrêté
    index_to_restart = 0 

    while True :
        i_name_txt = 1
        with open(f"{name_txt}{i_name_txt}.txt", create_or_add, encoding="utf-8") as fichier:
            # Index où reprendre après max token atteint
            save_index2 = 0
            for index2, j in enumerate(content[index_to_restart:]):

                # ajoute le nombre de token 
                occurrences = re.findall(' ', j.text)
                nombre_occurrences = len(occurrences)
                token_count += nombre_occurrences

                if index2 == 0 :
                    fichier.write("prends en contexte " + "\n" +"---" + "\n" +j.text + "\n")
                else :
                    fichier.write("---" + "\n" + j.text + "\n")

                save_index2 = index2

                if token_count>4000 :
                    index_to_restart = index2
                    break

        i_name_txt += 1

        if save_index2 == len(content):
            break


        


    driver.quit()

