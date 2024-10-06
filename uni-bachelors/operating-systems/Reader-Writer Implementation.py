# Maryam Rezaee (981813088)
# Reader-Writer Implementation

import threading
import logging
import random



# defining a new lock class for RW problem
# this class allows mulptiple readers through a lock
class RWLock:


    def __init__(self):
        
        self.monitor = threading.Lock()
        self.can_write = threading.Condition(self.monitor)
        self.can_read = threading.Condition(self.monitor)


    # writer aquiring lock of critical section
    # allows only one writer and no readers
    def wacquire(self, buffer):
        
        self.monitor.acquire()
        buffer.w_queue += 1
        while not buffer.writable():
            self.can_write.wait()
        buffer.w_queue -= 1
        buffer.count += 1
        self.monitor.release()

        
    # reader aquiring lock of critical section
    # allows multiple readers but no writers
    def racquire(self, buffer):
        
        self.monitor.acquire()
        while not buffer.readable():
            self.can_read.wait()
        buffer.user = 1
        buffer.count += 1
        self.monitor.release()

        
    # writer or reader releasing cs lock
    def release(self, buffer):
        
        self.monitor.acquire()
        buffer.count -= 1         # update count of users in buffer
        if (buffer.count == 0):   # if no users are in buffer
            buffer.user = 0       # set user type to priorotise writer
            
        # decide whether to notify a writer or readers
        # and call the notification for that condition
        if (buffer.w_queue) and (buffer.count == 0):
            self.can_write.notify()
        elif (not buffer.w_queue):
            self.can_read.notify_all()
            
        self.monitor.release()


    
# buffer class of shared data for syncing threads
# holds counts of users accessing or waiting on data
class Buffer:


    def __init__(self):
        
        self.data = []    # the shared data
        self.user = 0     # type of user accessing data
        self.count = 0    # count of users accessing buffer
        self.w_queue = 0  # count of waiting writers


    def writable(self):
        # allow writing when no one is accessing data
        return (self.count == 0)


    def readable(self):
        # allow reading when no one is accessing data
        # or other readers are accessing data
        # priority given to writers not being waiting
        return ((self.count == 0) or (self.user == 1)) and (self.w_queue == 0)



# synced writer function
# adds an int to shared data list
def writer(buffer, lock):
    
    lock.wacquire(buffer)                     # writer wants to write
    logging.info('is starting to write...')   # enters critial section

    value = random.randint(0, 100)
    buffer.data.append(value)
    logging.info(f'writes: {value}')

    logging.info('is exiting...')            # exits critical section
    lock.release(buffer)                     # releases lock on buffer



# synced reader function
# reads ints of shared data list
def reader(buffer, lock):

    lock.racquire(buffer)                    # reader wants to read
    logging.info('is starting to read...')   # enters critial section

    if buffer.data == []:
        logging.info('reads empty buffer.')
    else:
        for item in buffer.data:
            logging.info(f'reads: {item}')

    logging.debug('is exiting...')           # exits critical section
    lock.release(buffer)                     # releases lock



if __name__ == '__main__':
    
    buff = Buffer()        # shared data
    lock = RWLock()        # lock for syncing access to shared data
    ids = [0, 1]           # user types, 0 for writer, 1 for reader
    wcount, rcount = 0, 0  # number of general writers and readers
    threads = []           # list of threads created
    logging.basicConfig(level = logging.INFO,
                        format = '{threadName} {message}',
                        style = '{')

    # loop to create 10 threads
    for i in range(0, 10):
        # choose the type of thread
        user = random.choice(ids)

        # according to selected type create thread
        # and set the name based on previous threads
        if user == 0:
            wcount += 1
            thread = threading.Thread(target = writer, args = (buff, lock,))
            thread.name = f'Writer {wcount}'
        else:
            rcount += 1
            thread = threading.Thread(target = reader, args = (buff, lock,))
            thread.name = f'Reader {rcount}'

        # add created thread to list
        # and start its execution
        threads.append(thread)
        logging.info(f'is starting {thread.name}...')
        thread.start()


    # finally join the created threads
    for thread in threads:
        thread.join()


        
