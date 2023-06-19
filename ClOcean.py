import pymysql as c
conn = c.connect(host = "localhost",user = "root", password = "maverick",db = "cloocean", autocommit=True)

def login(pswrd):
    if pswrd=='yes':
        return True
    return False

def viewAllProducts():
    conn = c.connect(host = "localhost",user = "root", password = "maverick",db = "cloocean", autocommit=True)
    curr = conn.cursor()
    curr.execute("set autocommit = 0;")
    curr.execute("start transaction;")
    curr.execute("Select * from product")
    output = curr.fetchall()
    for i in output:
        print(i)
    curr.execute("commit;")
    curr.execute("set autocommit = 1;")
    conn.close()

def viewAllCombos():
    conn = c.connect(host = "localhost",user = "root", password = "maverick",db = "cloocean", autocommit=True)
    curr = conn.cursor()
    curr.execute("set autocommit = 0;")
    curr.execute("start transaction;")
    curr.execute("Select * from combo")
    output = curr.fetchall()
    for i in output:
        print(i)
    curr.execute("commit;")
    curr.execute("set autocommit = 1;")
    conn.close()

def addProductToCart(cid,pid,qty):
    conn = c.connect(host = "localhost",user = "root", password = "maverick",db = "cloocean", autocommit=True)
    curr = conn.cursor()
    curr.execute("set autocommit = 0;")
    curr.execute("start transaction;")
    curr.execute("select stock from product where pid = '"+pid+"';")
    stock = curr.fetchall()
    if(qty>stock[0][0]):
        print("Not enough stock")
        conn.close()
        return
    curr.execute("insert into cart_contains_product values('"+str(cid)+"','"+str(pid)+"','"+str(qty)+"');")
    curr.execute("commit;")
    curr.execute("set autocommit = 1;")
    conn.close()

def addComboToCart(cid,comboid,qty):
    conn = c.connect(host = "localhost",user = "root", password = "maverick",db = "cloocean", autocommit=True)
    curr = conn.cursor()
    curr.execute("set autocommit = 0;")
    curr.execute("start transaction;")
    curr.execute("select stock from combo where combo_id = '"+comboid+"';")
    stock = curr.fetchall()
    if(qty>stock[0][0]):
        print("Not enough stock")
        conn.close()
        return
    curr.execute("insert into cart_contains_combo values('"+str(cid)+"','"+str(comboid)+"','"+str(qty)+"');")
    curr.execute("commit;")
    curr.execute("set autocommit = 1;")
    conn.close()

def viewCart(cid):
    conn = c.connect(host = "localhost",user = "root", password = "maverick",db = "cloocean", autocommit=True)
    curr = conn.cursor()
    curr.execute("set autocommit = 0;")
    curr.execute("start transaction;")
    print("************ Product ************")
    curr.execute("select cart_contains_product.pid, product.product_name from cart_contains_product,product where cart_contains_product.cid = '"+str(cid)+"' and cart_contains_product.pid = product.pid;")
    output = curr.fetchall()
    for i in output:
        print(i[0],i[1])
    print("************ Combo **************")
    curr.execute("select cart_contains_combo.combo_id from cart_contains_combo where cart_contains_combo.cid = '"+str(cid)+"';")
    output = curr.fetchall()
    for i in output:
        print(i[0])
    print("*********************************")    
    curr.execute("select total_cart_val from cart where cid = '"+str(cid)+"';")
    output = curr.fetchall()
    for i in output:
        print("Total cart value : ",i[0])
    curr.execute("commit;")
    curr.execute("set autocommit = 1;")    
    conn.close()

