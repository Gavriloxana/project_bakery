from mongoengine import connect

# เชื่อม MongoDB Local
connect(db="pos_db", host="localhost", port=27017)

# หรือ MongoDB Atlas
# connect(db="pos_db", host="mongodb+srv://<username>:<password>@cluster0.mongodb.net/pos_db?retryWrites=true&w=majority")
