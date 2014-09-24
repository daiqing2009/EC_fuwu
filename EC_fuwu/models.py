from sqlalchemy import create_engine, Table, Column, Integer, String, DATETIME, ForeignKey, and_
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL  
from sqlalchemy.orm import sessionmaker
from datetime import datetime,date,timedelta
from sqlalchemy.sql import func
import settings

  
DeclarativeBase = declarative_base()
  
def db_connect():
    if settings.ENV == 'QA':
        return create_engine(URL(**settings.QA_DB_MYSQL))
    elif settings.ENV == 'DEBUG':
        return create_engine(URL(**settings.DEBUG_DB_MYSQL))
    else: 
        return create_engine(URL(**settings.DB_SQLITE))
  
def create_tables(engine):
    DeclarativeBase.metadata.create_all(engine)

class FuwuPurchase(DeclarativeBase):
    __tablename__ = "fuwu_purchase"
  
    id = Column(Integer, primary_key=True)
    #fuwu_buyer_id = Column('fuwu_buyer_id',Integer,ForeignKey('fuwu_buyer.id'))
    buyerNameMasked = Column('buyer_name_masked',String(256))
    buyerRank = Column('buyer_rank', String(128))
    
    purchaseTime = Column('purchase_time', DATETIME)
    licLength = Column('lic_length', String(128))
    licVersion = Column('lic_ver', String(128))    
    
    fuwu_ISV_id = Column('fuwu_ISV_id',Integer,ForeignKey('fuwu_ISV.id'))
    
    def __repr__(self):
        return "<FuwuPurchase(buyerNameMasked='%s',buyerRank='%s',purchaseTime='%s', licLength='%s', licVersion='%s', id=%d)>" % (self.buyerNameMasked,self.buyerRank,self.purchaseTime, self.licLength, self.licVersion,self.id)    

class FuwuISV(DeclarativeBase):
    __tablename__ = "fuwu_ISV"
    
    id = Column(Integer, primary_key = True)
    name = Column('name',String(256))
    category = Column('category',String(512))
    link = Column('link', String(512))
    # latest purchase time run by crawler last time
    purchaseTimeLastMarked = Column('pur_time_last_crawl', DATETIME)    
    
    bePurchased = relationship("FuwuPurchase", backref="fuwu_ISV")
    
    #check if certain purchase should be appended to bePurchased
    def logPurchase(self, purchase):
        if(self.purchaseTimeLastMarked is None or self.purchaseTimeLastMarked<purchase.purchaseTime):
            self.bePurchased.append(purchase)
#            self.latestPurchaseTime = purchase.purchaseTime
            return True
        else:
            return False
        
    def markLastPurchase(self):
        lastPurchaseTime = self.bePurchased[-1].purchaseTime
        if self.purchaseTimeLastMarked is None or self.purchaseTimeLastMarked < lastPurchaseTime:
                self.purchaseTimeLastMarked = lastPurchaseTime
             
    def __init__(self, name, category,link):
        self.name = name
        self.category = category
        self.link = link
    
    def __repr__(self):
        return "<FuwuISV(name='%s', category='%s', link='%s', id=%d)>" % (self.name, self.category, self.link,self.id)
    
#unit test, also serve as an example for how to process the DB data
if __name__ == "__main__":
    engine = create_engine('sqlite:///:memory:', echo=True)
    DeclarativeBase.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    servicePro1 = FuwuISV(name='dummyISV1',category='ERP',link="http://abc.com")
    session.add(servicePro1)
    
    #getISV data
    myISV = session.query(FuwuISV).\
                filter_by(name='dummyISV1').\
                one()
                
    print myISV
    
    purchase1 = FuwuPurchase(buyerNameMasked="dummyBuyer1", buyerRank="1_2",purchaseTime=datetime.now()- timedelta(days=7),licLength="3M", licVersion = "pro")
    purchase2 = FuwuPurchase(buyerNameMasked="dummyBuyer2", buyerRank="3_2",purchaseTime=datetime.now(),licLength="15D", licVersion = "trial")
    myISV.logPurchase(purchase1)
    myISV.bePurchased.append(purchase2)

  
    session.add(purchase1)
    session.add(purchase2)
    print purchase1.fuwu_ISV_id
    print purchase2.fuwu_ISV_id    
    
    print session.query(FuwuPurchase).\
            filter(FuwuPurchase.fuwu_ISV == myISV).\
            filter(and_(FuwuPurchase.purchaseTime >=date.today()- timedelta(days=1) ,FuwuPurchase.purchaseTime <=date.today()+ timedelta(days=1))).\
            all()
            
    #assume end of crawl
    #print session.query(.func.max(FuwuPurchase.purchaseTime).label("max_score")).one()
    myISV.markLastPurchase()
    print myISV.purchaseTimeLastMarked
    
    print purchase1.fuwu_ISV_id
    print purchase2.fuwu_ISV_id              
            
            
            

    

