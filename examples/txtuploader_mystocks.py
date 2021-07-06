import pandas as pd
import os
import sqlite3
from datetime import datetime


def txtupload():

 
    print("txtupload started....")

    con = sqlite3.connect("db.sqlite3")
    cur = con.cursor()
 


    myid = '1' # dcpark80
    kcurrencyrate = '1'

    currentPath = os.getcwd()
    print('currentPath : ',currentPath)
    
    
    filepath = currentPath+"\\examples\\uploadfiles\\mystocks_20210420.txt"

    # data = pd.read_csv('���ϰ��', sep = "\t", , engine='python', encoding = "���ڵ����")
    data = pd.read_csv(filepath, sep = "\t")
    print(data)

    query = "DELETE FROM examples_MyStocks where author_id = " + myid
    try:
        cur.execute(query)
        print("Successfully executed : ", query)
    except:
        print("Not executed : ", query)


    if data is not None:

        print("input data len : ",len(data))

        query = "INSERT INTO examples_MyStocks(invst_type,icode, iunitbuyprice, iquantity, timestamp,author_id, kcurrencyrate,iunitcurprice, kprofitratio, ktotalcurprice, kforeverholdyn) VALUES (:invst_type,:icode, :iunitbuyprice,:iquantity, :timestamp, :author_id,:kcurrencyrate, :iunitcurprice, :kprofitratio, :ktotalcurprice,:kforeverholdyn)"
        # query = "insert into examples_MyStocks values(:icode, :iunitbuyprice, :iquantity , :timestamp, :author)"
        dataList = []

        for index, row in data.iterrows():
            invst_type = row['invst_type']
            icode = row['icode']
            iunitbuyprice = row['iunitbuyprice']
            iquantity = row['iquantity']
            kforeverhold = row['kforeverholdyn']

            kforeverholdyn = False

            if kforeverhold == 1:
                kforeverholdyn = True



            # print('icode : ',icode)
            # print('iunitbuyprice : ',iunitbuyprice)
            print('kforeverholdyn : ',kforeverholdyn)

            dataList += {"invst_type":invst_type, "icode":icode , "iunitbuyprice":iunitbuyprice , "iquantity":iquantity , 
            "timestamp":datetime.now().strftime("%Y-%m-%d"),"author_id":myid ,"kcurrencyrate":kcurrencyrate,
            "iunitcurprice":0, "kprofitratio":0, "ktotalcurprice":0 ,"kforeverholdyn":kforeverholdyn},
     

        cur.executemany(query, dataList)
        con.commit()

 

    cur.execute("select * from examples_MyStocks")

    print(cur.fetchall())

    con.close()

if __name__ == '__main__':
    # getFinanceDataList()
    txtupload()