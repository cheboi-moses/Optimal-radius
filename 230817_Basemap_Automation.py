import arcpy
import re
from azure.storage.blob import ContainerClient, BlobServiceClient
import os



### Initialisation ###

print("======= Script started ======")

# Prompt for user input
#country = input("Enter the country name: ")
#iso3 = input("Enter the ISO3 code: ")

country = "France" #test
#list_iso3 = ["MEX","KEN","BDI"]

country_iso3_list = [
    ["South Sudan", "SSD"],["Sierra Leone", "SLE"], ["Eswatini", "SWZ"]
]

"""
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
"""

# Clean the country name to remove non-alphabetical characters and spaces
clean_country = re.sub(r'[^a-zA-Z]', '', country)

PATH_PROJECT = r"APRX_TEMPLATE/APRX_TEMPLATE.aprx"

# Create an ArcGIS Pro project object
aprx = arcpy.mp.ArcGISProject(PATH_PROJECT)

# Selecting the map
map = aprx.listMaps("Map")[0]

#Removing any undesired layer
for lyr in map.listLayers():
    map.removeLayer(lyr)


### Access to Azure + local download in folder ###

# Variables setup
blob_storage_account = 'dataplatformcontsolake'
blob_storage_container = 'unocc-gis'
sas_token = "sp=racwdl&st=2023-07-07T16:56:33Z&se=2024-01-01T01:56:33Z&spr=https&sv=2022-11-02&sr=c&sig=o1DnRtIIucFDfWhVsE7O0EqeU20K8EjMff07D0C2BFc%3D"
url = "https://"+blob_storage_account+".blob.core.windows.net/"+blob_storage_container
STORAGEACCOUNTURL= "https://"+blob_storage_account+".blob.core.windows.net/"
STORAGEACCOUNTKEY= sas_token
CONTAINERNAME= blob_storage_container

# Read
container_client = ContainerClient.from_container_url(
    container_url=url,
    credential=sas_token
)
container_client.list_blobs().next()

blobs_list = container_client.list_blobs()

print("======= List of files in BlobStorage ======")

for blob in blobs_list:
    print(blob.name)

# Download
blob_service_client_instance = BlobServiceClient(account_url=STORAGEACCOUNTURL, credential=STORAGEACCOUNTKEY)
blobs_list = container_client.list_blobs()

# Get the directory of the APRX file
script_directory = os.path.dirname(os.path.abspath(__file__))

# Create the symbologies folder if it doesn't exist in the APRX directory
symbologies_folder = os.path.join(script_directory, "symbologies")
os.makedirs(symbologies_folder, exist_ok=True)

print("======= Downloading files ======")

# Download - End
for blob in blobs_list:
    if blob.name.endswith(".lyrx") or blob.name.endswith(".pagx") or blob.name.endswith(".prj"):
        local_file_path = os.path.join(symbologies_folder, os.path.basename(blob.name))

        with open(local_file_path, "wb") as my_blob:
            blob_client_instance = blob_service_client_instance.get_blob_client(CONTAINERNAME, blob.name, snapshot=None)
            blob_data = blob_client_instance.download_blob()
            blob_data.readinto(my_blob)

        print("Downloaded " + blob.name + " to " + local_file_path)


### API URLs and definition queries ###

map = aprx.listMaps("Map")[0]

