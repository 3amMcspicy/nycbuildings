# nycbuildings

##Short Description:

The project is to develop an interactive webapp to visualize electricity and water consumption data in NYCHA housings. Using Folium and Pydeck, it generates 2 different map views for users to see the consumption datasets. The folium map view displays differences in the average consumption between 2 years inputted, while the pydeck map view illustrates the scale of the consumptions between bulidings and across a timeline. 

### In development

Instructions for installing and running the program:

```
conda install pandas streamlit numpy pydeck Pillow  streamlit-folium -c conda-forge 

git clone https://github.com/3amMcspicy/nycbuildings.git

cd ./nycbuildings/src

streamlit run app.py

Open browser with Network URL for the visualization of data
```
