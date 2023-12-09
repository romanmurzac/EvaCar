from bs4 import BeautifulSoup
import requests
import re


def get_raw_data(endpoint: str, element: str, html_class: str) -> list:
    """
    Provide URL, specific HTML element and class, and return list with all data.
    :params:
    endpoint: URL in string format
    element: HTML element in string format
    html_class: HTML class in string format
    return:
    raw_data: list with retrieved data

    """
    # Define URL and get content
    page = requests.get(endpoint)
    soup = BeautifulSoup(page.content, "html.parser")

    # Append all results to the list
    results = soup.find_all(element, class_=html_class)
    raw_data = []
    for item in results:
        raw_data.append(item.text)
    
    # Return list with data
    return raw_data


def select_list_elements(raw_list: list, quantity: int, index: int) -> list:
    """

    :params:

    return:

    """
    single_list = raw_list[index::quantity]

    return single_list


def split_str_to_elem(raw_list: list, splitter: str, initial_index: int, final_index: int) -> list:
    """

    :params:

    return:

    """
    elements_list = []
    for element in raw_list:
        new_element = element.split(splitter)[initial_index:final_index]
        if len(new_element) > 1:
            item = " ".join(new_element)
        elif len(new_element) != 0:
            item = new_element[0]
        else:
            item = new_element
        elements_list.append(item)
    
    return elements_list


def convert_str_to_int(raw_list: list, clean_mode: bool) -> list:
    """

    :params:

    return:

    """
    int_list = []
    for element in raw_list:
        split_list = element.split(" ")
        if len(split_list) > 1:
            if clean_mode:
                int_element = int("".join(split_list[:-1]))
            else:
                int_element = int("".join(split_list))
        elif len(split_list) != 0:
            int_element = int(split_list[0])
        else:
            int_element = int(split_list)
        int_list.append(int_element)

    return int_list


if __name__ == "__main__":
    ...
