#!/usr/bin/env python
# coding: utf-8

# # NDEx2 Client Objects

# #### Modules Required for NDEx2 Client Tutorial

# In[ ]:


import ndex2.client as nc
import io
import json
from IPython.display import HTML

#create a NDEx client object to access my accouont on the NDEx server
my_account="PUT YOUR USER HERE"
my_password="PUT YOUR PASSWORD HERE"

my_ndex=nc.Ndex2("http://public.ndexbio.org", my_account, my_password)
my_ndex.update_status()


# #### update_status()

# In[ ]:


try:
    my_ndex=nc.Ndex2("http://public.ndexbio.org", my_account, my_password)
    my_ndex.update_status()
    networks = my_ndex.status.get("networkCount")
    users = my_ndex.status.get("userCount")
    groups = my_ndex.status.get("groupCount")
    print("my_ndex client: %s networks, %s users, %s groups" % (networks, users, groups))
except Exception as inst:
    print("Could not access account %s with password %s" % (my_account, my_password))
    print(inst.args)


# #### get_user_by_username(username)

# In[ ]:


my_ndex.get_user_by_username("ENTER YOUR USER")


# #### save_new_network(cx)

# In[ ]:


query_result_cx=my_ndex.get_neighborhood('c9243cce-2d32-11e8-b939-0ac135e8bacf','XRN1')

uri_subset = my_ndex.save_new_network(query_result_cx)
uuid_subset = uri_subset.rpartition('/')[-1]
print ("URI of the subset is: ", uri_subset)
print ("UUID of the subset is: ", uuid_subset)

new_summary = my_ndex.get_network_summary(uuid_subset)
 
if new_summary.get("isValid"):
        print("New network has been validated by the server.\n")
else:
    print("failed\n")
    print (new_summary)


# #### save_cx_stream_as_new_network(cx_stream)

# In[ ]:


#I tried the code below, but got an error message:'list' object has no attribute 'encode'

#query_response = my_ndex.get_neighborhood_as_cx_stream('c9243cce-2d32-11e8-b939-0ac135e8bacf','XRN1')
#raw_cx = query_response.json()
#my_ndex.save_cx_stream_as_new_network(raw_cx)


# #### update_cx_network(cx_stream, network_id)

# In[ ]:


#did not try this method since don't understand well


# #### delete_network(network_id)

# In[ ]:


query_result_cx=my_ndex.get_neighborhood('c9243cce-2d32-11e8-b939-0ac135e8bacf','XRN1')

uri_subset = my_ndex.save_new_network(query_result_cx)
uuid_subset = uri_subset.rpartition('/')[-1]

list_uuid = my_ndex.get_network_ids_for_user("ENTER YOUR USER")

indexval = 0
for i in range(len(list_uuid)):
    if (list_uuid[indexval] != uuid_subset):
        my_ndex.delete_network(list_uuid[indexval])        
    else:
        print("URI of the newly created network %s is %s" % (uuid_subset, uri_subset))
    indexval += 1


# #### get_network_summary(network_id)

# In[ ]:


ns=my_ndex.get_network_summary('c9243cce-2d32-11e8-b939-0ac135e8bacf')
def summary2table(object):
    table = "<table>"
    for key, value in object.items():
        if key == "warnings":
            warning_list = ""
            for warning in value:
                warning_list += "%s<br>" % warning
            value = warning_list
        if key == "properties":
            property_table = "<table>"
            for property in value:
                property_table += "<tr>"
                property_table += "<td>%s</td><td>%s</td>" % (property.get("predicateString"), property.get("value"))
                property_table += "</tr>"
            property_table += "</table>"
            value = property_table
        table += "<tr>"
        table += "<td>%s</td><td>%s</td>" % (key, value)
        table += "</tr>"
    table += "</table>"
    return table

HTML(summary2table(ns))


# #### get_network_as_cx_stream(network_id)

# In[ ]:


response = my_ndex.get_network_as_cx_stream('c9243cce-2d32-11e8-b939-0ac135e8bacf')
raw_cx = cx_stream.json()


