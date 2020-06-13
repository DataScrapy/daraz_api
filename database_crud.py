import mysql.connector


mydb = mysql.connector.connect(
    host="70.32.23.41",
    user="panacheholdingsb_python_test",
    passwd="Raju@12345",
    database="panacheholdingsb_test20"
)

mycursor = mydb.cursor(buffered=True,dictionary=True)


def page_content_post(page_content):
    try:
        mycursor.execute("INSERT INTO tbl_page_content (file_name) VALUES ('%s')" % (page_content))
        mydb.commit()

    except:
        pass

def page_content_get(id):
    try:
        mycursor.execute("SELECT * FROM tbl_page_content WHERE file_id = %s" % id)
        data = mycursor.fetchall()
        mydb.commit()
        data = data[0]

        return {"status": "success", "data": {"content ": data}}

    except Exception as e:
        return {"status": "error", "data": str(e)}
        pass


def page_url_status_post(url, depth_level, status):
    try:
        sql = "INSERT INTO tbl_page_status_info (page_url, depth_level,request_status) VALUES (%s, %s,%s)"
        val = (url, depth_level, str(status))
        mycursor.execute(sql, val)
        mydb.commit()
    except:
        pass


def page_url_status_get(id):
    try:
        mycursor.execute("SELECT * FROM tbl_page_status_info WHERE (id = %s)" % id)
        data = mycursor.fetchall()
        mydb.commit()
        data = data[0]

        return {"status": "success", "data": {"Crawled_pages ": data}}

    except Exception as e:
        return {"status": "error", "data": str(e)}
        pass