def checkoutCart(cid):
    conn = c.connect(host = "localhost",user = "root", password = "maverick",db = "cloocean", autocommit=True)
    curr = conn.cursor()
    # Updating the cart, setting final amount to 0
    curr.execute("set autocommit = 0;")
    curr.execute("start transaction;")
    curr.execute("update cart set total_cart_val = 0 where cid = '"+str(cid)+"';")
    # Updating product and combo stock
    curr.execute("update product as p,cart_contains_product as c set p.stock = p.stock - c.qty where p.pid = c.pid and c.cid ='"+str(cid)+"';")
    curr.execute("update combo as co,cart_contains_combo as c set co.stock = co.stock - c.qty where co.combo_id = c.combo_id and c.cid ='"+str(cid)+"';")
    # Updating the history table
    curr.execute("select * from cart_contains_product where cid = '"+str(cid)+"';")
    output1 = curr.fetchall()
    curr.execute("select * from cart_contains_combo where cid = '"+str(cid)+"';")
    output2 = curr.fetchall()
    for i in output1:
        curr.execute("insert into history (cid,pid) values('"+str(cid)+"','"+str(i[1])+"');")
    for i in output2:
        curr.execute("insert into history (cid,combo_id) values('"+str(cid)+"','"+str(i[1])+"');")
    # Clearing the cart
    curr.execute("delete from cart_contains_product where cid = '"+str(cid)+"';")
    curr.execute("delete from cart_contains_combo where cid = '"+str(cid)+"';")
    # Updating seller_acc
    for i in output1:
        curr.execute("update seller_acc,product set total_earnings = total_earnings + product.cost*"+str(i[2])+" where product.pid ='"+str(i[1])+"' and seller_acc.sid = product.sid;")
    for i in output2:
        curr.execute("update seller_acc,combo set total_earnings = total_earnings + combo.cost*"+str(i[2])+" where combo.combo_id ='"+str(i[1])+"' and seller_acc.sid = combo.sid;")
    curr.execute("commit;")
    curr.execute("set autocommit = 1;")
    conn.close()

def viewHistory(cid):
    conn = c.connect(host = "localhost",user = "root", password = "maverick",db = "cloocean", autocommit=True)
    curr = conn.cursor()
    curr.execute("set autocommit = 0;")
    curr.execute("start transaction;")
    curr.execute("select * from history where cid='"+str(cid)+"';")
    output = curr.fetchall()
    for i in output:
        if(i[1] == None):
            print("product id not available",i[2])
        if(i[2] == None):
            print(i[1],"combo id not available")
    curr.execute("commit;")
    curr.execute("set autocommit = 1;")
    conn.close()
       
def myProfilecustomer(cid):
    conn = c.connect(host = "localhost",user = "root", password = "maverick",db = "cloocean", autocommit=True)
    curr = conn.cursor()
    curr.execute("set autocommit = 0;")
    curr.execute("start transaction;")
    curr.execute("select * from customer where cid='"+str(cid)+"';")
    output = curr.fetchall()
    for i in output:
        print(i[0],i[1],i[2],i[3],i[4])
    curr.execute("commit;")
    curr.execute("set autocommit = 1;")
    conn.close()

def checkLogin(cid):
    conn = c.connect(host = "localhost",user = "root", password = "maverick",db = "cloocean", autocommit=True)
    curr = conn.cursor()
    curr.execute("set autocommit = 0;")
    curr.execute("start transaction;")
    curr.execute("Select cid from customer;")
    output = curr.fetchall()
    curr.execute("commit;")
    curr.execute("set autocommit = 1;")
    conn.close()
    t = (cid,)
    if t in output:
        return True
    return False

def isCartEmpty(cid):
    conn = c.connect(host = "localhost",user = "root", password = "maverick",db = "cloocean", autocommit=True)
    curr = conn.cursor()
    curr.execute("set autocommit = 0;")
    curr.execute("start transaction;")
    curr.execute("select customer.cid from customer where customer.cid not in( select cid from cart_contains_combo UNION select cid from cart_contains_product);")
    output = curr.fetchall()
    if (cid,) in output:
        conn.close()
        return True
    curr.execute("commit;")
    curr.execute("set autocommit = 1;")
    return False

def viewAllSellerProducts(sid):
    conn = c.connect(host = "localhost",user = "root", password = "maverick",db = "cloocean", autocommit=True)
    curr = conn.cursor()
    curr.execute("set autocommit = 0;")
    curr.execute("start transaction;")
    curr.execute("Select * from product where sid = '"+ str(sid) +"';")
    output = curr.fetchall()
    for i in output:
        print(i)
    curr.execute("commit;")
    curr.execute("set autocommit = 1;")
    conn.close()

