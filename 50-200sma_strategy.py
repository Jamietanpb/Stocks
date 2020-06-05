import pandas as pd
import matplotlib

df = pd.read_csv('C:\\Users\\jamie\\OneDrive - RLS ,inc\\Python\\Stock\\ba.csv')
df.columns = df.columns.str.strip()
df['%change'] = df['Close'].pct_change() 
df['200 sma'] = df['Close'].rolling(window=200).mean().round(5)
df['50 sma'] = df['Close'].rolling(window=50).mean().round(5)
df['Criteria 1'] = df['Close'] >= df ['200 sma']
df['Criteria 2'] = (df['50 sma'] >= df['200 sma']) | df['Criteria 1'] == True
df['Buy and hold'] = 100*(1+df['%change']).cumprod()
df['200 sma model'] = 100*(1+df['Criteria 1'].shift(1)*df['%change']).cumprod()
df['200 sma + crossover model'] = 100*(1+df['Criteria 2'].shift(1)*df['%change']).cumprod()
# 200sma model's returns

start_model1 = df['200 sma model'].iloc[200]
end_model1 = df['200 sma model'].iloc[-1]
years = (df['200 sma model'].count()+1-200)/252
model1_average_return = (end_model1/start_model1)**(1/years)-1
print('200 sma model yields an average of', model1_average_return*100, '% per year')

#200 sma + crossover model's returns

start_model2 = df['200 sma + crossover model'].iloc[200]
end_model2 = df['200 sma + crossover model'].iloc[-1]
years = (df['200 sma model'].count()+1-200)/252
model2_average_return = (end_model2/start_model2)**(1/years)-1
print('200 sma + crossover model yields an average of', model2_average_return*100, '% per year')

#buy and hold's returns
start_spx = df['Close'].iloc[200]
end_spx = df['Close'].iloc[-1]
spx_average_return = (end_spx/start_spx)**(1/years)-1
print('Buy and hold yields an average of', spx_average_return*100, '% per year')

df[['Buy and hold', '200 sma model', '200 sma + crossover model']].plot(grid=True, kind='line', title='Different models', logy=True)