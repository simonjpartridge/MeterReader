from server import app


# print(server)


app.debug = True
app.run(host = '0.0.0.0',port=80)