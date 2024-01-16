# Import necessary modules
import requests
import pandas as pd

from datetime import datetime
from bs4 import BeautifulSoup

from . import source_url, raw_schema, html_elements, html_classes, car_pages

# Define functionalities
def get_raw_data(endpoint: str, html_element: str, html_class: str) -> list:
    """
    Provide URL, specific HTML element and class, and return list with all data.
        Parameters:
            endpoint (str): full URL
            html_element (str): HTML element
            html_class (str): HTML class
        Returns:
            raw_data (list): retrieved data
    """
    # Define URL and get content
    page = requests.get(endpoint)
    soup = BeautifulSoup(page.content, "html.parser")

    # Append all results to the list
    results = soup.find_all(html_element, class_=html_class)
    raw_data = []
    for item in results:
        raw_data.append(item.text)
    
    # Return list with data
    return raw_data


def get_date():
    """
    Get current date in specific format: YY-MM-DD.
        Returns:
            specific_date (str): retrieved data
    """ 
    year = str(datetime.datetime.now().year)[-2:]
    month = str(datetime.datetime.now().month)
    day = str(datetime.datetime.now().day)
    if len(month) == 1:
        month = "0" + month
    if len(day) == 1:
        day = "0" + day
    specific_date = f"{year}-{month}-{day}"
    return specific_date

current_date = get_date()

# Iterate through all cars manufacturer and available number of pages
for key in range(1, len(list(car_pages.keys()))):
    for index in range(1, car_pages[key][1]+1):
        try:
            # Define endpoint
            endpoint_url = f"{source_url}/{car_pages[key][0]}?page={index}"

            # Extract data based on endpoint, specific HTML element and class
            first_data = get_raw_data(endpoint=endpoint_url, element=html_elements[1], html_class=html_classes[1])
            second_data = get_raw_data(endpoint=endpoint_url, element=html_elements[2], html_class=html_classes[2])
            third_data = get_raw_data(endpoint=endpoint_url, element=html_elements[3], html_class=html_classes[3])
            fourth_data = get_raw_data(endpoint=endpoint_url, element=html_elements[4], html_class=html_classes[4])[::2]
            fifth_data = get_raw_data(endpoint=endpoint_url, element=html_elements[3], html_class=html_classes[5])

            # Create Pandas dataframe and save it to CSV file
            df = pd.DataFrame(list(zip(first_data, second_data, third_data, fourth_data, fifth_data)), columns=raw_schema)
            df.to_csv(f"RawDataDB-{current_date}.csv", sep=',', encoding='utf-8', index=False, header=False, mode="a")
            print(f"Uploaded page no.: {index} from {car_pages[key][0]} manufacturer.")
        
        # Skip pages with issues and continue for rest of the pages
        except Exception:
            print(f"Skipped page no.: {index} from {car_pages[key][0]} manufacturer.")
            continue

# Run file as a script
if __name__ == "__main__":
    ...
