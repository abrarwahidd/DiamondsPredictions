# 💎 Diamonds Price Prediction
This project aims to predict the price of diamonds based on various features such as carat, color, clarity, etc. I used three Machine Learning algorithms to compare which model gives the best results.

## 📌 Methodology
### Dataset
The dataset I used is from: https://github.com/tidyverse/ggplot2/blob/main/data-raw/diamonds.csv

The dataset used contains various diamond attributes such as carat, cut, color, clarity, depth, table, price, x, y, and z.
This data is then cleaned and processed to ensure good model quality.

### Algorithms Used:
I tried three algorithms to compare their performance, namely:

- Random Forest 🌳
- K-Nearest Neighbors (KNN) 📍
- Boosting (AdaBoost) 🚀

### Model Evaluation

The model is evaluated using Mean Squared Error (MSE) to see how accurate the predictions are.
The evaluation results show that Random Forest provides the best performance because it has the smallest MSE value compared to KNN and Boosting.

## 🔍 Results and Conclusions

Of the three models tested, Random Forest produced the most accurate diamond price predictions.
This suggests that the ensemble trees-based approach is more effective in capturing complex patterns in this dataset compared to other methods.

## 🚀 How to Run a Project (Use jupyter Notebook)
1. Clone this repository:
   ```
   git clone https://github.com/username/DiamondsPredictions.git
2. Go to the project directory
   ```
   cd DiamondsPredictions
3. install required dependencies
   ```
   pip install requirements.txt
5. Run Jupyter Notebook
   - If you don't have it installed, make sure Jupyter Notebook is available:
     ```
     pip install notebook
   - Then run the following command to open the notebook:
     ```
     jupyter notebook
7. Open the notebook file and run the cell
   - In Jupyter Notebook, open the notebooks/ folder, then select and run the available .ipynb file.

# Terima Kasih😁😊
