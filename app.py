import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px


st.set_page_config(
    page_title="Inteligo Venture Capital",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")

##load data

# Definir la ruta del archivo CSV
csv_path = 'data/k12_latam_enrollment_total.csv'

# Cargar el DataFrame desde el archivo CSV con el separador correcto y eliminando espacios en blanco
df = pd.read_csv(csv_path, sep=';', skipinitialspace=True)

# Convertir a formato largo
df_reshaped = pd.melt(df, id_vars=['Country'], var_name='year', value_name='value')



##sidebar
with st.sidebar:
    st.title('Dealflow Dashboard')
    
    year_list = list(df_reshaped.year.unique())[::-1]
    
    selected_year = st.selectbox('Select a year', year_list, index=len(year_list)-1)
    df_selected_year = df_reshaped[df_reshaped.year == selected_year]
    #df_selected_year_sorted = df_selected_year.sort_values(by="population", ascending=False)

    color_theme_list = ['blues', 'cividis', 'greens', 'inferno', 'magma', 'plasma', 'reds', 'rainbow', 'turbo', 'viridis']
    selected_color_theme = st.selectbox('Select a color theme', color_theme_list)



##layout
col = st.columns((2, 2, 1), gap='medium')



##K12 total latam
def graficar_k12_total_latam(csv_path):
    # Cargar el DataFrame desde el archivo CSV con el separador correcto y eliminando espacios en blanco
    df = pd.read_csv(csv_path, sep=';', skipinitialspace=True)

    # Convertir a formato largo usando 'Country' en lugar de 'Categoría'
    df_long = pd.melt(df, id_vars=['Country'], var_name='year', value_name='value')

    # Convertir las columnas 'Year' y 'Value' al tipo correcto
    df_long['year'] = df_long['year'].str.strip()
    df_long['value'] = df_long['value'].str.replace('.', '').astype(float)

    # Crear la gráfica de áreas con Plotly
    fig = px.area(df_long, x='year', y='value', color='Country', line_group='Country', markers=True)

    # Devolver la figura
    return fig


def crear_choropleth_latam(csv_path):
    # Cargar el DataFrame desde el archivo CSV con el separador correcto y eliminando espacios en blanco
    df = pd.read_csv(csv_path, sep=';', skipinitialspace=True)

    # Tomar solo las filas del último año disponible
    last_year = df.columns[-1]
    df = df[['Country', last_year]].copy()
    df.columns = ['Country', 'Value']
    
    # Limpiar los valores y convertir a flotante
    df['Value'] = df['Value'].str.replace('.', '').astype(float)
    
    # Corrección de nombres de países
    country_corrections = {
        'Brasil': 'Brazil',
        'CR': 'Costa Rica'
    }
    df['Country'] = df['Country'].replace(country_corrections)
    
    # Crear el mapa coroplético con Plotly
    fig = px.choropleth(df, locations='Country', locationmode='country names',
                        color='Value', hover_name='Country',
                        color_continuous_scale=px.colors.sequential.Plasma,
                        title=f'Enrollment in Latin America ({last_year})')
    
    # Ajustar el diseño del mapa para enfocarse en América Latina y usar tema oscuro
    fig.update_geos(
        visible=False, resolution=50,
        showcountries=True, countrycolor="Black",
        showcoastlines=True, coastlinecolor="Black",
        showland=True, landcolor="black",
        projection_type='mercator',
        lonaxis_range=[-120, -30], lataxis_range=[-60, 30]
    )

    fig.update_layout(
        paper_bgcolor='black',
        plot_bgcolor='black',
        geo=dict(bgcolor='black'),
        font=dict(color='white'),
        title_font=dict(size=24),
        height=800,
        width=1200
    )

    # Devolver la figura
    return fig


with col[0]:
    #st.markdown('## Enrollment in Latin America')

    k12_total_map = crear_choropleth_latam(csv_path)
    st.plotly_chart(k12_total_map, use_container_width=True)

with col[1]:
    #st.markdown('## K12 Enrollment')
    
    k12_total_latam = graficar_k12_total_latam(csv_path)
    st.plotly_chart(k12_total_latam, use_container_width=True)
    