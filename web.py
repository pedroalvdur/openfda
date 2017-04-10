import http.server
import json
import http.client

class OpenFDARedirect():

    def redirect_list(self,limit,funcion):
        html='''
        <html>
        <head>
           <!-- HTML meta refresh URL redirection -->
           <meta http-equiv="refresh"
        '''
        html+='content="0; url=http://212.128.254.41:8000/'+funcion+'?limit='+limit+'">'
        html+='''
        </head>
        <body>
            <h1>OpenFDA REDIRECTING</h1>
            Será redirigido a la página que desea en unos segundos...
        </body>
        </html>
        '''
        return html

    def redirect_search(self,limit,funcion,search):
        html='''
        <html>
        <head>
           <!-- HTML meta refresh URL redirection -->
           <meta http-equiv="refresh"
        '''
        html+='content="0; url=http://212.128.254.41:8000/'+funcion+'?limit='+limit+'&'+search+'">'
        html+='''
        </head>
        <body>
            <h1>OpenFDA REDIRECTING</h1>
            Será redirigido a la página que desea en unos segundos...
        </body>
        </html>
        '''
        return html

    def similar_path(self,url,funcion):
        inside=False
        letras=0
        for i in range(len(url)):
            if url[i] in funcion:
                letras+=1
        if letras>=(len(funcion)-2):
            inside=True
        return inside

class OpenFDAClient():

    #URL
    OPENFDA_API_URL='api.fda.gov'
    OPENFDA_API_EVENT='/drug/event.json'


    #GET EVENTS
    def get_events(self,limit):
        conn=http.client.HTTPSConnection(self.OPENFDA_API_URL)
        conn.request('GET',self.OPENFDA_API_EVENT + '?limit='+limit+'')
        r1=conn.getresponse()
        data1=r1.read()
        events=data1.decode('utf8')
        return events

    def get_events_search(self,search,limit):
        conn=http.client.HTTPSConnection(self.OPENFDA_API_URL)
        conn.request('GET',self.OPENFDA_API_EVENT + '?search='+search+'&limit='+limit+'')
        r1=conn.getresponse()
        data1=r1.read()
        events=data1.decode('utf8')
        return events

    def get_events_error(self,search):
        conn=http.client.HTTPSConnection(self.OPENFDA_API_URL)
        conn.request('GET',self.OPENFDA_API_EVENT + '?search='+search+'&limit=10')
        r1=conn.getresponse()
        data1=r1.read()
        events=data1.decode('utf8')
        return events

class OpenFDAParser():

    #GET LISTS
    def get_drug_list(self,events):
        lista=[]
        for event in events:
            lista=lista+[event['patient']['drug'][0]['medicinalproduct']]
        return lista

    def get_companynumb(self,events):
        lista=[]
        for event in events:
            lista=lista+[event['companynumb']]
        return lista

    def get_patientsex(self,events):
        lista=[]
        for event in events:
            lista=lista+[event['patient']['patientsex']]
        return lista