def viewAllSellerCombos(sid):
    conn = c.connect(host = "localhost",user = "root", password = "maverick",db = "cloocean", autocommit=True)
    curr = conn.cursor()
    curr.execute("set autocommit = 0;")
    curr.execute("start transaction;")
    curr.execute("Select * from combo where sid = '"+ str(sid) +"';")
    output = curr.fetchall()
    for i in output:
        print(i)
    curr.execute("commit;")
    curr.execute("set autocommit = 1;")
    conn.close()   

def checkpid(sid, pid):
    conn = c.connect(host = "localhost",user = "root", password = "maverick",db = "cloocean", autocommit=True)
    curr = conn.cursor()
    curr.execute("set autocommit = 0;")
    curr.execute("start transaction;")
    curr.execute("Select pid from product where sid = '"+str(sid)+"';")
    output = curr.fetchall()
    conn.close()
    t = (pid,)
    if t in output:
        return True
    curr.execute("commit;")
    curr.execute("set autocommit = 1;")
    return False

def checkallpid(pid):
    conn = c.connect(host = "localhost",user = "root", password = "maverick",db = "cloocean", autocommit=True)
    curr = conn.cursor()
    curr.execute("set autocommit = 0;")
    curr.execute("start transaction;")
    curr.execute("Select pid from product;")
    output = curr.fetchall()
    conn.close()
    t = (pid,)
    if t in output:
        return True
    curr.execute("commit;")
    curr.execute("set autocommit = 1;")
    return False

def checkallcomboid(combo_id):
    conn = c.connect(host = "localhost",user = "root", password = "maverick",db = "cloocean", autocommit=True)
    curr = conn.cursor()
    curr.execute("set autocommit = 0;")
    curr.execute("start transaction;")
    curr.execute("Select combo_id from combo;")
    output = curr.fetchall()
    conn.close()
    t = (combo_id,)
    if t in output:
        return True
    curr.execute("commit;")
    curr.execute("set autocommit = 1;")
    return False
    
def addProductforseller(pid,product_name,size,color,cost,stock,sid,category):
    conn = c.connect(host = "localhost",user = "root", password = "maverick",db = "cloocean", autocommit=True)
    curr = conn.cursor()
    curr.execute("set autocommit = 0;")
    curr.execute("start transaction;")
    curr.execute("insert into product values('"+str(pid)+"','"+str(product_name)+"','"+str(size)+"','"+str(color)+"','"+str(cost)+"','"+str(stock)+"','"+str(sid)+"','"+str(category)+"');")
    curr.execute("commit;")
    curr.execute("set autocommit = 1;")
    conn.close()    

def addComboforseller(combo_id,pid1,pid2,cost,stock,sid):
    conn = c.connect(host = "localhost",user = "root", password = "maverick",db = "cloocean", autocommit=True)
    curr = conn.cursor()
    curr.execute("set autocommit = 0;")
    curr.execute("start transaction;")
    curr.execute("insert into combo values('"+str(combo_id)+"','"+str(pid1)+"','"+str(pid2)+"','"+str(cost)+"','"+str(stock)+"','"+str(sid)+"');")
    curr.execute("commit;")
    curr.execute("set autocommit = 1;")
    conn.close()  

def viewbestseller():
    conn = c.connect(host = "localhost",user = "root", password = "maverick",db = "cloocean", autocommit=True)
    curr = conn.cursor()
    curr.execute("set autocommit = 0;")
    curr.execute("start transaction;")
    curr.execute("SELECT p.category, p.product_name, COUNT(*) as frequency FROM history h JOIN product p ON h.pid = p.pid WHERE h.cid IN (SELECT cid FROM cart) GROUP BY p.category, p.product_name ORDER BY p.category, frequency DESC;")
    output = curr.fetchall()
    for i in output:
        print(i)
    curr.execute("commit;")
    curr.execute("set autocommit = 1;")
    conn.close() 

