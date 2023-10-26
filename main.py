import requests
from bs4 import BeautifulSoup
import bs4
import pandas as pd
def has_p_but_no_li(tag):
    return tag.has_attr('p') and not tag.has_attr('ol')
for i in range(1,8):
    SPECIFIC_PAGE = "https://www.handbook.fca.org.uk/handbook/PROD/" +str(i)+"/?view=chapter"
    #SPECIFIC_PAGE = "https://www.handbook.fca.org.uk/handbook/PROD/1/?view=chapter"

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
    sections = results.find("section")
    if not sections:
        continue
    sections = results.find_all("section")
    for section in sections:
        details = section.find(class_ = "details")
        if not details:
            continue
        rule_reference = details.find(class_ = "extended").text
        rule = details.find(class_ = "section-type").text
        times = details.find("time").text
        print(rule_reference)
        print(rule)
        print(times.strip())
        paragraph = section.find(class_ = ["rule","UK","evidential","guidance"])
        children = paragraph.findChildren(recursive=False)
        subsection = paragraph.find("ol")
        if not subsection:
                el = paragraph.find_all('p')
                for ellsections in el:
                    print(ellsections.text.strip())
                    df.loc[len(df)] = [rule_reference,rule,times.strip(),"",ellsections.text.strip()]
        if subsection:
            external_ps = children[1].find_all(('p','ol'))
            for ps in external_ps:
                a = ps.find('li', recursive=False)
                if not a:
                    if not ps.previous_sibling:
                        continue
                    print(ps.previous_sibling.text.strip(),ps.text.strip())
                    ['Rule reference','Rule or Guidance','Date','Sub sections','Full text']
                    df.loc[len(df)] = [rule_reference,rule,times.strip(),ps.previous_sibling.text.strip(),ps.text.strip()]
    print(df.head(10))
    df.to_excel("output" + str(i)+".xlsx")

