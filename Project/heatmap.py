import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

SHAPEFILE = "World_Shape/Worldmap.shp"
EUROPE = ['ALB', 'AND', 'AUT', 'BLR', 'BEL', 'BIH', 'BGR', 'HRV', 'CZE', 'DNK', 'EST', 'FRO', 'FIN', 'FRA', 'DEU', 'GIB', 'GRC', 'GGY', 'VAT', 'HUN', 'ISL', 'IRL', 'IMN', 'ITA', 'JEY', 'LVA', 'LIE', 'LTU', 'LUX', 'MLT', 'MCO', 'MNE', 'NLD', 'MKD', 'NOR', 'POL', 'PRT', 'MDA', 'ROU', 'RUS', 'SMR', 'SRB', 'SVK', 'SVN', 'ESP', 'SJM', 'SWE', 'CHE', 'UKR', 'GBR', 'ALA']
ASIA = ['AFG', 'ARM', 'AZE', 'BHR', 'BGD', 'BTN', 'BRN', 'KHM', 'CHN', 'HKG', 'MAC', 'CYP', 'PRK', 'GEO', 'IND', 'IDN', 'IRN', 'IRQ', 'ISR', 'JPN', 'JOR', 'KAZ', 'KWT', 'KGZ', 'LAO', 'LBN', 'MYS', 'MDV', 'MNG', 'MMR', 'NPL', 'OMN', 'PAK', 'PHL', 'QAT', 'KOR', 'SAU', 'SGP', 'LKA', 'PSE', 'SYR', 'TJK', 'THA', 'TLS', 'TKM', 'TUR', 'ARE', 'UZB', 'VNM', 'YEM']
AFRICA = ['DZA', 'AGO', 'BEN', 'BWA', 'IOT', 'BFA', 'BDI', 'CPV', 'CMR', 'CAF', 'TCD', 'COM', 'COG', 'CIV', 'COD', 'DJI', 'EGY', 'GNQ', 'ERI', 'SWZ', 'ETH', 'ATF', 'GAB', 'GMB', 'GHA', 'GIN', 'GNB', 'KEN', 'LSO', 'LBR', 'LBY', 'MDG', 'MWI', 'MLI', 'MRT', 'MUS', 'MYT', 'MAR', 'MOZ', 'NAM', 'NER', 'NGA', 'RWA', 'REU', 'SHN', 'STP', 'SEN', 'SYC', 'SLE', 'SOM', 'ZAF', 'SSD', 'SDN', 'TGO', 'TUN', 'UGA', 'TZA', 'ESH', 'ZMB', 'ZWE']
AMERICAS = ['AIA', 'ATG', 'ARG', 'ABW', 'BHS', 'BRB', 'BLZ', 'BMU', 'BOL', 'BES', 'BVT', 'BRA', 'VGB', 'CAN', 'CYM', 'CHL', 'COL', 'CRI', 'CUB', 'CUW', 'DMA', 'DOM', 'ECU', 'SLV', 'FLK', 'GUF', 'GRL', 'GRD', 'GLP', 'GTM', 'GUY', 'HTI', 'HND', 'JAM', 'MTQ', 'MEX', 'MSR', 'NIC', 'PAN', 'PRY', 'PER', 'PRI', 'BLM', 'KNA', 'LCA', 'MAF', 'SPM', 'VCT', 'SXM', 'SGS', 'SUR', 'TTO', 'TCA', 'USA', 'VIR', 'URY', 'VEN']


def loadData():
    cols_to_use = ['Iso3_code', 'Country', 'Region', 'Category', 'Year', 'Unit of measurement', 'VALUE']
    crimeDf = pd.read_csv("EconomyCrime.csv", delimiter=';', usecols=cols_to_use)
    geoDf = gpd.read_file(SHAPEFILE, include_fields=['ADMIN', 'ADM0_A3', 'geometry'])
    geoDf.columns = ['country', 'country_code', 'geometry']
    geoDf = geoDf.drop(geoDf.loc[geoDf['country'] == 'Antarctica'].index)
    
    return crimeDf, geoDf

def mergeData(crimeDf, geoDf):
    mergedDf = pd.merge(left=geoDf, right=crimeDf, how='left', left_on='country_code', right_on='Iso3_code')
    mergedDf['VALUE'] = mergedDf['VALUE'].fillna(0)
    mergedDf = mergedDf.drop(['Iso3_code', 'Country'], axis=1)
    
    return mergedDf

def chosenData(heatDf, geoDf, year, crime, region, measure):
    match = {'Europe': EUROPE, 'Asia': ASIA, 'Africa': AFRICA, 'Americas': AMERICAS}
    blankMap = geoDf[['country_code', 'geometry']]
    if(region != 'All'):
        chosenDf = heatDf[heatDf['Region'] == region]
        blankMap = blankMap[blankMap['country_code'].isin(match[region])]
    else: chosenDf = heatDf
    chosenDf = chosenDf[(chosenDf['Year'] == year) & (chosenDf['Category'] == crime) & (chosenDf['Unit of measurement'] == measure)]
    if measure == 'Rate per 100,000 population':
        chosenDf['VALUE'] = chosenDf['VALUE'].str.replace(",", ".")
    return chosenDf, blankMap


def plotHeatmap(finalDf, blankMap, title):
    col = 'VALUE'
    vmin = finalDf[col].min()
    vmax = finalDf[col].max()
    cmap = 'summer'
    
    # Create figure and axes for Matplotlib
    fig, ax = plt.subplots(1, figsize=(20, 8))
    # Create map
    blankMap.plot(ax=ax, color='white', edgecolor='darkgrey')
   
    # Remove the axis
    ax.axis('off')
    plot = finalDf.plot(column=col, ax=ax, edgecolor='0.8', linewidth=1, cmap=cmap)
    # Add a title
    ax.set_title(title, fontdict={'fontsize': '25', 'fontweight': '3'})
    # Create colorbar as a legend
    sm = plt.cm.ScalarMappable(norm=plt.Normalize(vmin=vmin, vmax=vmax), cmap=cmap)
    # Empty array for the data range
    sm._A = []
    # Add the colorbar to the figure
    cbaxes = fig.add_axes([0.15, 0.25, 0.01, 0.4])
    cbar = fig.colorbar(sm, cax=cbaxes)
    del finalDf, blankMap
    return plot.get_figure()



def dataBasedCrimeHeatmap(year, crime, region, measure):
    # Load data
    crimeDf, geoDf = loadData()
    
    # Merge data
    crimeDf = mergeData(crimeDf, geoDf)
    
    # Choose data based on criteria
    crimeDf, geoDf = chosenData(crimeDf, geoDf, year, crime, region, measure)
    if(crimeDf.empty):
        raise Exception("No data found for this combination of criteria.") 
    # Set title
    title = f"{crime} in {year} in {'the world' if region == 'All' else region} ({measure})"
    
    # Plot and return heatmap
    heatmap = plotHeatmap(crimeDf, geoDf, title)
    heatmap.savefig("heatmap.jpeg", bbox_inches='tight', dpi=300)


if __name__ == '__main__':
    dataBasedCrimeHeatmap(2010, 'Burglary', 'All', 'Rate per 100,000 population')