import fitz  # PyMuPDF

def extract_unique_activities_from_pdf(pdf_path):
    unique_activities = set()  # Usamos un conjunto para frases únicas
    print(f"Abriendo el PDF en la ruta: {pdf_path}")

    # Abre el archivo PDF
    with fitz.open(pdf_path) as pdf:
        print(f"Número total de páginas en el PDF: {pdf.page_count}")
        
        # Recorre cada página del PDF
        for page_num in range(pdf.page_count):
            print(f"Procesando página: {page_num + 1}/{pdf.page_count}")
            page = pdf.load_page(page_num)
            text = page.get_text("text")
            print(f"Texto extraído de la página {page_num + 1}: {text[:100]}...")  # Muestra solo los primeros 100 caracteres
            
            # Busca las secciones que comienzan con "ACTIVIDAD PRINCIPAL" y terminan en "Domicilio"
            start_idx = 0
            while True:
                start_idx = text.find("ACTIVIDAD PRINCIPAL", start_idx)
                
                # Si no se encuentra más "ACTIVIDAD PRINCIPAL", termina la búsqueda en esta página
                if start_idx == -1:
                    print(f"No se encontraron más 'ACTIVIDAD PRINCIPAL' en la página {page_num + 1}.")
                    break
                
                end_idx = text.find("Domicilio", start_idx)
                
                # Extrae el texto si ambas frases fueron encontradas
                if end_idx != -1:
                    activity_text = text[start_idx + len("ACTIVIDAD PRINCIPAL"):end_idx].strip()
                    print(f"Actividad encontrada: '{activity_text}'")  # Muestra la actividad encontrada
                    unique_activities.add(activity_text)  # Agrega la actividad al conjunto para evitar duplicados
                else:
                    print(f"No se encontró 'Domicilio' después de 'ACTIVIDAD PRINCIPAL' en la página {page_num + 1}.")
                
                # Mueve el índice para la siguiente búsqueda
                start_idx = end_idx + len("Domicilio") if end_idx != -1 else -1
            
    print(f"Total de actividades únicas extraídas: {len(unique_activities)}")
    return unique_activities

pdf_path = '/home/veronica/Desktop/git_repos/dammPipelines/src/new_openings/BORME-A-2024-205-08.pdf'
unique_activities = extract_unique_activities_from_pdf(pdf_path)

# Imprime las actividades únicas
print("Actividades únicas extraídas del PDF:")
for activity in unique_activities:
    print(activity)
