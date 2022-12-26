from django.shortcuts import render
from yahoo_fin.stock_info import *
from django.http import HttpResponse
from threading import Thread
from time import sleep
from queue import Queue
from asgiref.sync import sync_to_async

# Create your views here.

def stockPicker(request):
    stock_picker=tickers_nifty50()
    print(stock_picker)
    return render(request,'app/stockpicker.html',{'stockpicker':stock_picker})

@sync_to_async
def checkAuthenticated(request):
    if not request.user.is_authenticated:
        return False
    else:
        return True

async def stockTracker(request):
    is_loginned = await checkAuthenticated(request)
    if not is_loginned:
        return HttpResponse("Login First")
    stockpicker=request.GET.getlist('stockpicker')
    print(stockpicker)
    data={}
    available_stocks=tickers_nifty50()
    for i in stockpicker:
        if i in available_stocks:
            pass
        else:
            return HttpResponse("Error")

    n_threads=len(stockpicker)
    thread_list=[]
    que=Queue()
    for i in range(n_threads):
        threads=Thread(target=lambda q,arg1:q.put({arg1:get_quote_table(arg1)}),args=(que,stockpicker[i]))
        thread_list.append(threads)
        thread_list[i].start()
    
    for thread in thread_list:
        thread.join()
    
    while not que.empty():
        res=que.get()
        data.update(res)
    
    print(data)
    return render(request,'app/stocktracker.html',{'data':data,'room_name':'track'})