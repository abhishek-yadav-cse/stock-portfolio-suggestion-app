from app.strategies import get_stock_list_all, get_strategy_stock_info, get_historical_strategy_stock_value
from flask import render_template, flash, redirect, request
from app import app
from .forms import InvestForm



@app.route('/', methods=['GET', 'POST'])
def invest():
    form = InvestForm(request.form)
    if request.method =='POST':
        try:
            form = InvestForm(request.form)
            amount = float(request.form['amount'])
            if amount < 5000:

                return render_template('error.html')
            else:
                print(amount)
            choices = request.form.getlist('strategies')
            if len(choices)<=0 or len(choices)>2:
                return render_template('error.html')
            print(choices)
            stocklist = get_stock_list_all(choices)
            details = get_strategy_stock_info(stocklist, amount)
            print ("details", details)
            print(stocklist)
            print('1234')
            history = get_historical_strategy_stock_value(stocklist, amount)
            print("history ",history)
            return render_template("result.html", details=details, history=history)

        except:
            return render_template('error.html')

    return render_template('invest.html', form=form,
                           strategy=app.config['STRATEGY'])

