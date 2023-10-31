# -----------------------------
### FETCHING ACLED DATA
# -----------------------------
import pandas as pd
from scipy.spatial import cKDTree
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import requests
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from io import StringIO
from pathlib import Path
import json
import arcpy
from arcpy.sa import *
import time
from sklearn.model_selection import train_test_split, GridSearchCV, KFold
from sklearn.neighbors import KernelDensity
import warnings
import os
import shutil
import datetime
import tkinter as tk
from tkinter import ttk


country_iso3_list = [
    ["Afghanistan", "AFG"], ["Albania", "ALB"], ["Algeria", "DZA"],
    ["Andorra", "AND"], ["Angola", "AGO"], ["Anguilla", "AIA"], ["Antigua and Barbuda", "ATG"],
    ["Argentina", "ARG"], ["Armenia", "ARM"], ["Australia", "AUS"], ["Austria", "AUT"], ["Azerbaijan", "AZE"],
    ["Bahamas", "BHS"], ["Bahrain", "BHR"], ["Bangladesh", "BGD"], ["Barbados", "BRB"], ["Belarus", "BLR"], ["Belgium", "BEL"],
    ["Belize", "BLZ"], ["Benin", "BEN"], ["Bhutan", "BTN"], ["Bolivia (Plurinational State of)", "BOL"],
    ["Bosnia and Herzegovina", "BIH"], ["Botswana", "BWA"], ["Brazil", "BRA"], ["Brunei Darussalam", "BRN"],
    ["Bulgaria", "BGR"], ["Burkina Faso", "BFA"], ["Burundi", "BDI"], ["Cabo Verde", "CPV"], ["Cambodia", "KHM"],
    ["Cameroon", "CMR"], ["Canada", "CAN"], ["Central African Republic", "CAF"], ["Chad", "TCD"],
    ["Chile", "CHL"], ["China", "CHN"], ["Colombia", "COL"], ["Comoros", "COM"], ["Congo", "COG"], ["Costa Rica", "CRI"],
    ["Côte d’Ivoire", "CIV"], ["Croatia", "HRV"], ["Cuba", "CUB"], ["Cyprus", "CYP"], ["Czechia", "CZE"],
    ["Democratic People's Republic of Korea", "PRK"], ["Democratic Republic of the Congo", "COD"], ["Denmark", "DNK"],
    ["Djibouti", "DJI"], ["Dominica", "DMA"], ["Dominican Republic", "DOM"], ["Ecuador", "ECU"], ["Egypt", "EGY"],
    ["El Salvador", "SLV"], ["Equatorial Guinea", "GNQ"], ["Eritrea", "ERI"], ["Estonia", "EST"], ["Eswatini", "SWZ"],
    ["Ethiopia", "ETH"], ["Fiji", "FJI"], ["Finland", "FIN"], ["France", "FRA"],
    ["Gabon", "GAB"], ["Gambia", "GMB"], ["Georgia", "GEO"], ["Germany", "DEU"], ["Ghana", "GHA"],
    ["Greece", "GRC"], ["Grenada", "GRD"], ["Guatemala", "GTM"],
    ["Guinea", "GIN"], ["Guinea-Bissau", "GNB"], ["Guyana", "GUY"], ["Haiti", "HTI"],
    ["Holy See", "VAT"], ["Honduras", "HND"], ["Hungary", "HUN"], ["Iceland", "ISL"],
    ["India", "IND"], ["Indonesia", "IDN"], ["Iran (Islamic Republic of)", "IRN"], ["Iraq", "IRQ"], ["Ireland", "IRL"],
    ["Israel", "ISR"], ["Italy", "ITA"], ["Jamaica", "JAM"], ["Japan", "JPN"],
    ["Jordan", "JOR"], ["Kazakhstan", "KAZ"], ["Kenya", "KEN"], ["Kiribati", "KIR"], ["Kuwait", "KWT"], ["Kyrgyzstan", "KGZ"],
    ["Lao People's Democratic Republic", "LAO"], ["Latvia", "LVA"], ["Lebanon", "LBN"], ["Lesotho", "LSO"], ["Liberia", "LBR"],
    ["Libya", "LBY"], ["Liechtenstein", "LIE"], ["Lithuania", "LTU"], ["Luxembourg", "LUX"], ["Madagascar", "MDG"],
    ["Malawi", "MWI"], ["Malaysia", "MYS"], ["Maldives", "MDV"], ["Mali", "MLI"], ["Malta", "MLT"], ["Marshall Islands", "MHL"],
    ["Martinique", "MTQ"], ["Mauritania", "MRT"], ["Mauritius", "MUS"], ["Mexico", "MEX"],
    ["Micronesia (Federated States of)", "FSM"], ["Monaco", "MCO"], ["Mongolia", "MNG"], ["Montenegro", "MNE"],
    ["Morocco", "MAR"], ["Mozambique", "MOZ"], ["Myanmar", "MMR"], ["Namibia", "NAM"], ["Nauru", "NRU"], ["Nepal", "NPL"],
    ["Netherlands", "NLD"], ["New Zealand", "NZL"], ["Nicaragua", "NIC"],
    ["Niger", "NER"], ["Nigeria", "NGA"], ["North Macedonia", "MKD"],
    ["Norway", "NOR"], ["Oman", "OMN"], ["Pakistan", "PAK"], ["Palau", "PLW"],
    ["Panama", "PAN"], ["Papua New Guinea", "PNG"], ["Paraguay", "PRY"], ["Peru", "PER"], ["Philippines", "PHL"],
    ["Poland", "POL"], ["Portugal", "PRT"], ["Qatar", "QAT"],
    ["Republic of Korea", "KOR"], ["Republic of Moldova", "MDA"], ["Romania", "ROU"], ["Russian Federation", "RUS"], ["Rwanda", "RWA"],
    ["Saint Kitts and Nevis", "KNA"], ["Saint Lucia", "LCA"], ["Saint Vincent and the Grenadines", "VCT"], ["Samoa", "WSM"],
    ["San Marino", "SMR"], ["Sao Tome and Principe", "STP"], ["Saudi Arabia", "SAU"], ["Senegal", "SEN"],
    ["Serbia", "SRB"], ["Seychelles", "SYC"], ["Sierra Leone", "SLE"], ["Singapore", "SGP"],
    ["Slovakia", "SVK"], ["Slovenia", "SVN"], ["Solomon Islands", "SLB"], ["Somalia", "SOM"], ["South Africa", "ZAF"],
    ["South Sudan", "SSD"], ["Spain", "ESP"], ["Sri Lanka", "LKA"], ["State of Palestine", "PSE"], ["Sudan", "SDN"], ["Suriname", "SUR"],
    ["Sweden", "SWE"], ["Switzerland", "CHE"], ["Syrian Arab Republic", "SYR"], ["Tajikistan", "TJK"],
    ["Thailand", "THA"], ["Timor-Leste", "TLS"], ["Togo", "TGO"], ["Tonga", "TON"],
    ["Trinidad and Tobago", "TTO"], ["Tunisia", "TUN"], ["Türkiye", "TUR"], ["Turkmenistan", "TKM"],
    ["Tuvalu", "TUV"], ["Uganda", "UGA"], ["Ukraine", "UKR"],
    ["United Arab Emirates", "ARE"], ["United Kingdom of Great Britain and Northern Ireland", "GBR"],
    ["United Republic of Tanzania", "TZA"], ["United States of America", "USA"], ["Uruguay", "URY"],
    ["Uzbekistan", "UZB"], ["Vanuatu", "VUT"], ["Venezuela (Bolivarian Republic of)", "VEN"], ["Viet Nam", "VNM"],
    ["Western Sahara", "ESH"], ["Yemen", "YEM"], ["Zambia", "ZMB"], ["Zimbabwe", "ZWE"]
]


