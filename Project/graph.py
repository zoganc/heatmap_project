import matplotlib.pyplot as plt
import pandas as pd

def loadData():
    cols_to_use = ['Iso3_code', 'Country', 'Region', 'Category', 'Year', 'Unit of measurement', 'VALUE']
    crimeDf = pd.read_csv('EconomyCrime.csv', delimiter=';', usecols=cols_to_use)
    crimeDf['VALUE'] = crimeDf['VALUE'].str.replace(',', '.').astype(float)
    crimeDf['Year'] = pd.to_numeric(crimeDf['Year'])
    return crimeDf

def chosenData(crimeDf, startYear, endYear, crime, country, measure):
    chosenDf = crimeDf[(crimeDf['Year'] >= startYear) & (crimeDf['Year'] <= endYear) & (crimeDf['Category'] == crime) & (crimeDf['Country'] == country) & (crimeDf['Unit of measurement'] == measure)]
    if chosenDf.empty:
        raise Exception("No data found for this combination of criteria.")
    if measure == 'Rate per 100,000 population':
        try:
            chosenDf['VALUE'] = chosenDf['VALUE'].str.replace(",", ".")
        except: 
            raise Exception("All values are floats, no need to replace commas.")
    return chosenDf

def plotGraph(chosenDf, title):
    
    chosenDf = chosenDf.drop(['Iso3_code', 'Region', 'Category', 'Country', 'Unit of measurement'], axis=1)
    year = chosenDf["Year"]
    val = chosenDf["VALUE"]
    fig, ax = plt.subplots()
    ax.set_title(title)
    ax.grid(True)
    ticks = chosenDf["Year"].unique()
    ax.set_xticks(ticks)
    fig.autofmt_xdate()
    ax.plot(year, val)
    ax.get_figure().savefig('graph.jpeg', bbox_inches='tight', dpi=300)

def dataBasedCrimeGraph(startYear, endYear, crime, country, measure):
    # Load data
    crimeDf = loadData()
    # Choose data
    chosenDf = chosenData(crimeDf, startYear, endYear, crime, country, measure)
    # Plot graph
    isRangeFull = True
    if(startYear != chosenDf['Year'].min() or endYear != chosenDf['Year'].max()):
        startYear = chosenDf['Year'].min()
        endYear = chosenDf['Year'].max()
        isRangeFull = False
        
    title = f"{crime} from {startYear} to {endYear} in {country} ({measure})"
    plotGraph(chosenDf, title)
    if(isRangeFull == False): return False
    else: return True
    
#if __name__ == "__main__":
    #dataBasedCrimeGraph(2003, 2018, 'Corruption', 'Poland', 'Counts')