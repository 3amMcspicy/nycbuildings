# New York City Housing Authority (NYCHA) electricity and water consumption visualization

### Description of project goal:
The project is to develop an interactive webapp to visualize electricity and water consumption data in NYCHA housings.

### Reasoining for the project:
In order to move towards a sustainable future, societies should be aware of how much of water and electricity they are consuming. While water management ensures cities have a steady supply of water, an effective way to conserve water is changing the consumer's behaviour. An example of this would be the californian government passing regulations on watering lawns. Similarly, being mindful of electricity consumption translates to less carbon emissions need to produce those energy. In the event that there are outliers, it might be indicative of leakages as well. In addition, this project helps to visualize the changes in consumption over the seasons as well. This may be useful to see where more supply of the water/electricity may need to be diverted to. Finally, the pandemic has led to an exodus of residents away from New York City. Using data from march 2020 onwards, it might be possible to see if it also affected residents in NYCHA housing. 

### Description of the project:
The water and electricity consumption data in NYCHA housing visualized. 
By comparing the data between 2010 to 2021, users can see the change in consumption through the years/months. Users can also see changes in data for specific buildings.
The webapp also presents mean statistics over areas/boroughs that can be compared with other areas.

### Description of User interaction:
Users will access the website through the link. There will be a map of New York City and users can see water consumption data as a heat map. There will be a slider to see the change in time and labels for searching specific areas.

#### Type of data user will provide:
None

### Description of code:
Folium: Package to create the interactive map.\
FastAPI: To build the API \ 
Pandas: Data processing\
Numpy: Data processing\
Streamlit: Webapp \

### Description of data:
Water consumption: https://data.cityofnewyork.us/Housing-Development/Water-Consumption-And-Cost-2013-2020-/66be-66yr
Electricity Consumption: https://data.cityofnewyork.us/Housing-Development/Electric-Consumption-And-Cost-2010-April-2020-/jr24-e7cr
Both datasets are provided by NYCHA through NYC open data that can be accessed through REST API in the format of JSON.

The data is then mapped using the NYCHA residential addresss dataset https://data.cityofnewyork.us/Housing-Development/NYCHA-Residential-Addresses/3ub5-4ph8. Which has longitude and latitude coordinates.


The Tenant Data System (TDS) number helps link all the three datasets together.

Output:

### Existing similar webapp:
https://energy.cusp.nyu.edu/#/ is a heatmap that allows for quick visualization. However, the map is displaying data that is calculated to fit their metrics. My website will be providing untouched data on water/electricity consumption.
