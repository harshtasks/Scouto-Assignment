import pymongo, dns
import os, re

password = os.getenv("password")
user = os.getenv("user")

client = pymongo.MongoClient(
    "mongodb+srv://" + user + ":" + password +
    "@cluster.geizz.mongodb.net/?retryWrites=true&w=majority")


db = client.library
books = db.books
trac = db.transactions


def prett(data):
    items = []
    for item in data:
        items.append(item)
    return items


def insert(query):
    data = books.insert_one(query)
    return data.inserted_id


def find_books_term(query):
    term = '(?i)' + re.escape(query['term'])
    data = books.find({"book_name": {"$regex": term}}, {"_id": 0})
    return prett(data)


def find_books_range(query):
    data = books.find({"rent": {
        "$gt": query["gt"], "$lt": query["lt"]
    }}, {"_id": 0})
    return prett(data)


def find_books(query):
    term = '(?i)' + re.escape(query['term'])
    data = books.find({
        "book_name": {"$regex": term},
        "rent": {"$gt": query["gt"], "$lt": query["lt"]},
        "category": query['category'].lower()
    }, {"_id": 0})
    return prett(data)


def issue_book(query):
    detail = books.find_one({'book_name': query['book']})
    if detail is not None:
        trac.insert_one({
            'book_name': query['book'],
            'person': query['person'],
            'issue_date': query['issue_date'],
            'return_date': None,
            'rent': detail['rent'],
            'total_rent': None
        })
        return {'status': 'Book Issued'}
    else:
        return {'status': 'Book not found'}


def return_book(query):
    detail = trac.find_one({
        'book_name': query['book'],
        'person': query['person']
    })
    if detail is not None and detail['return_date'] is None:
        rtdate = query['return_date']
        isdate = detail['issue_date']
        if rtdate > isdate:
            total_rent = (rtdate - isdate).days * detail['rent']
        else:
            return {'status': 'Error'}
        trac.update_one(detail, {'$set': {
            'return_date': rtdate,
            'total_rent': total_rent
        }})
        return {'status': 'Book Returned'}
    else:
        return {'status': 'Error'}


def book_issued(query):
    count = trac.count_documents({'book_name': query['book']})
    data = trac.find({
        'book_name': query['book'], 'total_rent': None
    }, {'person':1, '_id':0})
    
    return {
        'total_issued': count, 
        'currently_issued': prett(data)
    }


def book_rent(query):
    data = trac.aggregate([
        {'$match': {'book_name': query['book']}},
        {'$group': {
            '_id': None,
            'total_rent': {'$sum': '$total_rent'}
        }}
    ])
    tdata = prett(data)
    if len(tdata) == 0:
        return {'status': 'Book not issued to anyone'}
    return {'total_rent': tdata[0]['total_rent']}


def person_books(query):
    data = trac.find({
        'person': query['person'], 'total_rent': None
    }, {'book_name': 1, '_id': 0})
    
    return {
        'person': query['person'], 
        'books_issued': prett(data)
    }


def issue_date_range(query):
    start = query['start']
    end = query['end']
    if start > end:
        return []
    data = trac.find({
        'issue_date': {
            '$gte': start, '$lte': end
        }
    }, {'book_name': 1, 'person': 1, '_id': 0})
    return prett(data)
    