# Initialize the country and iso3 variables
country = ""
iso3 = ""

def on_country_select(event):
    global country, iso3
    country = country_combobox.get()
    for country_name, iso3_code in country_iso3_list:
        if country_name == country:
            iso3 = iso3_code
            iso3_label.config(text=f"ISO3 Code: {iso3}")
            break

# Create the main application window
root = tk.Tk()
root.title("Country Selector")

# Create a label
label = tk.Label(root, text="Select a country:")
label.pack(pady=10)

# Create a dropdown menu (Combobox)
country_combobox = ttk.Combobox(root, values=[country_name for country_name, _ in country_iso3_list])
country_combobox.pack()

# Create a label to display the ISO3 code
iso3_label = tk.Label(root, text="")
iso3_label.pack(pady=10)

# Bind the event handler for the Combobox
country_combobox.bind("<<ComboboxSelected>>", on_country_select)

# Function to continue with the rest of your script
def continue_script():
    print(f"Selected Country: {country}")
    print(f"ISO3 Code: {iso3}")
    # You can continue with your script here using the 'country' and 'iso3' variables

# Create a button to continue with the rest of the script
continue_button = tk.Button(root, text="Continue", command=continue_script)
continue_button.pack()

# Start the Tkinter main loop
root.mainloop()

# Code after the GUI window is closed or the "Continue" button is pressed
print("The GUI window is closed or the 'Continue' button is pressed. Continue with the rest of your script here.")


# Suppress SettingWithCopyWarning
warnings.filterwarnings("ignore", category=pd.core.common.SettingWithCopyWarning)

# ACLED API endpoint
ACLED_API_URL = "https://api.acleddata.com/acled/read?key=c30A*ffif2ei9Fy-HzdB&email=moses.cheboi@un.org.csv"

# Prompt for user input
access_key = "c30A*ffif2ei9Fy-HzdB"
email = "moses.cheboi@un.org"

# Fetch the current dataset
current_date = datetime.datetime.now()
months = int(input("Enter number of months (3, 6, 12, 24): "))

# Calculate the start and end dates for the current dataset
end_date_current = current_date
start_date_current = end_date_current - relativedelta(months=months)

# Fetch data for the current dataset
params_current = {
    "api_key": access_key,
    "email": email,
    "country": country,
    "event_date": f"{start_date_current.strftime('%Y-%m-%d')}|{end_date_current.strftime('%Y-%m-%d')}",
    "event_date_where": "BETWEEN",
    "format": "json",  # Change this to "csv" if you want to fetch CSV data
}
response_current = requests.get(ACLED_API_URL, params=params_current)

# Read the JSON response into a DataFrame for the current dataset
response_current = response_current.json()
if "data" in response_current:
    data_current = response_current['data']
    df = pd.DataFrame(data_current)  # Create a Pandas DataFrame for the current dataset
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    df['event_date'] = pd.to_datetime(df['event_date'])
    df = df.dropna(axis=1, how='all')  # Remove columns with all NaN (blank) rows

    # Remove specific columns
    columns_to_remove = [
        'time_precision', 'assoc_actor_1', 'inter1', 'assoc_actor_2', 'inter2',
        'civilian_targeting', 'source', 'source_scale', 'notes', 'tags', 'timestamp'
    ]
    df = df.drop(columns=columns_to_remove)
else:
    print("Error: Unable to retrieve current ACLED data.")
# Define the time range for the previous dataset
end_date_previous = start_date_current - timedelta(days=1)
start_date_previous = end_date_previous - relativedelta(months=months)

# Fetch data for the previous dataset
params_previous = {
    "api_key": access_key,
    "email": email,
    "country": country,
    "event_date": f"{start_date_previous.strftime('%Y-%m-%d')}|{end_date_previous.strftime('%Y-%m-%d')}",
    "event_date_where": "BETWEEN",
    "format": "json",  # Change this to "csv" if you want to fetch CSV data
}
response_previous = requests.get(ACLED_API_URL, params=params_previous)
response_data_previous = response_previous.json()

if "data" in response_data_previous:
    data_previous = response_data_previous['data']
    df_previous = pd.DataFrame(data_previous)  # Create a Pandas DataFrame for the previous dataset
    df_previous = df_previous.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    df_previous['event_date'] = pd.to_datetime(df_previous['event_date'])
    df_previous = df_previous.dropna(axis=1, how='all')  # Remove columns with all NaN (blank) rows

    # Remove specific columns
    columns_to_remove_previous = [
        'time_precision', 'assoc_actor_1', 'inter1', 'assoc_actor_2', 'inter2',
        'civilian_targeting', 'source', 'source_scale', 'notes', 'tags', 'timestamp'
    ]
    df_previous = df_previous.drop(columns=columns_to_remove_previous)
else:
    print("Error: Unable to retrieve previous ACLED data.")
print("Fetching data from ACLED completed")
df.head()
# -----------------------------
### DATA VISUALIZATIONS###
# -----------------------------
# Define the PDF output path and filename
pdf_output_path = os.path.join("PDF", "Conflict_pdfs")
pdf_filename = f"{country}_Conflict_Analysis.pdf"
pdf_full_path = os.path.join(pdf_output_path, pdf_filename)

# Create the output directory if it doesn't exist
os.makedirs(pdf_output_path, exist_ok=True)

# Create a PDF document
pdf_pages = PdfPages(pdf_full_path)

# Rest of your code remains unchanged...


def plot_events_per_admin(df):
    events_per_admin1 = df.groupby('admin1')['event_id_cnty'].count()

    plt.figure(figsize=(10, 6))
    events_per_admin1.plot(kind='bar')
    plt.xlabel('admin1')
    plt.ylabel('Events ID Count')
    plt.title('Number of Events per admin')
    plt.xticks(rotation=45, ha='right')

    for i, count in enumerate(events_per_admin1):
        plt.text(i, count + 10, str(count), ha='center', va='bottom')

    plt.tight_layout()

    # Save the plot into the PDF document
    pdf_pages.savefig()
    plt.close()  # Close the plot to free up resources

    print("Plotting events per admin successful")