#Initialization of layers
api_layers = {
    #Settlements fron settlements API
    "Settlements_AdminOne_capital": "https://services5.arcgis.com/YpQPX1qUo0ioHY5T/arcgis/rest/services/settlements/FeatureServer/0",
    "TEST": "https://services5.arcgis.com/YpQPX1qUo0ioHY5T/arcgis/rest/services/settlements/FeatureServer/0",
    "Settlements_AdminZero_capital":"https://services5.arcgis.com/YpQPX1qUo0ioHY5T/arcgis/rest/services/settlements/FeatureServer/0",
    #Settlements from World Cities API
    "Settlements_AdminOne_capitalBis":"https://services.arcgis.com/P3ePLMYs2RVChkJx/arcgis/rest/services/World_Cities/FeatureServer/0",

    #GIS vector tile posted in UNOCC Agol
    "Hydrology_Ocean&Sea": "https://www.arcgis.com/sharing/rest/content/items/5e2156773a954198926a643414c8da54/resources/styles/root.json",
    #GIS layer from WFP
    "Hydrology_Rivers": "https://gis.wfp.org/arcgis/rest/services/GLOBAL/GlobalRivers/FeatureServer/0",
    #GIS layer
    "Hydrology_Coastline": "https://services5.arcgis.com/YpQPX1qUo0ioHY5T/arcgis/rest/services/Global_boundary_lines/FeatureServer/0",

    #GIS layer from WFP hosted in UNOCC agol
    "Globalbase": "https://services5.arcgis.com/YpQPX1qUo0ioHY5T/arcgis/rest/services/UNOCC_Watch_Room_Print_Map_WFL/FeatureServer/3",
    "Countrybase": "https://services5.arcgis.com/YpQPX1qUo0ioHY5T/arcgis/rest/services/UNOCC_Watch_Room_Print_Map_WFL/FeatureServer/3",

    #GIS layer of main roads
    "Transport_roads": "https://services5.arcgis.com/YpQPX1qUo0ioHY5T/arcgis/rest/services/Transport_roads/FeatureServer/0",

    #GIS layer of border crossings
    "Border_Crossing": "https://gis.wfp.org/arcgis/rest/services/GLOBAL/GLOBAL_Border_Crossing_Points/FeatureServer/0",

    #GIS layer of airports
    "Airports": "https://gis.wfp.org/arcgis/rest/services/GLOBAL/GlobalAirports/FeatureServer/0",

    #GIS layers from UNGIS
    "Boundary_AdminZero_Non_National_UNGIS": "https://services5.arcgis.com/YpQPX1qUo0ioHY5T/arcgis/rest/services/Global_boundary_lines/FeatureServer/0",
    "Boundary_AdminZero_UNGIS": "https://services5.arcgis.com/YpQPX1qUo0ioHY5T/arcgis/rest/services/Global_boundary_lines/FeatureServer/0",
    "Boundary_Disputed_UNGIS": "https://services5.arcgis.com/YpQPX1qUo0ioHY5T/arcgis/rest/services/Global_boundary_lines/FeatureServer/0",

    #GIS layers from WFP hosted in UNOCC agol
    "Boundary_AdminZero_WFP":"https://services5.arcgis.com/YpQPX1qUo0ioHY5T/arcgis/rest/services/UNOCC_Watch_Room_Print_Map_WFL/FeatureServer/3",
    "Boundary_AdminOne_WFP":"https://services5.arcgis.com/YpQPX1qUo0ioHY5T/arcgis/rest/services/UNOCC_Watch_Room_Print_Map_WFL/FeatureServer/4",
    "Boundary_AdminTwo_WFP":"https://services5.arcgis.com/YpQPX1qUo0ioHY5T/arcgis/rest/services/UNOCC_Watch_Room_Print_Map_WFL/FeatureServer/5",
    "Boundary_AdminThree_WFP":"https://services5.arcgis.com/YpQPX1qUo0ioHY5T/arcgis/rest/services/UNOCC_Watch_Room_Print_Map_WFL/FeatureServer/6",
    "Boundary_Disputed_WFP":"https://services5.arcgis.com/YpQPX1qUo0ioHY5T/arcgis/rest/services/UNOCC_Watch_Room_Print_Map_WFL/FeatureServer/3",

    #Not working due to credential issue
    #"Hillshade":"https://services.arcgisonline.com/arcgis/rest/services/Elevation/World_Hillshade/MapServer/0",

    #Not working due to permission issue
    #"Peacekeeping":"https://utility.arcgis.com/usrsvcs/servers/109637f160da49a496ec3d96d9b624c9/rest/services/UNOM_GLOBAL_COGI_CVW_01/FeatureServer",

    #World topographic map
    "Topographic":"https://unocc.maps.arcgis.com/sharing/rest/content/items/8808a2df8edc4959b234b488f754a170/resources/styles/root.json"
}

