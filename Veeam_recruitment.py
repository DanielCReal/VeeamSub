# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 13:43:57 2024

@author: Daniel Côrte-Real
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 12:40:57 2024

@author: Daniel Côrte-Real
"""

import os, shutil
#import schedule
import time
import sys
import hashlib


def hash_file(filepath):
    """Generate an MD5 hash for a file's contents."""
    hasher = hashlib.md5()
    with open(filepath, 'rb') as f:
        chunk = f.read(8192)
        while chunk:
            hasher.update(chunk)
            chunk = f.read(8192)
    return hasher.hexdigest()


def build_hash_table(source_directory):
    """Build a hash table where keys are file paths and values are hashes."""
    hash_table = {}
    for root, dirs, files in os.walk(source_directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            relative_path = os.path.relpath(filepath, source_directory)
            file_hash = hash_file(filepath)
            if relative_path not in hash_table:
                hash_table[relative_path] = file_hash
    return hash_table



def replica(replica_hash_table, origin, dest, log):
    
    
    source_hash_table = build_hash_table(origin)
    
    for key in source_hash_table:
        if (key in replica_hash_table):
            if (source_hash_table[key] != replica_hash_table[key]):
                
                absolute_path = os.path.join(origin, key)
                absolute_dest = os.path.join(dest, key)
                os.makedirs(os.path.dirname(absolute_dest), exist_ok=True)
                shutil.copy(absolute_path, absolute_dest)
                
                print("File " + key + " replaced (copied) sucessfully.\n")
                with open(log, "a") as record:
                    record.write("File " + key + " replaced (copied) sucessfully.\n")
        else:
            
            absolute_path = os.path.join(origin, key)
            absolute_dest = os.path.join(dest, key)
            os.makedirs(os.path.dirname(absolute_dest), exist_ok=True)
            
            shutil.copy(absolute_path, absolute_dest)
            
            print("File " + key +  " created sucessfully.\n")
            with open(log, "a") as record:
                record.write("File " + key + " created sucessfully.\n")
    
    for key in replica_hash_table:
        if (key not in source_hash_table):
            
            absolute_dest = os.path.join(dest, key)
            os.remove(absolute_dest)
            
            print("File " + key +  " removed sucessfully.\n")
            with open(log, "a") as record:
                record.write("File " + key +  " removed sucessfully.\n")

    
    return source_hash_table

        
        
        
        
        
        
        
        
        
def s(interval):
    source_path = sys.argv[1]
    dest_path = sys.argv[2]
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    replica_hash_table = build_hash_table(dest_path)
    while (True):
        replica_hash_table = replica(replica_hash_table, source_path, dest_path, sys.argv[3])
        time.sleep(int(interval)*60)
        
        

if (len(sys.argv) < 5):
    print("ERROR - Program usage: \n<source> <destination> <log file> <Interval (in minutes)>")
    sys.exit()

s(sys.argv[4])
        