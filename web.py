
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

#Author:

#Pedro Jesús Álvarez Durán

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
                <h1>OpenFDA Client</h1>
                <table style="width:100%">
                    <tr>
                        <th>·Show 10 drugs </th>
                        <th>·Enter a drug and show 10 companies </th>
                        <th>·Show 10 companies </th>
                        <th>·Enter a company and show 10 drugs </th>
                    </tr>
                    <tr></tr>
                    <tr></tr>
                    <tr></tr>
                    <tr></tr>
                    <tr></tr>
                    <tr></tr>
                    <tr></tr>
                    <tr></tr>
                    <tr></tr>
                    <tr></tr>
                    <tr></tr>
                    <tr>
                        <td>
                            <form method='get' action='listDrugs'>
                                <input type='submit' value='Drug list: Send to OpenFDA'></input>
                            </form>
                        </td>
                        <td>
                            <form method='get' action='searchCompany'>
                                <input type='text' name='drug'></input>
                                <input type='submit' value='Drug Search: Send to OpendFDA'></input>
                            </form>
                        </td>
                        <td>
                            <form method='get' action='listCompanies'>
                                <input type='submit' value='Company list: Send to OpenFDA'></input>
                            </form>
                        </td>
                        <td>
                            <form method='get' action='searchDrug'>
                                <input type='text' name='company'></input>
                                <input type='submit' value='Company Search: Send to OpendFDA'></input>
                            </form>
                        </td>
                    </tr>
                </table>
            </body>
        </html>
        '''
        return html

    #GET EVENTS
    def get_events(self):
        conn=http.client.HTTPSConnection(self.OPENFDA_API_URL)
        conn.request('GET',self.OPENFDA_API_EVENT + '?limit=10')
        r1=conn.getresponse()
        data1=r1.read()
        events=data1.decode('utf8')
        return events

    def get_events_drug(self,drug):
        conn=http.client.HTTPSConnection(self.OPENFDA_API_URL)
        conn.request('GET',self.OPENFDA_API_EVENT + '?search='+drug+'&limit=10')
        r1=conn.getresponse()
        data1=r1.read()
        events=data1.decode('utf8')
        return events

    def get_events_companies(self,company):
        conn=http.client.HTTPSConnection(self.OPENFDA_API_URL)
        conn.request('GET',self.OPENFDA_API_EVENT + '?search='+company+'&limit=10')
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

    #LIST TO HTML
    def get_html(self,busqueda):
        busq_html='''
        <html>
            <head>
            <title>OpenFDA Cool App</title>
            </head>
            <body>
                <h1>OpenFDA Drugs</h1>
                <ul>
        '''
        for busq in busqueda:
            busq_html +='<li>'+busq+'</li>'

        busq_html+= '''
                </ul>
            </body>
        </html>
        '''
        return busq_html


    # GET
    def do_GET(self):

        # Send response status code
        self.send_response(200)

        # Send headers
        self.send_header('Content-type','text/html')
        self.end_headers()

        # Send message back to client
        html=self.get_main_page()

        #Al cargar la pagina:
        if self.path=='/':
            self.wfile.write(bytes(html, "utf8"))

        #Al pulsar el botón:
        elif '/listDrugs' in self.path:
            events_str=self.get_events()
            events=json.loads(events_str)
            events=events['results']
            drugs=self.get_drug_list(events)
            drugs_html=self.get_html(drugs)
            self.wfile.write(bytes(drugs_html, 'utf8'))

        elif '/searchCompany' in self.path:
            drug=self.path.split('=')[1]
            events_str=self.get_events_drug(drug)
            events=json.loads(events_str)
            events=events['results']
            companynumb=self.get_companynumb(events)
            companynumb_html=self.get_html(companynumb)
            self.wfile.write(bytes(companynumb_html, 'utf8'))

        elif '/listCompanies' in self.path:
            events_str=self.get_events()
            events=json.loads(events_str)
            events=events['results']
            companies=self.get_companynumb(events)
            companies_html=self.get_html(companies)
            self.wfile.write(bytes(companies_html, 'utf8'))

        elif '/searchDrug' in self.path:
            company=self.path.split('=')[1]
            events_str=self.get_events_companies(company)
            events=json.loads(events_str)
            events=events['results']
            drugs=self.get_drug_list(events)
            drug_html=self.get_html(drugs)
            self.wfile.write(bytes(drug_html, 'utf8'))