# Dictionary adding alternative names with no non-alphabetical characters as it otherwise causes issues on some parts of the script
content_tab_names = {
    "Settlements_AdminOne_capital": "SettlementsAdminOnecapital",
    "Settlements_AdminZero_capital": "SettlementsAdminZerocapital",
    "Settlements_AdminOne_capitalBis":"SettlementsAdminOnecapitalBis",
    "Hydrology_Ocean&Sea": "HydrologyOceanSea",
    "Hydrology_Rivers": "HydrologyRivers",
    "Hydrology_Coastline": "HydrologyCoastline",
    "Globalbase": "Globalbase",
    "Countrybase": "Countrybase",
    "Transport_roads": "Transportroads",
    "Border_Crossing": "BorderCrossing",
    "Airports": "Airports",
    "Boundary_AdminZero_Non_National_UNGIS":"BoundaryAdminZeroNonNationalUNGIS",
    "Boundary_AdminZero_UNGIS":"BoundaryAdminZeroUNGIS",
    "Boundary_Disputed_UNGIS": "BoundaryDisputedUNGIS",
    "Boundary_AdminZero_WFP":"BoundaryAdminZeroWFP",
    "Boundary_AdminOne_WFP":"BoundaryAdminOneWFP",
    "Boundary_AdminTwo_WFP":"BoundaryAdminTwoWFP",
    "Boundary_AdminThree_WFP":"BoundaryAdminThreeWFP",
    "Boundary_Disputed_WFP":"BoundaryDisputedWFP",
    "Hillshade":"Hillshade",
    "Topographic":"Topographic",
    "TEST":"TEST"
}

iso3 = "FRA" #This is only for initialization purposes, as well as the first definition queries

#Iterate over the API layers to apply definition queries
for api_name, layer_url in api_layers.items():
    try:
        web_layer = map.addDataFromPath(layer_url)
        definition_query = None

        if api_name in ["Countrybase", "Boundary_AdminZero_WFP", "Boundary_AdminOne_WFP", "Boundary_AdminTwo_WFP", "Boundary_AdminThree_WFP", "Airports"]:
            definition_query = f"iso3 = '{iso3}'"

        elif api_name == "Settlements_AdminZero_capital":
            definition_query = f"ADM0_A3 = '{iso3}' AND FEATURECLA = 'Admin-0 capital'"

        elif api_name == "Settlements_AdminOne_capital":
            definition_query = f"ADM0_A3 = '{iso3}' AND FEATURECLA IN ('Admin-1 capital', 'Admin-1 region capital')"

        elif api_name == "Settlements_AdminOne_capitalBis":
            definition_query = f"CNTRY_NAME = '{country}' And STATUS NOT IN ('National capital', 'National and provincial capital', 'National capital and provincial capital enclave')"

        elif api_name == "Hydrology_Coastline":
            definition_query = "BDYTYP = 0"

        elif api_name == "Globalbase":
            definition_query = f"iso3 <> '{iso3}'"

        elif api_name == "Boundary_AdminZero_UNGIS":
            definition_query = f"ISO3CD LIKE '%{iso3}%' AND BDYTYP = 1"

        elif api_name == "Boundary_AdminZero_Non_National_UNGIS":
            definition_query = f"ISO3CD NOT LIKE '%{iso3}%' AND BDYTYP = 1"

        elif api_name == "Boundary_Disputed_UNGIS":
            definition_query = f"BDYTYP IN (2, 3, 4)"

        elif api_name == "Boundary_Disputed_WFP":
            definition_query = f"stscod IN ('Occupied Palestinian Territory', 'Sovereignty unsettled', 'Special Region or Province')"

        elif api_name == "Border_Crossing":
            definition_query = f"iso3_1 = '{iso3}' Or iso3_2 = '{iso3}'"

        # Apply the definition query to the web layer
        if definition_query:
            web_layer.definitionQuery = definition_query

        # Set the display name in the content tab
        if api_name in content_tab_names:
            web_layer.name = content_tab_names[api_name]

        print(f"{api_name} web layer added and definition query applied.")

    #In case of an error
    except Exception as e:
        print(f"Error occurred while processing {api_name}: {str(e)}")
        continue


