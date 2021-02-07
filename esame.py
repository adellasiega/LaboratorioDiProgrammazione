# Esame laboratorio di programmazione, appello 09/02/2021, Alessandro Della Siega

class ExamException(Exception):

        pass

class CSVTimeSeriesFile: # Classe istanziata sul nome del file e con metodo get_data
    
    def __init__(self, name):
        self.name = name

        if not isinstance(self.name, str): # Controllo che la classe venga istanziata correttamente
            raise ExamException('La classe va istanziata su una stringa che contiene il nome di un file!')
    
    def get_data(self):
        time_series = [] # Lista in cui andranno inserite le liste annidate formate da due dati: epoch e temperatura
        
        try: # Controllo che sia possibile aprire il file, nel caso in cui non esista o non sia leggibile alzo un eccezione
            myfile = open(self.name, 'r')
        
        except Exception as e: # Faccio in modo che venga alzata un'eccezione "ExamException"
            raise ExamException('Impossibile aprire il file: {}\n ({})'.format(self.name, e)) from None # Non tengo traccia dell'eccezione specifica che ha generato l'errore
            return None
            
        for line in myfile: # Dal file csv, linea per linea, converto i dati da stringa a int e float e li inserisco in time_series
            single_time_series = [] # Lista che conterrà un epoch e relativa temperatura
            data = line.split(',') # Divido la linea sulla virgola e salvo in "data" le due stringhe appena create

            try: # Provo a convertire le due stringhe e le salvo in due variabili
                epoch = int(data[0])
                temperature = float(data[1])

                if temperature == 0: # Da specifiche, una temperatura nulla va ignorata, dunque passo alla linea successiva
                    continue
                
                single_time_series.append(epoch)  # Aggiungo alla lista i valori epoch e temperature
                single_time_series.append(temperature)

                time_series.append(single_time_series) # Aggiungo alla lista principale la lista con i valori epoch e temperature

            except: # Nel caso si verifichi qualche eccezione nel convertire le stringhe in int/float semplicemente ignoro la linea che genera il problema e passo alla linea del file successiva
                continue

        # Controllo che i timestamp siano ordinati e non ci siano duplicati, in caso contrario alzo un'eccezione
        for i in range(0, len(time_series)-1):
            for j in range (i+1, len(time_series)):
                if time_series[i][0] >=  time_series[j][0]:
                    raise ExamException('Timestamp non ordinati o duplicati!')
        
        return time_series


def daily_stats(time_series): # Funzione che prende in input una time_series generata da get_data e crea una nuova lista di liste dove ci sono le statistiche riguardo la temperatura giorno per giorno
    
    if not isinstance(time_series, list) or len(time_series) == 0: # Controllo che venga inserita una lista e che non sia vuota
        raise ExamException('La lista time_series inserita è vuota o non è una lista!')

    for item in time_series: #Controllo che venga inserita una lista con elementi che possano essere processati dagli algoritmi di questa funzione
        if (not isinstance(item, list)) or (len(item) != 2) or (not isinstance(item[0], int)) or (not isinstance(item[1], float)):
            raise ExamException("La lista inserita non è una lista 'time_series'")
    
    daily_stats_list = [] # Lista in cui andranno inserite le statistiche giornaliere anch'esse raccolte in liste di tre elementi: minimo giornaliero, massimo giornaliero e media giornaliera

    # Cicli annidati che suddividono la lista in giornate e calcolano le statistiche richieste
    
    i = 0 # Indice che si riferisce alla posizione nella lista della prima misurazione di ciascuna giornata
    
    while i < len(time_series):

        max = time_series[i][1] # Imposto, per ora, la prima temperatura di ogni giornata come massimo e minimo della giornata
        min = time_series[i][1]
        sum = 0 # Variabile in cui confluirà la sommatoria delle temperatura della i-esima giornata
        single_day_stat = [] # Lista che conterrà le statistiche della singola giornata

        j = i # Indice che scorre sulle varie misurazioni, ovviamente deve partire da i che indica la prima misurazione giornaliera
        c = 0 # Contatore delle misurazioni presenti in ogni giornata, valore necessario per calcolare la temperatura media giornaliera
        
        while (j < len(time_series)) and (time_series[j][0] // 86400 == time_series[i][0] // 86400): # Il ciclo while su j deve continuare finchè l'epoch della j-esima misurazione appartiene alla i-esima giornata, utilizzo la divisione intera per capire a quale giorno si riferisca l'epoch

            if time_series[j][1] > max: # Via via aggiorno il massimo e minimo giornaliero
                max = time_series[j][1]
            
            if time_series[j][1] < min:
                min = time_series[j][1]

            sum += time_series[j][1] # Aggiorno la sommatoria delle temperature
            
            c += 1 # Aggiorno il contatore 
            j += 1 # Passo alla misurazione successiva

        average = sum/c # Una volta passate tutte le misurazioni della i-esima giornata posso calcolarne la media

        single_day_stat.append(min) # Aggiungo alla lista le statistiche
        single_day_stat.append(max)
        single_day_stat.append(average)
        
        daily_stats_list.append(single_day_stat) # Aggiungo alla lista principale la lista delle statistiche giornaliere

        i = j # La giornata successiva inizia dopo l'ultima misurazione della giornata precedente

    return daily_stats_list