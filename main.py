# we want to import the flask class so we can access methods inside it


from flask import Flask, render_template, request, redirect, url_for
import psycopg2
from datetime import datetime



# we are creating a variable that we use to acccess the variable we add the __name__ argument so that we ca pass the context
app = Flask(__name__)

conn = psycopg2.connect(user="postgres", password="19972612",
                        host="localhost", port="5432", database="myduka")
cur = conn.cursor()


# add a declaration to find the route
# every route is attached to a function all the logic is processed here

@app.route("/")
def hello_world():
    name = "Zandile"
    return render_template("index.html", name=name)

# inventories route


@app.route("/inventories")
def inventories():
    cur.execute("SELECT * from productsdets;")
    records = cur.fetchall()
    #print(records)
    return render_template("inventories.html", records=records)

# sales  route


@app.route("/sales")
def sales():
    cur.execute("SELECT * from sales;")
    information = cur.fetchall()
    print(information)
    return render_template("sales.html", information=information)


@app.route("/add_product", methods=["POST"])
def add_product():
    productname = request.form["product_name"]
    print(productname)
    buyingprice = request.form["buying_price"]
    print(buyingprice)
    sellingprice = request.form["selling_price"]
    print(sellingprice)
    stockquantity = request.form ["stock_quantity"]
    print (stockquantity)

    cur.execute("INSERT INTO productsdets (name, buying_price, selling_price,stock_quantity) VALUES (%s, %s, %s,%s)",
                (productname, buyingprice, sellingprice,stockquantity))
    conn.commit()

    
    return redirect(url_for("inventories"))

@app.route ("/make_sale", methods= ["GET", "POST"])
def make_sale():
    quantity = request.form ["quantity"]
    print(quantity)
    productid = request.form ["pid"]
    print(productid)
    created_at = datetime.now()
    print (created_at)
    
    cur.execute ("INSERT INTO sales (pid, quantity,created_at)VALUES(%s,%s,%s)",(productid, quantity,created_at))
    conn.commit()

    return redirect (url_for("inventories"))
#viewsale route
@app.route("/sales/<int:pid>")
def view_sales(pid):
    
		cur.execute("SELECT * FROM sales WHERE pid=%s;",[pid])
		information = cur.fetchall()
		return render_template("sales.html", information=information) 



# dashboard route
@app.route("/dashboard")
def dashboard():
    cur.execute ("select productsdets.name, sum (productsdets.selling_price * sales.quantity) from productsdets join sales on sales.pid = productsdets.id group by name;")
    items = cur.fetchall()
    list1 = []
    list2 = []
    for items in items:
        list1.append(items[0])
        list2.append(float(items[1]))
    cur.execute(" select to_char(sales.created_at,'YYYY-MM') sales,sum(sales.quantity*productsdets.selling_price) as amount from productsdets join sales on sales.pid=productsdets.id group by sales;")
    mysales = cur.fetchall()
    mysales1 =[]
    mysales2 =[]

    for mysales in mysales:
        mysales1.append(mysales[0])
        mysales2.append(float (mysales[1]))
    
    cur.execute (" select sales.category from sales;")
    mycategory = cur.fetchall()
    mycategory1 = []
    mycategory2 = []

    for mycateggory in mycategory:
        mycategory1.append

    return render_template("dashboard.html", list1=list1,list2=list2,mysales1=mysales1, mysales2=mysales2)
    
    


if __name__ == "__main__":
    app.run()