print("======= Applying symbologies ======")
print("Loading ...")



### Styling the layers ###

map = aprx.listMaps("Map")[0]

# Defining new in_layers
Settlements_AdminZero_capital_layer = map.listLayers("SettlementsAdminZerocapital")[0]
Settlements_AdminOne_capital_layer = map.listLayers("SettlementsAdminOnecapital")[0]
Settlements_AdminOne_capitalBis_layer = map.listLayers("SettlementsAdminOnecapitalBis")[0]
Hydrology_Ocean_Sea_layer = map.listLayers("HydrologyOceanSea")[0]
Hydrology_Rivers_layer = map.listLayers("HydrologyRivers")[0]
Hydrology_Coastline_layer = map.listLayers("HydrologyCoastline")[0]
Globalbase_layer = map.listLayers("Globalbase")[0]
Countrybase_layer = map.listLayers("Countrybase")[0]
Transport_roads_layer = map.listLayers("Transportroads")[0]
Border_Crossing_layer = map.listLayers("BorderCrossing")[0]
Airports_layer = map.listLayers("Airports")[0]
Boundary_AdminZero_UNGIS_layer = map.listLayers("BoundaryAdminZeroUNGIS")[0]
Boundary_AdminZero_Non_National_UNGIS_layer = map.listLayers("BoundaryAdminZeroNonNationalUNGIS")[0]
Boundary_AdminZero_WFP_layer = map.listLayers("BoundaryAdminZeroWFP")[0]
Boundary_AdminOne_WFP_layer = map.listLayers("BoundaryAdminOneWFP")[0]
Boundary_AdminTwo_WFP_layer = map.listLayers("BoundaryAdminTwoWFP")[0]
Boundary_AdminThree_WFP_layer = map.listLayers("BoundaryAdminThreeWFP")[0]
Boundary_Disputed_UNGIS_layer = map.listLayers("BoundaryDisputedUNGIS")[0]
Boundary_Disputed_WFP_layer = map.listLayers("BoundaryDisputedWFP")[0]


# Entering the path to the symbologies that have been downloaded through Blob
script_directory = os.path.dirname(os.path.abspath(arcpy.mp.ArcGISProject(PATH_PROJECT).filePath))
symbologies_path = os.path.join(script_directory, "..", "symbologies")

Settlements_AdminZero_capital_API = os.path.join(symbologies_path, "National Capital.lyrx")
Settlements_AdminOne_capital_API = os.path.join(symbologies_path, "populated_places_API.lyrx")
Settlements_AdminOne_capitalBis_API = os.path.join(symbologies_path, "populated_places_WorldCities_API.lyrx")
Hydrology_Rivers_API = os.path.join(symbologies_path, "River_API.lyrx")
Hydrology_Coastline_API = os.path.join(symbologies_path, "Coastline_API.lyrx")
Globalbase_API = os.path.join(symbologies_path, "Mask External.lyrx")
Countrybase_API = os.path.join(symbologies_path, "Country_base_API.lyrx")
Transport_roads_API = os.path.join(symbologies_path, "Transport_roads_API.lyrx")
Border_Crossing_API = os.path.join(symbologies_path, "Border_Crossing.lyrx")
Airports_API = os.path.join(symbologies_path, "Airports.lyrx")
Boundary_AdminZero_UNGIS_API = os.path.join(symbologies_path, "Boundary_lines_subject_API.lyrx")
Boundary_AdminZero_Non_National_UNGIS_API = os.path.join(symbologies_path, "Boundary_lines_Not_subject_API.lyrx")
Boundary_AdminZero_WFP_API = os.path.join(symbologies_path, "Boundary_polygons_subject.lyrx")
Boundary_AdminOne_WFP_API = os.path.join(symbologies_path, "AdminOne_polygons_API.lyrx")
Boundary_AdminTwo_WFP_API = os.path.join(symbologies_path, "AdminTwo_polygons_API.lyrx")
Boundary_AdminThree_WFP_API = os.path.join(symbologies_path, "AdminTwo_polygons_API.lyrx")
Boundary_Disputed_UNGIS_API = os.path.join(symbologies_path, "Disputed_boundaries_API.lyrx")
Boundary_Disputed_WFP_API = os.path.join(symbologies_path, "Disputed_polygons_API.lyrx")


