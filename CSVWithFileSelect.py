import pandas as pd
import plotly.express as px
import os
import tkinter as tk
from tkinter import filedialog
import pandas as pd
from datetime import datetime

# Create a Tkinter root window (it will be hidden)
root = tk.Tk()
root.withdraw()

# Ask the user to select a CSV file
file_path = filedialog.askopenfilename(title="Select a CSV file", filetypes=[("CSV files", "*.csv")])

def process_array(arr):
    result = arr.copy()
    count_false = 0
    last_true_index = -1

    for i in range(len(result)):
        if result[i] is False:
            count_false += 1
        else:
            if count_false > 0 and count_false < 10:
                for j in range(last_true_index + 1, i):
                    result[j] = True
            count_false = 0
            last_true_index = i

    # Check for the end of the array
    if count_false > 0 and count_false < 10:
        for j in range(last_true_index + 1, len(result)):
            result[j] = True

    return result  

# Check if a file was selected
if file_path:

    # CSV dosyalarını oku
    veri1 = pd.read_csv(file_path, encoding='ISO-8859-9')

    # 'durumu' ve 'zaman' sütunlarını al

    veri1["Insan Bilgisayar Onunde"] = veri1["Insan Bilgisayar Onunde"].astype(bool)
    veri1["Insan Makine Onunde"] = veri1["Insan Makine Onunde"].astype(bool)

    veri1["Makine İnsan Etkileşimi"] = veri1["Insan Bilgisayar Onunde"] | veri1["Insan Makine Onunde"]

    durum1 = veri1['Makine']
    durum2 = veri1['Makine İnsan Etkileşimi']

    
    zaman1 = veri1['Timestamp']

    zaman_str = veri1['Timestamp'] = pd.to_datetime(veri1['Timestamp'], unit='s').dt.strftime('%H:%M:%S')
    
    

    modified_array1 = process_array(durum1)


    true_indices1 = [i for i, value in enumerate(modified_array1)]


    modified_array2 = process_array(durum2)

    true_indices2 = [i for i, value in enumerate(modified_array2)]


    # Create y-values for modified_array1 and modified_array2
    y_values1 = [1 if value else 0 for value in modified_array1]
    y_values2 = [1 if value else 0 for value in modified_array2]
    
    # Değerleri 'TRUE' ve 'FALSE' olarak değiştir
    durum1 = durum1.replace({True: 1, False: 0})
    durum2 = durum2.replace({True: 1, False: 0})

    durum1 = durum1[::-1]
    durum2 = durum2[::-1]

    # Sürekli zaman dilimlerini hesapla
    zaman_araligi1 = (zaman1 - zaman1.shift()).fillna(0)

    calismaSuresi1 = durum1.sum()
    calismaSuresi2 = durum2.sum()


    # Plotly ile detaylı grafik oluşturma (önceki kod ile aynı)
    fig = px.line()
    fig.add_scatter(x=true_indices1, y=y_values1, mode='lines+markers', name='Makine Hareketi', line=dict(width=2), marker=dict(color='red'))
    fig.add_scatter(x=true_indices2, y=y_values2, mode='lines+markers', name='Makine İnsan Etkileşimi', line=dict(width=2), marker=dict(color='blue'))
    
    fig.update_traces(line=dict(width=2, shape='hv'))
    
    fig.update_layout(
        title='Durum Zaman Grafiği',
        xaxis_title='Zaman',
        yaxis_title='Durumu',
        xaxis=dict(showgrid=True, gridwidth=1, gridcolor='lightgrey'),  # Izgara özellikleri
        yaxis=dict(showgrid=True, gridwidth=1, gridcolor='lightgrey'),
        legend=dict(title='Veri Setleri'),  # Açıklamaların başlığı
        plot_bgcolor='white',  # Grafik arka plan rengi
    )
    
        # Update y-axis labels
    fig.update_layout(yaxis=dict(
        tickvals=[1, 0],  # Custom tick positions
        ticktext=['TRUE', 'FALSE']  # Custom tick labels
    ))

    calismaSuresi1_str = datetime.now().replace(
                hour=int(calismaSuresi1 // 3600),
            minute=int((calismaSuresi1 % 3600) // 60),
            second=int(calismaSuresi1 % 60)
        ).strftime("%H:%M:%S")
    
    calismaSuresi2_str = datetime.now().replace(
                hour=int(calismaSuresi2 // 3600),
            minute=int((calismaSuresi2 % 3600) // 60),
            second=int(calismaSuresi2 % 60)
        ).strftime("%H:%M:%S")
    
    calismaSuresi3_str = datetime.now().replace(
            hour=int(len(y_values2) // 3600),
        minute=int((len(y_values2) % 3600) // 60),
        second=int(len(y_values2) % 60)
    ).strftime("%H:%M:%S")
    
    # Grafik üzerine toplam "TRUE" sürelerini metin olarak ekleme
    fig.add_annotation(x=1.15, y=0.75,
                       text=f'Makine Hareketi Toplam Süre : {calismaSuresi1_str}',
                       showarrow=False, font=dict(color='blue', size=12), align='right', xref='paper', yref='paper')

    fig.add_annotation(x=1.15, y=0.7,
                       text=f'Makine İnsan Etkileşimi Toplam Süre : {calismaSuresi2_str}',
                       showarrow=False, font=dict(color='red', size=12), align='right', xref='paper', yref='paper')
    
    fig.add_annotation(x=1.15, y=0.65,
                       text=f'Toplam Süre : {calismaSuresi3_str}',
                       showarrow=False, font=dict(color='black', size=12), align='right', xref='paper', yref='paper')


    fig.update_traces(marker=dict(size=1))  # Nokta boyutları

    fig.show()

    file_name = os.path.basename(file_path)
    
    # Save the figure as HTML
    fig.write_html(f"{file_name}.html")