def myProfileseller(sid):
    conn = c.connect(host = "localhost",user = "root", password = "maverick",db = "cloocean", autocommit=True)
    curr = conn.cursor()
    curr.execute("set autocommit = 0;")
    curr.execute("start transaction;")
    curr.execute("select * from seller where sid='"+str(sid)+"';")
    output = curr.fetchall()
    for i in output:
        print(i[0],i[1],i[2],i[3],i[4],i[5])
    curr.execute("commit;")
    curr.execute("set autocommit = 1;")
    conn.close()  

def topsellingproduct():
    conn = c.connect(host = "localhost",user = "root", password = "maverick",db = "cloocean", autocommit=True)
    curr = conn.cursor()
    curr.execute("set autocommit = 0;")
    curr.execute("start transaction;")
    curr.execute("SELECT p.category, p.product_name, COUNT(*) as frequency FROM history h JOIN product p ON h.pid = p.pid WHERE h.cid IN (SELECT cid FROM cart) GROUP BY p.category, p.product_name ORDER BY p.category, frequency DESC")
    output = curr.fetchall()
    for i in output:
        print(i)
    curr.execute("commit;")
    curr.execute("set autocommit = 1;")
    conn.close() 

def cidhighestvalue():
    conn = c.connect(host = "localhost",user = "root", password = "maverick",db = "cloocean", autocommit=True)
    curr = conn.cursor()
    curr.execute("set autocommit = 0;")
    curr.execute("start transaction;")
    curr.execute('''SELECT h.cid, SUM(IFNULL(p.cost, 0) + IFNULL(c.cost, 0)) AS total_price FROM history h
                    LEFT JOIN product p ON h.pid = p.pid
                    LEFT JOIN combo ccp ON h.combo_id = ccp.combo_id
                    LEFT JOIN (
                    SELECT combo_id, SUM(cost) AS cost FROM combo
                    GROUP BY combo_id
                    ) c ON h.combo_id = c.combo_id GROUP BY h.cid
                    ORDER BY total_price DESC LIMIT 1;''')
    output = curr.fetchall()
    for i in output:
        print(i[0],i[1])
    curr.execute("commit;")
    curr.execute("set autocommit = 1;")
    conn.close()           
    
def totalearnsellerbycateg():
    conn = c.connect(host = "localhost",user = "root", password = "maverick",db = "cloocean", autocommit=True)
    curr = conn.cursor()
    curr.execute("set autocommit = 0;")
    curr.execute("start transaction;")
    curr.execute('''SELECT category, SUM(total_earnings) as total_earnings FROM seller_acc
                    INNER JOIN product
                    ON seller_acc.sid = product.sid
                    GROUP BY category WITH ROLLUP;''')
    output = curr.fetchall()
    for i in output:
        print(i[0],i[1])
    curr.execute("commit;")
    curr.execute("set autocommit = 1;")
    conn.close()

def totalnoprodcombycatensize():
    conn = c.connect(host = "localhost",user = "root", password = "maverick",db = "cloocean", autocommit=True)
    curr = conn.cursor()
    curr.execute("set autocommit = 0;")
    curr.execute("start transaction;")
    curr.execute('''SELECT category, size, SUM(qty) as total_qty FROM (
                    SELECT category, size, qty
                    FROM cart_contains_product
                    JOIN product ON cart_contains_product.pid = product.pid
                    UNION ALL
                    SELECT category, size, qty
                    FROM cart_contains_combo
                    JOIN combo ON cart_contains_combo.combo_id = combo.combo_id JOIN product ON combo.pid1 = product.pid
                    ) AS qty_by_product_and_combo GROUP BY category, size;''')
    output = curr.fetchall()
    for i in output:
        print(i[0],i[1],i[2])
    curr.execute("commit;")
    curr.execute("set autocommit = 1;")
    conn.close() 

def cidemptycart():
    conn = c.connect(host = "localhost",user = "root", password = "maverick",db = "cloocean", autocommit=True)
    curr = conn.cursor()
    curr.execute("set autocommit = 0;")
    curr.execute("start transaction;")
    curr.execute('''select customer.cid from customer where customer.cid not in( select cid from cart_contains_combo UNION select cid from cart_contains_product);''')
    output = curr.fetchall()
    for i in output:
        print(i[0])
    curr.execute("commit;")
    curr.execute("set autocommit = 1;")
    conn.close() 