# Applying symbology from layer
Settlements_AdminZero_capital = arcpy.management.ApplySymbologyFromLayer(in_layer=Settlements_AdminZero_capital_layer, in_symbology_layer=Settlements_AdminZero_capital_API)[0]
Settlements_AdminOne_capital = arcpy.management.ApplySymbologyFromLayer(in_layer=Settlements_AdminOne_capital_layer, in_symbology_layer=Settlements_AdminOne_capital_API)[0]
Settlements_AdminOne_capitalBis = arcpy.management.ApplySymbologyFromLayer(in_layer=Settlements_AdminOne_capitalBis_layer, in_symbology_layer=Settlements_AdminOne_capitalBis_API)[0]
Hydrology_Rivers = arcpy.management.ApplySymbologyFromLayer(in_layer=Hydrology_Rivers_layer, in_symbology_layer=Hydrology_Rivers_API)[0]
Hydrology_Coastline = arcpy.management.ApplySymbologyFromLayer(in_layer=Hydrology_Coastline_layer, in_symbology_layer=Hydrology_Coastline_API)[0]
Globalbase = arcpy.management.ApplySymbologyFromLayer(in_layer=Globalbase_layer, in_symbology_layer=Globalbase_API)[0]
Countrybase = arcpy.management.ApplySymbologyFromLayer(in_layer=Countrybase_layer, in_symbology_layer=Countrybase_API)[0]
Transport_roads = arcpy.management.ApplySymbologyFromLayer(in_layer=Transport_roads_layer, in_symbology_layer=Transport_roads_API)[0]
Border_Crossing = arcpy.management.ApplySymbologyFromLayer(in_layer=Border_Crossing_layer, in_symbology_layer=Border_Crossing_API)[0]
Airports = arcpy.management.ApplySymbologyFromLayer(in_layer=Airports_layer, in_symbology_layer=Airports_API)[0]
Boundary_AdminZero_UNGIS = arcpy.management.ApplySymbologyFromLayer(in_layer=Boundary_AdminZero_UNGIS_layer, in_symbology_layer=Boundary_AdminZero_UNGIS_API)[0]
Boundary_AdminZero_Non_National_UNGIS = arcpy.management.ApplySymbologyFromLayer(in_layer=Boundary_AdminZero_Non_National_UNGIS_layer, in_symbology_layer=Boundary_AdminZero_Non_National_UNGIS_API)[0]
Boundary_AdminZero_WFP = arcpy.management.ApplySymbologyFromLayer(in_layer=Boundary_AdminZero_WFP_layer, in_symbology_layer=Boundary_AdminZero_WFP_API)[0]
Boundary_AdminOne_WFP = arcpy.management.ApplySymbologyFromLayer(in_layer=Boundary_AdminOne_WFP_layer, in_symbology_layer=Boundary_AdminOne_WFP_API)[0]
Boundary_AdminTwo_WFP = arcpy.management.ApplySymbologyFromLayer(in_layer=Boundary_AdminTwo_WFP_layer, in_symbology_layer=Boundary_AdminTwo_WFP_API)[0]
Boundary_AdminThree_WFP = arcpy.management.ApplySymbologyFromLayer(in_layer=Boundary_AdminThree_WFP_layer, in_symbology_layer=Boundary_AdminThree_WFP_API)[0]
Boundary_Disputed_UNGIS = arcpy.management.ApplySymbologyFromLayer(in_layer=Boundary_Disputed_UNGIS_layer, in_symbology_layer=Boundary_Disputed_UNGIS_API)[0]
Boundary_Disputed_WFP = arcpy.management.ApplySymbologyFromLayer(in_layer=Boundary_Disputed_WFP_layer, in_symbology_layer=Boundary_Disputed_WFP_API)[0]

