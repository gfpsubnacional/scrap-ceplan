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
    if resultado:
        st.success("Resultado del Scraping:")
        st.write(resultado)
    else:
        st.error("Hubo un error al hacer el scraping.")
