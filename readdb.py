from pymongo import MongoClient  # type: ignore

def connect_db():
    client = MongoClient('mongodb+srv://ngvh1110:1234@cluster0.3f4lo.mongodb.net/')
    db = client['newsletter']
    return db

def build_query(category=None, meta=None, title=None, content=None):
    query = {}
    if category:
        query['category'] = {'$regex': category, '$options': 'i'}
    if meta:
        query['meta'] = {'$regex': meta, '$options': 'i'}
    if title:
        query['title'] = {'$regex': title, '$options': 'i'}
    return query

def search_db(collection_name, query):
    results = collection_name.find(query, {'title':1})
    return [article['title'] for article in results]

def main():
    db = connect_db()
    vneconomy_collection = db['vneconomy']
    cafef_collection = db['cafef']

    category = input('Enter category: ')
    meta = input('Enter time: ')
    meta2 = meta.replace('/', '-')
    title = input('Enter title: ')

    query = build_query(category , meta, title)
    query2 = build_query(category, meta2, title)

    vneconomy_results = search_db(vneconomy_collection, query)
    cafef_results = search_db(cafef_collection, query2)

    results = vneconomy_results + cafef_results

    with open ('results.txt', 'w', encoding ='utf-8') as file:
        for result in results:
            file.write(result + '\n')

if __name__ == '__main__':
    main()