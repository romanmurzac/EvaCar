from bs4 import BeautifulSoup
import requests
import pandas as pd


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


def select_list_elements(raw_data: list, index: int, step: int) -> list:
    """
    Take a list and extract elements from a specific index and with specific step.
        Parameters:
            raw_data (list): initial elements
            index (int): starting index of extracting
            step (int): step of extracting elements
        Returns:
            extracted_elements (list): extracted data
    """
    # Extract elements with specific step from a list
    extracted_elements = raw_data[index::step]

    # Return list with data
    return extracted_elements


def split_str_to_elem(raw_data: list, splitter: str, initial_index: int, final_index: int) -> list:
    """
    Split list elements on custom splitter and return specific part of it.
        Parameters:
            raw_data (list): initial list
            splitter (str): symbol that serve as splitter
            initial_index (int): starting index of element to be kept
            final_index (int): final index of element to be kept
        Returns:
            split_list (list): split data
    """
    # Iterate through list and split each element on specific splitter
    split_list = []
    for element in raw_data:
        split_element = element.split(splitter)[initial_index:final_index]

        # Create new element
        if len(split_element) > 1:
            item = " ".join(split_element)
        elif len(split_element) != 0:
            item = split_element[0]
        else:
            item = split_element
        split_list.append(item)

    # Return list with data
    return split_list


def convert_str_to_int(raw_data: list, clean_mode: bool) -> list:
    """
    Eliminate unnecessary part of a string and convert it into integer.
        Parameters:
            raw_data (list): initial list
            clean_mode (bool): eliminate or not a part of the string
        Returns:
            int_list (list): casted data
    """
    # Iterate through list elements
    int_list = []
    for element in raw_data:

        # Split elements by empty space
        split_list = element.split(" ")

        # Check how many new elements were resulted
        if len(split_list) > 1:

            # Build new element from all resulted elements
            # Excluding last one in clean mode
            if clean_mode:
                int_element = int("".join(split_list[:-1]))
            else:
                int_element = int("".join(split_list))
        elif len(split_list) != 0:
            int_element = int(split_list[0])
        else:
            int_element = int(split_list)
        int_list.append(int_element)

    # Return list with data
    return int_list


def save_to_csv(file_name: str, column_names: list, data_series: list) -> None:
    """
    Convert lists in Pandas DataFrame and save it in a CSV file.
        Parameters:
            file_name (str): CSV file name where to save data
            column_names (list): list with columns name
            data_series (list): list with data list names
        Returns:
            None
    """
    # Convert lists to DataFrame
    df = pd.DataFrame(list(zip(element_lists)), columns=column_names)

    # Save DataFrame to CSV file
    df.to_csv(f"{file_name}.csv", sep=',', encoding='utf-8', index=False, header=False, mode="a")


# Run file as a script
if __name__ == "__main__":
    ...
