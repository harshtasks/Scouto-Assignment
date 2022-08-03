from flask import Blueprint, request
from datetime import datetime
from .. import extensions as ext
import json

api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/find')
def books_query():
    term = request.args.get('term')
    lt = request.args.get('lt')
    gt = request.args.get('gt')
    category = request.args.get('category')
    data = []

    try:
        if term is None and None not in [lt, gt]:
            data = ext.find_books_range({
                'lt': int(lt), 'gt': int(gt)
            })

        elif None in [lt, gt] and term is not None:
            data = ext.find_books_term({'term': term})

        elif None not in [lt, gt, term, category]:
            data = ext.find_books({
                'term': term, 'lt': int(lt),
                'gt': int(gt), 'category': category
            })
    except:
        data = []

    return json.dumps(data)


@api.route('/book/issue')
def issue_book():
    book = request.args.get('book')
    person = request.args.get('person')
    issue_date = request.args.get('date')
    data = []

    try:
        issue_date = datetime.strptime(issue_date, '%d-%m-%Y')
        if None not in [book, person, issue_date]:
            data = ext.issue_book({
                'book': book,
                'person': person,
                'issue_date': issue_date
            })
    except:
        data = {'status': 'Error'}

    return json.dumps(data)


@api.route('/book/return')
def return_book():
    book = request.args.get('book')
    person = request.args.get('person')
    return_date = request.args.get('date')
    data = []

    try:
        return_date = datetime.strptime(return_date, '%d-%m-%Y')
        if None not in [book, person, return_date]:
            data = ext.return_book({
                'book': book,
                'person': person,
                'return_date': return_date
            })
    except:
        data = {'status': 'Error'}

    return json.dumps(data)


@api.route('/book/issued')
def book_issued():
    book = request.args.get('book')
    data = []
    if book is not None:
        data = ext.book_issued({'book': book})
    return json.dumps(data)


@api.route('/book/rent')
def book_rent():
    book = request.args.get('book')
    data = []
    if book is not None:
        data = ext.book_rent({'book': book})
    return json.dumps(data)


@api.route('/person/books')
def person_books():
    person = request.args.get('person')
    data = []
    if person is not None:
        data = ext.person_books({'person': person})
    return json.dumps(data)


@api.route('/book/daterange')
def issue_date_range():
    start = request.args.get('start')
    end = request.args.get('end')
    data = []
    try:
        start = datetime.strptime(start, '%d-%m-%Y')
        end = datetime.strptime(end, '%d-%m-%Y')
        print(start, end)
        if None not in [start, end]:
            data = ext.issue_date_range({
                'start': start,
                'end': end
            })
    except:
        data = []

    return json.dumps(data)




# @api.route('/find/<term>')
# def find_by_term(term):
#     data = ext.find_books_term({'term': term})
#     return json.dumps(data)


# @api.route('/find/<int:gt>/<int:lt>')
# def find_by_range(gt, lt):
#     data = ext.find_books_range({'lt': int(lt), 'gt': int(gt)})
#     return json.dumps(data)


# @api.route('/find/<term>/<int:gt>/<int:lt>/<category>')
# def find_by_all(term, gt, lt, category):
#     data = ext.find_books({
#         'term': term,
#         'lt': int(lt),
#         'gt': int(gt),
#         'category': category
#     })
#     return json.dumps(data)


# @api.route('/issue/<book>/<person>/<date>')
# def issue_book(book, person, date):
#     try:
#         issue_date = datetime.strptime(date, '%d-%m-%Y')
#     except:
#         return {'status': 'Invalid issue date'}
#     ext.issue_book({
#         'book': book,
#         'person': person,
#         'date': issue_date
#     })
#     return {'status': 'Book Issued'}


# @api.route('/return/<book>/<person>/<date>')
# def return_book(book, person, date):
#     try:
#         return_date = datetime.strptime(date, '%d-%m-%Y')
#     except:
#         return {'status': 'Invalid return date'}
#     ext.return_book({
#         'book': book,
#         'person': person,
#         'date': return_date
#     })
#     return {'status': 'Book Returned'}