#the code below copied for the v2.0 Tutorial. I don't understand well
print("Received %s characters of CX" % len(response.content))
def getNumberOfNodesAndEdgesFromCX(cx):
    numberOfEdges = numberOfNodes = 0;
    for aspect in cx:
        #print('key')
        if 'nodes' in aspect:
            numberOfNodes = len(aspect['nodes'])
        if 'metaData' in aspect:
            metaData = aspect['metaData']
            for element in metaData:
                if (('name' in element) and (element['name'] == 'nodes')):
                    numberOfNodes = element.get('elementCount')
                if (('name' in element) and (element['name'] == 'edges')):
                    numberOfEdges = element.get('elementCount')
            break
    return numberOfNodes, numberOfEdges

nodes, edges = getNumberOfNodesAndEdgesFromCX(raw_cx)
print("network contains %s nodes and %s edges." % (nodes, edges))


# #### set_network_system_properties(network_id, network_system_properties)

# In[ ]:


#did not try this method since don't understand well


# #### make_network_private(network_id)

# In[ ]:


my_ndex.make_network_private("ENTER YOUR NETWORK ID")


# #### make_network_public(network_id)

# In[ ]:


my_ndex.make_network_public("ENTER YOUR NETWORK ID")


# #### set_read_only(network_id, value)

# In[ ]:


#revert network to read-write 
my_ndex.set_read_only("ENTER YOUR NETWORK ID", False)
new_summary = my_ndex.get_network_summary("ENTER YOUR NETWORK ID")
print("The read only status has been reverted to %s" % new_summary.get('isReadOnly'))


# ##### update_network_group_permission(group_id, network_id, permission)

# ##### grant_networks_to_group(group_id, network_ids, permission=”READ”)

# ##### update_network_user_permission(user_id, network_id, permission)

# ##### grant_network_to_user_by_username(username, network_id, permission)

# ##### grant_networks_to_user(user_id, network_ids, permission=”READ”)

# #### update_network_profile(network_id, network_profile)

# In[ ]:


network_profile={"name":"My Network", "description":"learn from Tutorial", "version":"1.0"}
my_ndex.update_network_profile("ENTER YOUR NETWORK ID", network_profile)    


# ##### set_network_properties(network_id, network_properties)

# ##### get_provenance(network_id)

# In[ ]:


my_ndex.get_provenance('c9243cce-2d32-11e8-b939-0ac135e8bacf')


# ##### set_provenance(network_id, provenance)

# #### search_networks(search_string=”“, account_name=None, start=0, size=100, include_groups=False)

# In[ ]:


list_tutorial_networks=my_ndex.search_networks('tutorial')
print("%s netwoks found." % (len(list_tutorial_networks)))
print ("\nNetwork names and uuids:\n")
for i in list_tutorial_networks.get('networks'): 
    print( "%s -->> %s" % (i.get('name'), i.get('externalId')))


# #### find_networks(search_string=”“, account_name=None, start=0, size=100)

# In[ ]:


#This method is deprecated; search_networks should be used instead.


# ##### get_network_summaries_for_user(account_name)

# In[ ]:


my_ndex.get_network_summaries_for_user("ENTER YOUR USER")


# #### get_network_ids_for_user(account_name)

# In[ ]:


list_uuid = my_ndex.get_network_ids_for_user("ENTER YOUR USER")
print (list_uuid)


# #### get_neighborhood_as_cx_stream(network_id, search_string, search_depth=1, edge_limit=2500)

# In[ ]:


query_result_cx_stream = my_ndex.get_neighborhood_as_cx_stream('c9243cce-2d32-11e8-b939-0ac135e8bacf','XRN1')
raw_cx = query_result_cx_stream.json()


# #### get_neighborhood(network_id, search_string, search_depth=1, edge_limit=2500)

# In[ ]:


query_result_cx=my_ndex.get_neighborhood('c9243cce-2d32-11e8-b939-0ac135e8bacf','XRN1')
                                       
for aspect in query_result_cx:
    if 'nodes' in aspect:
        number_of_nodes = len(aspect['nodes'])
    if 'edges' in aspect:
        number_of_edges = len(aspect['edges'])

print("Query result network contains %s nodes and %s edges." % (number_of_nodes, number_of_edges))


# ##### get_task_by_id(task_id)

# # NiceCX Objects

# #### Modules Required for NiceCX Tutorial

# In[102]:


from ndex2.nice_cx_network import NiceCXNetwork
import ndex2.client as nc
import ndex2
import networkx as nx
import pandas as pd
import os


# #### *ndex2.create_nice_cx_from_raw_cx(cx)

# In[ ]:


