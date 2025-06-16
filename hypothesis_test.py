# import necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import pingouin
from scipy.stats import mannwhitneyu 


# load the dataset for men and womens results
men_results = pd.read_csv('men_results.csv') 
women_results = pd.read_csv('women_results.csv')  


# Convert date column to datetime data type 
men_results['date'] = pd.to_datetime(men_results['date'])
women_results['date'] = pd.to_datetime(women_results['date']) 


# Verify the conversion
print(men_results['date'].dtype) 
print(women_results['date'].dtype) 


# Determine the unique tournaments in the dataset
print(list(men_results['tournament'].unique())) 


# Filter the men and womens dataset for the fifa world cup games played after 2002   
# Subset for men's Fifa World Cup games played after 2002
mens_fifa_wc = men_results['tournament'] == 'FIFA World Cup' 
mens_2002 = men_results['date'] > '2002-01-01'


# Subset for women's Fifa World Cup games played after 2002
womens_fifa_wc = women_results['tournament'] == 'FIFA World Cup'  
womens_2002 = women_results['date'] > '2002-01-01' 


# Subsetting with the two filters 
men_goals = men_results[mens_fifa_wc & mens_2002] 
women_goals = women_results[womens_fifa_wc & womens_2002] 


# Create columns for group and goals scored 
men_goals['group']= 'men' 
men_goals['goals_scored'] = men_goals['home_score'] + men_goals['away_score'] 

women_goals['group'] = 'women'
women_goals['goals_scored'] = women_goals['home_score'] + women_goals['away_score'] 


# Visualize distribution of goals scored for both groups
men_goals['goals_scored'].hist()
plt.show()
plt.clf() 

women_goals['goals_scored'].hist()
plt.show()
plt.clf() 

# Combine both datasets 
men_women_goals = both = pd.concat([men_goals, women_goals], axis=0, ignore_index=True) 


# Pivot the combined dataset to have a wide format for easier comparison
men_women_goals_wide = men_women_goals.pivot(columns="group", values="goals_scored")

# Perform the pingouin Mann-Whitney U test
results_pg = pingouin.mwu(x=men_women_goals_wide["women"],
                          y=men_women_goals_wide["men"],
                          alternative="greater") 


# Alternative SciPy solution: 
# Perform the Mann-Whitney U test using SciPy
results_scipy = mannwhitneyu(x=men_goals["goals_scored"],
                             y=women_goals["goals_scored"],
                             alternative="greater") 


# Extract p-value as a float
p_val = results_pg["p-val"].values[0]

# Determine the result based on the p-value
if p_val <= 0.01:
    result = "reject"
else:
    result = "fail to reject"

result_dict = {"p_val": p_val, "result": result}

print(result_dict)

