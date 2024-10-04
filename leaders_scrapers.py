import requests
from bs4 import BeautifulSoup
import json
import re

# def get_first_paragraph(wikipedia_url):
def get_first_paragraph(wikipedia_url,session):
    req_wiki=session.get(wikipedia_url)
    contents= req_wiki.content
    soup = BeautifulSoup(contents, "html.parser")
    paragraph=soup.find_all("p")
    for p in paragraph:
        if p.find("b"):
            para= p.text
            break
    output_string = re.sub(r"[\[0-9,a-z,\']*]", " ", para) 
    cleaned_text = re.sub(r"[\W]+", " ", output_string)
    #cleaned_text_new= re.sub(r" ","",cleaned_text)
    #print(cleaned_text)
             
    return cleaned_text

def get_leaders():
    session=requests.Session()
    root_url = "https://country-leaders.onrender.com/"
    resp_cookies = session.get(f"{root_url}/cookie/")
    cookies = resp_cookies.cookies
    resp_countries = session.get(f"{root_url}/countries/", cookies=cookies)
    countries = resp_countries.json()
    leaders_per_country = {}

    for country in countries:
        try:
            response = session.get(f"{root_url}/leaders/", params={"country": country})  # Removed cookies from this line
            if response.status_code == 200:
                leaders = response.json()
                for leader in leaders:
                    url = leader["wikipedia_url"]
                    para = get_first_paragraph(url, session)
                    leader["first_paragraph"] = para  
                leaders_per_country[country] = leaders

        except:
            resp_cookies = session.get(f"{root_url}/cookie/")
            cookies = resp_cookies.cookies

    return leaders_per_country


def save(leaders_per_country):
    with open('output.json', 'w') as Output_file:
        return json.dump(out, Output_file,indent=4)
    
out= get_leaders()
save_file=save(out)
print(out)