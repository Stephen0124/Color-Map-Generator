from os import path
import folium
import geopandas as gpd
from color import get_color

def generate(cmap: str, target_folder: str):
    # Load world map data
    world = gpd.read_file(r'data\世界国家.shp')
    world.crs="epsg:4326"

    # Select the country/countries you want to display
    country_names = ["CHINA", "RUSSIAN FEDERATION", "KAZAKHSTAN", "INDIA", "MONGOLIA", "PAKISTAN", "MYANMAR",
                    "AFGHANISTAN", "VIET NAM", "KYRGYZSTAN", "LAOS", "KOREA,DEMOCRATIC PEOPLE'S REPUBLIC OF",
                    "NEPAL", "BHUTAN", "INDONESIA", "JAPAN", "MALAYSIA", "PHILIPPINES", "KOREA, REPUBLIC OF",
                    "BRUNEI", "TAJIKISTAN"]
    selected_countries = world[world['NAME'].isin(country_names)]

    # Convert selected country data to GeoJSON format and display using Folium
    my_map = folium.Map(title="World Map",location=(40,120),max_zoom=6,control_scale=True,
                        prefer_canvas=True,zoom_control=False,
                        width='100%',height='100%',zoom_start=3,
                        tiles=folium.TileLayer('https://{s}.tile.thunderforest.com/mobile-atlas/{z}/{x}/{y}.png?apikey={apikey}',
                        attr='&copy; <a href="http://www.thunderforest.com/">Thunderforest</a>, &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
                    apikey='pk.eyJ1IjoiZGluZ3diIiwiYSI6ImNsY3doNmluazBmd2Qzb29lbzVrYXltdjYifQ.H8sWvLIDzRD7hbZDYlbUCQ',maxZoom=24,overlay=True)            )

    count_x = selected_countries['NAME'].count()

    folium.GeoJson(
        selected_countries,
        style_function=lambda feature: {
            'fillColor': get_color(country_names.index(feature['properties']['NAME']), count_x, cmap),
            'color': 'gold',
            'fillOpacity':1,
            'opacity':0.7,
            'weight': 1,
            'dashArray': '0.8, 0.8'
        }
    ).add_to(my_map)

    # Save the map as an HTML file
    my_map.save(path.join(target_folder, 'map.html'))
