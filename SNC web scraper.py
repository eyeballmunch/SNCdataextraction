import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

startingexl = pd.read_excel(r'') ## here choose a innput path containing a excel with a collunm called "url" containg urls to SNC finder of a specific startup page
web_pages_data = []
runtime = 0
for index, row in startingexl.iterrows():
    
    # Send a GET request to the website
    url = row['url']
    response = requests.get(url)
    if response.status_code == 200:
        print('Web site exists')
        # Create a BeautifulSoup object to parse the HTML
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the desired information on the page
        company_name_element = soup.find("h1", class_="company-profile-name")
        company_discription_element = soup.find("h2", class_="company-profile-description")

        #extract funding data // NEED TO CLEAN
        company_funding_element = soup.find_all("div", id="company-funding-container")

        #extract stats data // NEED TO CLEAN
        company_stats_element = soup.find_all("div", id="company-stats-container")

        #extract people
        company_people_element = soup.find_all("div", class_="team-member-text-content")

        #extracting investing info
        company_investment_element = soup.find_all("div",id="private-equity-funding-container")

         #extract private investments info
        company_privateinvestment_element = soup.find_all("div",id="non-equity-funding-container")

        #extract investors info
        company_investors_element = soup.find_all("div",class_="investors")

        #extract company tags info
        company_sector_element = soup.find_all("div",id="company-tags-container")

        # Check if the elements exist before accessing their text attribute
        company_name = company_name_element.text.strip() if company_name_element else "N/A"
        company_discription_element = company_discription_element.text.strip() if company_discription_element else "N/A"
        company_funding_element = company_funding_element if company_funding_element else "N/A"
        company_stats_element = company_stats_element if company_stats_element else "N/A"
        company_people_element = company_people_element if company_people_element else "N/A"
        company_investment_element = company_investment_element if company_investment_element else "N/A"
        company_investors_element = company_investors_element if company_investors_element else "N/A"
        company_sector_element = company_sector_element if company_sector_element else "N/A"
        company_privateinvestment_element = company_privateinvestment_element if company_privateinvestment_element else "N/A"

        ##Print the scraped information
        #this is for funding data
        temp = str(company_funding_element)
        soup2 = BeautifulSoup(''.join(temp), 'html.parser')

        a = soup2.find('a',href=True)
        a = a if a else "N/A"
        if a != "N/A":

            displayed_text = a.text
            funding_stage = str(displayed_text)
            spans = soup2.find_all('span')
            span_text = [span.text for span in spans]
            total_fundings = span_text[0]
            last_funding = span_text[2]
            total_rounds = span_text[3]
            investors = span_text[4]
        else: 
            total_fundings = "N/A"
            last_funding = "N/A"
            total_rounds = "N/A"
            investors = "N/A"

        #this is for stats data
        temp2 = str(company_stats_element)
        soup3 = BeautifulSoup(''.join(temp2), 'html.parser')
        hrefs = soup3.find_all('a',href = True)

        founded_href = soup3.find('h4', string='Founded').find_next('a').text  #find the founded using h4
        business_models_hrefs = [a.text for a in soup3.find('h4', string='Business models').find_next('span').find_all('a')] #find the b models using h4
        business_model = ' '.join(business_models_hrefs)
        href_text = [span.text for span in hrefs] # getting all data

        product_stage_href = href_text[-1]
        employees_href = href_text[-2]
        
        ##this is for exctracting people
        temp3 = str(company_people_element)
        soup3 = BeautifulSoup(''.join(temp3), 'html.parser')
        b = soup3.text
        cleaned_text = re.sub(r"\s{2,}", " ", b)
        cleaned_text = re.sub(r"[\[\]]", "", cleaned_text)
        cleaned_text = cleaned_text.strip()
        workernames = cleaned_text.split(", ")

        staff = ', '.join(workernames)

        #this is for investing data
        temp4 = str(company_investment_element)
        soup4 = BeautifulSoup(''.join(temp4), 'html.parser')
        details = soup4.find_all('div',class_="lifecycle-header-container")
        temp = [span.text for span in details]
        newlistofinvestments = []
        for round in temp:
            t2 = round.replace('\n', '').strip()
            t2 = re.sub(r'\s+', ' ', t2)
            newlistofinvestments.append(t2)

        list_of_investments = ', '.join(newlistofinvestments)

        #this is for privatte investing data
        temp7 = str(company_privateinvestment_element)
        soup7 = BeautifulSoup(''.join(temp7), 'html.parser')
        details = soup7.find_all('div',class_="lifecycle-header-container")
        temp8 = [span.text for span in details]
        newlistoninvestments = []
        for round in temp8:
            t2 = round.replace('\n', '').strip()
            t2 = re.sub(r'\s+', ' ', t2)
            newlistoninvestments.append(t2)

        list_of_privateinvestments = ', '.join(newlistoninvestments)

        #this is for invester data
        temp6 = str(company_investors_element)
        soup6 = BeautifulSoup(''.join(temp6), 'html.parser')
        investor_list_containers = soup6.find_all(class_="investors")
    
        result_list = []
        for hello_class in investor_list_containers:
            hello2_classes = hello_class.find_all(class_="investor-list-container")
            hello2_strings = [hello2.get_text() for hello2 in hello2_classes]
            result_list.append(' '.join(hello2_strings))

        cleaned_company_list = []
        for element in result_list:
            cleaned_element = " ".join(element.split()).replace('\xa0', '')
            cleaned_company_list.append(cleaned_element)
        
        company_list = list(dict.fromkeys(cleaned_company_list))
        
        #this is for companny tags
        temp5 = str(company_sector_element)
        soup5 = BeautifulSoup(''.join(temp5), 'html.parser')
        tags= soup5.text
        cleaned_text = re.sub(r"\s{2,}", " ", tags)
        cleaned_text = re.sub(r"[\[\]]", "", cleaned_text)
        tags_list = ", ".join(cleaned_text.split())

        #create a excel with the dat
        page_data = {"Url:":url,
                    "Company Name": company_name , 
                    "Company discription": company_discription_element,
                    "funding stage": funding_stage,
                    "total fundings": total_fundings,
                    "last_fundings": last_funding,
                    "total rounds": total_rounds,
                    "investors": investors,
                    "founded": founded_href,
                    "business model": business_model,
                    "employees": employees_href,
                    "product stage": product_stage_href,
                    "staff": staff,
                    "investments": list_of_investments,
                    "private investtments": list_of_privateinvestments,
                    "who invested what round": company_list,
                    "tags": tags_list
        }

        web_pages_data.append(page_data) 
        df = pd.DataFrame(web_pages_data)
    else:
        print('Web site does not exist') 
    print(runtime)
    runtime +=1
print(df)
df.to_csv(r'') # here choose a output location and add at the end the name of the desired file.xlsx example:"SNCdata.xlsx"
    