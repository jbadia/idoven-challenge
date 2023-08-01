from redis import Redis
from rq import Worker

# import controllers
import dask
from modules import metrics

w = Worker(['default'], connection=Redis(host='redis', port=6379))
w.work()