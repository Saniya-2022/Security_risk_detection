from database.mongo import alerts_collection

print(alerts_collection.count_documents({}))