def plot_event_type_percentages(df):
    events_per_event_type = df.groupby('event_type')['event_id_cnty'].count()
    total_events = events_per_event_type.sum()
    event_type_percentages = (events_per_event_type / total_events) * 100

    plt.figure(figsize=(10, 6))
    event_type_percentages.plot(kind='bar')
    plt.xlabel('Event Type')
    plt.ylabel('Percentage Share')
    plt.title('Percentage Share of Events per Event Type')
    plt.xticks(rotation=45, ha='right')

    for i, percentage in enumerate(event_type_percentages):
        plt.text(i, percentage + 1, f"{percentage:.2f}%", ha='center', va='bottom')

    plt.tight_layout()

    # Save the plot into the PDF document
    pdf_pages.savefig()
    plt.close()  # Close the plot to free up resources

    print("Plotting event types percentages successful")

def create_grouped_bar_chart(df, n, n_actor2):
    df = df[(df['actor1'] != '') & (df['actor2'] != '')]
    events_per_actor1_actor2 = df.groupby(['actor1', 'actor2'])['event_id_cnty'].count().unstack()

    top_n_categories = events_per_actor1_actor2.sum().nlargest(n).index
    df_top_n = df[df['actor1'].isin(top_n_categories)]
    events_per_actor1_actor2_top_n = df_top_n.groupby(['actor1', 'actor2'])['event_id_cnty'].count().unstack()

    top_n_actor2 = events_per_actor1_actor2_top_n.sum().nlargest(n_actor2).index
    events_per_actor1_actor2_top_n = events_per_actor1_actor2_top_n[top_n_actor2]

    percentage_per_actor2 = (events_per_actor1_actor2_top_n / events_per_actor1_actor2_top_n.sum()) * 100

    fig, ax = plt.subplots(figsize=(10, 6))
    events_per_actor1_actor2_top_n.plot(kind='bar', stacked=True, ax=ax)

    ax.set_xlabel('actor1 Category')
    ax.set_ylabel('Percentage')
    ax.set_title(f'Percentage of Events per Top {n_actor2} Actor2 Categories within Top {n} actor1 Categories')
    ax.set_xticks(np.arange(len(top_n_categories)))
    ax.set_xticklabels(top_n_categories, rotation=30, ha='right')
    plt.tight_layout()

    # Save the plot into the PDF document
    pdf_pages.savefig()
    plt.close()  # Close the plot to free up resources

    print("Plotting actor1 vs actor2 successful")

def plot_event_type_comparison(df_current, df_previous):
    events_per_event_type_current = df_current.groupby('event_type')['event_id_cnty'].count()
    events_per_event_type_previous = df_previous.groupby('event_type')['event_id_cnty'].count()

    event_types = np.union1d(events_per_event_type_current.index, events_per_event_type_previous.index)
    index = np.arange(len(event_types))

    bar_width = 0.35
    fig, ax = plt.subplots(figsize=(10, 6))

    bar1 = ax.bar(index, events_per_event_type_previous.reindex(event_types, fill_value=0), bar_width, label='Previous Period')
    bar2 = ax.bar(index + bar_width, events_per_event_type_current.reindex(event_types, fill_value=0), bar_width, label='Current Period')

    ax.set_xlabel('event_type')
    ax.set_ylabel('Events ID Count')
    ax.set_title('Number of Events per event_type Comparison')
    ax.set_xticks(index + bar_width / 2)
    ax.set_xticklabels(event_types, rotation=45, ha="right")
    ax.legend()

    percentage_change = ((events_per_event_type_current - events_per_event_type_previous) / events_per_event_type_previous) * 100

    for i, event_type in enumerate(event_types):
        prev_count = events_per_event_type_previous[event_type] if event_type in events_per_event_type_previous else 0
        curr_count = events_per_event_type_current[event_type] if event_type in events_per_event_type_current else 0

        plt.text(index[i] + bar_width, curr_count + 5, f"{percentage_change.get(event_type, 0):.2f}%", ha='center', va='bottom')

    plt.tight_layout()

    # Save the plot into the PDF document
    pdf_pages.savefig()
    plt.close()  # Close the plot to free up resources

    print("Plotting event type comparison")

if __name__ == "__main__":
    # Assuming you have df (current dataframe) and df_previous dataframes available

    # Call the encapsulated functions with the dataframes
    plot_events_per_admin(df)
    plot_event_type_percentages(df)
    create_grouped_bar_chart(df, n=3, n_actor2=3)
    plot_event_type_comparison(df, df_previous)

    # Close the PDF document
    pdf_pages.close()

    # Print a message indicating the PDF file has been saved
    print(f"PDF file saved as {pdf_full_path}")

# -----------------------------
### FILTERING ( VIOLENT & NON-VIOLENT)###
# -----------------------------
def filter_violence(df, non_violent_events):
    # Filter out non-violent events (include only specified non-violent events) for the dataset
    df_non_violent = df[df["sub_event_type"].isin(non_violent_events)]

    # Filter out violent events (exclude specified non-violent events) for the dataset
    df_violent = df[~df["sub_event_type"].isin(non_violent_events)]

    print("Filtering current violence and non-violence successful")

    return df_non_violent, df_violent

def filter_previous_violence(df_previous, non_violent_events):
    # Filter out non-violent events (include only specified non-violent events) for the previous dataset
    df_previous_non_violent = df_previous[df_previous["sub_event_type"].isin(non_violent_events)]

    # Filter out violent events (exclude specified non-violent events) for the previous dataset
    df_previous_violent = df_previous[~df_previous["sub_event_type"].isin(non_violent_events)]

    print("Filtering previous violence and non-violence successful")

    return df_previous_non_violent, df_previous_violent

if __name__ == "__main__":
    non_violent_events = ["Peaceful protest", "Protest with intervention"]

    # Filter violence events for the current dataset
    df_non_violent, df_violent = filter_violence(df, non_violent_events)

    # Filter violence events for the previous dataset
    df_previous_non_violent, df_previous_violent = filter_previous_violence(df_previous, non_violent_events)
# -----------------------------
### CONFLICT INTENSITY COMPUTATION###
# -----------------------------
# GEOMEAN CURRENT
# Clean latitude and longitude values
def clean_lat_long(value):
    try:
        return float(value)
    except ValueError:
        return None

# Define admin levels to check in order of preference
admin_levels = ['admin2','admin3', 'admin1']

# Assuming df_violent is your original DataFrame
# Create a copy of the DataFrame
df_violent_copy = df_violent.copy()

