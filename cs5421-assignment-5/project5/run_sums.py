import argparse
from sqlalchemy.orm import sessionmaker
import time
from db_connect import get_conn
from sqlalchemy import Column, Integer, Float
from sqlalchemy.ext.declarative import declarative_base

# Declarative Mapping for account table
Base = declarative_base()
class Account(Base):
	__tablename__ = 'account'

	id = Column(Integer, primary_key=True)
	branch = Column(Integer)
	balance = Column(Float)

## Argument parser to take the parameters from the command line
## Example on how to run: python run_sums.py 10 READ_COMMITTED
parser = argparse.ArgumentParser()
parser.add_argument('S', type = int, help = 'number of sums')
parser.add_argument('I', help = 'isolation level')
args = parser.parse_args()

## Execute a sum query and return the results
def sum_balance(sess):
    ## 1. Execute a query that sum the balance of all accounts.
    ## 2. Fetch the result and return it.
    return sess.query(Account).count()

## Create S sums operations
def S_sums(sess, S):
    sums = []
    start = time.time()

    for i in xrange(0, S):
        while True:
            try:
                sum = sum_balance(sess)
                sums.append(sum)
            except Exception as e:
                print e
                continue
            break

    stop = time.time()
    return sums, stop-start

## Create the engine and run the sums
engine = get_conn()
Session = sessionmaker(bind=engine.execution_options(isolation_level=args.I, autocommit=True))
sess = Session()
sums, time = S_sums(sess, args.S)
print sums
