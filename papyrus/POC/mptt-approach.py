#  NOTE: MPTT approach

# ------------------------ Tree Creation

def make_tree(root, l, level){      # for root: f(root, 1,0)
    r = l+1
    for (child in root.chldren):
        r = make_tree(child, r,level+1)

    root.l = l
    root.r = r
    root.level = level
    return r+1
}

# ------------------------------- Print all the descendends

def print_desc(root){
    """ fetch l & r values of root from sql-db
            mysql_query('SELECT title FROM tree WHERE parent="root";');   
    """
    l = c.execute('SELECT l FROM tree WHERE parent="root";')
    r = c.execute('SELECT r FROM tree WHERE parent="root";')

    desc = []
    rows = c.execute('SELECT * FROM tree WHERE lft BETWEEN '.$row['lft'].' AND '.$row['rgt'].' ORDER BY lft ASC;')
    for row in rows:
        desc.append(row)
    return desc
}

# ------------------------------ Print just the immediate children of root

def print_children(root){
    """ fetch l & r values of root from sql-db
            mysql_query('SELECT title FROM tree WHERE parent="root";');   
    """
    l = c.execute('SELECT l FROM tree WHERE parent="root";')
    r = c.execute('SELECT r FROM tree WHERE parent="root";')
    level = c.execute('SELECT level FROM tree WHERE parent="root";')

    desc = []
    rows = c.execute('SELECT * FROM tree WHERE lft BETWEEN '.$row['lft'].' AND '.$row['rgt'].' AND level = '.$(level+1).'ORDER BY lft ASC;')
    for row in rows:
        desc.append(row)
    return desc
}


#============================================================== PHP's original code ========================

<?php 

//NOTE: ----------------------------------------------------          this is simple DFS
// $parent is the parent of the children we want to see 
//$level is increased when we go deeper into the tree, used to display a nice indented tree 

function display_children($parent, $level) { 
    // retrieve all children of $parent 
    $result = mysql_query('SELECT title FROM tree WHERE parent="'.$parent.'";'); 

    // display each child 
    while ($row = mysql_fetch_array($result)) { 
        // indent and display the title of this child 
        echo str_repeat('  ',$level).$row['title']."n"; 
        // call this function again to display this child's children 
        display_children($row['title'], $level+1); 
    } 
} 

// to display whole tree,call
display_children('',0);

//NOTE: -------------------------------------------------------------   MPTT : Display the tree i.e. QUERY

function display_tree($root) {  
    // retrieve the left and right value of the $root node  
    $result = mysql_query('SELECT lft, rgt FROM tree WHERE title="'.$root.'";');  
    $row = mysql_fetch_array($result);  

    // start with an empty $right stack  
    $right = array();  
    // now, retrieve all descendants of the $root node  
    $result = mysql_query('SELECT title, lft, rgt FROM tree WHERE lft BETWEEN '.$row['lft'].' AND '.$row['rgt'].' ORDER BY lft ASC;');  
    // display each row  
    while ($row = mysql_fetch_array($result)) {  
        // only check stack if there is one  
        if (count($right)>0) {  
            // check if we should remove a node from the stack  
            while ($right[count($right)-1]<$row['rgt']) {  
                array_pop($right);  
            }  
        }  
        echo str_repeat('  ',count($right)).$row['title']."n";  
        $right[] = $row['rgt'];  
    }  
}  
//NOTE: -------------------------------------------------------------   Adj List to MPTT :: Making the tree actually

function rebuild_tree($parent, $left) {   
    // the right value of this node is the left value + 1   
    $right = $left+1;   
    // get all children of this node   
    $result = mysql_query('SELECT title FROM tree WHERE parent="'.$parent.'";');   
    while ($row = mysql_fetch_array($result)) {   
        // recursive execution of this function for each   
        // child of this node   
        // $right is the current right value, which is   
        // incremented by the rebuild_tree function   
        $right = rebuild_tree($row['title'], $right);   
    }   
    // we've got the left value, and now that we've processed   
    // the children of this node we also know the right value   
    mysql_query('UPDATE tree SET lft='.$left.', rgt='.$right.' WHERE title="'.$parent.'";');   
    // return the right value of this node + 1   
    return $right+1;   
} 