for selected_admin_level in admin_levels:
    if selected_admin_level in df_violent_copy.columns:
        # Clean latitude and longitude columns in the copy
        df_violent_copy['latitude'] = df_violent_copy['latitude'].apply(clean_lat_long)
        df_violent_copy['longitude'] = df_violent_copy['longitude'].apply(clean_lat_long)

        # Count the number of events and calculate the sum of fatalities per selected admin level
        events_and_fatalities_per_admin = df_violent_copy.groupby(selected_admin_level).agg(
            count_of_events=pd.NamedAgg(column='event_id_cnty', aggfunc='count'),
            sum_of_fatalities=pd.NamedAgg(column='fatalities', aggfunc='sum'),
            latitude=pd.NamedAgg(column='latitude', aggfunc=lambda x: np.mean(x)),
            longitude=pd.NamedAgg(column='longitude', aggfunc=lambda x: np.mean(x))
        )

        # Reset index and rename columns
        df_conflict_intensity = events_and_fatalities_per_admin.reset_index()
        df_conflict_intensity.rename(columns={selected_admin_level: 'Admin'}, inplace=True)

        # Calculate the sum of individual digits in the "Sum of Fatalities" column
        df_conflict_intensity['Sum of Fatalities'] = df_conflict_intensity['sum_of_fatalities'].astype(str).apply(lambda x: sum(int(digit) for digit in x))

        # Display only the desired columns
        df_display = df_conflict_intensity[['Admin', 'count_of_events', 'Sum of Fatalities', 'latitude', 'longitude']]

        # Check for blank rows in the "Admin" column
        if df_display['Admin'].str.strip().eq('').any():
            print(f"Admin name is empty for {selected_admin_level}. Trying next admin level.")
        else:
            # Add 0.1 to all values in the "count_of_events" and "Sum of Fatalities" columns
            df_modified = df_display.copy()
            df_modified['count_of_events'] += 0.1
            df_modified['Sum of Fatalities'] += 0.1

            # Calculate geometric mean
            df_modified['Geomean'] = np.sqrt(df_modified['count_of_events'] * df_modified['Sum of Fatalities'])
            # Print the modified DataFrame
            print("Geomean computed for current computed")

            # Exit the loop
            break
else:
    print("Unable to find a valid admin level with non-empty rows.")

# GEOMEAN PREVIOUS
# Clean latitude and longitude values
def clean_lat_long(value):
    try:
        return float(value)
    except ValueError:
        return None

# Create a copy of df_previous_violent
df_previous_violent_copy = df_previous_violent.copy()

# Assuming selected_admin_level_current is determined in the geomean_current part
# selected_admin_level = selected_admin_level_current  # Use the same admin level selected for geomean_current

if selected_admin_level in df_previous_violent_copy.columns:
    # Clean latitude and longitude columns
    df_previous_violent_copy['latitude'] = df_previous_violent_copy['latitude'].apply(clean_lat_long)
    df_previous_violent_copy['longitude'] = df_previous_violent_copy['longitude'].apply(clean_lat_long)

    # Count the number of events and calculate the sum of fatalities per selected admin level
    events_and_fatalities_per_admin = df_previous_violent_copy.groupby(selected_admin_level).agg(
        count_of_events=pd.NamedAgg(column='event_id_cnty', aggfunc='count'),
        sum_of_fatalities=pd.NamedAgg(column='fatalities', aggfunc='sum'),
        latitude=pd.NamedAgg(column='latitude', aggfunc=lambda x: np.mean(x)),
        longitude=pd.NamedAgg(column='longitude', aggfunc=lambda x: np.mean(x))
    )

    # Reset index and rename columns
    df_conflict_intensity = events_and_fatalities_per_admin.reset_index()
    df_conflict_intensity.rename(columns={selected_admin_level: 'Admin'}, inplace=True)

    # Calculate the sum of individual digits in the "Sum of Fatalities" column
    df_conflict_intensity['Sum of Fatalities'] = df_conflict_intensity['sum_of_fatalities'].astype(str).apply(
        lambda x: sum(int(digit) for digit in x))

    # Drop rows with empty 'Admin' values
    df_conflict_intensity.dropna(subset=['Admin'], inplace=True)

    # Display only the desired columns
    df_display = df_conflict_intensity[['Admin', 'count_of_events', 'Sum of Fatalities', 'latitude', 'longitude']]

    # Add 0.01 to all values in the "count_of_events" and "Sum of Fatalities" columns
    df_modified_previous = df_display.copy()
    df_modified_previous['count_of_events'] += 0.1
    df_modified_previous['Sum of Fatalities'] += 0.1

    # Calculate geometric mean
    df_modified_previous['Geomean'] = np.sqrt(df_modified_previous['count_of_events'] * df_modified_previous['Sum of Fatalities'])

    # Print the modified DataFrame
    print("Geomean computed for previous period:")
else:
    print(f"Selected admin level {selected_admin_level} not present in df_previous_violent_copy.")

# Create the df_geomean_change dataframe
df_geomean_change = pd.DataFrame()

# Copy columns from df_modified
df_geomean_change['Admin'] = df_modified['Admin']
df_geomean_change['Geomean current'] = df_modified['Geomean']
df_geomean_change['latitude'] = df_modified['latitude']
df_geomean_change['longitude'] = df_modified['longitude']

# Add columns from df_modified_previous
df_geomean_change['Geomean previous'] = df_modified_previous['Geomean']

# Fill missing values with 0.1 in 'Geomean current' and 'Geomean previous' columns
if 'Geomean current' in df_geomean_change.columns:
    df_geomean_change['Geomean current'].fillna(0.1, inplace=True)
if 'Geomean previous' in df_geomean_change.columns:
    df_geomean_change['Geomean previous'].fillna(0.1, inplace=True)

# Calculate percentage change
df_geomean_change['Percentage Change'] = ((df_geomean_change['Geomean current'] - df_geomean_change['Geomean previous']) / df_geomean_change['Geomean previous']) * 100

# Create 'Trend' column based on percentage change
df_geomean_change['Trend'] = df_geomean_change['Percentage Change'].apply(
    lambda x: 'Increasing' if x > 0 else ('Decreasing' if x < 0 else 'Stalemate'))

# Create df_geomean_change_sorted dataframe
df_geomean_change_sorted = df_geomean_change.sort_values(by='Percentage Change', ascending=False)

# TOP n in both previous and current merged
# Define the value of n (top n entries)
n = 7

# Get the top n entries based on Geomean for current and previous periods
top_n_current = df_geomean_change_sorted.nlargest(n, 'Geomean current')
top_n_previous = df_geomean_change_sorted.nlargest(n, 'Geomean previous')

# Combine the admin names from both current and previous top n entries without duplicates
unique_admin_names = list(set(top_n_current['Admin']).union(set(top_n_previous['Admin'])))

# Filter rows from df_geomean_change_sorted based on the unique admin names
filtered_df = df_geomean_change_sorted[df_geomean_change_sorted['Admin'].isin(unique_admin_names)]

# Sort the percentage_change_df DataFrame by 'Percentage Change' column in descending order
percentage_change_df_sorted = filtered_df.sort_values(by='Percentage Change', ascending=False)
percentage_change_df_sorted
###NEW_CONFLICT_ZONES

