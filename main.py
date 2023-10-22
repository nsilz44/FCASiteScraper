import requests
from bs4 import BeautifulSoup
import pandas as pd

for i in range(1,8):
    SPECIFIC_PAGE = "https://www.handbook.fca.org.uk/handbook/PROD/" +str(i)+"/?view=chapter"

    MAIN_URL = "https://www.fca.org.uk/"


    if SPECIFIC_PAGE[:5] == "https":
        page = requests.get(SPECIFIC_PAGE)
    else:
        try:
            page = requests.get(MAIN_URL+SPECIFIC_PAGE)
        except:
            print("NOT A REAL URL")

    df = pd.DataFrame(columns=['Rule reference','Rule or Guidance','Date','Sub sections','Full text'])

    def make_hyperlink(value):
        url = "{}"
        return '=HYPERLINK("%s", "%s")' % (url.format(value).split(' ')[0], url.format(value).split(' ')[1])

    soup = BeautifulSoup(page.content, "html.parser")

    results = soup.find(class_="full-chapter")
    sections = results.find_all("section")
    for section in sections:
        try:
            details = section.find(class_ = "details")
            rule_reference = details.find(class_ = "extended").text
            rule = details.find(class_ = "section-type").text
            times = details.find("time").text
            print(rule_reference)
            print(rule)
            print(times.strip())

            paragraph = section.find(class_ = ["rule","UK","evidential","guidance"])
            subsection = paragraph.find("ol")
            if not subsection:
                    el = paragraph.find_all('p')
                    for ellsections in el:
                        print(ellsections.text.strip())
                        df.loc[len(df)] = [rule_reference,rule,times.strip(),"",ellsections.text.strip()]
            if subsection:
                allSubsections = subsection.find_all('li', recursive=False)
                for subsections in allSubsections:
                    el = subsections.find_all('p')
                    for ellsections in el:
                        sub = ellsections.previous_sibling.text
                        print(sub,ellsections.text)
                        ['Rule reference','Rule or Guidance','Date','Sub sections','Full text']
                        df.loc[len(df)] = [rule_reference,rule,times.strip(),sub,ellsections.text]
        except:
            continue
    print(df.head(10))
    df.to_excel("output" + str(i)+".xlsx")

