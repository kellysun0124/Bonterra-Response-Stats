#The report should be formatted as a delimited file returned by your program. 

import requests

#NGPvan api /broadcastEmails
url = "https://api.myngp.com/v2/broadcastEmails"

headers = {
    "accept": "application/json",
    "authorization": "Basic YXBpdXNlcjowNDQ3NzBBQS1GRkM5LTQ2RDItQUY1Ni05NkJFREE5OTQ5Njk="
}

response = requests.get(url, headers=headers)
response_list = response.json()["items"]


"""
It should include all emails sent, in reverse order of sending based on EmailMessageId. 
"""
def ID_num(item):
    return item["emailMessageId"]
#reverse order
response_list.sort(key = ID_num, reverse = True)


"""
get top variant
"""
def top_variant(ID, variant_list):
    top_opens = 0
    top_name = ""
    for var_ID in variant_list:
        variant_url = url + "/" + str(ID) + "/variants/" + str(var_ID) + "?$expand=statistics"

        response = requests.get(variant_url, headers=headers).json()
        
        #get percentage
        percent_opens = response['statistics']['opens'] / response['statistics']['recipients']
        #get top percentage and variant
        if percent_opens >= top_opens:
            top_name = response['name']
            
    return top_name
        
        
"""
For each email, you should display the EmailMessageID and name of the email, plus all available top-line stats (Recipients, Opens, Clicks, Unsubscribes, Bounces). 
get stat
"""
def email_stats(ID_num):

    email_url = url + "/" + str(ID_num) + "?$expand=statistics"
    
    response = requests.get(email_url, headers=headers).json()

    # Finally, you should include the name of the variant associated with that email that has the highest percentage-based performance on Opens.
    
    stats_dict = response["statistics"]
    variants = [ variant['emailMessageVariantId'] for variant in response["variants"] ]
    stats_dict["Top Variant"] = top_variant(ID_num, variants)

    return stats_dict


#print to response_stats.csv file
response_csv = open("response_stats.csv", "w")   
response_csv.write("Email Message ID, Email Name, Recipients, Opens, Clicks, Unsubscribes, Bounces, Top Variant")
for email in response_list:
    to_print = '\n' + str(email['emailMessageId']) + ", " + email['name'] + ', '
    to_print += ', '.join( str(stat) for stat in email_stats(email['emailMessageId']).values() )
    response_csv.write(to_print)
    
#print to terminal
print("Email report complete, file is response_stats.csv")