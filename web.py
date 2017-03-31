
#MIT License

#Copyright (c) 2017


#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.


#Author: Pedro Jesús Álvarez Durán


import http.server
import json
import http.client


# HTTPRequestHandler class
class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    #URL
    OPENFDA_API_URL='api.fda.gov'
    OPENFDA_API_EVENT='/drug/event.json'


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
                                <input type='text' size='3' maxlength='2' name='gender'></input>
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


    #GET EVENTS
    def get_events(self,limit):
        conn=http.client.HTTPSConnection(self.OPENFDA_API_URL)
        conn.request('GET',self.OPENFDA_API_EVENT + '?limit='+limit+'')
        r1=conn.getresponse()
        data1=r1.read()
        events=data1.decode('utf8')
        return events

    def get_events_search(self,search):
        conn=http.client.HTTPSConnection(self.OPENFDA_API_URL)
        conn.request('GET',self.OPENFDA_API_EVENT + '?search='+search+'&limit=10')
        r1=conn.getresponse()
        data1=r1.read()
        events=data1.decode('utf8')
        return events


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

    def error_search(self,events,busqueda):
        html='''
        <html>
            <head>
            <title>OpenFDA Cool App</title>
            </head>
            <body>
                <h1 align='left'>Error 404: Not Found</h1>
            </body>
        '''
        if 'error' in events:
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


    # GET
    def do_GET(self):

        response = 200

        #Main page
        if self.path=='/':
            html=self.get_main_page()

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
                events_str=self.get_events(limit)
                events=json.loads(events_str)
                events=events['results']
                drugs=self.get_drug_list(events)
                html=self.get_drug_html(drugs)
            else:
                html=self.error_limit()

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
                events_str=self.get_events(limit)
                events=json.loads(events_str)
                events=events['results']
                companies=self.get_companynumb(events)
                html=self.get_company_html(companies)
            else:
                html=self.error_limit()

        elif '/searchDrug' in self.path:
            path=self.path.split('=')
            drug=path[1]
            events_str=self.get_events_search(drug)
            events=json.loads(events_str)
            if 'error' in events or drug=='':
                html=self.error_search(events,drug)
            else:
                events=events['results']
                companynumb=self.get_companynumb(events)
                html=self.get_company_html(companynumb)

        elif '/searchCompany' in self.path:
            path=self.path.split('=')
            company=path[1]

            events_str=self.get_events_search(company)
            events=json.loads(events_str)

            if 'error' in events or company=='':
                html=self.error_search(events,company)

            else:
                events=events['results']
                drugs=self.get_drug_list(events)
                html=self.get_drug_html(drugs)

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
                events_str=self.get_events(limit)
                events=json.loads(events_str)
                events=events['results']
                gender=self.get_patientsex(events)
                males=self.male_gender(gender)
                females=self.female_gender(gender)
                html=self.get_gender_html(gender,males,females)
            else:
                html=self.error_limit()

        else:
            response = 404
            html=self.error_no_exist()

        # Send response
        self.send_response(response)

        # Send headers
        self.send_header('Content-type','text/html')
        self.end_headers()

        #Send HTML
        self.wfile.write(bytes(html, 'utf8'))