# Assuming df_geomean_change is the original DataFrame
# Create df_new_conflict_zones by applying the filter condition
df_new_conflict_zones = df_geomean_change[(df_geomean_change['Geomean previous'].isna()) & (df_geomean_change['Geomean current'] > 0)]

# Reset the index of the new DataFrame
df_new_conflict_zones.reset_index(drop=True, inplace=True)
print("New conflict zones dataframe created")


##
# SPLITTING df_geomean_change_sorted FOR ENTIRE ADMIN COLUMN INTO INCREASING AND DECREASING TO GET COUNT

# Create a DataFrame for Decreasing trends
all_decreasing_df = df_geomean_change_sorted [df_geomean_change_sorted ['Trend'] == 'Decreasing']

# Create a DataFrame for Increasing trends
all_increasing_df = df_geomean_change_sorted [df_geomean_change_sorted ['Trend'] == 'Increasing']

# Compute count of values in decreasing_df
decreasing_count = all_decreasing_df.shape[0]

# Compute count of values in increasing_df
increasing_count = all_increasing_df.shape[0]

# SPLITTING percentage_change_df_sorted FOR Top_n ADMIN COLUMN INTO INCREASING AND DECREASING

increasing_df = percentage_change_df_sorted [percentage_change_df_sorted ['Trend'] == 'Increasing']

decreasing_df = percentage_change_df_sorted [percentage_change_df_sorted ['Trend'] == 'Decreasing']

# Check which DataFrame is dominant based on the counts
if increasing_count > decreasing_count:
    dominant_df = increasing_df
    non_dominant_df = decreasing_df
else:
    dominant_df = decreasing_df
    non_dominant_df = increasing_df

# Define the desired number of rows for the dominant and non-dominant DataFrames
dominant_desired_rows = 4
non_dominant_desired_rows = 2

# Trim the dominant DataFrame to the desired number of rows
dominant_df = dominant_df.nlargest(dominant_desired_rows, 'Percentage Change')

# Trim the non-dominant DataFrame to the desired number of rows
non_dominant_df = non_dominant_df.nlargest(non_dominant_desired_rows, 'Percentage Change')

# Create separate DataFrames for Increased and Decreased intensity
if increasing_count > decreasing_count:
    Increased_intensity_df = dominant_df
    Decreased_intensity_df = non_dominant_df
else:
    Decreased_intensity_df = dominant_df
    Increased_intensity_df = non_dominant_df

# Print the trimmed DataFrames
print("Conflict intensity DataFrames created")


# -----------------------------
### FEATURE CLASSES CREATION###
# -----------------------------
def create_and_insert_feature_class(feature_class_name, data_frame, event_type, required_fields, country_folder):
    try:
        # Set the workspace to the country_shapefiles_folder
        arcpy.env.workspace = country_folder
        default_gdb = arcpy.env.workspace
        # Create the feature class
        output_fc = arcpy.management.CreateFeatureclass(
            default_gdb,
            feature_class_name,
            "POINT",
            spatial_reference=arcpy.SpatialReference(4326)  # Assuming WGS 1984 coordinate system (EPSG:4326)
        )

        # Define a mapping between full column names and shorter field names within 10 characters
        field_mapping = {
            "Admin": "Admin",
            "Geomean Current": "GeoCurr",
            "Geomean Previous": "GeoPrev",
            "Percentage Change": "Percentage Change",
            "latitude": "Latitude",
            "longitude": "Longitude",
            "Trend(Decreasing)": "TrendDec",
            "Trend(Increasing)": "TrendInc",
            "event_id_cnty": "EventId",
            "admin3": "Admin3",
            "fatalities": "fatalities"
        }

        # Add required fields from the DataFrame to the feature class with maximum field length
        for field in required_fields:
            arcpy.management.AddField(output_fc, field_mapping[field], field_type='TEXT', field_length=10)

        # Open an insert cursor for the feature class
        with arcpy.da.InsertCursor(output_fc, ['SHAPE@XY'] + [field_mapping[field] for field in required_fields]) as cursor:
            # Iterate over events and insert points
            for _, row in data_frame.iterrows():
                point = arcpy.Point(row['longitude'], row['latitude'])
                row_values = [str(row[field_mapping[field]]) if field in row.index else None for field in required_fields]
                cursor.insertRow([(point.X, point.Y)] + row_values)

        print(f"Feature class '{feature_class_name}' for {event_type} events created successfully.")

        # Iterate through shapefiles in the workspace
        for shapefile in arcpy.ListFeatureClasses():
            # Create a layer file for the shapefile
            layer_file_path = os.path.join(country_folder, f"{os.path.splitext(shapefile)[0]}.lyr")
            arcpy.management.MakeFeatureLayer(shapefile, layer_file_path)

    except arcpy.ExecuteError as e:
        if "Output Layer: Dataset" in str(e) and "already exists" in str(e):
            print(f"Shapefile {feature_class_name}.shp already exists. Skipping...")
        else:
            print(f"Error encountered: {str(e)}")


def main():
    # List of required fields for the feature classes
    required_fields_decreased_intensity = ["Admin"]
    required_fields_increased_intensity = ["Admin"]
    required_fields_non_violent = []
    required_fields_violent = []
    required_fields_new_conflict_zones = ["Admin"]

    # Get the directory of the script
    script_directory = os.path.dirname(os.path.abspath(__file__))
    shapefiles_folder = os.path.join(script_directory, "SHAPEFILES")

    # Path to the subfolder for the specified country
    country_folder = os.path.join(shapefiles_folder, f"{country}_shapefiles")
    print(f"Shapefiles have been saved in this path: {country_folder}")

    # Delete everything in the country_folder if it exists
    if os.path.exists(country_folder):
        for item in os.listdir(country_folder):
            item_path = os.path.join(country_folder, item)
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
            else:
                os.remove(item_path)
    else:
        # Create the country_folder if it doesn't exist
        os.makedirs(country_folder)

    # Create and insert feature classes
    create_and_insert_feature_class("Decreased_intensity", Decreased_intensity_df, "decreased intensity", required_fields_decreased_intensity, country_folder)
    create_and_insert_feature_class("Increased_intensity", Increased_intensity_df, "increased intensity", required_fields_increased_intensity, country_folder)
    create_and_insert_feature_class("non_violent_events", df_non_violent, "non-violent", required_fields_non_violent, country_folder)
    create_and_insert_feature_class("violent_events", df_violent, "violent", required_fields_violent, country_folder)
    create_and_insert_feature_class("new_conflict_zones", df_new_conflict_zones, "new conflict zones", required_fields_new_conflict_zones, country_folder)


if __name__ == "__main__":
    main()

###CLUSTERING
# Clean latitude and longitude values
def clean_lat_long(value):
    try:
        return float(value)
    except ValueError:
        return None

