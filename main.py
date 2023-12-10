from internal_tools import data_scrapper
import var_const

# Define variables
car_identifier = var_const.variables.car_pages
unique_cars = len(var_const.variables.car_pages)
raw_schema = var_const.variables.raw_schema
html_elements = var_const.variables.html_elements
html_classes = var_const.variables.html_classes

# Define user inputs
user_url = input("Please introduce the base URL:\n")
user_filename = input("Please introduce name for CSV file to store raw data:\n")

# Iterate through all cars type for individual number of pages
for key in range(1, unique_cars + 1):
    for index in range(1, car_identifier[key][1] + 1):
        # Try to load full content from page
        try:
            # Retrieve content from first area and split in 3 features
            first_data = data_scrapper.get_raw_data(
                endpoint=f"{user_url}/{car_identifier[key][0]}?page={index}",
                html_element=html_elements[1], html_class=html_classes[1])
            data_1 = data_scrapper.select_list_elements(raw_data=first_data, index=0, step=3)
            data_2 = data_scrapper.select_list_elements(raw_data=first_data, index=1, step=3)
            data_3 = data_scrapper.select_list_elements(raw_data=first_data, index=2, step=3)

            # Retrieve content from second area and split in 3 features
            second_data = data_scrapper.get_raw_data(
                endpoint=f"{user_url}/{car_identifier[key][0]}?page={index}",
                html_element=html_elements[2], html_class=html_classes[2])
            data_4 = data_scrapper.split_str_to_elem(
                raw_data=second_data, splitter=" ", initial_index=0, final_index=car_identifier[key][2])
            data_5 = data_scrapper.split_str_to_elem(
                raw_data=second_data, splitter=" ", initial_index=car_identifier[key][2],
                final_index=car_identifier[key][2] + car_identifier[key][3])
            data_6 = data_scrapper.split_str_to_elem(
                raw_data=second_data, splitter=" ",
                initial_index=car_identifier[key][2] + car_identifier[key][3], final_index=999)

            # Retrieve content from third area and split in 3 features
            third_data = data_scrapper.get_raw_data(
                endpoint=f"{user_url}/{car_identifier[key][0]}?page={index}",
                html_element=html_elements[3], html_class=html_classes[3])
            data_07 = data_scrapper.select_list_elements(raw_data=third_data, index=0, step=2)
            data_7 = data_scrapper.split_str_to_elem(raw_data=data_07, splitter=" ", initial_index=0, final_index=1)
            data_8 = data_scrapper.split_str_to_elem(raw_data=data_07, splitter=" ", initial_index=1, final_index=2)
            data_9 = data_scrapper.select_list_elements(raw_data=third_data, index=1, step=2)

            # Retrieve content from fourth area
            fourth_data = data_scrapper.get_raw_data(
                endpoint=f"{user_url}/{car_identifier[key][0]}?page={index}",
                html_element=html_elements[4], html_class=html_classes[4])
            data_10 = fourth_data

            # Retrieve content from fifth area
            fifth_data = data_scrapper.get_raw_data(
                endpoint=f"{user_url}/{car_identifier[key][0]}?page={index}",
                html_element=html_elements[3], html_class=html_classes[5])
            data_11 = fifth_data

            # Retrieve content from sixth area
            sixth_data = data_scrapper.get_raw_data(
                endpoint=f"{user_url}/{car_identifier[key][0]}?page={index}",
                html_element=html_elements[3], html_class=html_classes[6])
            data_12 = sixth_data

            # Compress in a list all data series
            data_series = [data_4, data_5, data_1, data_3, data_2, data_10,
                           data_11, data_7, data_5, data_6, data_6, data_12]

            # Save to CSV file raw dataset
            data_scrapper.save_to_csv(file_name=user_filename, column_names=var_const.variables.raw_schema,
                                      data_series=data_series)

            # Print which page was loaded
            print(f"Uploaded page no.: {index}")

        # If a error occur, skip current page and continue from the next page
        except Exception:
            print(f"Skipped page no.: {index}")
            continue
