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
        Returns *NODE* just the immediate children of node in tag-tree where node.NodeName = root
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

    pc.printMsg(" root.LeftMptt = {} , root.RightMptt = {} , root.DepthLevel = {}\n".format(root_mptt_values[0], root_mptt_values[1],root_mptt_values[2]))

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