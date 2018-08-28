import pickle
import networkx as nx
import pandas as pd
import difflib
class transportweb:

    def __init__( self):
        self.src_prompt = 'Please Enter The Source Of Journey: '
        self.dest_prompt = 'Please Enter The Destination Of Journey: '
        self.priority_prompt = 'Please Choose from : c(cost) or t(time) as preference: '
        
        self.default_priority = 'cost_time'
        self.chosen_priority = self.default_priority
        
        try :
            self.graph = pickle.load(open('final_combined_graph','rb'))
        except Exception as e:
            print(e)
        try :
            self.available_stations = sorted(pd.read_csv('all_station_names_improved.csv')['station_name'])                    
        except Exception as e:
            print(e)
            
    def check_in_available(self, station ):
        available_stations = self.available_stations
        if station in available_stations :
            return True,station
        else :
            possible = difflib.get_close_matches( station, available_stations)
            if len( possible) > 0:
                return False, possible[0: max( 1, len(possible))]
            else :
                return False, 0
            
    def check_priority(self, priority):
        if priority.lower() not in ['c','t']:
            return False, 'invalid option'
        else :
            return True, 0
    
    def begin(self):
        src = input(self.src_prompt).lower()
        is_valid, station_list = self.check_in_available(src)
        while not is_valid:
            if station_list != 0:
                print()
                print('No entry found for {} !'.format(src))
                print('Nearest matches to input are:')
                for i in station_list:
                    print(i)
            else :
                print()
                print('No entry found for {} !'.format(src))
            src = input(self.src_prompt).lower()
            is_valid, station_list = self.check_in_available(src)

        dest = input(self.dest_prompt).lower()
        is_valid, station_list = self.check_in_available(dest)
        while not is_valid:
            choice = 'n'
            if station_list != 0:
                print()
                print('No entry found for {} !'.format(dest))
                print('Nearest matches to input are:')
                for i in station_list:
                    print(i)
            else :
                print()
                print('No entry found for {} !'.format(dest))
            dest = input(self.dest_prompt).lower()
            is_valid, station_list = self.check_in_available(dest)
            
        priority = 't'                 ##comment this line and uncomment block below to get priority by cost.. disabled it as metro cost wasnt available
        is_priority_valid = True
		##uncomment from here
#         priority = input( self.priority_prompt).lower()
#         is_priority_valid, result = self.check_priority(priority)
#         while not is_priority_valid:
#             if result != 0:
#                 print()
#                 print(result)
#             priority = input(self.priority_prompt).lower()
#             is_priority_valid, station_list = self.check_priority(priority)

        ##uncomment till here

        if is_priority_valid:
            if priority == 't':
                self.chosen_priority = 'cost_time'
            else :
                self.chosen_priority = 'cost_amount'
        
        print()
        graph = self.graph
        
        if src == dest:
            print('source and destination must be different!')
        else :
            paths = nx.dijkstra_path( graph, src, dest, self.chosen_priority)
            total_time = 0
            total_fare = 0
            for index, place in enumerate( paths):
                try :
                    data = graph.get_edge_data( place, paths[index+1])
                    if len(data.keys()) > 1:
                        #checking only time since cost data for metro wasn't provided
                        #can add the cost_amount weight to graph once its provided
                        t_min = min(data[0]['cost_time'], data[1]['cost_time'])
                        if t_min == data[0]['cost_time']:
                            data = data[0]
                        else :
                            data = data[1]
                    else :
                        data = data[0]
                    total_time += data['cost_time']
                    mode = data['mode']

                    print('{}- <from: {} to: {} > <mode: {}> '.format(index+1,place, paths[index+1], data['mode']))
                    total_fare += data['cost_amount']

                except Exception as e:
                    pass
            print()
            print('from: {} to: {}'.format( src, dest))
            if mode != 'metro':
                print('priority: {} \ntotal time (minutes): {} '.format('Time' if priority == 't' else 'Cost', total_time//60))
            else :
                print('priority: {} \ntotal time (minutes): {}'.format('Time' if priority == 't' else 'Cost', total_time//60))
            print('please note that cost info for metro was not not available but can be added if data is provided.')
        
c = transportweb()
c.begin()
