import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import pandas as pd 

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


data = pd.DataFrame(columns=[''])    


def entrarespecificos(especificos, driver):
    for filtro, boton, valor in especificos:
        print(f"\nProcesando filtro: {filtro}, botón: {boton}, valor buscado: {valor}")
        
        # Guardamos el contenido original de las filas
        filas_anteriores = driver.find_elements(By.XPATH, "/html/body/form/div[3]/div/div[5]/div/table[2]/tbody/tr")
        textos_anteriores = [fila.text for fila in filas_anteriores]
        print(f"textos_anteriores: {textos_anteriores}")
        
        # Esperamos a que el contenido cambie
        def contenido_cambiado(driver):
            try: 
                filas_actuales = driver.find_elements(By.XPATH, "/html/body/form/div[3]/div/div[5]/div/table[2]/tbody/tr")
                textos_actuales = [fila.text for fila in filas_actuales]
                print(f"textos_actuales: {textos_actuales}")
            except: 
                contenido_cambiado(driver)

            return textos_actuales != textos_anteriores

        # Hacer clic en el botón correspondiente
        try:
            boton_elemento = driver.find_element("id", boton)
            print(f"Botón '{boton}' encontrado. Haciendo clic...")
            globals()['f_' + filtro + 's'] = boton_elemento.click()
        except Exception as e:
            print(f"Error al hacer clic en el botón '{boton}': {e}")
            continue

        # Esperar hasta que la fila con el valor deseado aparezca
        encontrada = False
        timeout = 10  # tiempo máximo de espera por intento
        intentos = 3  # número máximo de intentos
        intento = 0

        while not encontrada and intento < intentos:
            try:
                WebDriverWait(driver, timeout).until(contenido_cambiado)
                filas = driver.find_elements(By.XPATH, "/html/body/form/div[3]/div/div[5]/div/table[2]/tbody/tr")
                print(f"Intento {intento+1}: {len(filas)} filas encontradas.")

                for row in filas:
                    cell = row.find_element(By.XPATH, "td[2]")
                    cell_text = cell.text.lower()
                    print(f"Texto de celda: '{cell_text}'")

                    if valor.lower() in cell_text:
                        print(f"Coincidencia encontrada: '{cell_text}' contiene '{valor.lower()}'")
                        cell.click()
                        encontrada = True
                        break

                if not encontrada:
                    print(f"No se encontró coincidencia en intento {intento+1}. Esperando antes de reintentar...")
                    time.sleep(0.1)

            except Exception as e:
                print(f"Error durante la espera o búsqueda en intento {intento+1}: {e}")
            
            intento += 1

        if not encontrada:
            print(f"¡Advertencia! No se encontró el valor '{valor}' para el filtro '{filtro}' tras {intentos} intentos.")
            return 
        
        print(f"{filtro.upper()}: {valor.upper()}")


def get_bullet(nivel):
    bullets = {
        0: "●",
        1: "○",
        2: "+",
        3: "-",
    }
    return bullets.get(nivel, "")




def esperar_clickable(by, selector, driver, timeout=10):
    return WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((by, selector)))

def esperar_presente(by, selector, driver, timeout=10):
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, selector)))