print("Symbologies applied")
print("======= Naming, grouping and moving layers ======")
print("Loading ...")



### Naming the layers properly, with non-alphabetical characters ###

# Rename the labels with proper names displayed in ArcGIS, with non-alphabetic characters
map.listLayers("SettlementsAdminZerocapital")[0].name = "National Capital"
map.listLayers("SettlementsAdminOnecapital")[0].name = "Admin Capital - Source 1"
map.listLayers("SettlementsAdminOnecapitalBis")[0].name = "Admin Capital - Source 2"
map.listLayers("HydrologyOceanSea")[0].name = "Sea/Ocean/Lake"
map.listLayers("HydrologyCoastline")[0].name = "Coastline"
map.listLayers("HydrologyRivers")[0].name = "River"
map.listLayers("Globalbase")[0].name = "Mask External"
map.listLayers("Countrybase")[0].name = "Mask Internal"
map.listLayers("Transportroads")[0].name = "Roads"
map.listLayers("BorderCrossing")[0].name = "Border Crossing Points"
map.listLayers("Airports")[0].name = "Airports"
map.listLayers("BoundaryAdminZeroNonNationalUNGIS")[0].name = "Adm0_External - UNGIS"
map.listLayers("BoundaryAdminZeroUNGIS")[0].name = "Adm0 - UNGIS"
map.listLayers("BoundaryDisputedUNGIS")[0].name = "Disputed - UNGIS"
map.listLayers("BoundaryAdminZeroWFP")[0].name = "Adm0 - WFP"
map.listLayers("BoundaryAdminOneWFP")[0].name = "Adm1 - WFP"
map.listLayers("BoundaryAdminTwoWFP")[0].name = "Adm2 - WFP"
map.listLayers("BoundaryAdminThreeWFP")[0].name = "Adm3 - WFP"
map.listLayers("BoundaryDisputedWFP")[0].name = "Disputed - WFP"
# map.listLayers("Hillshade")[0].name = "Topography Hillshade" #Not working due to credentials problem
map.listLayers("Topographic")[0].name = "World Topographic Map"
map.listLayers("TEST")[0].name = "TEST"


### Group the layers in different categories in the ArcGIS panel ###
# Obtain the absolute path for the Group.lyrx file
script_directory = os.path.dirname(os.path.abspath(arcpy.mp.ArcGISProject(PATH_PROJECT).filePath))
group_filename = r"symbologies/Group.lyrx"
group_path = os.path.join(script_directory, group_filename)

# Defined new groups including each layers
empty_group_layer_file = arcpy.mp.LayerFile(group_path)

group_layers = {
    "Cities": [Settlements_AdminZero_capital, Settlements_AdminOne_capital,Settlements_AdminOne_capitalBis],
    "Admin Boundaries": [Boundary_Disputed_UNGIS,Boundary_AdminZero_UNGIS,Boundary_AdminZero_Non_National_UNGIS,Boundary_Disputed_WFP,Boundary_AdminZero_WFP, Boundary_AdminOne_WFP,Boundary_AdminTwo_WFP, Boundary_AdminThree_WFP],
    "Hydrology": [Hydrology_Coastline,Hydrology_Rivers],
    "Infrastructure": [Transport_roads,Border_Crossing,Airports],
    "Peacekeeping": [],
}

# Create layers inside the new group layer and removing unused ones
for group_name, layers in group_layers.items():
    group = map.addLayer(empty_group_layer_file)[0]
    group.name = group_name
    for lyr in layers:
        map.addLayerToGroup(group, lyr)
        map.removeLayer(lyr)

# Turn off some layers
map.listLayers("Admin Capital - Source 1")[0].visible = False
map.listLayers("Mask Internal")[0].visible = False
map.listLayers("Adm0 - WFP")[0].visible = False
map.listLayers("Border Crossing Points")[0].visible = False
map.listLayers("Airports")[0].visible = False
map.listLayers("Roads")[0].visible = False
map.listLayers("Adm2 - WFP")[0].visible = False
map.listLayers("Adm3 - WFP")[0].visible = False
map.listLayers("TEST")[0].visible = False

