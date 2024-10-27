import pandas as pd
import numpy as np
#pip install openpxyl



EXCEL_NUTRIMENTS_FILE_PATH = "./Nutrition_data/Excel/Nutriments.xlsx"

ex  = pd.ExcelFile(EXCEL_NUTRIMENTS_FILE_PATH)
sheet_names = ex.sheet_names

PARAMS_SHEET = sheet_names[0]
PRODUCTS_SHEET = sheet_names[1]

PARAMS_VARIABLES = "Variables"
PARAMS_NUTRIMENTS = "Nutriments"

PARAMS_NUTRIMENT_NAME_INDEX = 2 #Col C
PARAMS_NUTRIMENT_VALUE_INDEX = 3 #Col D
PARAMS_NUTRIMENT_UNIT_INDEX = 4 #Col E

PARAMS_VARIABLE_VALUE_INDEX = 6 #Col G
PARAMS_VARIABLE_NAME_INDEX = 7 #Col H

PRODUCTS_NUTRIMENTS = "Nutriments"
PRODUCTS_NUTRIMENTS_NAME_INDEX = 2
PRODUCTS_NUTRIMENTS_VALUE_START_INDEX = 3

VITAMINS = ["A",
            "B1",
            "B2",
            "B3",
            "B5",
            "B6",
            "B7",
            "B9",
            "B12",
            "C",
            "D",
            "E",
            "K"
        ]

class DataFinder():

    def __init__(self):
        self.products_df = pd.read_excel(EXCEL_NUTRIMENTS_FILE_PATH,
                                    sheet_name=PRODUCTS_SHEET)
        
        self.params_df = pd.read_excel(EXCEL_NUTRIMENTS_FILE_PATH,
                                    sheet_name=PARAMS_SHEET)
        
        self.params_nutriments_dict = {}
        self.params_create_nutriments_dict()
        #print(self.params_nutriments_dict)

        self.params_values_to_reach_dict = {}
        self.params_create_values_to_reach_dict()
        #print(self.params_values_to_reach_dict)

    
        self.products_dict = {}
        self.products_nutritional_values_create_dict()

    def params_create_nutriments_dict(self):

        len_nutriments = len(self.params_df[PARAMS_NUTRIMENTS])

        for row in range(len_nutriments):
            key = self.params_df.iloc[row, PARAMS_NUTRIMENT_NAME_INDEX]
            if key in VITAMINS:
                key = f"Vitamine {key}"
            value = self.params_df.iloc[row, PARAMS_NUTRIMENT_VALUE_INDEX]
            unit = self.params_df.iloc[row, PARAMS_NUTRIMENT_UNIT_INDEX]
            self.params_nutriments_dict[key] = value, unit
        
    def params_create_values_to_reach_dict(self):

        len_variables = len(self.params_df[PARAMS_VARIABLES])

        for row in range(len_variables):
            key = self.params_df.iloc[row, PARAMS_VARIABLE_NAME_INDEX]
            value = self.params_df.iloc[row, PARAMS_VARIABLE_VALUE_INDEX]
            self.params_values_to_reach_dict[key] = float(value)
    
    def get_all_products(self) -> list :
        """Returns a list of all products in the PRODUCT_SHEET"""

        number_of_columns = len(self.products_df.columns)
        all_products = []
        for i in range(number_of_columns):
            column_name = self.products_df.columns[i]
            if column_name == "Nutriments" or column_name == f"Unnamed: {i}":
                continue
            all_products.append(column_name)
        return all_products

    def products_nutritional_values_create_dict(self):
        """Quantites in grams"""

        number_of_columns = len(self.products_df.columns)
        len_nutriments = len(self.products_df[PRODUCTS_NUTRIMENTS])
        product_column = PRODUCTS_NUTRIMENTS_VALUE_START_INDEX

        for i in range(number_of_columns):
            column_name = self.products_df.columns[i]
            if column_name == "Nutriments" or column_name == f"Unnamed: {i}":
                continue

            intermediate_dict = {}
            for j in range (len_nutriments):

                nutriment_name = self.products_df.iloc[j, PRODUCTS_NUTRIMENTS_NAME_INDEX]
                if nutriment_name in VITAMINS:
                    nutriment_name = f"Vitamine {nutriment_name}"

                value = self.products_df.iloc[j, product_column]
                intermediate_dict[nutriment_name] = value

            product_column += 1
            #print(f"product_column = {product_column}")

            self.products_dict[column_name] = intermediate_dict

    
    def get_nutritional_values(self, product: str):
        return self.products_dict[product]

    def get_product_dict(self):
        return self.products_dict

    def get_all_nutriments(self):
        len_nutriments = len(self.products_df[PRODUCTS_NUTRIMENTS])
        all_nutriments = []
        for i in range(len_nutriments):
            nutriment_name = self.products_df.iloc[i, PRODUCTS_NUTRIMENTS_NAME_INDEX]
            if nutriment_name in VITAMINS:
                nutriment_name = f"Vitamine {nutriment_name}"
            all_nutriments.append(nutriment_name)
        return all_nutriments

    def get_params_values_to_reach_dict(self):
        return self.params_nutriments_dict



datafinder = DataFinder()
if __name__ == "__main__":
    print(datafinder.get_all_nutriments())
#print(datafinder.get_product_dict())
#print(datafinder.get_nutritional_values("Lait lactel demi écrémé")["Protéines"])