def entrar(parameters, especificos, driver, nivel=0):

    for n in range(len(parameters)):
        if parameters[n][1] in ["ctl00_CPH1_BtnActividadOperativa"]:
            parameters[n] = (parameters[n][0], parameters[n][1], parameters[n][2], parameters[n][3] * 2 - 1)

    if sum(1 for param in parameters if param[2] == 1) > 4:
        print("Un máximo de 4 elementos pueden ser elegidos para contarlos en la pantalla de resultados.")
        return

    if nivel == 0:
        globals()['parametersinicial'] = parameters

    var, filtername, contar = parameters[0]

    esperar_clickable(By.NAME, filtername).click()

    rows = driver.find_elements(By.XPATH, "/html/body/form/div[3]/div/div[5]/div/table[2]/tbody/tr")
    print(f"rows encontradas: {len(rows)}")

    globals()[f'count_{var}s'] = len(rows)

    if filtername not in ["ctl00_CPH1_BtnActividadOperativa"]:
        globals()[f'countprint_{var}s'] = len(rows)
    else:
        globals()[f'countprint_{var}s'] = len(rows) // 2

    if contar == 1:
        print(f"{'  ' * nivel}hay {globals()[f'countprint_{var}s']} {var}s")

    if len(parameters) > 1:
        globals()[f'z_{var}'] = 0
        for z in range(0, globals()[f'count_{var}s'] + 1):
            if filtername not in ["ctl00_CPH1_BtnActividadOperativa"] or z % 2 == 1:
                globals()[f'z_{var}'] = z
                globals()[f'zprint_{var}'] = z if filtername not in ["ctl00_CPH1_BtnActividadOperativa"] else (z + 1) // 2

                xpath = f"/html/body/form/div[3]/div/div[5]/div/table[2]/tbody/tr[{z}]"
                esperar_clickable(By.XPATH, xpath).click()

                if contar == 1:
                    print(f"{'  ' * nivel}{get_bullet(nivel)} click en {var} {globals()[f'zprint_{var}']}")

                next_params = parameters[1:]
                nivel += 1
                entrar(next_params, especificos=especificos, nivel=nivel, driver=driver)
                nivel -= 1

    if len(parameters) == 1:
        globals()[f'z_{var}'] = 0
        for a in range(0, globals()[f'count_{var}s'] + 1):
            if filtername not in ["ctl00_CPH1_BtnActividadOperativa"] or a % 2 == 1:
                globals()[f'z_{var}'] = a
                globals()[f'zprint_{var}'] = a if filtername not in ["ctl00_CPH1_BtnActividadOperativa"] else (a + 1) // 2

                data.loc[len(data)] = [None] * len(data.columns)
                data.at[len(data)-1, 'fechadelaconsulta'] = time.ctime(time.time())

                data.at[len(data)-1, 'actproy'] = esperar_presente(By.CSS_SELECTOR, "select[id='ctl00$CPH1$DrpActProy'] option[selected='selected']").get_attribute("value")
                data.at[len(data)-1, 'ano_eje'] = esperar_presente(By.CSS_SELECTOR, "select[id='ctl00$CPH1$DrpYear'] option[selected='selected']").get_attribute("value")

                xpath_base_1 = "/html/body/form/div[3]/div/div[4]/table/tbody/tr"
                fields_1 = [item[0] for item in especificos] + [param[0] for param in globals()['parametersinicial'][:-1]]

                for x, field in enumerate(fields_1):
                    xpath = f"{xpath_base_1}[{x+2}]/td[2]"
                    data.at[len(data)-1, field] = esperar_presente(By.XPATH, xpath).text.strip()

                xpath_base_2 = f"/html/body/form/div[3]/div/div[5]/div/table[2]/tbody/tr[{a}]/td"
                fields_2 = ['POI_aprobado', 'PIA', 'POI_consistente_PIA', 'PIM', 'POI modificado', 'DEV', 'ejecutado', 'POI/PIA']
                fields_2.insert(0, globals()['parametersinicial'][-1][0])

                for x, field in enumerate(fields_2):
                    xpath = f"{xpath_base_2}[{x+2}]"
                    value = esperar_presente(By.XPATH, xpath).text.strip()
                    data.at[len(data)-1, field] = value


    conteobacks = len(driver.find_elements(By.XPATH, "//*[starts-with(@id, 'ctl00_CPH1_RptHistory_ctl') and substring(@id, string-length(@id) - 2) = 'TD0']"))
    esperar_clickable(By.ID, f"ctl00_CPH1_RptHistory_ctl{str(conteobacks).zfill(2)}_TD0").click()
    globals()[f'conteobacks_{var}'] = conteobacks
    
    

def scrape_ceplan():
    
    # actproy='Proyecto'
    # actproy='Actividad'
    actproy='ActProy'

    year=2024

    #### Regional ####
    especificos = [
        ("nivel_gobierno","ctl00_CPH1_BtnTipoGobierno","regional"),
        ("sector","ctl00_CPH1_BtnSector","99: gobiernos regionales"),
        ("pliego","ctl00_CPH1_BtnPliego","loreto"),
        ("categoria_pptal","ctl00_CPH1_BtnProgramaPpto","57")
        ]
    
    # parameters= [(nombre del filtro, name del boton como elemento de pagina web, dummy print, empezar desde)]

    parameters = [
        ("ejecutora","ctl00_CPH1_BtnEjecutora",1),
        ("c_costo","ctl00_CPH1_BtnCentroCosto",1),
        ("act_op","ctl00_CPH1_BtnActividadOperativa",1)
        ]


    options = Options()
    options.headless = True  # Hacer que el navegador no se abra visualmente (modo headless)

    # Configuración del driver de Selenium
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Acceder a la página principal
    url = "https://app.ceplan.gob.pe/ConsultaCEPLAN/consulta/Default.aspx?y=" + str(year) + "&ap="+str(actproy)

    driver.get(url)
    
    driver.switch_to.frame("frame0")

    entrarespecificos(especificos, driver)

    entrar(parameters, especificos, driver)


    # Extraer el contenido de la página después del clic
    content = driver.page_source

    # Cerrar el navegador
    driver.quit()

    if not content:
        return "No se encontró contenido en la página."

    return data
