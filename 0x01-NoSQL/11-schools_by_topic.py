#!/usr/bin/env python3
"""
Where should I learn Python?
"""
import pymongo


def schools_by_topic(mongo_collection, topic):
    """
    find by specific values
    """
    return mongo_collection.find({"topics":  {"$in": [topic]}})
