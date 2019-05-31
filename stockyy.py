from flask import Flask, render_template, request, flash
import pandas as pd
import quandl
import matplotlib.pyplot as plt
app = Flask(__name__, template_folder='templates')
app.secret_key = 'anyrandomsecretkey'
counter = 1
@app.route('/',methods = ['GET', 'POST'])
def stockyy():
    if request.method == 'POST':

        global counter
        quandl_code = request.form['datapath']
        
        if(quandl_code[0:4] != 'BSE/'):
            error = 'You have enetered an incorrect quandl code or a code which is unsupported(non Bombay Stock Exchange code) by this web application.'
            return render_template("home.html", error = error)

        df = quandl.get(quandl_code)
        row = len(df.index)
        col = len(df.columns)
        fig, ax = plt.subplots()
        pst_flow = 0
        ngt_flow = 0
        
        
        if(row>=220):
            LTSMA = []
            STSMA = []
            X_axis = []
            for i in range(0,20):
                LTSMA.append(sum(df.iloc[-220+i:-19+i, 3])/200)
            for i in range(0,20):
                STSMA.append(sum(df.iloc[-40+i:-19+i, 3])/20)
            for i in range(1,21):
                X_axis.append(str(i))
            for i in range(1,len(LTSMA)):
                if(LTSMA[i-1] < LTSMA[i]):
                    pst_flow = pst_flow + 1
                else:
                    ngt_flow = ngt_flow + 1
            flow_list = [pst_flow, ngt_flow]
            if (max(flow_list) == pst_flow):
                con1 = "Long Term Analysis: Retain or Buy"
            else:
                con1 = "Long Term Analysis: Sell"
            flow_list = []
            pst_flow = 0
            ngt_flow = 0
            for i in range(1,len(STSMA)):
                if(STSMA[i-1] < STSMA[i]):
                    pst_flow = pst_flow + 1
                else:
                    ngt_flow = ngt_flow + 1
            flow_list = [pst_flow, ngt_flow]
            if (max(flow_list) == pst_flow):
                con2 = "Short Term Analysis: Retain or Buy"
            else:
                con2 = "Short Term Analysis: Sell"
            plt.plot(X_axis, LTSMA, color='orange')
            plt.ylabel("SMA( orange:200 days - green:20 days)")
            plt.xlabel("SMA number (oldest to latest)")
            plt.title("Trend Analysis Graph")
            plt.plot(X_axis, STSMA, color='green')
            plt.savefig('static/spa'+str(counter)+'.png')
                

        elif(row>=40):
            STSMA = []
            X_axis = []
            for i in range (0,20):
                STSMA.append(sum(df.iloc[-40+i:-19+i,3])/20)
            for i in range(1,21):
                X_axis.append(str(i))
            plt.plot(X_axis, STSMA, color='green')
            plt.ylabel("SMA(20 days)")
            plt.xlabel("SMA number (oldest to latest)")
            plt.title("Short Term Trade Analysis Graph")
            plt.savefig('static/spa'+str(counter)+'.png')
            con1 = "Long Term Analysis: NA"
            for i in range(1,len(STSMA)):
                if(STSMA[i-1] < STSMA[i]):
                    pst_flow = pst_flow + 1
                else:
                    ngt_flow = ngt_flow + 1
            flow_list = [pst_flow, ngt_flow]
            if (max(flow_list) == pst_flow):
                con2 = "Short Term Analysis: Retain or Buy"
            else:
                con2 = "Short Term Analysis: Sell"
                
        else:
            con1 = "The source data set don't have enough data for prediction."
            con2 = "Try again with some other dataset."

        igr="/static/spa"+str(counter)+".png"
        counter = counter + 1
        return render_template("result.html", con1 = con1, con2 = con2, igr = igr)
    error=''
    return render_template("home.html",error=error)
    

        
if __name__ == "__main__":
    app.run(debug=True)

