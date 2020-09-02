
from django.shortcuts import render, redirect
from .models import Stock
from .forms import StockForm
from django.contrib import messages



def home(request):
    import requests
    import json 

    if request.method == "POST":
        ticker = request.POST['ticker'] # name=ticker의 value를 가져옴
        api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + ticker + "/quote?token=password")
        
        try:
            api = json.loads(api_request.content)
        except Exception as e:
            api = 'Error...'

        return render(request, 'home.html', {'api':api})
    else:
        # 홈페이지 기본값
        api_request = requests.get("https://cloud.iexapis.com/stable/stock/aapl/quote?token=password")
        
        try:
            api = json.loads(api_request.content)
        except Exception as e:
            api = 'Error...'

        return render(request, 'home.html', {'api':api, 'ticker': "Enter Another Ticker Symbol Above"})

def add_stock(request):
    import time
    import requests
    import json 

    start = time.time() # 실행시간 확인

    if request.method == "POST":
        form = StockForm(request.POST or None)
        
        if form.is_valid():
            form.save()
            messages.success(request, ("추가되었습니다."))
            time = time.time() - start
            print('add_stock [POST] :' + str(time))
            return redirect('add_stock')
    else:
        ticker = Stock.objects.all()
        output = []
        for ticker_item in ticker: 
            api_request = requests.get("https://cloud.iexapis.com/stable/stock/" + str(ticker_item) + "/quote?token=password")
            
            try:
                api = json.loads(api_request.content)
                output.append(api)
                time = time.time() - start
                print('add_stock [get] :' + str(time))
            except Exception as e:
                api = 'Error...'
            
        return render(request, 'add_stock.html', {'ticker':ticker, 'output':output})

    
            

def delete(request, stock_id):
    import time

    start = time.time() # 실행시간 확인

    item = Stock.objects.get(pk=stock_id)
    item.delete()
    messages.success(request, ("삭제되었습니다."))

    time = time.time() - start
    print('delete : ' + str(time))
    return redirect(add_stock)