def updateproductstock(pid):
    conn = c.connect(host = "localhost",user = "root", password = "maverick",db = "cloocean", autocommit=True)
    curr = conn.cursor()
    n = input("Enter the new stock for the product: ")
    curr.execute("set autocommit = 0;")
    curr.execute("start transaction;")
    curr.execute("update product set stock = "+ n+" where pid = '"+str(pid)+"';")
    print("Stock update successfully !!!")
    curr.execute("commit;")
    curr.execute("set autocommit = 1;")
    conn.close() 

def updateproductscost(pid):
    conn = c.connect(host = "localhost",user = "root", password = "maverick",db = "cloocean", autocommit=True)
    curr = conn.cursor()
    n = input("Enter the new cost for the product: ")
    curr.execute("set autocommit = 0;")
    curr.execute("start transaction;")
    curr.execute("update product set cost = "+ n+" where pid = '"+str(pid)+"';")
    print("Stock update successfully !!!")
    curr.execute("commit;")
    curr.execute("set autocommit = 1;")
    conn.close() 

def updatecombosstock(pid):
    conn = c.connect(host = "localhost",user = "root", password = "maverick",db = "cloocean", autocommit=True)
    curr = conn.cursor()
    n = input("Enter the new stock for the combo: ")
    curr.execute("set autocommit = 0;")
    curr.execute("start transaction;")
    curr.execute("update combo set stock = "+ n+" where combo_id = '"+str(pid)+"';")
    print("Stock update successfully !!!")
    curr.execute("commit;")
    curr.execute("set autocommit = 1;")
    conn.close() 

def updatecombocost(pid):
    conn = c.connect(host = "localhost",user = "root", password = "maverick",db = "cloocean", autocommit=True)
    curr = conn.cursor()
    n = input("Enter the new cost for the combo: ")
    curr.execute("set autocommit = 0;")
    curr.execute("start transaction;")
    curr.execute("update combo set cost = "+ n+" where combo_id = '"+str(pid)+"';")
    print("Stock updated successfully !!!")
    curr.execute("commit;")
    curr.execute("set autocommit = 1;")
    conn.close() 

def dropproduct(pid,cid,qty):
    conn = c.connect(host = "localhost",user = "root", password = "maverick",db = "cloocean", autocommit=True)
    curr = conn.cursor()
    curr.execute("set autocommit = 0;")
    curr.execute("start transaction;")
    curr.execute("update cart_contains_product set qty = qty - "+str(qty)+" where cid = '"+str(cid)+"' and pid = '"+str(pid)+"';")
    curr.execute("update cart,product set total_cart_val = total_cart_val - product.cost*"+str(qty)+" where cart.cid = '"+str(cid)+"' and product.pid = '"+str(pid)+"';")
    curr.execute("delete from cart_contains_product where qty = 0;")
    curr.execute("commit;")
    curr.execute("set autocommit = 1;")
    print("Cart updated successfully !!!")
    conn.close() 

def dropcombo(combo_id,cid,qty):
    conn = c.connect(host = "localhost",user = "root", password = "maverick",db = "cloocean", autocommit=True)
    curr = conn.cursor()
    curr.execute("set autocommit = 0;")
    curr.execute("start transaction;")
    curr.execute("update cart_contains_combo set qty = qty - "+str(qty)+" where cid = '"+str(cid)+"' and combo_id = '"+str(combo_id)+"';")
    curr.execute("update cart,combo set total_cart_val = total_cart_val - combo.cost*"+str(qty)+" where cart.cid = '"+str(cid)+"' and combo.combo_id = '"+str(combo_id)+"';")
    curr.execute("delete from cart_contains_combo where qty = 0;")
    curr.execute("commit;")
    curr.execute("set autocommit = 1;")
    print("Cart updated successfully !!!")
    conn.close() 