#this method requests to create a NDEx2 Client object
#import ndex2.client as nc
#import json
#my_account="PUT YOUR USER HERE"
#my_password="PUT YOUR PASSWORD HERE"
#my_ndex=nc.Ndex2("http://public.ndexbio.org", my_account, my_password)
#my_ndex.update_status()
#query_result_cx_stream = my_ndex.get_neighborhood_as_cx_stream('c9243cce-2d32-11e8-b939-0ac135e8bacf','XRN1')
#raw_cx = query_result_cx_stream.json()

NiceCX_from_stream = ndex2.create_nice_cx_from_raw_cx(raw_cx)
NiceCX_from_stream.print_summary()


# #### *ndex2.create_nice_cx_from_file(path)

# In[ ]:


nice_cx_from_cx_file = ndex2.create_nice_cx_from_file('SimpleNetwork.cx')


# #### *ndex2.create_nice_cx_from_networkx(networkx)

# In[ ]:


#create an Empty NetworkX
G = nx.Graph()
nice_cx_from_networkx = ndex2.create_nice_cx_from_networkx(G)


# #### *ndex2.create_nice_cx_from_pandas(dataframe)

# In[ ]:


#create an Empty Pandas Dataframe
df = pd.DataFrame()
nice_cx_from_pandas = ndex2.create_nice_cx_from_pandas(df)


# #### *ndex2.create_nice_cx_from_server(server, username=None, password=None, uuid=None)

# In[ ]:


uuid = "1c69beff-1229-11e6-a039-06603eb7f303"
nice_cx_from_server = ndex2.create_nice_cx_from_server(server='http://public.ndexbio.org', uuid=uuid)
nice_cx_from_server.print_summary()


# #### create_node(name, represents=None)

# In[ ]:


#Starting with an Empty Network
NiceCX_creatures = NiceCXNetwork()
node_id_list = []

#create_node() method returns the new node id. IDs are always assigned in an ascending order.
#add 10 nodes to the network
for i in range(10):
    node_name = "new node" + str(i)
    node_id = NiceCX_creatures.create_node(node_name) 
    node_id_list.append(node_id)
print (node_id_list)


# #### add_node(node)

# In[ ]:


#This method has been deprecated. Please use create_node()


# #### set_node_attribute(node, attribute_name, values, type=None, subnetwork=None)

# In[ ]:


NiceCX_creatures = NiceCXNetwork()
node_id = NiceCX_creatures.create_node("new node")
NiceCX_creatures.set_node_attribute(node_id, "new attribute", "new attribute value is xxxx") 


# #### *add_node_attribute(node,  attribute_name, values)

# In[ ]:


NiceCX_creatures = NiceCXNetwork()
node_id = NiceCX_creatures.create_node("new node")
NiceCX_creatures.add_node_attribute(node_id, "new attribute", "new attribute value is xxxx") 


# #### get_node_attribute(node, attribute_name, subnetwork=None)

# In[ ]:


NiceCX_creatures = NiceCXNetwork()
node_id = NiceCX_creatures.create_node("new node")
NiceCX_creatures.set_node_attribute(node_id, "new attribute", "new attribute value is nnnn") 
NiceCX_creatures.get_node_attribute(node_id, "new attribute")


# ##### get_node_attribute_objects(node, attribute_name)

# In[ ]:


#get_node_attribute_objects() is deprecated.  Please use get_node_attribute() instead


# #### get_node_attributes(node)

# In[ ]:


NiceCX_creatures = NiceCXNetwork()

#create one node
node_id = NiceCX_creatures.create_node("new node") 

#add 10 attributes with value for this new node
for i in range(10):
    attr_name = "new attribute " + str(i)
    attr_value = "new attribute value is  " + str(i)
    NiceCX_creatures.set_node_attribute(node_id, attr_name, attr_value)   

NiceCX_creatures.get_node_attributes(node_id)


# #### get_nodes()

# In[ ]:


NiceCX_creatures = NiceCXNetwork()

#add 10 nodes to the network, each node has 5 attribute with value
for i in range(10):
    node_name = "node " + str(i)
    node_id = NiceCX_creatures.create_node(node_name) 
    
    for j in range(5):
        attr_name = "attribute " + str(i) + str(j)
        attr_value = "attribute value is  " + str(i) + str(j)
        NiceCX_creatures.set_node_attribute(node_id, attr_name, attr_value)   
        print("\n",NiceCX_creatures.get_node_attribute(node_id, attr_name))
        
NiceCX_creatures.get_nodes()


# #### *get_node(node)

