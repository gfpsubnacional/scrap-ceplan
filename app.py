import streamlit as st
from scraper import scrape_ceplan  # Asegúrate de que este archivo esté en la misma carpeta

# Título de la página
st.title("Web Scraper de CEPLAN")

# Inputs del usuario
gobierno_regional = st.text_input("Ingrese el nombre del Gobierno Regional:")
categoria_presupuestal = st.text_input("Ingrese la Categoría Presupuestal:")

# Botón para ejecutar el scraping
if st.button("Scrapear"):
    if gobierno_regional and categoria_presupuestal:
        with st.spinner("Ejecutando el scraping..."):
            resultado = scrape_ceplan(gobierno_regional, categoria_presupuestal)

        if resultado is not None and not resultado.empty:
            st.success("Resultado del Scraping:")
            st.dataframe(resultado)
        else:
            st.error("No se obtuvieron datos del scraping.")
    else:
        st.warning("Por favor, complete ambos campos.")
