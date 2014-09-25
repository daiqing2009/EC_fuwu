# -*- coding: utf-8 -*-
from sqlalchemy.orm import sessionmaker
from models import FuwuPurchase,FuwuISV, db_connect, create_tables
from sqlalchemy.orm.exc import NoResultFound
from items import FuwuISVItem,FuwuPurchaseItem
from spiders import TBfuwuSpider 
from sqlalchemy import and_

from scrapy import log
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class TutorialPipeline(object):
    def process_item(self, item, spider):
        return item

  
class RdbPipeline(object):
    def __init__(self):
        engine = db_connect()
        create_tables(engine)
        self.Session = sessionmaker(bind=engine)
  
    def process_item(self, item, spider):
        #TODO: should not generate new session for same ISV page, may consider AOP/metaclass
        session = self.Session()

        #check whether session is always the same or one instance from session pool
        #self.log(Debug, session)
        
        try: 
            fuwuISV = None
            if type(item) is FuwuPurchaseItem:
                #pop up fuwuISV and remove certan list
                fuwuISVItem = item.pop('fuwuISV')
                fuwuISV = FuwuISV(**fuwuISVItem)
            elif type(item) is FuwuISVItem:
                fuwuISV = FuwuISV(**item)
                log.msg("fuwuISV .name= %s " % fuwuISV.name, level=log.DEBUG)
            #print  "fuwuISV .name= %s " % fuwuISV.name
            #make sure fuwuISV is unique       
            try:
                fuwuISV = session.query(FuwuISV).\
                    filter(FuwuISV.name==fuwuISV.name).one()
                log.msg("fuwuISV found in record .id= %d" % fuwuISV.id, level=log.DEBUG)
                #print " fuwuISV found in record .id= %d" % fuwuISV.id
            except NoResultFound, e:
                print e                
                session.merge(fuwuISV) 
            
                      
            if type(item) is FuwuPurchaseItem:
                #link purchase info into ISV            
                purchase = FuwuPurchase(**item)                
                if fuwuISV.logPurchase(purchase):            
                    session.add(purchase)
     
            session.commit()
#            print "new fuwuISV.id= %d" % fuwuISV.id
#             if purchase is not None:
#                 print purchase.fuwu_ISV_id
        except Exception, e:
            print e
            session.rollback()
        finally:
            session.close()         
                
        return item
    
    def close_spider(self, spider):
        print "closing spider in rdbpipleline"
        print type(spider)
        print spider.__class__.name
#         if type(spider) is not TBfuwuSpider:
#             return
        session = self.Session()
        ISVs = session.query(FuwuISV).all()
        
        for fuwu_ISV in ISVs:
            fuwu_ISV.markLastPurchase()
#             print fuwu_ISV.purchaseTimeLastMarked
        session.commit()