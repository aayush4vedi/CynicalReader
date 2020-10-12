import time
import json
from datetime import datetime
import logging

import sqlite3
from utilities import print_in_color as pc


def return_all_descendents(ts,root):
    """
        Returns all the descendents of node in tag-tree where node.NodeName = root
    """

    pc.printMsg(" \t\t???????????????????????????????????? Query for All Descendents of NodeName = {}".format(root))

    descendents = []
    th_db = 'dbs/th.db'
    th_table = 'th_' + str(int(ts)) 
    conn = sqlite3.connect(th_db, timeout=10)
    c = conn.cursor()
    pc.printMsg("\t -------------------------------------- < query_children_th: DB Connection Opened > ---------------------------------------------\n")
    
    q = 'select LeftMptt, RightMptt from ' + th_table + ' where NodeName = ?'
    root_mptt_values = c.execute(q,('{}'.format(root),))
    root_mptt_values = c.fetchone()
    if root_mptt_values is None:
        pc.printErr(" \t\tXXXXXXXXXXXXX-> Asked node with name = {} not found in table = {} \t...... returning NULL as descendents".format(root,th_table))
        return descendents

    pc.printMsg(" root.LeftMptt = {} , root.RightMptt = {} \n".format(root_mptt_values[0], root_mptt_values[1]))

    q = 'select * from ' + th_table + ' where LeftMptt > ? AND RightMptt < ?'
    d = (root_mptt_values[0], root_mptt_values[1])
    rows_head = c.execute(q,d)
    rows = rows_head.fetchall()
    for row in rows:
        pc.printWarn(" \t\t * DESCENDENT of {} :: {}".format(root,row))
        descendents.append(row)

    conn.commit()
    conn.close()
    pc.printMsg("\t -------------------------------------- < query_children_th: DB Connection Closed > ---------------------------------------------\n")
    return descendents




def return_imm_children(ts,root):
    """
        INPUT: ts, root.name (string)

        OUTPUT:
            Returns full row(ID, NodeName, LeftMptt, RightMptt, DepthLevel, ItemCount, AvgPopI, HN_IDs,R_IDs) 
            of just the immediate children of node in tag-tree where node.NodeName = root
    """

    # pc.printMsg(" \t\t ???????????????????????????????????? Query for Immediate Children of NodeName = {}".format(root))

    children = []
    th_db = 'dbs/th.db'
    th_table = 'th_' + str(int(ts)) 
    conn = sqlite3.connect(th_db, timeout=10)
    c = conn.cursor()
    # pc.printMsg("\t -------------------------------------- < query_children_th: DB Connection Opened > ---------------------------------------------\n")
    
    q = 'select LeftMptt, RightMptt, DepthLevel from ' + th_table + ' where NodeName = ? ;'
    root_mptt_values = c.execute(q,('{}'.format(root),))
    root_mptt_values = c.fetchone()
    if root_mptt_values is None:
        pc.printErr(" \t\tXXXXXXXXXXXXX-> Asked node with name = {} not found in table = {} \t...... returning NULL as children".format(root,th_table))
        return children

    pc.printMsg(" \t ROOT: {} \troot.LeftMptt = {} , root.RightMptt = {} , root.DepthLevel = {}\n".format(root,root_mptt_values[0], root_mptt_values[1],root_mptt_values[2]))

    q = 'select * from ' + th_table + ' where LeftMptt > ? AND RightMptt < ? And DepthLevel = ? '
    d = (root_mptt_values[0], root_mptt_values[1],root_mptt_values[2]+1)
    rows_head = c.execute(q,d)
    rows = rows_head.fetchall()
    for row in rows:
        pc.printWarn(" \t\t *  CHILD of {} :: {}".format(root,row[1]))
        children.append(row)

    conn.commit()
    conn.close()
    # pc.printMsg("\t -------------------------------------- < query_children_th: DB Connection Closed > ---------------------------------------------\n")
    return children


def ReturnTopTenItemsofTag(tag, ts,lim):
    """
        returns top #lim number of  <ID,SourceSite,Title,Url,Popi> items(HN & r) of tag
    """
    # 1. get top 10 ids from th_table
    
    th_db = 'dbs/th.db'
    th_table = 'th_' + str(int(ts)) 
    conn = sqlite3.connect(th_db, timeout=10)
    c = conn.cursor()

    # 1.1 doing it for HN items
    q = 'select HN_IDs from ' + th_table + ' where NodeName = ?'
    hn_itemIDs = c.execute(q,('{}'.format(tag),));
    hn_itemIDs = c.fetchone()[0]            # returns the array in form of string: hn -> hn_itemIDs[0] = '['
    conn.commit()

    hn_itemIDs = hn_itemIDs.strip('][').split(', ')         # convert the string to list
    top_hn_itemIDs = hn_itemIDs[:lim]

    # 1.2 doing it for reddit 
    q = 'select r_IDs from ' + th_table + ' where NodeName = ?'
    r_itemIDs = c.execute(q,('{}'.format(tag),));
    r_itemIDs = c.fetchone()[0]            # returns the array in form of string: hn -> hn_itemIDs[0] = '['
    conn.commit()
    
    r_itemIDs = r_itemIDs.strip('][').split(', ')         # convert the string to list
    top_r_itemIDs = r_itemIDs[:lim]

    conn.close()
    # print(hn_itemIDs)
    # print(top_r_itemIDs)

    # 2. get item details for each item from wc_table
    wc_db = 'dbs/wc.db'
    wc_table = 'wc_' + str(int(ts))
    conn = sqlite3.connect(wc_db)
    c = conn.cursor()

    top_hn_items_wc = []
    top_r_items_wc = []

    print("\n----------------- Here are top {} HN items for tag = {}".format(lim,tag))
    for item in top_hn_itemIDs:
        if item:
            q = 'select ID, Title, Url, CreationDate, PopI from ' + wc_table + ' where ID = ' + item
            wc_item = c.execute(q)
            wc_item = c.fetchall()[0]
            print(wc_item)              # retuns a list: [ID, Title, Url, CreationDate, PopI] 
            conn.commit()
            top_hn_items_wc.append(wc_item)

    print("\n------------------ Here are top {} reddit items for tag = {}".format(lim,tag))
    for item in top_r_itemIDs:
        if item:
            q = 'select ID, Title, Url, CreationDate, PopI from ' + wc_table + ' where ID = ' + item
            wc_item = c.execute(q)
            wc_item = c.fetchall()[0]
            print(wc_item)              # retuns a list: [ID, Title, Url, CreationDate, PopI] 
            conn.commit()
            top_r_items_wc.append(wc_item)
    
    conn.close()
    return top_hn_items_wc,top_r_items_wc