from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options


import sys
from collections import defaultdict
import time
import re
from tqdm import tqdm
import pandas as pd

csv = sys.argv[1]

data = pd.read_csv(csv)

DEBUG = False
options = Options()
options.add_argument("--headless")
driver = webdriver.Firefox(options=options)
# nos = {"orientador": [], "avaliador1": [], "avaliador2": [], "avaliador3": [], "avaliador4": []}

# nos = defaultdict(list)
nos = []
i=0
pattern = r"orcid\.org/[0-9A-Za-z]{4}-[0-9A-Za-z]{4}-[0-9A-Za-z]{4}-[0-9A-Za-z]{4}"
# pattern = r"orcid\.org/\d{4}-\d{4}-\d{4}-\d{4}"
for url in tqdm(data["url"]):
    # tqdm.write(url)
    driver.get("https://www.google.com/")
    driver.get(url)
    if i==0:
        if int(csv.split(".")[0][-4:]) < 2021:
            marctags_button = driver.find_element(By.XPATH, "/html/body/main/div[1]/div/div[1]/div[2]/div/div/div/div/div/div[1]/div/div/button[3]")
        else:
            marctags_button = driver.find_element(By.XPATH, "/html/body/main/div[1]/div/div[1]/div[1]/div/div/div/div/div/div[1]/div/div/button[3]")
        
        marctags_button.click()
    else:
        time.sleep(2)
    try:
        marc_tags = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.ID, 'divMARCTags'))
        )
    except:
        no = defaultdict(str)
        no[f"orientador"] = "Selenium_error"
        nos.append(pd.Series(no))
        continue

    marc_tags_text = marc_tags.get_attribute("innerText")
    # print(marc_tags_text)
    
    avaliador_qtd = 0
    # s = pd.Series()
    no = defaultdict(str)
    for line in marc_tags_text.split("\n"):
        if "Orientador" in line and "700" in line:
            matches = re.findall(pattern, line)
            if matches == []:
                no[f"orientador"] = "sem orcid"
                continue
            # print(matches)
            # nos[matches[0]] = []
            # orientador = matches[0]
            # nos["orientador"].append(matches[0])
            no["orientador"] = matches[0]
        elif "Avaliador" in line:
            avaliador_qtd -=- 1
            matches = re.findall(pattern, line)
            if matches == []:
                # nos[f"avaliador{avaliador_qtd}"].append("sem orcid")
                no[f"avaliador{avaliador_qtd}"] = "sem orcid"
                continue
            # print(matches)
            # nos[orientador].append(matches[0])
            # nos[f"avaliador{avaliador_qtd}"].append(matches[0])
            no[f"avaliador{avaliador_qtd}"] = matches[0]
    nos.append(pd.Series(no))
    if i == 5 and DEBUG: break
    i-=-1
        # break
# print(nos)
# print(body.text )
# print(nos)
# import json
# with open(txt.replace("txt", "json"), 'w') as fp:
#     json.dump(nos, fp)
# data_links = pd.DataFrame(nos)
# data["orientador"] = nos["orientador"]
# data["avaliador1"] = nos["avaliador1"]
# data["avaliador2"] = nos["avaliador2"]
# data["avaliador3"] = nos["avaliador3"]
# data["avaliador4"] = nos["avaliador4"]
data = pd.concat([data, pd.concat(nos, axis=1).T], axis=1)

data.to_csv(csv.replace("links", "defesas"), index=False)