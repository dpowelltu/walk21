from neo4j import GraphDatabase
import logging
from neo4j.exceptions import ServiceUnavailable
import csv




if __name__ == "__main__":
   


    journey_id = 0
    journey_start=""
    journey_end = "" 
    last_id = ""
    start_node = ""
    node_list =[]
    
    file = open("sample_journey2.csv")
    csvreader = csv.reader(file)
    header = next(csvreader)
    
    for row in csvreader:
        if row[1] != last_id:
            #print("new", len(node_list))
            
            if len(node_list)!=0:
                #print("node list", node_list)
                #create a journy node now
                #print("journey ", node_list[0][2], "->", node_list[len(node_list)-1][2], " time:",  node_list[0][3], "->", node_list[len(node_list)-1][3])
                #create the journey!

                #journey has a journey node and X event nodes, along with STARTS, ENDS

                #convert the journey points into a list of events
                for i in range(len(node_list)):
                    print("CREATE (event",i,":EVENT {loc_code:'",node_list[i][2] ,"', time:'",node_list[i][3] , "', ts:apoc.date.parse('",node_list[i][3] ,"','ms','dd/MM/yyyy hh:mm')})", sep='')

                    #ts=node_list[i][3].replace(" ", "T")
                    
                    #print("CREATE (event",i,":EVENT {loc_code:'",node_list[i][2] ,"', time:datetime('",ts ,"')})", sep='')
                
                    
                print("CREATE (journey:Journey {journey_id:",node_list[0][1] ,"})", sep='')

                print("CREATE (journey)-[:STARTS]->(event0)", sep='')
                print("CREATE (journey)-[:ENDS]->(event", len(node_list)-1,")", sep='')

                for i in range(len(node_list)-1):
                    print("CREATE (event",i,")-[:NEXT]->(event",i+1,")", sep='')
                    
                print(";")
                #extract the events now:- and link them to each other and the journey! 

                #for 
                
                node_list=[]

            node_list.append(row)
            
            #add first person
            #app.AddPerson(row[0])
            #add in first event node 
            #app.AddNode(row[1])
            #connect first event to the person
            #app.AddJourney(row[0],row[1])
            
            last_id = row[1]
            start_node = row[2]
        else:
            #this is part of a journey
            node_list.append(row)
            #print(start_node, "->", row[1])
            #add new node_to the graph
            #app.AddNode(row[1])
            #app.AddJourney(start_node,row[1])
            #join this new node to the last node!
            
            start_node = row[2]
            
        #print(row)



