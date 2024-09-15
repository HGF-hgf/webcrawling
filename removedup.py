from pymongo import MongoClient # type: ignore

def remove_duplicates():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['news']
    collection = db['newscrawl']

    # Lọc các tài liệu trùng lặp
    pipeline = [
        {
            "$group": {
                "_id": "$url",
                "unique_ids": {"$addToSet": "$_id"},
                "count": {"$sum": 1}
            }
        },
        {
            "$match": {
                "count": {"$gt": 1}
            }
        }
    ]

    duplicates = collection.aggregate(pipeline)

    for doc in duplicates:
        unique_ids = doc["unique_ids"]
        # Giữ lại một tài liệu duy nhất và xóa các tài liệu còn lại
        unique_ids.pop(0)
        collection.delete_many({"_id": {"$in": unique_ids}})

    # Tạo chỉ mục duy nhất để ngăn chặn việc chèn các tài liệu trùng lặp trong tương lai
    collection.create_index([("url", 1)], unique=True)