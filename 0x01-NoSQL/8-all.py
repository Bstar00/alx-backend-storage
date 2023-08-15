#!/usr/bin/env python3
"""
Python function that inserts a new document in a collection based on kwargs
"""
import pymongo


def list_all(mongo_collection):
    """
    function to list all documents in a collection
    """
    if not mongo_collection:
        return []
    documents = mongo_collection.find()
    return [post for post in documents]