# Convert 'fatalities' column to integer type
df['fatalities'] = df['fatalities'].astype(int)

# Assuming you have a DataFrame called 'df'
# Create a new DataFrame 'df_fatalities' with selected columns
selected_columns = ['latitude', 'longitude', 'fatalities']
df_fatalities = df[selected_columns].copy()

# Assuming you have already created 'df_fatalities' as shown in the previous response

# Delete rows with fatalities equal to zero
df_fatalities = df_fatalities[df_fatalities['fatalities'] != 0]


# Assuming you have a DataFrame called 'df' with columns 'latitude', 'longitude', and 'fatalities'

# Clean latitude and longitude columns
df['latitude'] = df['latitude'].apply(clean_lat_long)
df['longitude'] = df['longitude'].apply(clean_lat_long)

# Filter out invalid values
valid_df = df.dropna(subset=['latitude', 'longitude'])

# Calculate extent dimensions
min_latitude = valid_df['latitude'].min()
max_latitude = valid_df['latitude'].max()
min_longitude = valid_df['longitude'].min()
max_longitude = valid_df['longitude'].max()

width = max_longitude - min_longitude
length = max_latitude - min_latitude

# Choose the longer side
longer_side = max(width, length)

# Calculate the cluster radius
cluster_radius = longer_side / 8

print("Cluster Radius:", cluster_radius)

import pandas as pd
from scipy.spatial import cKDTree
import numpy as np

# Assuming you have a DataFrame named df_fatalities with columns "fatalities", "latitude", and "longitude"

# Set the cluster radius
cluster_radius = cluster_radius  # Adjust this value as needed

# Create a KD-Tree for efficient spatial clustering
points = df_fatalities[["latitude", "longitude"]].values
kdtree = cKDTree(points)

# Find clusters using the KD-Tree
clusters = kdtree.query_ball_tree(kdtree, cluster_radius)

# Create a list to store cluster information
cluster_data = []

# Iterate through clusters and calculate the sum of fatalities for each
for cluster_indices in clusters:
    cluster_points = points[cluster_indices]
    cluster_fatalities = df_fatalities.iloc[cluster_indices]["fatalities"].sum()
    cluster_latitude = np.mean(cluster_points[:, 0])
    cluster_longitude = np.mean(cluster_points[:, 1])

    cluster_data.append({
        "latitude": cluster_latitude,
        "longitude": cluster_longitude,
        "Sum of fatalities": cluster_fatalities
    })

# Create the df_clusters DataFrame from the cluster data
df_clusters = pd.DataFrame(cluster_data)

# Print the resulting DataFrame with cluster information
df_clusters
###FC CLUSTERING
import arcpy
import os
import pandas as pd

def create_and_insert_clustered_fatalities_feature_class(data_frame, country_folder):
    try:
        # Set the workspace to the country_shapefiles_folder
        arcpy.env.workspace = country_folder
        default_gdb = arcpy.env.workspace

        # Check if the feature class already exists
        output_fc = os.path.join(default_gdb, "Clustered_fatalities.shp")
        if arcpy.Exists(output_fc):
            # Delete the existing feature class
            arcpy.Delete_management(output_fc)

        # Create the feature class
        arcpy.management.CreateFeatureclass(
            default_gdb,
            "Clustered_fatalities",
            "POINT",
            spatial_reference=arcpy.SpatialReference(4326)  # Assuming WGS 1984 coordinate system (EPSG:4326)
        )

        # Define a mapping between full column names and shorter field names within 10 characters
        field_mapping = {
            "Sum of Fatalities": "SumFatal",
        }

        # Add the fields using the mapped short names
        for full_field_name, short_field_name in field_mapping.items():
            arcpy.management.AddField(output_fc, short_field_name, field_type='LONG')

        # Open an insert cursor for the feature class
        with arcpy.da.InsertCursor(output_fc, ['SHAPE@XY'] + list(field_mapping.values())) as cursor:
            # Iterate over cluster data and insert points
            for _, row in data_frame.iterrows():
                point = arcpy.Point(row['mean_long'], row['mean_lat'])
                sum_fatalities = int(
                    row['Sum of Fatalities']) if 'Sum of Fatalities' in row.index else 0  # Provide a default value of 0
                cursor.insertRow([(point.X, point.Y), sum_fatalities])

        print("Clustered_fatalities shapefile created successfully.")

    except arcpy.ExecuteError as e:
        print(f"Error encountered: {str(e)}")

def main():
    # Specify the absolute path to the folder where your shapefiles should be located

    script_directory = os.path.dirname(os.path.abspath(__file__))
    shapefiles_folder = os.path.join(script_directory, "SHAPEFILES")
    country_folder = os.path.join(shapefiles_folder, f"{country}_shapefiles")

    # Create and insert the "Clustered_fatalities" feature class
    create_and_insert_clustered_fatalities_feature_class(df_clusters, country_folder)

if __name__ == "__main__":
    main()


#----------------------------------------------------------
### COMPUTING SEARCH RADIUS(k-fold cross validation)###
#----------------------------------------------------------

# Shuffle the data based on event_date
df_violent = df_violent.sample(frac=1, random_state=42).reset_index(drop=True)
df_non_violent = df_non_violent.sample(frac=1, random_state=42).reset_index(drop=True)

# Split violent and non-violent data into training, validation, and test sets
violent_train, violent_test = train_test_split(df_violent, test_size=0.3, random_state=42)
violent_train, violent_val = train_test_split(violent_train, test_size=0.2, random_state=42)

non_violent_train, non_violent_test = train_test_split(df_non_violent, test_size=0.3, random_state=42)
non_violent_train, non_violent_val = train_test_split(non_violent_train, test_size=0.2, random_state=42)


# Function to calculate bandwidth using different methods
def calculate_bandwidths(data):
    data[['latitude', 'longitude']] = data[['latitude', 'longitude']].apply(pd.to_numeric)  # Convert to numeric
    IQR = data[['latitude', 'longitude']].apply(lambda x: np.percentile(x, 75) - np.percentile(x, 25))
    std_dev = data[['latitude', 'longitude']].apply(np.std)
    n = len(data)

    bandwidth_bowman = (IQR / 1.34).min() * (n ** (-1/5))
    bandwidth_sj = np.power(1.06 * std_dev * n ** (-0.2), 0.5).min()
    bandwidth_scott = np.power(n, -1 / 6) * np.min(std_dev)
    bandwidth_hansen = 1.5 * np.min(std_dev) * n ** (-0.2)

    return bandwidth_bowman, bandwidth_sj, bandwidth_scott, bandwidth_hansen


# Calculate bandwidths for violent events
bw_violent_bowman, bw_violent_sj, bw_violent_scott, bw_violent_hansen = calculate_bandwidths(violent_train)

