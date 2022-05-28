import hou 


perfix_name = "OUT_"
obj_merge_perfix_name = "read_"
null_color = (0.02, 0.02, 0.02)

NULL_TYPE = "null"
MERGE_Type = "merge"
OBJ_MERGE_TYPE = "object_merge"


def get_cursor_pos():
    #pane = hou.ui.paneTabUnderCursor()
    #pos = pane.cursorPosition()
    return hou.ui.paneTabUnderCursor().cursorPosition() 

def get_current_node():
    # to get the context node 
        
    network_editor = hou.ui.paneTabUnderCursor()
    network_path = network_editor.pwd()
    display_node= hou.node(network_path.displayNode().path())
    
    return display_node.parent()


def create_node(parent, type, name , clr = (0.75,0.75,0.75)):
    node = parent.createNode(type, name)
    
    node.setDisplayFlag(True)
    node.setRenderFlag(True)
    
    # set color to null node
    color = hou.Color(clr)
    node.setColor(color)
    
    return node


def create_objmerge(): 
    # create null or null & merge for the selected nodes 
    # get selected node
    pos = get_cursor_pos()
    

    selected_nodes = hou.selectedNodes()
    if selected_nodes == ():
        #create empty objmerge in cursor pos
        parent_node = get_current_node()
        obj_merge_node = create_node(parent_node,"object_merge","read_")
        obj_merge_node.setPosition(pos)
        
    elif len(selected_nodes) == 1 : 
        #create null & connect it to selected 
        selected_node_name = selected_nodes[0].name()
        parent_node = selected_nodes[0].parent()
        null_node = create_node(parent_node,"null" , perfix_name+selected_node_name ,null_color )
        null_node.setInput(0, selected_nodes[0])
        null_node.moveToGoodPosition()
        
        #create obj merge in cursor pos and set path parameter to created null 
        parent_node = get_current_node()
        obj_merge_node = create_node(parent_node,"object_merge","read_"+selected_node_name)
        obj_merge_node.setPosition(pos)
        obj_merge_node.parm("objpath1").set(null_node.path())
        
    elif len(selected_nodes) >= 1 : 
        #create merge node
        parent_node = selected_nodes[0].parent()
        merge_node =  create_node(parent_node,"merge" , "merge")
        #set it input to all nodes 
        for num , selected_node in enumerate(selected_nodes): 
            merge_node.setInput(num , selected_node)
        merge_node.moveToGoodPosition()
        #create null 
        null_node = create_node(parent_node,"null" , perfix_name+"merge" ,null_color )
        null_node.setFirstInput(merge_node)
        null_node.moveToGoodPosition()
        #create obj merge in cursor pos and set path parameter to created null
        parent_node = get_current_node()
        obj_merge_node = create_node(parent_node,"object_merge","read_"+"merge")
        obj_merge_node.setPosition(pos)
        obj_merge_node.parm("objpath1").set(null_node.path())

    print("done")
    
create_objmerge()