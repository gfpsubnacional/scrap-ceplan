import streamlit as st
from scraper import scrape_ceplan  # Asegúrate de que este archivo esté en la misma carpeta

# Título de la página
st.title("Web Scraper de CEPLAN")

# Botón para ejecutar el scraping
if st.button("Scrapear"):
    with st.spinner("Ejecutando el scraping..."):
        # Llamar a la función de scraping
        resultado = scrape_ceplan()

    # Mostrar el resultado
    if resultado is not None and not resultado.empty:
        st.success("Resultado del Scraping:")
        st.dataframe(resultado)
    else:
        st.error("No se obtuvieron datos del scraping.")
