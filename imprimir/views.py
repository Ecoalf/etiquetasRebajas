from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.middleware.csrf import get_token
import pandas as pd
import zebra
from . forms import formulario

# Create your views here.

@csrf_protect
def Formulario(request):
    if request.method == 'POST':
        form = formulario(request.POST)
        print("CSRF Token:", get_token(request)) 
        if form.is_valid():
            barcode = form.cleaned_data['barcode']
            number = form.cleaned_data['number']
            
            barcode = int(barcode)
            
            # Read excel file
            excel_path = 'https://ecolabels.blob.core.windows.net/labels/Etiquetas.xlsx'
            # df = pd.read_excel("\\\\servidor\\ECOALF\\etiquetasECI\\Etiquetas.xlsx")
            df = pd.read_excel(excel_path)
            
            # Search "barcode"
            
            item = df[df['Código de barras'] == barcode]
            
            print(item) # true
            
            if not item.empty:
                description = item['Descripción de artículo'].values[0]
                model = item['Model'].values[0]
                size = item['Size'].values[0]
                color = item['Color'].values[0]
                color_description = item['Color Description'].values[0]
                precio = item['Precio de lista'].values[0]
                rebaja = item['Precio rebajado'].values[0]
                rebaja = f"{rebaja:.2f}"
                
                # Create label
                z = zebra.Zebra()
                try:
                    z.setqueue('ZDesigner ZD220-203dpi ZPL')
                except FileNotFoundError as e:
                    # Manejar la ausencia de `lpstat` o `lpr` adecuadamente
                    return render(request, 'formulario.html', {'form': form})
            
                etiqueta = f"""
                ^XA
                ^LH0,0

                ^FO12,22^A0N,20,20^FD{description}^FS
                ^FO12,50^A0N,18,18^FD{model}^FS
                ^FO12,78^A0N,18,18^FD{size}^FS
                ^FO12,106^A0N,18,18^FDColor: {color}/{color_description} ^FS

                ^FO290,70^GB50,1,1^FS  
                ^FO290,64^A0N,18,18^FD{precio}   EUR^FS  
                
                ^FO290,104^A0N,18,18^FD{rebaja}  EUR^FS  
                
                ^FO40,130^BY2.4,2,50^BEN,50,Y,N^FD{barcode}^FS

                ^XZ
                """
                
                for _ in range(number):
                    z.output(etiqueta)
                    
            return redirect('Formulario')          
    else:
        form = formulario(initial={'number': 1})    
    return render(request, 'formulario.html', {'form': form})   