### Drawing order ###
print("Changing order of layers...")

# Moving layers
refLayer = map.listLayers("Hydrology")[0]
movedLayer = map.listLayers("Peacekeeping")[0]
map.moveLayer(refLayer, movedLayer, "AFTER")
movedLayer = map.listLayers("Cities")[0]
map.moveLayer(refLayer, movedLayer, "BEFORE")
movedLayer = map.listLayers("Admin boundaries")[0]
map.moveLayer(refLayer, movedLayer, "BEFORE")
movedLayer = map.listLayers("Mask External")[0]
map.moveLayer(refLayer, movedLayer, "BEFORE")
movedLayer = map.listLayers("Infrastructure")[0]
map.moveLayer(refLayer, movedLayer, "BEFORE")

refLayer = map.listLayers("Sea/Ocean/Lake")[0]
movedLayer = map.listLayers("World Topographic Map")[0]
map.moveLayer(refLayer, movedLayer, "AFTER")

refLayer = map.listLayers("National Capital")[0]
movedLayer = map.listLayers("TEST")[0]
map.moveLayer(refLayer, movedLayer, "AFTER")
movedLayer = map.listLayers("Admin Capital - Source 2")[0]
map.moveLayer(refLayer, movedLayer, "AFTER")
movedLayer = map.listLayers("Admin Capital - Source 1")[0]
map.moveLayer(refLayer, movedLayer, "AFTER")

refLayer = map.listLayers("River")[0]
movedLayer = map.listLayers("Coastline")[0]
map.moveLayer(refLayer, movedLayer, "BEFORE")

refLayer = map.listLayers("Adm0 - UNGIS")[0]
movedLayer = map.listLayers("Disputed - WFP")[0]
map.moveLayer(refLayer, movedLayer, "AFTER")
movedLayer = map.listLayers("Adm0_External - UNGIS")[0]
map.moveLayer(refLayer, movedLayer, "AFTER")
movedLayer = map.listLayers("Disputed - UNGIS")[0]
map.moveLayer(refLayer, movedLayer, "BEFORE")

print("Naming, grouping and moving applied")
print("======= Creating layout ======")
print("Loading ...")

### Create layouts ###

# Get the directory of the layout template
templatePath = os.path.dirname(os.path.abspath(arcpy.mp.ArcGISProject(PATH_PROJECT).filePath))
template_filename = r"symbologies\Large_Basemap.pagx"
template_pagx = os.path.join(templatePath, template_filename)