class OpenFDAHTML():

    #MAIN PAGE
    def get_main_page(self):
        html='''
        <html>
            <head>
                <title>OpenFDA Cool App</title>
            </head>
            <body>
                <h1 align='center'><u>OpenFDA Client</u></h1>
                <table style="width:100%">
                    <tr>
                        <th align='left'>·Show list of drugs:</th>
                    </tr>
                    <tr>
                        <td><br></td>
                    </tr>
                    <tr>
                        <td>
                            <form method='get' action='listDrugs'>
                                <input type='text' size='3' maxlength='2' name='limit'></input>
                                <input type='submit' value='Drug list: Send to OpenFDA'></input>
                            </form>
                        </td>
                    </tr>
                    <tr>
                        <td><br></td>
                    </tr>
                    <tr>
                        <th align='left'>·Show list of companies:</th>
                    </tr>
                    <tr>
                        <td><br></td>
                    </tr>
                    <tr>
                        <td>
                            <form method='get' action='listCompanies'>
                                <input type='text' size='3' maxlength='2' name='limit'></input>
                                <input type='submit' value='Company list: Send to OpenFDA'></input>
                            </form>
                        </td>
                    </tr>
                    <tr>
                        <td><br></td>
                    </tr>
                    <tr>
                        <th align='left'>·Show list of patient gender:</th>
                    </tr>
                    <tr>
                        <td><br></td>
                    </tr>
                    <tr>
                        <td>
                            <form method='get' action='listGender'>
                                <input type='text' size='3' maxlength='2' name='limit'></input>
                                <input type='submit' value='Gender Report: Send to OpenFDA'></input>
                            </form>
                        </td>
                    </tr>
                    <tr>
                        <td><br></td>
                    </tr>
                    <tr>
                        <th align='left'>·Enter a drug and show its companies:</th>
                    </tr>
                    <tr>
                        <td><br></td>
                    </tr>
                    <tr>
                        <td>
                            <form method='get' action='searchDrug'>
                                <input type='text' size='3' maxlength='2' name='limit'></input>
                                <input type='submit' value='Drug Search: Send to OpendFDA'></input>
                                <input type='text' name='drug'></input>
                                <body align='left'>*</body>
                            </form>
                        </td>
                    </tr>
                    <tr>
                        <td><br></td>
                    </tr>
                    <tr>
                        <th align='left'>·Enter a company and show its drugs:</th>
                    </tr>
                    <tr>
                        <td><br></td>
                    </tr>
                    <tr>
                        <td>
                            <form method='get' action='searchCompany'>
                                <input type='text' size='3' maxlength='2' name='limit'></input>
                                <input type='submit' value='Company Search: Send to OpendFDA'></input>
                                <input type='text' name='company'></input>
                                <body align='left'>*</body>
                            </form>
                        </td>
                    </tr>
                    <tr>
                        <td><br></td>
                    </tr>
                    <tr>
                        <td align='right'>Debe completar los campos obligatorios (*)</td>
                    </tr>
                    <tr>
                        <td align='right'>Si no introduce el número de eventos, se mostraran 10</td>
                    </tr>
                </table>
            </body>
        </html>
        '''
        return html


    #LIST TO HTML
    def get_drug_html(self,drugs):
        html='''
        <html>
            <head>
            <title>OpenFDA Cool App</title>
            </head>
            <body>
                <h1 align='center'><u>OpenFDA Drugs</u></h1>
        '''
        html+='<body><u><b>·Se muestran '+str(len(drugs))+' elementos:</b></u></body>'
        html+='''
                <ul>
        '''

        for drug in drugs:
            html +='<li>'+drug+'</li>'

        html+= '''
                </ul>
            </body>
        </html>
        '''
        return html

    def get_company_html(self,companies):
        html='''
        <html>
            <head>
            <title>OpenFDA Cool App</title>
            </head>
            <body>
                <h1 align='center'><u>OpenFDA Companies</u></h1>
        '''
        html+='<body><u><b>·Se muestran '+str(len(companies))+' elementos:</b></u></body>'
        html+='''
                <ul>
        '''
        for company in companies:
            html +='<li>'+company+'</li>'

        html+= '''
                </ul>
            </body>
        </html>
        '''
        return html

    def get_gender_html(self,gender,males,females):
        html='''
        <html>
            <head>
            <title>OpenFDA Cool App</title>
            </head>
            <body>
                <h1 align='center'><u>OpenFDA Patient Sex</u></h1>
        '''
        html+='<body><u><b>·Se muestran '+str(len(gender))+' elementos:</b></u></body>'
        html+='''
            <body><br></body>
        '''
        html+='<h4>  El número de hombres es: '+str(males)+'</h4>'
        html+='<h4>  El número de mujeres es: '+str(females)+'</h4>'
        html+='''
                <ul>
        '''
        for sex in gender:
            html +='<li>'+sex+'</li>'
        html+= '''
                </ul>
            </body>
        </html>
        '''
        return html

class OpenFDAError():

    #ERRORES
    def error_limit(self):
        html='''
        <html>
            <head>
            <title>OpenFDA Cool App</title>
            </head>
            <body>
                <h1 align='left'>Error 404: Not Found</h1>
            </body>
            <body>· El campo del límite de eventos es erróneo. </body>
        </html>
        '''
        return html

    def error_search(self,is_number,events_error,busqueda):
        html='''
        <html>
            <head>
            <title>OpenFDA Cool App</title>
            </head>
            <body>
                <h1 align='left'>Error 404: Not Found</h1>
            </body>
        '''
        if not is_number:
            html+='''
                <body>· El campo del límite de eventos es erróneo. </body>
                <body><br></body>
            '''
        if 'error' in events_error:
            html+='''
                <body>· No existe el campo introducido. </body>
                <body><br></body>
            '''

        if busqueda=='':
            html+='''
                <body>· No ha introducido el campo obligatorio.(*) </body>
                <body><br></body>
                '''
        html+='''
        </html>
        '''

        return html

    def error_test(self):
        html='''
        <html>
            <head>
            <title>OpenFDA Cool App</title>
            </head>
            <body>
                <h1 align='left'>Error 404: Not Found</h1>
            </body>
            <body>· El medicamento introducido no existe. </body>
        </html>
        '''
        return html

    def error_no_exist(self):
        html='''
        <html>
            <head>
            <title>OpenFDA Cool App</title>
            </head>
            <body>
                <h1 align='left'>Error 404: Not Found</h1>
            </body>
            <body>· Esta URL no existe en esta página. </body>
        </html>
        '''
        return html

class OpenFDAGender():

    #SUMATORIO DE GENERO
    def male_gender(self,gender):
        contador=0
        for i in range(len(gender)):
            if gender[i]=='1':
                contador=contador+1
        return contador

    def female_gender(self,gender):
        contador=0
        for i in range(len(gender)):
            if gender[i]=='2':
                contador=contador+1
        return contador