def insertcid():
    conn = c.connect(host = "localhost",user = "root", password = "maverick",db = "cloocean", autocommit=True)
    curr = conn.cursor()
    curr.execute("set autocommit = 0;")
    curr.execute("SELECT MAX(cid) FROM customer ;")
    output = curr.fetchone()
    max_cid = output[0]
    new_cid = max_cid + 1
    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")
    phone_no = input("Enter phone number: ")
    address = input("Enter address: ")
    dob = input("Enter date of birth (yyyy-mm-dd): ")
    sql = "INSERT INTO customer (cid, first_name, last_name, phone_no, address, dob) VALUES (%s, %s, %s, %s, %s, %s)"
    val = (new_cid, first_name, last_name, phone_no, address, dob)
    curr.execute(sql, val)
    curr.execute("set autocommit = 1;")
    print("New customer added with cid:", new_cid) 

def insertsid():
    conn = c.connect(host = "localhost",user = "root", password = "maverick",db = "cloocean", autocommit=True)
    curr = conn.cursor()
    curr.execute("set autocommit = 0;")
    curr.execute("SELECT MAX(sid) FROM seller ;")
    output = curr.fetchone()
    max_sid = output[0]
    new_sid = max_sid + 1
    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")
    phone_no = input("Enter phone number: ")
    address = input("Enter address: ")
    dob = input("Enter date of birth (YYYY-MM-DD): ")
    sql = "INSERT INTO seller (sid, first_name, last_name, phone_no, address, dob) VALUES (%s, %s, %s, %s, %s, %s)"
    val = (new_sid, first_name, last_name, phone_no, address, dob)  
    curr.execute(sql, val)
    curr.execute("insert into seller_acc values ('"+str(new_sid)+"','0');")
    curr.execute("set autocommit = 1;")
    print("New seller added with sid:", new_sid)