### Map creation via ArcPy ###
for country_iso3 in country_iso3_list:
    country = country_iso3[0]
    iso3 = country_iso3[1]

    # Import template and rename it
    aprx.importDocument(template_pagx)
    lyt = aprx.listLayouts('Basemap Template')[0]
    lyt.name = f"{country}"

    # Selecting the map
    map = aprx.listMaps("Map")[0]

    print("======= Applying definition queries ======")

    #Iterate over the API layers to apply definition queries
    for lyr in map.listLayers():
        try:
            definition_query = None

            if lyr.name in ["Mask Internal", "Adm0 - WFP", "Adm1 - WFP", "Adm2 - WFP", "Adm3 - WFP", "Airports"]:
                definition_query = f"iso3 = '{iso3}'"

            elif lyr.name == "National Capital":
                definition_query = f"ADM0_A3 = '{iso3}' AND FEATURECLA = 'Admin-0 capital'"

            elif lyr.name == "Admin Capital - Source 1":
                definition_query = f"ADM0_A3 = '{iso3}' AND FEATURECLA IN ('Admin-1 capital', 'Admin-1 region capital')"

            elif lyr.name == "Admin Capital - Source 2":
                definition_query = f"CNTRY_NAME = '{country}' And STATUS NOT IN ('National capital', 'National and provincial capital', 'National capital and provincial capital enclave')"

            elif lyr.name == "Coastline":
                definition_query = "BDYTYP = 0"

            elif lyr.name == "Mask External":
                definition_query = f"iso3 <> '{iso3}'"

            elif lyr.name == "Adm0 - UNGIS":
                definition_query = f"ISO3CD LIKE '%{iso3}%' AND BDYTYP = 1"

            elif lyr.name == "Adm0_External - UNGIS":
                definition_query = f"ISO3CD NOT LIKE '%{iso3}%' AND BDYTYP = 1"

            elif lyr.name == "Disputed - UNGIS":
                definition_query = f"BDYTYP IN (2, 3, 4)"

            elif lyr.name == "Disputed - WFP":
                definition_query = f"stscod IN ('Occupied Palestinian Territory', 'Sovereignty unsettled', 'Special Region or Province')"

            elif lyr.name == "Border Crossing Points":
                definition_query = f"iso3_1 = '{iso3}' Or iso3_2 = '{iso3}'"

            # Apply the definition query to the web layer
            if definition_query:
                lyr.definitionQuery = definition_query


            print(lyr.name+" definition query applied.")

        #In case of an error
        except Exception as e:
            print(f"Error occurred while applying definition query.")
            continue



    ### Zooming to the country on layout
    map_frames = lyt.listElements('MAPFRAME_ELEMENT', '*') #lyt is tehe layout that we created before
    mf = map_frames[1]  # Index 1 for the second map frame element (0 being the Globe Map)
    mf.map = aprx.listMaps("Map")[0]
    boundary_layer = map.listLayers("Mask Internal")[0]
    mf.camera.setExtent(mf.getLayerExtent(boundary_layer))

    #Delete the template retrieved as it is unnecessary
    delete_map = aprx.listMaps("Template Map")[0]
    aprx.deleteItem(delete_map)


    ### Update Globe Map ###

    # Get capital city coordinates to center it
    map = aprx.listMaps("Map")[0]
    national_capital_layer = map.listLayers("National Capital")[0]
    with arcpy.da.SearchCursor(national_capital_layer, ["LATITUDE", "LONGITUDE"]) as cursor:
        for row in cursor:
            YCapital, XCapital = row

    # Get the path to the script directory
    script_directory = os.path.dirname(os.path.abspath(arcpy.mp.ArcGISProject(PATH_PROJECT).filePath))

    # Specify the path to the spatial_reference_globe.prj file
    system_filename = r"symbologies\spatial_reference_globe.prj"
    system_filepath = os.path.join(script_directory, system_filename)

    # Read the content of the file and replace placeholders with values
    with open(system_filepath, 'r') as file:
        system_content = file.read()
    system_content = system_content.replace("LONGITUDE", str(XCapital))
    system_content = system_content.replace("LATITUDE", str(YCapital))

    # Write the updated content back to the file
    with open(system_filepath, 'w') as file:
        file.write(system_content)
    #Apply the new spatial reference to the globe and update the layers
    sr = arcpy.Describe(system_filepath).spatialReference
    m = aprx.listMaps("Template Globe")[0]
    m.spatialReference = sr
    lyr = m.listLayers("Mask Internal")[0]
    lyr.definitionQuery = f"iso3 = '{iso3}'"

    # Export layout to PDF
    pdf_output_path = os.path.join("PDF", "Script_Outputs")
    pdf_filename = f"{iso3}_Default_Basemap.pdf"
    pdf_full_path = os.path.join(pdf_output_path, pdf_filename)
    os.makedirs(pdf_output_path, exist_ok=True) # Create the output directory if it doesn't exist
    lyt.exportToPDF(pdf_full_path) # Export the layout to PDF


    ### End  ###

    # Save the project
    aprx_output_path = os.path.join("APRX", "Raw")
    aprx_filename = f"{iso3}.aprx"
    aprx_full_path = os.path.join(aprx_output_path, aprx_filename)
    os.makedirs(aprx_output_path, exist_ok=True) # Create the output directory if it doesn't exist
    aprx.saveACopy(aprx_full_path)

    delete_globe = aprx.listMaps("Template Globe")[0]
    aprx.deleteItem(delete_globe)
    aprx.deleteItem(lyt)


    print("############# MAP OF "+iso3+" HAS BEEN FINALIZED ####################")

# End messages

print("Process completed successfully!")