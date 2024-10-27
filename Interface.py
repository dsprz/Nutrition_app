from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QLineEdit, QVBoxLayout, QHBoxLayout, QGroupBox, QLabel
import sys
from DataFinder import DataFinder

class Interface(QWidget):

    def __init__(self, datafinder: DataFinder):
        super().__init__()
        self.datafinder = datafinder

        #main layout
        self.main_layout = QHBoxLayout()
        
        #divide main layout into 2 vertical layouts
        self.left_vertical_layout = QVBoxLayout()
        self.right_vertical_layout = QVBoxLayout()
        self.bottom_vertical_layout = QVBoxLayout()
        self.results_layout = QVBoxLayout()
        button = QPushButton("Confirm for all")
        button.clicked.connect(lambda checked: self.display_results())
        self.bottom_vertical_layout.addWidget(button)
        self.create_clickable_products()


        self.main_layout.addLayout(self.left_vertical_layout)
        self.main_layout.addLayout(self.right_vertical_layout)
        self.main_layout.addLayout(self.bottom_vertical_layout)
        self.main_layout.addLayout(self.results_layout)
        self.setLayout(self.main_layout)

        self.line_edits_list = []
        self.added_products = []
        self.results_labels = []
    
    def add_line_edit(self, product_name):

        if product_name in self.added_products:
            return
        #create a group box and an empty vertical layout
        groupbox = QGroupBox(product_name)
        groupbox.setMaximumSize(400, 50)
        vertical_layout = QHBoxLayout()

        #create line edits and buttons
        line_edit = QLineEdit("1")
        line_edit.setPlaceholderText(f"Portion of {product_name}")
        portionLabel = QLabel("Portion")
        #line_edit_confirmation_button = QPushButton("Confirm")
        #line_edit_confirmation_button.clicked.connect(lambda checked: self.compute_nutritional_value(product_name, float(line_edit.text())))

        #add widgets to the vertical layout
        vertical_layout.addWidget(portionLabel)
        vertical_layout.addWidget(line_edit)
        #vertical_layout.addWidget(line_edit_confirmation_button)
        groupbox.setLayout(vertical_layout)

        self.right_vertical_layout.addWidget(groupbox)

        self.line_edits_list.append(line_edit)
        self.added_products.append(product_name)
    
    def create_clickable_products(self):
        all_products = self.datafinder.get_all_products()
        
        for product_name in all_products:
            button = QPushButton(product_name)

            #ne pas changer la ligne sinon ça marche pas
            button.clicked.connect(lambda checked, p=product_name: self.create_interaction_with_product(p))
            self.left_vertical_layout.addWidget(button)


    def create_interaction_with_product(self, product):
        self.add_line_edit(product)
    
    def compute_nutritional_value(self, product, portion):
        all_nutriments = self.datafinder.get_all_nutriments()
        nutriments_and_values_dict = {}

        for nutriment in all_nutriments:
            nutriments_and_values_dict[nutriment] = 0

        nutritional_values = self.datafinder.get_nutritional_values(product)
        for key, value in nutritional_values.items():
            nutriments_and_values_dict[key] = portion*value
        
        return nutriments_and_values_dict

    def compute_total_nutritional_value(self):
        """Compute the total nutriments for the chosen products"""

        all_nutriments = self.datafinder.get_all_nutriments()
        all_line_edit_values = [float(self.line_edits_list[i].text()) for i in range (len(self.line_edits_list))]

        #create a basic dictionary 
        nutriments_and_total_values_dict = {}
        for nutriment in all_nutriments:
            nutriments_and_total_values_dict[nutriment] = 0

        #compute for each product
        i=0
        for product in self.added_products:
            nutritional_values = self.datafinder.get_nutritional_values(product)
            for key, value in nutritional_values.items():
                nutriments_and_total_values_dict[key] += float(all_line_edit_values[i]*value)
                nutriments_and_total_values_dict[key] = round(nutriments_and_total_values_dict[key], 3)
            i+=1

        return nutriments_and_total_values_dict

    def display_results(self):

        self.delete_widgets_in_layout(self.results_layout)
        self.results_labels.clear()

        goals = self.datafinder.get_params_values_to_reach_dict()
        print(goals)
        results = self.compute_total_nutritional_value()
        for key, value in results.items():
            goal = goals[key][0]
            unit = goals[key][1]
            #Parce qu'il y a des trucs du genre ("15-20")
            if type(goal) == str and "-" in goal:
                t = goal.split("-")
                goal = float(t[0])
                
            ratio = round(100*value/goal, 2)
            label = QLabel(f"{key} : {value} {unit} ===> {ratio}%")
            if(ratio < 30):
                label.setStyleSheet("font-weight: bold; color: red;")
            else:
                label.setStyleSheet("font-weight: bold;")

            self.results_layout.addWidget(label)
            self.results_labels.append(label)
    
    def delete_widgets_in_layout(self, layout):

        while layout.count():
            item = layout.takeAt(0)
            if item.widget() != None:
                item.widget().deleteLater()


if __name__ == "__main__":
    datafinder = DataFinder()
    app = QApplication(sys.argv)
    interface = Interface(datafinder)
    interface.show()
    sys.exit(app.exec_())
