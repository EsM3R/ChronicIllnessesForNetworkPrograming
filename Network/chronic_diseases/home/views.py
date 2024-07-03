from django.shortcuts import render ,HttpResponse
from .neo4jdb import Neo4jConnection

def form_view(request):
    if request.method == 'POST':
        female = 0 
        male = 0
        treatment_labels = []
        treatment_data = []
        weather_labels = []
        weather_data = []
        tag_labels = []
        tag_data = []
        condition_labels = []
        condition_data = []
        trackable_name = request.POST.get('trackable_name')
        neo4j_conn = Neo4jConnection('bolt://localhost:7687', 'neo4j', 'Mehmet1173.')
        results = neo4j_conn.get_trackable_stats(trackable_name)
        treatments = neo4j_conn.get_treatments(trackable_name)
        weathers =  neo4j_conn.get_weather(trackable_name)
        tags = neo4j_conn.get_tag(trackable_name)
        conditions = neo4j_conn.get_condition(trackable_name)

    
        for index, treatment in enumerate(treatments):
            if index < 10: 
                treatment_labels.append(treatment[0])
                treatment_data.append(treatment[1])
            else:
                break 
                    
        for index, weather in enumerate(weathers) :
            if index < 10: 
                 weather_labels.append(weather[0])
                 weather_data.append(weather[1])
            else:
                break 
           
        
        for index , tag in enumerate(tags) :
            if index < 10: 
                tag_labels.append(tag[0])
                tag_data.append(tag[1])
            else:
                break 
            
            
        
        for index , condition in enumerate(conditions) :
            if index < 10: 
                condition_labels.append(condition[0])
                condition_data.append(condition[1])
            else:
                break 
           
        
        neo4j_conn.close()
       
       
        if results != []:
            female = results[0][1]
            male = results[1][1]
            
        context = {
            "female": female,  
            "male": male,    
            "trackable_name": trackable_name,
            "treatment_labels" : treatment_labels,
            "treatment_data" : treatment_data,
            "weather_labels" : weather_labels,
            "weather_data" : weather_data,
            "tag_labels" : tag_labels,
            "tag_data" : tag_data,
            "condition_labels" : condition_labels,
            "condition_data" : condition_data,
            
        }
        return render(request, 'home.html', context)
    else:
        return render(request, 'home.html')