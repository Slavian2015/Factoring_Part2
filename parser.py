from bs4 import BeautifulSoup
import os
import requests as req
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import schedule


main_path_data = os.path.abspath("./data")
link_main = 'https://data.gov.ua/dataset/ab09ed00-4f51-4f6c-a2f7-1b2fb118be0f'



def restart():

    all_links = []
    ################   Models   ####################################
    Base = declarative_base()
    class doc_lost(Base):
        __tablename__ = 'lost_documents'

        id = Column(Integer, primary_key=True)
        doc_id = Column(Integer)
        doc_type = Column(Integer)
        doc_seria = Column(String)
        doc_num = Column(String)
        doc_stat = Column(String)
        doc_date_sit = Column(String)
        doc_date_sign = Column(String)
        doc_depart = Column(String)


    class doc_type(Base):
        __tablename__ = 'document_type'

        id = Column(Integer, primary_key=True)
        name = Column(String(1000))
        term = Column(Integer, default=0)
        seria = Column(Integer, default=0)


    engine = create_engine('sqlite:///all.db', echo=False)
    Base.metadata.create_all(engine)
    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()

    ###############     Ask the Link    #########################
    resp = req.get(link_main, headers={'User-Agent': 'Mozilla'})
    soup = BeautifulSoup(resp.text, 'html.parser')

    for rows in soup.find_all("section", attrs={"id": "dataset-resources"}):
        for item in rows.find_all("a", attrs={"class": "resource-url-analytics"}):
            all_links.append(item.get('href'))


    def pars_json(link):
        resp = req.get(link, headers={'User-Agent': 'Mozilla'})
        ContentUrl = resp.json()

        for v in ContentUrl:
            print(v['ID'])
            doc = session.query(doc_lost).filter_by(doc_id=v['ID']).first()
            if doc:
                pass
            else:
                new_doc = doc_lost(doc_id=v['ID'], doc_type=v['D_TYPE'], doc_seria=v['D_SERIES'], doc_num=v['D_NUMBER'],
                                   doc_stat=v['D_STATUS'], doc_date_sit=v['THEFT_DATA'],
                                   doc_date_sign=v['INSERT_DATE'], doc_depart=v['OVD'])
                if v['D_SERIES']:
                    ser = 1
                else:
                    ser = 0
                new_type = doc_type(id=v['ID'], name=v['D_TYPE'], term=0, seria=ser)
                session.add_all([new_doc, new_type])
                session.commit()
        return

    for i in all_links:
        if 'mvswantedpassport_shema.json' in f'**{i}**':
            pass
        else:
            pars_json(i)
            break


schedule.every().day.at("00:00").do(restart)