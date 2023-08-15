#!/usr/bin/env python3
"""
 Find top students
"""
import pymongo


def top_students(mongo_collection):
    """
    Find and sort students 
    """
    return mongo_collection.aggregate([
        {"$project": {"name": "$name", "averageScore": {"$avg": "$topics.score"}}},
        {"$sort": {"averageScore": -1}}
    ])
