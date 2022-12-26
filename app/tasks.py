from celery import shared_task
from yahoo_fin.stock_info import *
from threading import Thread
from queue import Queue
from asyncio.events import new_event_loop,set_event_loop
from channels.layers import get_channel_layer

@shared_task(bind=True)
def update_stock(self,stockpicker):
    data={}
    available_stocks=tickers_nifty50()
    for i in stockpicker:
        if i in available_stocks:
            pass
        else:
            return stockpicker.remove(i)

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

    channel_layer = get_channel_layer()
    loop = new_event_loop()

    set_event_loop(loop)
    loop.run_until_complete(channel_layer.group_send(
        "stock_track",
        {
            'type':'send_stock_update',
            'message':data
        }
    ))

    return "Done"