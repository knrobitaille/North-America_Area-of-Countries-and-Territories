import requests
from bs4 import BeautifulSoup
import pandas as pd

# Webscrape wikipedia table
url = 'https://en.wikipedia.org/wiki/List_of_North_American_countries_by_area'
response = requests.get(url)
soup = BeautifulSoup(response.text,'html.parser')
# print(soup.prettify())
tables = soup.find_all('table',{'class':'wikitable sortable'})

# Create dataframe for countries
df_con = pd.read_html(str(tables))[0]
df_con = df_con[df_con['Rank'].notna()]
df_con = df_con.rename(columns={"Country[2][3]": "Name","Rank":"Country Rank"})
df_con['Country/Territory'] = 'Country'
df_con["Area (km²)"] = df_con["Area (km²)"]/1000000
df_con = df_con.drop(columns=['Notes'])
# print(df_con.head())

# Create dataframe for territories
df_ter = pd.read_html(str(tables))[1]
df_ter = df_ter.rename(columns={"Territory": "Name","Rank":"Territory Rank"})
df_ter['Country/Territory'] = 'Territory'
df_ter['Territory of'] = df_ter['Name'].str.extract('.*\((.*)\).*')
df_ter['Name'] = df_ter['Name'].str.replace(r"\(.*\)","")
df_ter["Area (km²)"] = df_ter["Area (km²)"]/1000000
df_ter = df_ter.drop(columns=['Notes'])
# print(df_ter.head())

# Create combined dataframe
df = pd.concat([df_con,df_ter])
df = df[["Country Rank","Territory Rank","Name","Area (km²)","Country/Territory",'Territory of']]
df = df.sort_values(by=['Area (km²)'],ascending=False)
# print(df.head())
# print(df.describe())




# Graphing
import matplotlib.pyplot as plt

# Separate graph for countries and territories
def sbs_graphs():
    # print(plt.style.available)
    # plt.style.use("ggplot")
    
    names_con = df_con['Name']
    values_con = df_con['Area (km²)']
    names_ter = df_ter['Name']
    values_ter = df_ter['Area (km²)']
    
    # fig = plt.figure(figsize=(15, 5))
    fig = plt.figure()
    fig.suptitle('North America\n',fontsize = 16)
    ax1 = fig.add_subplot(1,2,1)
    ax2 = fig.add_subplot(1,2,2)
    plt.draw()
    
    ax1.bar(names_con, values_con,label="Country",color="blue")
    ax1.set_title('Countries',fontsize=13)
    # ax1.legend()
    # ax1.set_xlabel("Name")
    ax1.set_xticklabels(names_con,rotation=90)
    ax1.set_ylabel("Area (millions of km²)")
    ax1.set_yscale('log')
    
    ax2.bar(names_ter, values_ter,label="Territory",color="orange")
    ax2.set_title('Territories',fontsize=13)
    # ax2.legend()
    # ax2.set_xlabel("Name")
    ax2.set_xticklabels(names_ter,rotation=90)
    ax2.set_ylabel("Area (millions of km²)")
    ax2.set_yscale('log')
    plt.tight_layout()
    plt.savefig('sbs_plots.png')

# Method 1: Combined graph for countries and territories
def comb2_graphs():
    # print(plt.style.available)
    # plt.style.use("ggplot")
    
    names_con = df_con['Name']
    values_con = df_con['Area (km²)']
    names_ter = df_ter['Name']
    values_ter = df_ter['Area (km²)']
    
    plt.figure(figsize=(10, 6))

    plt.bar(names_con, values_con,label="Country",color="blue")
    plt.bar(names_ter, values_ter,label="Territory",color="orange")
    plt.legend()
    # plt.xlabel("Name")
    plt.xticks(rotation=90)
    plt.ylabel("Area (millions of km²)")
    plt.yscale('log',basey=10)
    plt.tight_layout()
    plt.title("North America")

    plt.savefig('comb2_plot.png')

# Method 2: Combined graph for countries and territories
def comb1_graphs():
    # print(plt.style.available)
    # plt.style.use("ggplot")
    
    names = df['Name']
    values = df['Area (km²)']
    con_col = 'blue'
    ter_col = 'orange'
    colors = [con_col if region == 'Country' else ter_col for region in df['Country/Territory']]
    labels = ['Country' if region == 'Country' else 'Territory' for region in df['Country/Territory']]

    plt.figure(figsize=(10, 6))

    plt.bar(names,values,color=colors)
    
    plt.legend(labels=("Country","Territory"))
    
    # plt.xlabel("Name")
    plt.xticks(rotation=90)
    plt.ylabel("Area (millions of km²)")
    plt.yscale('log',basey=10)
    plt.tight_layout()
    plt.title("North America")

    plt.savefig('comb1_plot.png')
    
def pie_chart():
    # print(plt.style.available)
    # plt.style.use("ggplot")
    
    top = 5
    df_pie = df[:top].copy()
    new_row = pd.DataFrame(data = {'Name':['Others'],'Area (km²)':[df['Area (km²)'][top:].sum()]})
    df_pie = pd.concat([df_pie, new_row])
    
    names = df_pie['Name']
    values = df_pie['Area (km²)']

    plt.figure(figsize=(10, 6))

    plt.pie(values,labels=names)

    plt.tight_layout()
    plt.title("North America - Area (millions of km²)")

    plt.savefig('pie_chart.png')
    
    
### Call Graph Functions ###
# sbs_graphs()
# comb2_graphs()
comb1_graphs()
# pie_chart()