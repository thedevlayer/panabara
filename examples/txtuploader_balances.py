import pandas as pd
import os
import sqlite3
from datetime import datetime


def txtupload():

 
    print("txtupload started....")

    con = sqlite3.connect("db.sqlite3")
    cur = con.cursor()
 


    myid = '1' # dcpark80
    # kcurrencyrate = '1'

    currentPath = os.getcwd()
    print('currentPath : ',currentPath)
    
    
    filepath = currentPath+"\\examples\\uploadfiles\\BalanceTrend.csv"
    # 탭으로 분리된(tsv) .txt 텍스트파일 불러오기
    # data = pd.read_csv('파일경로', sep = "\t", , engine='python', encoding = "인코딩방식")
    data = pd.read_csv(filepath, sep = ",")
    print(data)

    query = "DELETE FROM examples_Balances where bauthor_id = " + myid
    try:
        cur.execute(query)
        print("Successfully executed : ", query)
    except:
        print("Not executed : ", query)


    if data is not None:

        print("input data len : ",len(data))


    # bdate = models.DateField( auto_now=False, null=True)
    # bamount = models.DecimalField(max_digits=12, decimal_places=0, null=True)
    # bauthor = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, null=True, blank=True)
    # bincreased = models.DecimalField(max_digits=12, decimal_places=0, null=True) 
    # bincreasedratio = models.DecimalField(max_digits=10, decimal_places=1,null=True, default=0.0)


        query = "INSERT INTO examples_Balances(bdate,bamount, bauthor_id, bincreased) VALUES (:bdate,:bamount, :bauthor_id,:bincreased)"
        # query = "insert into examples_MyStocks values(:icode, :iunitbuyprice, :iquantity , :timestamp, :author)"
        dataList = []

        for index, row in data.iterrows():
            bdate = row['bdate']
            bamount = row['bamount']
            bincreased = row['bincreased']
            bauthor_id = myid


            # print('icode : ',icode)
            # print('iunitbuyprice : ',iunitbuyprice)
            # print('iquantity : ',iquantity)

            dataList += {"bdate":bdate, "bamount":bamount , "bincreased":bincreased , "bauthor_id":bauthor_id },
     

        cur.executemany(query, dataList)
        con.commit()

 

    cur.execute("select * from examples_Balances")

    print(cur.fetchall())

    con.close()

if __name__ == '__main__':
    # getFinanceDataList()
    txtupload()