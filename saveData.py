#-*- encoding: utf-8 -*-
import readExcel
import os
import MySQLdb
import datetime

BASE_DIR= os.path.dirname(os.path.realpath(__file__))
class saveDate:
    def __init__(self):
        self.conn = MySQLdb.connect(
            host='localgost',
            port=3306,
            user='root',
            passwd='welcome123',
            db='d_easyhin_stat_ret',
            charset="utf8",
        )

    def changeDB(self, dbname):
        if dbname == '':
            self.conn.close()
            self.conn = MySQLdb.connect(
                #host='',
                #port=3306,
                #user='',
                #passwd='',
                #db='',
                #charset="utf8",
            )
        return 'change db to %s successfully' % (dbname)

    def __del__(self):
        self.conn.close()

    def jdbc(self, sql):
        cursor = self.conn.cursor()
        try:
            cursor.execute(sql)
            self.conn.commit()
            cursor.close()
            return True
        except:
            print "Error: unable to fecth data"
            self.conn.rollback

    def savedata(self):
        result = readExcel.getexcel()
        TODAY =datetime.date.today()
        if len(result) > 0:
            #第三方关注数
            sql1 = 'update t_screen_total_user set f_third_user = %s where f_crt_time = "%s" '%(str(result[0]),TODAY)
            self.jdbc(sql1)
            # 文章阅读量
            sql2 = 'update t_screen_article_read set f_third_read = %s where f_crt_date = "%s" ' % (str(result[1]), TODAY-datetime.timedelta(days=1))
            self.jdbc(sql2)
            return 'update success'
        return 'update failed'
if __name__ == "__main__":
    sd = saveDate()
    print sd.savedata()