while(1):
    print("|***********************|")
    print("|  WELCOME TO CLOOCEAN  |")
    print("|***********************|")
    print("|***********************|")
    print("| 1. Login              |")
    print("| 2. Register           |")
    print("| 3. Admin              |")
    print("| 4. Exit               |")
    print("|***********************|")
    n = int(input("Enter your choice : "))
    if(n==1):
        while(1):
            print("|***********************|")
            print("|         LOGIN         |")
            print("|***********************|")
            print("|***********************|")
            print("| 1. Login as customer  |")
            print("| 2. Login as seller    |")
            print("| 3. Go Back            |")
            print("| 4. Exit               |")
            print("|***********************|")
            n1 = int(input("Enter your choice : "))
            if(n1==1):
                while(1):
                    print("*************************")
                    print("1.Enter cid")
                    print("2.Go back to main menu")
                    print("*************************")
                    n3 = int(input("Enter your choice : "))
                    if(n3 == 1):
                        cid = int(input("Enter your cid = "))
                        pswrd = input("Enter your password = ") 
                        if checkLogin(cid)& login(pswrd) == True :
                            while(1):
                                print("******** MAIN MENU ********")
                                print("1. View all products")
                                print("2. View all combos")
                                print("3. Add a product to cart")
                                print("4. Add a combo to cart")
                                print("5. View cart")
                                print("6. View History")
                                print("7. My profile")
                                print("8. Back")
                                print("9. Exit")
                                print("***************************")

                                n2 = int(input("Enter your choice: "))

                                if(n2==1):
                                    viewAllProducts()

                                elif(n2==2):
                                    viewAllCombos()

                                elif(n2==3):
                                    p = input("Enter the pid of the product to be added: ")
                                    qty = int(input("Enter the quantity of the product to be added: "))
                                    addProductToCart(cid,p,qty)

                                elif(n2==4):
                                    co = input("Enter the comboid of the combo to be added")
                                    qty = int(input("Enter the quantity of the combo to be added"))
                                    addComboToCart(cid,co,qty)

                                elif(n2==5):
                                    viewCart(cid)
                                    while(1):
                                        print("*************************")
                                        print("1. Drop any product/combo from cart")
                                        print("2. Checkout cart")
                                        print("3. Go Back")
                                        print("*************************")
                                        n3 = int(input("Enter your choice : "))
                                        if(n3 == 1):
                                            while(1):
                                                print("*******************************")
                                                print("1. Drop a product from cart")
                                                print("2. Drop a combo from cart")
                                                print("3. Go Back")
                                                print("*******************************")
                                                n5 = int(input("Enter your choice : "))
                                                if(n5 == 1):
                                                    pid = input("Enter the product id : ")
                                                    qty = input("Enter the quantity you want to decrease : ")
                                                    dropproduct(pid,cid,qty)
                                                elif(n5 == 2):
                                                    combo_id = input("Enter the combo id : ")
                                                    qty = input("Enter the quantity you want to decrease : ")
                                                    dropcombo(combo_id,cid,qty)
                                                elif(n5 == 3):
                                                    break
                                                else:
                                                    print("Invalid Input")            
                                        elif(n3 == 2):
                                            checkoutCart(cid)
                                        elif(n3 == 3):
                                            break
                                        else:
                                            print("Invalid Input")

                                elif(n2==6):
                                    viewHistory(cid)

                                elif(n2==7):
                                    myProfilecustomer(cid)
                                    print() 
                                    choice = input("Press 1 to go back. \n")
                                    if(choice == 1):
                                        continue
                                    else:
                                        print("Invalid Input")
        
                                elif(n2==8):
                                    break

                                elif(n2==9):
                                    print(" ")
                                    print("THANK YOU FOR VISITING CLOOCEAN, HOPE TO SEE YOU AGAIN !!!")
                                    print("")
                                    exit(0)

                                else:
                                    print("Enter a valid choice")

                        else:
                            print("Customer ID not found or Password is incorrect")

                    elif(n3 == 2):
                        break

                    else:
                        print("Invalid Input")            

            elif(n1==2):
                
                while(1):
                    print("*************************")
                    print("1.Enter sid")
                    print("2.Go back to main menu")
                    print("*************************")
                    n3 = int(input("Enter your choice : "))
                    if(n3 == 1):
                        sid = int(input("Enter sid: "))
                        pswrd1 = input("Enter password: ")
                        if checkLogin(sid) & login(pswrd1) == True:
                            while(1):
                                print("********** MAIN MENU **********")
                                print("1. View my products")
                                print("2. View my combos")
                                print("3. Edit product/combo details")
                                print("4. Add product")
                                print("5. Add combo")
                                print("6. View bestseller")
                                print("7. My profile")
                                print("8. Go Back")
                                print("9. Exit")
                                print("********************************")
                                n2 = int(input("Enter your choice :"))
                                print("********************************")
                                if(n2==1):
                                    viewAllSellerProducts(sid)
                                elif(n2==2):
                                    viewAllSellerCombos(sid)
                                elif(n2==3):
                                    while(1):
                                        print("*********** EDIT **************")
                                        print("1. Update product stock")
                                        print("2. Update combo stock")
                                        print("3. Update products cost")
                                        print("4. Update combo cost")
                                        print("5. Go back")
                                        print("*******************************")
                                        n4 = int(input("Enter your choice : "))
                                        print("*******************************")
                                        if(n4 == 1):
                                            pid = input("Enter the product id : ")
                                            if checkpid(sid,pid) == True:
                                                updateproductstock(pid)
                                            else:
                                                print("Product ID not found")    
                                        elif(n4 == 2):
                                            pid = input("Enter the product id : ")
                                            if checkpid(sid,pid) == True:
                                                updatecombosstock(pid)
                                            else:
                                                print("Product ID not found")  
                                        elif(n4 == 3):
                                            pid = input("Enter the product id : ")
                                            if checkpid(sid,pid) == True:
                                                updateproductscost(pid)
                                            else:
                                                print("Product ID not found")  
                                            
                                        elif(n4 == 4):
                                            pid = input("Enter the product id : ")
                                            if checkpid(sid,pid) == True:
                                                updatecombocost(pid)
                                            else:
                                                print("Product ID not found")
                                        elif(n4 == 5):
                                            break
                                        else:
                                            print("Invalid Input")

                                            
                                elif(n2==4):
                                    print("************ ENTER PRODUCT DETAILS ************")
                                    pid = input("Enter the product id : ")
                                    if checkallpid(pid) == False:
                                        product_name = input("Enter the product name : ")
                                        size = input("Enter the product size : ")
                                        color = input("Enter the product color : ")
                                        cost = input("Enter the product cost : ")
                                        stock = input("Enter the product stock : ")
                                        category = input("Enter the product category : ")
                                        print("********************************************")
                                        print("Product added successfully !!!")
                                        print("********************************************")
                                        addProductforseller(pid,product_name,size,color,cost,stock,sid,category)
                                    else:
                                        print("Product ID already exists")
                                    
                                elif(n2==5):
                                    print("************ MAKE A COMBO ************")
                                    combo_id = input("Enter the combo id : ")
                                    if checkallcomboid(combo_id) == False:
                                        pid1 = input("Enter pid1 : ")
                                        pid2 = input("Enter pid2 : ")
                                        if checkallpid(pid1) & checkallpid(pid2) == True:
                                            cost = input("Enter the combo cost : ")
                                            stock = input("Enter the combo stock : ")
                                            print("********************************************")
                                            print("Combo added successfully !!!")
                                            print("********************************************")
                                            addComboforseller(combo_id,pid1,pid2,cost,stock,sid)
                                        else:
                                            print("Pid does not exists")    
                                    else:
                                        print("Combo ID already exists")

                                elif(n2==6):
                                    viewbestseller()

                                elif(n2==7):
                                    myProfileseller(sid) 
                                
                                elif(n2==8):    
                                    break

                                elif(n2 == 9):
                                    exit(0)

                                else:
                                    print("Enter a valid choice")

                            else:
                                print("Seller ID not found")
                                
                    if(n3 == 2):
                        break

                    else:
                        print("Invalid Input")

            elif(n1==3):
                break

            elif(n1==4):
                print(" ")
                print("THANK YOU FOR VISITING CLOOCEAN, HOPE TO SEE YOU AGAIN !!!")
                print("")
                exit(0)

            else:
                print("Enter valid option")
    elif(n == 2):
        while(1):
            print("|**************************|")
            print("|      REGISTERATION       |")
            print("|**************************|")
            print("|**************************|")
            print("| 1. Register as customer  |")
            print("| 2. Register as seller    |")
            print("| 3. Go Back               |")
            print("| 4. Exit                  |")
            print("|**************************|")
            n1 = int(input("Enter your choice : "))
            if(n1==1):
                insertcid()
            elif(n1==2):
                insertsid()
            elif(n1==3):
                break
            elif(n1==4):
                print(" ")
                print("THANK YOU FOR VISITING CLOOCEAN, HOPE TO SEE YOU AGAIN !!!")
                print("")
                exit(0) 
            else:
                print("Invalid Input")      

    elif(n == 3):
        print("*************************************************************************")
        username = input("Enter username : ")
        password = input("Enter password : ")
        if(username == "admin" and password == "admin"):
            while(1):
                print("*************************************************************************")
                print("1. Check Top selling products by category")
                print("2. Check Customer id with the highest total value")
                print("3. Get total earnings of sellers by category")
                print("4. Get the total number of products and combos sold by category and size")
                print("5. Check all the customer ids for whom the cart is empty")
                print("6. Go Back")
                print("7. Exit")
                print("*************************************************************************")
                n4 = int(input("Enter your choice : "))
                print("*************************************************************************")
                if(n4 == 1):
                    topsellingproduct()
                elif(n4 == 2): 
                    cidhighestvalue()
                elif(n4 == 3):    
                    totalearnsellerbycateg()
                elif(n4 == 4):
                    totalnoprodcombycatensize()
                elif(n4 == 5): 
                     cidemptycart()
                elif(n4 == 6):
                    break    
                elif(n4 == 7):
                    print(" ")
                    print("THANK YOU FOR VISITING CLOOCEAN, HOPE TO SEE YOU AGAIN !!!")
                    print("")
                    exit(0)  
                else:
                    print("INVALID INPUT")      

    elif(n == 4):
        print(" ")
        print("THANK YOU FOR VISITING CLOOCEAN, HOPE TO SEE YOU AGAIN !!!")
        print("")
        exit(0)
    else:
        print("INVALID INPUT")                          