class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):

        redirect=OpenFDARedirect()
        client=OpenFDAClient()
        parser=OpenFDAParser()
        HTML=OpenFDAHTML()
        ERROR=OpenFDAError()
        GENDER=OpenFDAGender()
        response=200

        #Main page
        if self.path=='/':
            html=HTML.get_main_page()

        #Second pages
        elif '/listDrugs' in self.path:
            limit=self.path.split('=')[1]
            if limit=='':
                limit='10'
            is_number=True
            try:
                int(limit)
            except ValueError:
                is_number=False
            if is_number:
                events_str=client.get_events(limit)
                events=json.loads(events_str)
                events=events['results']
                drugs=parser.get_drug_list(events)
                html=HTML.get_drug_html(drugs)
            else:
                html=ERROR.error_limit()

        elif '/listCompanies' in self.path:
            limit=self.path.split('=')[1]
            if limit=='':
                limit='10'
            is_number=True
            try:
                int(limit)
            except ValueError:
                is_number=False
            if is_number:
                events_str=client.get_events(limit)
                events=json.loads(events_str)
                events=events['results']
                companies=parser.get_companynumb(events)
                html=HTML.get_company_html(companies)
            else:
                html=ERROR.error_limit()

        elif '/listGender' in self.path:
            limit=self.path.split('=')[1]
            if limit=='':
                limit='10'
            is_number=True
            try:
                int(limit)
            except ValueError:
                is_number=False
            if is_number:
                events_str=client.get_events(limit)
                events=json.loads(events_str)
                events=events['results']
                gender=parser.get_patientsex(events)
                males=GENDER.male_gender(gender)
                females=GENDER.female_gender(gender)
                html=HTML.get_gender_html(gender,males,females)
            else:
                html=ERROR.error_limit()

        elif '/searchDrug' in self.path:
            iguales=self.path.count('=')
            if iguales==2:
                path=self.path.split('=')
                drug=path[2]
                with_number=path[1]
                limit=with_number.split('&')[0]
                if limit=='':
                    limit='10'
                is_number=True
                try:
                    int(limit)
                except ValueError:
                    is_number=False
                events_str=client.get_events_search(drug,limit)
                events=json.loads(events_str)
                error=client.get_events_error(drug)
                events_error=json.loads(error)
                if 'error' in events_error or drug=='' or not is_number:
                    html=ERROR.error_search(is_number,events_error,drug)
                else:
                    events=events['results']
                    companynumb=parser.get_companynumb(events)
                    html=HTML.get_company_html(companynumb)
            elif iguales==1:
                drug=self.path.split('=')[1]
                events_str=client.get_events_error(drug)
                events=json.loads(events_str)
                if 'error' in events:
                    html=ERROR.error_test()
                else:
                    events=events['results']
                    companynumb=parser.get_companynumb(events)
                    html=HTML.get_company_html(companynumb)
            else:
                html=ERROR.error_no_exist()

        elif '/searchCompany' in self.path:
            iguales=self.path.count('=')
            if iguales==2:
                path=self.path.split('=')
                company=path[2]
                with_number=path[1]
                limit=with_number.split('&')[0]

                if limit=='':
                    limit='10'
                is_number=True
                try:
                    int(limit)
                except ValueError:
                    is_number=False

                events_str=client.get_events_search(company,limit)
                events=json.loads(events_str)
                error=client.get_events_error(company)
                events_error=json.loads(error)

                if 'error' in events_error or company=='' or not is_number:
                    html=ERROR.error_search(is_number,events_error,company)
                elif 'error' not in events_error or company!='' or is_number:
                    events=events['results']
                    drugs=parser.get_drug_list(events)
                    html=HTML.get_drug_html(drugs)
            elif iguales==1:
                company=self.path.split('=')[1]
                events_str=client.get_events_error(company)
                events=json.loads(events_str)
                if 'error' in events:
                    html=ERROR.error_test()
                else:
                    events=events['results']
                    drugs=parser.get_drug_list(events)
                    html=HTML.get_drug_html(drugs)
            else:
                html=ERROR.error_no_exist()

        else:
            url=self.path.split('?')[0]
            funcion1='listDrugs'
            funcion2='listCompanies'
            funcion3='listGender'
            funcion4='searchDrug'
            funcion5='searchCompany'
            if redirect.similar_path(url,funcion1):
                limit=self.path.split('=')[1]
                html=redirect.redirect_list(limit,funcion1)

            elif redirect.similar_path(url,funcion2):
                limit=self.path.split('=')[1]
                html=redirect.redirect_list(limit,funcion2)

            elif redirect.similar_path(url,funcion3):
                limit=self.path.split('=')[1]
                html=redirect.redirect_list(limit,funcion3)

            elif redirect.similar_path(url,funcion4):
                search=self.path.split('&')[1]
                with_number=self.path.split('=')[1]
                limit=with_number.split('&')[0]
                html=redirect.redirect_search(limit,funcion4,search)

            elif redirect.similar_path(url,funcion5):
                search=self.path.split('&')[1]
                with_number=self.path.split('=')[1]
                limit=with_number.split('&')[0]
                html=redirect.redirect_search(limit,funcion5,search)

            else:
                response=404
                html=ERROR.error_no_exist()

        # Send response
        self.send_response(response)

        # Send headers
        self.send_header('Content-type','text/html')
        self.end_headers()

        #Send HTML
        self.wfile.write(bytes(html, 'utf8'))
