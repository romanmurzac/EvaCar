
# EvaCar

## Price Evaluation & Prediction on Romanian second-hand Car market

### Description
EvaCar is a repository that contains code and documentation for Romanian second-hand market:
- evaluation of the current state of the market.
- prediction of the car price based on car model, year of production, fuel, mileage, etc.

#### General notes

The dataset used in this study is obtained from one of the most important car seller platform in Romania.\
The dataset was obtained from one single source.\
The dataset contains data available on 10th December 2023 on Car Seller Platform.

### Statements

1. #### Business understanding
2. #### Analytic approach
3. #### Data requirements

### Data processing

1. #### Data collection
Data collection was performed with internal tool --> data_scrapper.\
Data were retrieved on 10th December 2023 from Romanian Car selling platform.
#### Stages
1. Identify online resources that sell cars in Romania, e.g. Autovit, OLX, Lajumate, Bestauto, etc.
2. Create a list with all available cars.
3. Analyze source HTML structure, identify necessary HTML elements and HTML classes.
4. Create schema with desired columns that will be retrieved from source.
5. Create web scrapper using Beautiful Soup library and Pandas for save to CSV file.
6. Apply data_scrapper.

![Raw Dataset.](media/image_1.PNG "Raw Dataset")


2. #### Data understanding
3. #### Data preparation

### Model build

1. #### Modeling
2. #### Evaluation

### Model deployment

1. #### Deployment

### Continuous improvement

1. #### Feedback
