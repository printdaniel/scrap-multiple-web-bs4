from constantes import *
from bs4 import BeautifulSoup
import requests


class InfoExtractor:
    def __init__(self):
        #Clima datos
        self.clima_meteored()
        self.clima_accuweather()
        self.clima_pextendido()
        self.clima_infclima()
        #Dollar y uva
        self.valor_uva()
        self.valor_dolar()

    def soup_validator(self,url):
        """ Retorna el html parseado """
        header = {
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)'
                }

        page = requests.get(url,headers = header)
        try:
            soup = BeautifulSoup(page.content,"html.parser")
        except:
            return None
        return soup
    

    def clima_meteored(self):
        """ Retorna el estado y temperatura según el sitio meteored"""
        soup = self.soup_validator(METEORED)
        temp_data = soup.find_all('span',attrs={'class':'dato-temperatura changeUnitT'})
        estado_data = soup.find_all('span',attrs={'descripcion'})
        for e in estado_data:
            self.meteored_e = e.text
        for i in temp_data:
            self.meteored_t = i.text
        return self.meteored_e,self.meteored_t


    def clima_accuweather(self):
        """ Retorna el estado y temperatura según el sitio Accuweather"""
        sopa = self.soup_validator(ACUWEATHER)
        temp_data = sopa.find_all('div',attrs={'class':'temp'})
        estado_data = sopa.find_all('div',attrs={'class':'phrase'})
        for t in temp_data:
            self.accuweather_t = t.text
            break

        for e in estado_data:
            self.accuweather_e = e.text
            break
        return self.accuweather_e,self.accuweather_t

    
    def clima_pextendido(self):
        """ Retrona el estado y la temperatura según el sitio Pronostico Extendido"""
        sopa = self.soup_validator(PRONOSTICO_EXTENDIDO)
        temp_data = sopa.find_all('span',attrs={'class':'prono-ahora-izq-cond-t'})
        estado_data = sopa.find_all('p',attrs={'class':'prono-ahora-cond'})
        for t in temp_data:
            self.pextendido_t = t.text

        for e in estado_data:
            self.pextendido_e = e.text
        return self.pextendido_e,self.pextendido_t


    def clima_infclima(self):
        """Retorna el estado y la temperatura según el sitio Info Clima"""
        sopa = self.soup_validator(INFO_CLIMA)
        temp_data = sopa.find_all('div',attrs={'class':'d1'})
        estado_data = sopa.find_all('div',attrs={'d1'})
        
        for t in temp_data:
            if t.find('p') != None:
                sub = t.find('p').text
                self.infoClima_t = sub
                break
        for e in estado_data:
            self.infoClima_e = e.text.replace('\n','')
            break
        return self.infoClima_e,self.infoClima_t

    def computrabajo(self):
        """Retrona las ofertas de trabajo admnistrativo 
        de la página computrabjo """
        
        sopa = self.soup_validator(COMPU_TRABAJO)
        content_data = sopa.find_all('div',attrs={'class':'w100 bClick'})
        count = 0 
        
        for i in content_data:
            sub = i.find('a')
            print(sub.text)
            count += 1
            if count == 12:
                break

    def valor_uva(self):
        """Retorna el valor UVA del BCRA Argentina"""
        
        sopa = self.soup_validator(UVA)
        content_data = sopa.find_all('div','col-md-12')
        for i in content_data:
            self.uva = i.text.replace('\n','')
        return self.uva

    def valor_dolar(self):
        """Retorna el valor de venta del dollar ofcial"""

        sopa = self.soup_validator(DOLLAR)
        content_data = sopa.find_all('div','values')
        for i in content_data:
            self.dollar = i.text.replace('\n','')
        return self.dollar

    def Main(self):
        """Controla el formato y flujo de información"""

        print(f"{'Clima':=^42}")
        print(f"{'Estado':.<30} {'Temperatura'}")
        print("METEORED")
        print(f"{self.meteored_e:.<30} {self.meteored_t}")
        print("ACCUWEATHER")
        print(f"{self.accuweather_e:.<30} {self.accuweather_t}")
        print("PRONOSTICO EXTENDIDO")
        print(f"{self.pextendido_e:.<30} {self.pextendido_t}")
        print("INFOCLIMA")
        print(f"{self.infoClima_e:.<30} {self.infoClima_t}")
        print(f"{'Dollar y UVA':=^42}")
        print("DOLLAR")
        print(self.dollar)
        print("\nUnidad de Valor Adquisitivo")
        print(self.uva,"\n")
        print(f"{'Computrabajo':=^42}")
        self.computrabajo()


if __name__ == '__main__':
    inf = InfoExtractor()
    inf.Main()
    