# Calculate bandwidths for non-violent events
bw_non_violent_bowman, bw_non_violent_sj, bw_non_violent_scott, bw_non_violent_hansen = calculate_bandwidths(non_violent_train)

# Define a range of bandwidth values to search over for Cross-Validation
search_radii_violent = [bw_violent_bowman, bw_violent_sj, bw_violent_scott, bw_violent_hansen]
search_radii_non_violent = [bw_non_violent_bowman, bw_non_violent_sj, bw_non_violent_scott, bw_non_violent_hansen]

# Perform k-fold cross-validation to select the optimal bandwidth for violent events
kf = KFold(n_splits=5, shuffle=True, random_state=42)
grid_search_violent = GridSearchCV(KernelDensity(), {'bandwidth': search_radii_violent}, cv=kf)
grid_search_violent.fit(violent_train[['longitude', 'latitude']])
optimal_bandwidth_violent = grid_search_violent.best_params_['bandwidth']

# Perform k-fold cross-validation to select the optimal bandwidth for non-violent events
grid_search_non_violent = GridSearchCV(KernelDensity(), {'bandwidth': search_radii_non_violent}, cv=kf)
grid_search_non_violent.fit(non_violent_train[['longitude', 'latitude']])
optimal_bandwidth_non_violent = grid_search_non_violent.best_params_['bandwidth']

# Print the bandwidths and optimal bandwidths
print("Optimal Bandwidth for Violent Events:", optimal_bandwidth_violent)

print("Optimal Bandwidth for Non-Violent Events:", optimal_bandwidth_non_violent)

# Clean latitude and longitude columns
df['latitude'] = df['latitude'].apply(clean_lat_long)
df['longitude'] = df['longitude'].apply(clean_lat_long)

# Filter out invalid values
valid_df = df.dropna(subset=['latitude', 'longitude'])

# Calculate extent dimensions
min_lat = valid_df['latitude'].min()
max_lat = valid_df['latitude'].max()
min_lon = valid_df['longitude'].min()
max_lon = valid_df['longitude'].max()

# Calculate cell size
# Calculate cell size
extent_height = max_lat - min_lat
extent_width = max_lon - min_lon
cell_size = min(extent_height, extent_width) / 250
# Print the bandwidths and optimal bandwidths
print("Cell size:", cell_size)

# -----------------------------
### CREATING CONFLICT RASTERS###
# -----------------------------
# List feature classes in the default geodatabase

# Clean latitude and longitude values
def clean_lat_long(value):
    try:
        return float(value)
    except ValueError:
        return None

# Function to perform Kernel Density analysis
def perform_kernel_density_analysis(input_features,cell_size,search_radius):

    #measurement_units = "SQUARE_KILOMETERS"
    population_field = "NONE"
    area_units = "SQUARE_KILOMETERS"
    method = "PLANAR"  # Use "PLANAR" method for 2D analysis
    #barrier_layer = None
    out_cell_values = "DENSITIES"

    # Perform Kernel Density analysis with specified parameters
    output_raster = arcpy.sa.KernelDensity(input_features,population_field,cell_size,search_radius,area_units,out_cell_values,method)

    print(f"Kernel Density analysis completed. Output raster: {output_raster}")

    return output_raster



# Specify the output raster names
output_raster_violent = "kdensout_violent"
output_raster_non_violent = "kdensout_non_violent"


# Construct the full paths for the output rasters using the default geodatabase path
script_directory = os.path.dirname(os.path.abspath(__file__))
shapefiles_folder = os.path.join(script_directory, "SHAPEFILES")

aprx_path = r"APRX/Raw/{}.aprx".format(iso3)  # Replace with the actual path template
aprx = arcpy.mp.ArcGISProject(aprx_path)
country_folder = os.path.join(shapefiles_folder, f"{country}_shapefiles")

default_gdb_path = aprx.defaultGeodatabase

output_raster_violent_path = os.path.join(default_gdb_path, output_raster_violent)
output_raster_non_violent_path = os.path.join(default_gdb_path, output_raster_non_violent)

# Construct the full paths for the input feature shapefiles
violent_features = os.path.join(country_folder, "violent_events.shp")
non_violent_features = os.path.join(country_folder, "non_violent_events.shp")

# Access the first map in the project
aprx_path = r"APRX/Raw/{}.aprx".format(iso3)  # Replace with the actual path template
aprx = arcpy.mp.ArcGISProject(aprx_path)

map_obj = aprx.listMaps()[1]

# Find the index of the layer labeled "Sea/Ocean/Lake"
sea_ocean_lake_index = None
for i, layer in enumerate(map_obj.listLayers()):
    if "Sea/Ocean/Lake" in layer.name:
        sea_ocean_lake_index = i
        break

# Use calculated cell size for Kernel Density analysis
output_raster_violent = perform_kernel_density_analysis(violent_features,cell_size,optimal_bandwidth_violent)

# Perform Kernel Density analysis for non-violent events
output_raster_non_violent = perform_kernel_density_analysis(non_violent_features,cell_size,optimal_bandwidth_non_violent)


# -----------------------------
### ADDING DATA TO MAP
# -----------------------------

# Load the ArcGIS project
aprx_path = r"APRX/Raw/{}.aprx".format(iso3)  # Replace with the actual path template
aprx = arcpy.mp.ArcGISProject(aprx_path)

# Define the map object you want to work with
map_obj = aprx.listMaps()[1]  # You might need to adjust the index if you have multiple maps

# Print the names of all layers in the map before removal
#print("Layers in the map before removal:")
#for layer in map_obj.listLayers():
#    print(layer.name)

# Remove only layers with ".shp" and ".tif" files from the map
layers_to_remove = []
for layer in map_obj.listLayers():
    if layer.supports("DATASOURCE") and (layer.dataSource.lower().endswith(".shp") or layer.dataSource.lower().endswith((".tif", ".tiff"))):
        layers_to_remove.append(layer)
for layer in layers_to_remove:
    map_obj.removeLayer(layer)

# Print a message after removing previous shapefile and raster layers
print("All previous shapefile and raster layers have been removed from the map.")

# Construct the relative shapefile folder path
script_directory = os.path.dirname(os.path.abspath(__file__))
shapefiles_folder = os.path.join(script_directory, "SHAPEFILES", f"{country}_shapefiles")

# Debug: Print the constructed shapefiles_folder path
print("Constructed shapefiles_folder:", shapefiles_folder)


# Define the folder containing both shapefiles and rasters
data_folder = shapefiles_folder  # Use the same folder for both shapefiles and rasters

# Iterate through files in the folder and add shapefiles and rasters to the map
for dirpath, dirnames, filenames in os.walk(data_folder):
    for file in filenames:
        data_path = os.path.join(dirpath, file)
        if file.endswith(".shp"):
            map_obj.addDataFromPath(data_path)
            print(f"Added shapefile: {data_path}")
        elif file.lower().endswith((".tif", ".tiff", ".jpg", ".jpeg", ".png", ".bmp", ".gif")):
            map_obj.addDataFromPath(data_path)
            print(f"Added raster: {data_path}")

