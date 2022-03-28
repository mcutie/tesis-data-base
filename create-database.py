from obspy import read
import  obspy.io.nordic.core as nd
import pandas as pd
import string, os, sys

dir_rea = 'D:\\TESIS\\datos\\rea'
dir_wav = 'D:\\TESIS\\datos\\wav'
dir_output = 'D:\\TESIS\\datos'
files_rea = os.listdir(dir_rea)
df = pd.DataFrame(columns=['Origin_Time',
                           'Latitude',
                           'Longitude',
                           'Depth',
                           'RMS',
                           'ML',
                           'P_time',
                           'Distance',
                           'Back_Azimuth',
                           'Azimuth',
                           'WAV_file',
                           'Z_data',
                           'N_data',
                           'E_data'
                           ])

for f in files_rea:
    print ('Archivo REA :',dir_rea + os.sep + f)
    waveForms= nd.readwavename(dir_rea + os.sep + f)
    print('Cantidad de waveform :',len(waveForms))
    print (waveForms)
    #---------------Ejecuto solo si el evento contiene los waveforms ------------
    if len(waveForms) != 0 :
        event= nd.read_nordic(dir_rea + os.sep + f)[0]    
        with open(dir_rea + os.sep + f, "r") as archivo_lectura:
            for linea in archivo_lectura: 
                if "RCC"  in linea:  #----- Busco la linea para extraer azimuth y distancia
                    if "HZ" in linea or "BZ" in linea:                
                        salida = linea
                        print(salida)
                        back_azimuth = int(salida[76:79])
                        azimuth = abs(back_azimuth -180)
                        print(back_azimuth)
                        distance = float(salida[70:75])
                        print(distance)
        #print(event.origins[0])
        #print(event.origins[0].time)
        #print(event.origins[0].latitude)
        #print(event.origins[0].longitude)
        #print(event.origins[0].depth)
        #print(event.origins[0].quality.standard_error)
        #print(event.magnitudes[0].mag)    
        #print(len(event.picks))
        # ------------Selecciono el tiempo de P solo de RCC ---------
        for pick in event.picks:            
            if pick.waveform_id.station_code == "RCC" and pick.waveform_id.channel_code == "HZ" and pick.phase_hint == "P":
                p_time_arrival= pick.time
                print (p_time_arrival)
                start_time=p_time_arrival - 0.5
                print (start_time)
                end_time= p_time_arrival + 1
                print (end_time)
        # ------------- Selecciono solo la traza que contenga RCC
        for waveForm in waveForms:         
            st= read(dir_wav + os.sep + waveForm)            
            tmp =  st.select(station="RCC")
            print('el select de RCC',tmp)
            if  len(tmp) != 0:
                #st.plot()
                rcc=tmp
                #rcc.plot()
                rcc_filtered=rcc.filter("bandpass",freqmin=3,freqmax=15)
                #rcc_filtered.plot()                
                rcc_sliced= rcc_filtered.slice(start_time, end_time)
                #rcc_sliced.plot()

                new_row = {'Origin_Time':event.origins[0].time,
                           'Latitude':event.origins[0].latitude,
                           'Longitude':event.origins[0].longitude,
                           'Depth':event.origins[0].depth,
                           'RMS':event.origins[0].quality.standard_error,
                           'ML':event.magnitudes[0].mag,
                           'P_time': p_time_arrival,
                           'Distance': distance,
                           'Back_Azimuth': back_azimuth,
                           'Azimuth': azimuth,
                           'WAV_file': waveForm,
                           'Z_data':rcc_sliced[0].data,
                           'N_data':rcc_sliced[1].data,
                           'E_data':rcc_sliced[2].data
                          }
                df = pd.concat([df, pd.DataFrame([new_row])]).reset_index(drop=True)
                #df['Z_data'] = df['Z_data'].map(list)
                #df['N_data'] = df['N_data'].map(list)
                #df['E_data'] = df['E_data'].map(list)
                print(df)
df.to_csv(dir_output + os.sep +'rcc_earthquake_database.csv')
