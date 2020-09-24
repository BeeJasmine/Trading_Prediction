### Trading prediction in Streamlit app

The stock prediction of this app is based on time series algotithms. Soon, i will add the sentiment analysis of news to adjust the predictions.


#### Requirements & project's downloading


``
git clone https://github.com/BeeJasmine/Trading_Prediction.git
cd Trading_Prediction
python -m venv venv/
source venv/Scripts/activate # Windows
source venv/bin/activate # Mac
conda create -n financeTimeSeries
conda activate financeTimeSeries
pip install -r requirements.txt
streamlit run trading.py
``


#### Preprocessing

I made an Exploratory Data Analysis in the ``/notebooks `` folder.

#### Modelling

We observed the results are slightly better with a simple LSTM so we trained and saved the simple model for each stock.







###### ToDo:
-> finish flask application