# Print a confirmation message after new shapefiles and raster data have been added to the map
print("New shapefiles and raster data have been added to the map.")

# -----------------------------
### TURNING OFF LAYERS###
# -----------------------------
# Turn off specific layers
for layer in map_obj.listLayers():
    if layer.name in ["violent_events", "non_violent_events"]:
        layer.visible = False

# Print a message after applying symbology and turning off layers
print("Specific layers have been turned off.")
aprx.save()


###MOVING LAYERS

# Define the map
map_obj = aprx.listMaps()[1]

# Get a reference to the reference layer ("Mask Internal")
ref_layer = map_obj.listLayers("Mask Internal")[0]

# Iterate through all layers in the map
for layer in map_obj.listLayers():
    if layer.name.endswith(".tif"):
        # Move the layer with ".tif" extension before the reference layer
        map_obj.moveLayer(ref_layer, layer, "BEFORE")


# Print the names of all layers in the map after MOVING
print("Layers in the map after MOVING:")
for layer in map_obj.listLayers():
    print(layer.name)

# -----------------------------
### APPLYING SYMBOLOGY TO LAYERS
# -----------------------------

# Entering the path to the symbologies that have been downloaded through Blob
script_directory = os.path.dirname(os.path.abspath(__file__))
symbologies_path = os.path.join(script_directory, "symbologies")

template = os.path.join(symbologies_path, "Kernel_raster_symbology.lyrx")
violent_layer = map_obj.listLayers("KernelD_violent1.tif")[0]
non_violent_layer = map_obj.listLayers("KernelD_non_vio1.tif")[0]
# Apply symbology
KernelD_violent1 = arcpy.management.ApplySymbologyFromLayer(in_layer=violent_layer, in_symbology_layer=template, symbology_fields="#",  update_symbology="DEFAULT")[0]
KernelD_non_vio1 = arcpy.management.ApplySymbologyFromLayer(in_layer=non_violent_layer, in_symbology_layer=template, symbology_fields="#", update_symbology="DEFAULT")[0]

print("Symbologies to Kernel rasters applied")


# Apply symbology to the layers using the provided symbology paths within the script folder
decreased_intensity_symbology_path = os.path.join(script_directory, "symbologies", "Decreased.lyrx")
increased_intensity_symbology_path = os.path.join(script_directory, "symbologies", "Increased.lyrx")
violent_intensity_symbology_path = os.path.join(script_directory, "symbologies", "Violent.lyrx")
non_violent_intensity_symbology_path = os.path.join(script_directory, "symbologies", "Violent.lyrx")
Clustered_fatalities_symbology_path = os.path.join(script_directory, "symbologies", "Clustered_fatalities.lyrx")
kernel_raster_symbology_path = os.path.join(script_directory, "symbologies", "Kernel_raster_symbology.lyrx")
new_conflict_zones_path = os.path.join(script_directory, "symbologies", "new_conflict_zones.lyrx")


# Iterate through the map layers and apply symbology
for layer in map_obj.listLayers():
    if layer.isFeatureLayer:
        if layer.name == "Decreased_intensity":
            arcpy.management.ApplySymbologyFromLayer(layer, decreased_intensity_symbology_path)
        elif layer.name == "Increased_intensity":
            arcpy.management.ApplySymbologyFromLayer(layer, increased_intensity_symbology_path)
        elif layer.name == "Violent_intensity":
            arcpy.management.ApplySymbologyFromLayer(layer, violent_intensity_symbology_path)
        elif layer.name == "Non_violent_intensity":
            arcpy.management.ApplySymbologyFromLayer(layer, non_violent_intensity_symbology_path)
        elif layer.name == "Clustered_fatalities":
            arcpy.management.ApplySymbologyFromLayer(layer, Clustered_fatalities_symbology_path)
        elif layer.name == "new_conflict_zones":
            arcpy.management.ApplySymbologyFromLayer(layer, new_conflict_zones_path)


# Print a message after applying symbology
print("Symbology has been applied to shapefiles layers.")

# Save the project with the added layers and symbology
aprx.save()



# -----------------------------
### EXPORTING PDFS###
# -----------------------------

# Construct the relative shapefile folder path
script_directory = os.path.dirname(os.path.abspath(__file__))



pdf_output_path = os.path.join("PDF", "Conflict_pdfs")



# Create the output directory if it doesn't exist
os.makedirs(pdf_output_path, exist_ok=True)

# Debug: Print the constructed pdf_output_path path
print("Constructed pdf_output_path:", pdf_output_path)

# Assuming 'map_obj' is a Map object

aprx_path = r"APRX/Raw/{}.aprx".format(iso3)  # Replace with the actual path template
aprx = arcpy.mp.ArcGISProject(aprx_path)

# Get the map object
map_obj = aprx.listMaps()[1]

# Find the layout by its name
layout_name = country  # Update this with the correct layout name
lyt = None

for lyt in aprx.listLayouts():
    if lyt.name == layout_name:
        break

if lyt is None:
    print(f"Layout '{layout_name}' not found.")
else:
    # Access the layers
    layer_violent = map_obj.listLayers("KernelD_violent1.tif")[0]
    layer_new_conflict_zones = map_obj.listLayers("new_conflict_zones")[0]
    layer_Clustered_fatalities = map_obj.listLayers("Clustered_fatalities")[0]
    layer_Increased_intensity = map_obj.listLayers("Increased_intensity")[0]
    layer_Decreased_intensity = map_obj.listLayers("Decreased_intensity")[0]
    layer_non_violent = map_obj.listLayers("KernelD_non_vio1.tif")[0]
    # Export PDF with Violent events raster on and Non-violent events raster off
    pdf_violent_output_path = os.path.join(pdf_output_path, "Violent_events.pdf")
    layer_violent.visible = True  # Turn on the violent layer
    layer_non_violent.visible = False  # Turn off the non-violent layer
    lyt.exportToPDF(pdf_violent_output_path, resolution=300)
    print("Violent events PDF EXPORTED")
    # Export PDF with Non-violent events raster on and Violent events raster off
    pdf_non_violent_output_path = os.path.join(pdf_output_path, "Non_violent_events.pdf")
    layer_violent.visible = False  # Turn off the violent layer
    layer_non_violent.visible = True  # Turn on the non-violent layer
    layer_new_conflict_zones = False
    layer_Clustered_fatalities = False
    layer_Increased_intensity = False
    layer_Decreased_intensity = False
    lyt.exportToPDF(pdf_non_violent_output_path, resolution=300)
    print("Non_violent events PDF EXPORTED")
    # Reset the visibility of the layers
    layer_violent.visible = True
    layer_non_violent.visible = True


    # Print statements for tracking
    print("PDFS EXPORTED")
    # Save the project after exporting PDFs
    #aprx.save()