# In[ ]:


NiceCX_creatures = NiceCXNetwork()
node_id = NiceCX_creatures.create_node("new node")
NiceCX_creatures.set_node_attribute(node_id, "new attribute", "new attribute value is nnnn") 
NiceCX_creatures.get_node(node_id)


# #### create_edge(source, target, interaction)

# In[ ]:


NiceCX_creatures = NiceCXNetwork()

#create_edge() method returns the new edge id. IDs are always assigned in an ascending order.
print(NiceCX_creatures.create_edge("A", "B"))
print(NiceCX_creatures.create_edge("C", "D"))
print(NiceCX_creatures.create_edge("B", "C"))


# #### add_edge(edge)

# In[ ]:


#This method has been deprecated. Please use create_edge()


# #### set_edge_attribute(edge, attribute_name, values, type=None, subnetwork=None)

# In[ ]:


NiceCX_creatures = NiceCXNetwork()
edge_id = NiceCX_creatures.create_edge("A", "B")
NiceCX_creatures.set_edge_attribute(edge_id, "new edge attribute", "edge attribute value is nnnnn" )


# #### get_edge_attribute(edge, attribute_name, subnetwork=None)

# In[ ]:


NiceCX_creatures = NiceCXNetwork()
edge_id = NiceCX_creatures.create_edge("A", "B")
NiceCX_creatures.set_edge_attribute(edge_id, "new edge attribute", "new edge attribute value is nnnnn" )
NiceCX_creatures.get_edge_attribute(edge_id, "new edge attribute")


# #### get_edge_attribute_objects(edge, attribute_name)

# In[ ]:


#This method has been deprecated. Please use get_edge_attributes()


# #### get_edge_attributes(edge)

# In[ ]:


NiceCX_creatures = NiceCXNetwork()
edge_id = NiceCX_creatures.create_edge("A", "B")

# add 5 attributes to the edge
for i in range(5):
    attr_name = "name " + str(i)
    attr_value = "value is " + str(i)
    NiceCX_creatures.set_edge_attribute(edge_id, attr_name, attr_value )
    #print(NiceCX_creatures.get_edge_attribute(edge_id, attr_name))
NiceCX_creatures.get_edge_attributes(edge_id)


# #### get_edges()

# In[ ]:


NiceCX_creatures = NiceCXNetwork()

#add 3 edges to the network
edge_1 = NiceCX_creatures.create_edge("A", "B")
edge_2 = NiceCX_creatures.create_edge("C", "D")
edge_3 = NiceCX_creatures.create_edge("B", "C")

NiceCX_creatures.get_edges()


# ##### get_name()

# #### set_name(network name)

# In[ ]:


#create/initial an empty niceCX network before setting the network name
NiceCX_creatures = NiceCXNetwork()
NiceCX_creatures.set_name("new web")


# ##### getSummary()

# ##### set_network_attribute(name=None, values=None, type=None, subnetwork_id=None)

# ##### get_network_attribute(attribute_name, subnetwork_id=None)

# ##### get_network_attribute_objects(attribute_name)

# ##### get_network_attributes()

# ##### get_metadata()

# ##### set_metadata()

# ##### getProvenance()

# ##### set_provenance(provenance)

# ##### get_context(context)

# ##### set_context()

# ##### set_context()

# ##### set_context()

# ##### get_opaque_aspect(aspect_name)

# ##### set_opaque_aspect(aspect_name, aspect_elements)

# ##### set_opaque_aspect(aspect_name, aspect_elements)

# ##### get_opaque_aspect_names()

# ##### to_cx()

# ##### to_cx_stream()

# #### to_networkx()

# In[ ]:


NiceCX_creatures = NiceCXNetwork()
networkx_network = NiceCX_creatures.to_networkx()


# #### to_pandas_dataframe()

# In[ ]:


NiceCX_creatures = NiceCXNetwork()
pandas_network = NiceCX_creatures.to_pandas_dataframe()


# #### upload(ndex_server, username, password, update_uuid=None)

# In[ ]:


upload_message = NiceCX_creatures.upload_to("http://public.ndexbio.org", "ENTER YOUR USER", "ENTER YOUR PASSWORD")
uuid = upload_message.rpartition('/')[-1]


# ##### apply_template(server, username, password, uuid)

# ##### addNode(json_obj=None)

# ##### add_edge_element(json_obj=None, edge)

# ##### addNetworkAttribute(json_obj=None)
