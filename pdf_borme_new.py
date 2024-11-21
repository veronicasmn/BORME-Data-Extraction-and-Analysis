from os.path import exists
import requests
import PyPDF4
import os
from lxml import etree
import datetime

def download_file(url):
    local_filename = url.split('/')[-1]
    
    if not exists(local_filename):
        with requests.get(url) as r:
            with open(local_filename, 'wb') as f:
                f.write(r.content)

    return local_filename

def get_owners(info):
    info = info.lower()
    adm = info.split("adm.")
    owners = []
    
    if len(adm) > 1:
        adm_string_field = adm[1].split(":")[1].split(".")[0]
        adm_names = adm_string_field.split(";")
        for name in adm_names:
            name = name.strip().split(" ")
            name = ' '.join([n.capitalize() for n in name if n != ''])
            owners.append(name) 
            
    else: 
        presi = info.split("presidente")
        if len(presi) > 1:
            presi_string_field = presi[1].split(":")[1].split(".")[0]
            presi_names = presi_string_field.split(";")
            for name in presi_names:
                name = name.strip().split(" ")
                name = ' '.join([n.capitalize() for n in name if n != ''])
                owners.append(name) 

    return owners

def get_openings_borme(pdf_url, province):
    pdf_file = download_file(pdf_url)
    pdfFileObj = open(pdf_file, 'rb')
    pdfReader = PyPDF4.PdfFileReader(pdfFileObj)
    numpages = pdfReader.numPages

    possible_openings = []
    palabras_clave = [''] #aquí deben poner las palabras clave relacionadas con la tipología del sector

    for page in range(numpages):
        pageObj = pdfReader.getPage(page)
        text = pageObj.extractText()

        text = text.split("\n")
        empresas = []
        empresas_info = [i for i,x in enumerate(text) if x==' - ']

        for i, index in enumerate(empresas_info):
            try: 
                next_empresa = empresas_info[i+1] - empresas_info[i]
                empresas.append({
                    'Empresa': text[index+1],
                    'Accion': text[index+2],
                    'Informacion': [x for x in text[index+3:index+next_empresa-1]]})

            except IndexError:
                pass

        for empresa in empresas:
            interesante = False
            empresa['Domicilio'] = None
            informacion = empresa["Informacion"]
            
            if any(action in empresa['Accion'] for action in ['Constitución.']):
                for info in informacion:
                    info = info.lower()
                    if any(palabra in info for palabra in palabras_clave):
                        interesante = True
            
            if interesante: 
                domicilio = ''
                for info in informacion:
                    if 'Domicilio:' in info:
                        domicilio = info.split('Domicilio:')[-1].strip()  # Limpieza del domicilio
                        break
                    
                empresa['Domicilio'] = domicilio.lower().strip() if domicilio else None
                
                otra_info = ''.join([f'{x} ' for x in informacion if x != ' '])
                empresa["Informacion"] = otra_info
                administradores = get_owners(empresa['Informacion'])
                empresa["Administradores"] = administradores if administradores else None
                empresa["Provincia"] = province
                possible_openings.append(empresa)

    pdfFileObj.close()
    os.remove(pdf_file)

    return possible_openings

def get_borme_data(date='Today', search_province=None):
    if date == 'Today':
        today = datetime.date.today()
        date = today.strftime('%Y%m%d')

    seed_url = 'https://www.boe.es'
    summary_url = f'/datosabiertos/api/borme/sumario/{date}'

    print(f'· Checking if there is a BORME report for date {date[6:8]}/{date[4:6]}/{date[0:4]}')
    full_url = seed_url + summary_url
    print(full_url) 
    page = requests.get(full_url, headers={"Accept": "application/xml"})

    if page.status_code != 200:
        print(f"Error: No se pudo obtener datos para la fecha {date}. Código de estado: {page.status_code}.")
        return []
    
    root = etree.fromstring(page.content)

    print(f'\n· Looking for provinces in the summary')
    borme_provinces = []
    for section in root.xpath('//sumario/diario/apartado'):
        province = section.findtext('provincia')
        if province == search_province:
            pdf_url = section.findtext('url_pdf')
            if pdf_url:
                try:
                    full_pdf_url = seed_url + pdf_url
                    borme_provinces += get_openings_borme(full_pdf_url, province)
                except Exception as e:
                    print(f"Error reading PDF for {province}: {e}")

    print(f'\n· Checking BORME report for {search_province} on {date}')
    return borme_provinces


