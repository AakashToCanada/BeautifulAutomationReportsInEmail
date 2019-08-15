
# coding: utf-8

# In[19]:



# coding: utf-8

# In[33]:



# coding: utf-8

# In[1]:


import json
import matplotlib.pyplot as plt
import smtplib
from optparse import OptionParser
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication
from decimal import Decimal
import os as os
from os import listdir
from os.path import isfile, join
import sys


#argument 1 will be location of files
print ("argument: ", sys.argv[1])
mypath=sys.argv[1]

#argument 2 for products
data1=sys.argv[2]
if data1 != 'na' and data1 != 'NA' and data1 != 'Na':
    data1=data1.replace("'","")
    data1=data1.replace('{','')
    data1=data1.replace('}','')
    count=data1.count(',')
    ##print(count+1)
    dict1={}
    i=0
    list1=[]
    while i<=count:
        list1=data1.split(',')
        j=0
        while j < len(list1):
            dict1[list1[j].split(':')[0]] = list1[j].split(':')[1]
            j=j+1
        i=i+1


#dict1={'CRM': '@CRMALL', 'Customer Service': '@CS-Regression', 'Sales Automation': '@SA-REGRESSION'}
###print(dict1)

#Argument 3 for Owners
data2=sys.argv[3]
if sys.argv[3] != 'na' and sys.argv[3] != 'NA' and sys.argv[3] != 'Na':
    data2=data2.replace("'","")
    count=data2.count(',')
    f=0
    owners=[]
    while f<=count:
        owners=data2.split(',')
        f+=1


totalJsonFiles = 0
json_filenames = []
receipients = []
total_jobs_run=[]
def loadJsonFile(fileName):
    with open(fileName, 'r') as F:
        dict = json.load(F)
        total_jobs_run.append(dict)
        path, file = os.path.split(fileName)
        file = file.split('.')[0]
        json_filenames.append(file)
        F.close()
    return;


#mypath='C:\\Users\\shara6\\Desktop\\SendEmailArtifacts\\cucumber-tests-json-results'

onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]


totalJsonFiles = len(onlyfiles)
i=0
while i<totalJsonFiles:
    onlyfiles[i] = mypath + "/" + onlyfiles[i]
    loadJsonFile(onlyfiles[i])
    i=i+1
    
    

# Create the body of the message.
html1 = ""
     
html2 = """</br></br></br></br></br></br></br></br></br></br><table border = "1"><tr bgcolor = '#728CA3'><th>Feature Name</th>
                         <th>Scenario Name</th>
                         <th>Total Test-cases</th>
                         <th>Test-cases Passed</th>
                         <th>Test-cases Failed</th>
                         <th>Test-cases Skipped</th>                      
                         <th>Scenario Status</th></tr>      
    """



job=0

#for test cases graph
totalPassed=0 
totalFailed=0
totalSkipped=0

#for scenarios graph
scenariosPassed=0
scenariosFailed=0
scenariosSkipped=0

#extra
scenario_result = []
# scenario_owner = {"Amit Chaturvedi":0,"Zenith":0,"Mirage":0,"X-Force":0,"SPARK":0,"Raghavendra Koundinya":0,"Amit Patel":0,"No OWNER":0}
# scenario_owner_pass = {"Amit Chaturvedi":0,"Zenith":0,"Mirage":0,"X-Force":0,"SPARK":0,"Raghavendra Koundinya":0,"Amit Patel":0,"No OWNER":0}
# scenario_owner_fail = {"Amit Chaturvedi":0,"Zenith":0,"Mirage":0,"X-Force":0,"SPARK":0,"Raghavendra Koundinya":0,"Amit Patel":0, "No OWNER":0}
scenario_owner={}
scenario_owner_pass={}
scenario_owner_fail={}

if sys.argv[3] != 'na' and sys.argv[3] != 'NA' and sys.argv[3] != 'Na':
    for i in range(0,len(owners)):
        scenario_owner[owners[i]] = 0
        scenario_owner_pass[owners[i]] = 0
        scenario_owner_fail[owners[i]] = 0
    ##print(scenario_owner)

scenario_owner["No OWNER"]=0
scenario_owner_pass["No OWNER"]=0
scenario_owner_fail["No OWNER"]=0


#tag_fail = {"CRM":0,"Customer Service":0,"Sales Automation":0,"None":0}
#tag_pass = {"CRM":0, "Customer Service":0,"Sales Automation":0,"None":0}
#tag = {"CRM":0, "Customer Service":0,"Sales Automation":0,"None":0}
tag_fail={}
tag_pass={}
tag={}


tag_details=[]
if sys.argv[2] != 'na' and sys.argv[2] != 'NA' and sys.argv[2] != 'Na':
    tag_details=list(dict1.values())
    ##print("tag_details: ", tag_details)
    for key, value in dict1.items():
        tag_fail[key]=0
        tag_pass[key]=0
        tag[key]=0
    
##print(tag_details)    
tag_fail["none"]=0
tag_pass["none"]=0
tag["none"]=0

scenario_passed_testcases = []
scenario_failed_testcases = []
scenario_skipped_testcases = []

#total features and scenarios
while job<len(total_jobs_run):
    #for creating a dictionary with feature against their scenarios
    cucumber_report_dict = total_jobs_run[job]
    
    i=0
    
    
    
    
    while i<len(cucumber_report_dict):
        try:
            feature_name = cucumber_report_dict[i]['name']
        except KeyError as e:
            #print("There is no feature name available")
            feature_name="not available"
        
        try:
            tags_in_feature = len(cucumber_report_dict[i]['tags'])
        except KeyError as e:
            #print("There is no tag in feature")
            tags_in_feature=0
        
        
        
        rowSpan = 0
        a=0
        scenarios_in_feature = len(cucumber_report_dict[i]['elements'])
        scenarios_for_tag = scenarios_in_feature
        while a < scenarios_in_feature:
            tags_in_scenario = 0
            if cucumber_report_dict[i]['elements'][a]['type'] !="background":
                rowSpan = rowSpan +1
                tags_in_scenario = len(cucumber_report_dict[i]['elements'][a]['tags'])
            a = a+1
        backgorun_in_Feature = len(cucumber_report_dict[i]['elements'])
        
        
        html2 +="<tr><td rowspan='{}' bgcolor='#87CEFA'>{}</td>".format(rowSpan, feature_name)
        
        j=0
        steps_in_background=0
        
        #Extra
        background_step_result = []
        p_background=0
        s_background=0
        f_background=0
        
        while j<scenarios_in_feature:
            backgroundResult='Passed'
            scenarioResult='Passed'
            
            steps_in_scenario_and_Background=0
            steps_in_scenario=0
            passed_in_scenario=0
            failed_in_scenario=0
            skipped_in_scenario=0
            scenario_step_result = []
            background_and_scenario_step_result = []
            scenario_step_result.clear()
            background_and_scenario_step_result.clear()          
            
            flag_For_Background=0
            flag_for_Scenario=0
            p=0
            s=0
            f=0
            
            if cucumber_report_dict[i]['elements'][j]['keyword'] == "Background":
                scenarios_for_tag -=1
                background_step_result.clear()
                steps_in_background =len(cucumber_report_dict[i]['elements'][j]['steps'])
                k=0
                flag_for_Scenario=0
                while k<steps_in_background:
                    if cucumber_report_dict[i]['elements'][j]['steps'][k]['result']['status'] == 'failed':
                        backgroundResult='Failed'
                        background_step_result.append('failed')
                        failed_in_scenario +=1
                        flag_For_Background=1
                        f_background+=1
                    elif cucumber_report_dict[i]['elements'][j]['steps'][k]['result']['status'] == 'skipped':
                        backgroundResult='Failed'
                        background_step_result.append('skipped')
                        skipped_in_scenario+=1
                        flag_For_Background=1
                        s_background+=1
                    else:
                        background_step_result.append('passed')
                        passed_in_scenario+=1
                        p_background+=1
                    k=k+1
                
                
            else:
                scenario_name = cucumber_report_dict[i]['elements'][j]['name']
                
                steps_in_scenario =len(cucumber_report_dict[i]['elements'][j]['steps'])
                steps_in_scenario_and_Background = steps_in_scenario + steps_in_background
                background_and_scenario_step_result += background_step_result
                
                k=0
                while k<steps_in_scenario:
                    if cucumber_report_dict[i]['elements'][j]['steps'][k]['result']['status'] == 'failed' or cucumber_report_dict[i]['elements'][j]['steps'][k]['result']['status'] == 'undefined':
                        scenarioResult='Failed'
                        scenario_step_result.append('failed')
                        flag_for_Scenario=1
                        f += 1
                    elif cucumber_report_dict[i]['elements'][j]['steps'][k]['result']['status'] == 'skipped':
                        scenarioResult='Failed'
                        scenario_step_result.append('skipped')
                        flag_for_Scenario=1
                        s += 1
                    else:
                        scenario_step_result.append('passed')
                        p += 1
                    
                    k=k+1
                background_and_scenario_step_result += scenario_step_result
            
            p += p_background
            f += f_background
            s += s_background
            if cucumber_report_dict[i]['elements'][j]['keyword'] != "Background":
                if scenarioResult =='Failed' or backgroundResult=='Failed':
                    html2 +="<td bgcolor='#FF0000'>{}</td>".format(scenario_name)
                    html2 +="<td bgcolor='#FF0000'>{}</td>".format(steps_in_scenario_and_Background)
                    html2 +="<td bgcolor='#FF0000'>{}</td>".format(str(background_and_scenario_step_result.count('passed')))
                    html2 +="<td bgcolor='#FF0000'>{}</td>".format(str(background_and_scenario_step_result.count('failed')))
                    html2 +="<td bgcolor='#FF0000'>{}</td>".format(str(background_and_scenario_step_result.count('skipped')))
                    html2 +="<td bgcolor='#FF0000'>{}</td></tr>".format("Failed")
                    
                else:
                    html2 +="<td bgcolor='#32CD32'>{}</td>".format(scenario_name)
                    html2 +="<td bgcolor='#32CD32'>{}</td>".format(steps_in_scenario_and_Background)
                    html2 +="<td bgcolor='#32CD32'>{}</td>".format(str(background_and_scenario_step_result.count('passed')))
                    html2 +="<td bgcolor='#32CD32'>{}</td>".format(str(background_and_scenario_step_result.count('failed')))
                    html2 +="<td bgcolor='#32CD32'>{}</td>".format(str(background_and_scenario_step_result.count('skipped')))
                    html2 +="<td bgcolor='#32CD32'>{}</td></tr>".format("Passed")
                    
                if flag_for_Scenario == 0 and flag_For_Background==0:
                    scenario_result.append('passed')
                    count=0
                    for key, value in scenario_owner.items():
                        if key in feature_name:
                            ##print("pass: ", feature_name, "key looked for: ", key)
                            scenario_owner_pass[key] +=1
                            count=1
                            break
                    if count==0:
                        ##print("not able to find:  ", feature_name, "key looked for: ", key)
                        scenario_owner_pass["No OWNER"] +=1
                            
                        
                    x=0
                    cs_tags = 0
                    sa_tags = 0
                    crm_tags = 0
                    t=0
                    while x< tags_in_scenario:
                        e=0
                        c=0
                        while e<len(tag_details):
                            try:
                                string=cucumber_report_dict[i]['elements'][j]['tags'][x]['name']
                            except KeyError as e:
                                #print("There is no tag in scenario")
                                string="not available"
                    
                            
                            tag_details_e=tag_details[e]
                            if string.lower()==tag_details_e.lower():
                                t=1
                                c=1
                                for key, value in dict1.items():
                                    ##print(tag_details[e])
                                    if value == tag_details[e]:                                       
                                        tag_pass[key] +=1
                                        #print("tag found in scenario: ",scenario_name," tag: ", value)
                                        break
                                break
                            e=e+1
                        if c==1:
                            break
                        #print("tag not found in scenario: ",scenario_name," tag: ", tag_details_e)
                        x +=1
                    if tags_in_feature >0 and c==0:
                        x=0
                        while x< tags_in_feature:
                            e=0
                            c=0
                            while e<len(tag_details):
                                try:
                                    string=cucumber_report_dict[i]['tags'][x]['name']
                                except KeyError as e:
                                    #print("There is no tag in feature")
                                    string="not available"
                                
                                tag_details_e=tag_details[e]
                                if string.lower()==tag_details_e.lower():
                                    t=1
                                    c=1
                                    for key, value in dict1.items():
                                        ##print("feature: ", tag_details[e])
                                        if value == tag_details[e]:                                       
                                            tag_pass[key] +=1
                                            #print("tag found in feature: ",feature_name," tag: ", tag_details_e)
                                            break
                                    break
                                e=e+1
                            if c==1:
                                break
                            #print("tag not found in feature: ",feature_name," tag: ", tag_details_e)
                            x +=1
                    
                    if t ==0:
                        tag_pass["none"] +=1
                                   
                  
                else:
                    scenario_result.append('failed')
                    count=0
                    for key, value in scenario_owner.items():
                        if key in feature_name:
                            scenario_owner_fail[key] +=1
                            count=1
                            break
                    if count==0:
                        ##print(feature_name)
                        scenario_owner_fail["No OWNER"] +=1                        
                    x=0
                    cs_tags = 0
                    sa_tags = 0
                    crm_tags = 0
                    t=0
                    
                    while x< tags_in_scenario:
                        e=0
                        c=0
                        while e<len(tag_details):
                            try:
                                string=cucumber_report_dict[i]['elements'][j]['tags'][x]['name']
                            except KeyError as e:
                                #print("There is no tag in scenario")
                                string="not available" 
                            tag_details_e=tag_details[e]
                            if  string.lower()==tag_details_e.lower():
                                t=1
                                c=1
                                for key, value in dict1.items():
                                    ##print(tag_details[e])
                                    if value == tag_details[e]:                                       
                                        tag_fail[key] +=1
                                        #print("tag found in scenario: ",scenario_name," tag: ", value)
                                        break
                                break
                            e=e+1
                            
                        if c==1:
                            break
                        #print("tag not found in scenario: ",scenario_name," tag: ", tag_details_e)
                        x +=1
                    if tags_in_feature >0 and c==0:
                        x=0
                        while x< tags_in_feature:
                            e=0
                            c=0
                            while e<len(tag_details):
                                try:
                                    string=cucumber_report_dict[i]['tags'][x]['name']
                                except KeyError as e:
                                    #print("There is no tag in feature")
                                    string="not available"
                                tag_details_e=tag_details[e]
                                if string.lower()==tag_details_e.lower():
                                    t=1
                                    c=1
                                    for key, value in dict1.items():
                                        ##print("feature: ", tag_details[e])
                                        if value == tag_details[e]:                                       
                                            tag_fail[key] +=1
                                            #print("tag found in feature: ",feature_name," tag: ", tag_details_e)
                                            break
                                    break
                                e=e+1
                            if c==1:
                                break
                            #print("tag not found in feature: ",feature_name," tag: ", tag_details_e)
                            x +=1    
                    if t ==0:
                        
                        tag_fail["none"] +=1
                    
                    
                    flag_For_Background=0
                    flag_for_Scenario=0
                   
            scenario_passed_testcases.append(background_and_scenario_step_result.count('passed'))
            scenario_failed_testcases.append(background_and_scenario_step_result.count('failed'))
            scenario_skipped_testcases.append(background_and_scenario_step_result.count('skipped'))
            j=j+1#scenario 
                    
        i=i+1#feature
    
    job=job+1#json file
    
html2 = html2 +"</table>"
   
# In[46]:




#Pie chart for test scenarios
labels = ['Passed', 'Failed', 'Skipped']
sizes = [scenario_result.count('passed'), scenario_result.count('failed'),
         scenario_result.count('skipped')]


#colors
colors = ['limegreen', 'red', 'grey']
 
fig1, ax1 = plt.subplots(figsize=(3,2))
ax1.pie(sizes, colors = colors, labels=['','',''], autopct='', startangle=90)
#draw circle
centre_circle = plt.Circle((0,0),0.60,fc='white')
fig1 = plt.gcf()
fig1.gca().add_artist(centre_circle)

#create labels
passL = Decimal((scenario_result.count('passed')
                 /(scenario_result.count('passed')
                   +scenario_result.count('failed')
                   +scenario_result.count('skipped')))*100)
passL=round(passL,2)

failL = Decimal((scenario_result.count('failed')
                 /(scenario_result.count('passed')
                   +scenario_result.count('failed')
                   +scenario_result.count('skipped')))*100)
failL=round(failL,2)

skippedL = Decimal((scenario_result.count('skipped')
                 /(scenario_result.count('passed')
                   +scenario_result.count('failed')
                   +scenario_result.count('skipped')))*100)
skippedL=round(skippedL,2)

fig1.gca().legend(('Passed: '+str(passL)+'%', 'Failed: '+str(failL)+'%', 'Skipped: '+str(skippedL)+'%'))



# Equal aspect ratio ensures that pie is drawn as a circle
ax1.axis('equal') 
 
plt.tight_layout()
fig1.savefig("scenarioCRM.png")


totalPassed = sum(scenario_passed_testcases)
totalFailed = sum(scenario_failed_testcases)
totalSkipped = sum(scenario_skipped_testcases)



#Pie chart for test cases
labels = ['Passed', 'Failed', 'Skipped']
sizes = [totalPassed, totalFailed, totalSkipped]
#colors
colors = ['limegreen', 'red', 'grey']
 
fig1, ax1 = plt.subplots(figsize=(3,2))
ax1.pie(sizes, colors = colors, labels=['','',''], autopct='', startangle=90)
#draw circle
centre_circle = plt.Circle((0,0),0.60,fc='white')
fig1 = plt.gcf()
fig1.gca().add_artist(centre_circle)

#create labels
passL = Decimal((totalPassed/(totalPassed+totalFailed+totalSkipped))*100)
passL=round(passL,2)

failL = Decimal((totalFailed/(totalPassed+totalFailed+totalSkipped))*100)
failL=round(failL,2)

skippedL = Decimal((totalSkipped/(totalPassed+totalFailed+totalSkipped))*100)
skippedL=round(skippedL,2)

fig1.gca().legend(('Passed: '+str(passL)+'%', 'Failed: '+str(failL)+'%', 'Skipped: '+str(skippedL)+'%'))


# Equal aspect ratio ensures that pie is drawn as a circle
ax1.axis('equal') 
 
plt.tight_layout()
fig1.savefig("testCRM.png")

total_testcases = totalPassed+totalFailed+totalSkipped
total_scenarios = scenario_result.count('passed')+scenario_result.count('failed')+scenario_result.count('skipped')
html3="<br><br><br>"
if sys.argv[3] != 'na' and sys.argv[3] != 'NA' and sys.argv[3] != 'Na':
    html3 = '''
<table border = "1"><tr bgcolor = '#728CA3'><th>Owners</th>
                         <th>Total Scenario Run</th>
                         <th>Scenario Passed</th>
                         <th>Scenario Failed</th>
                         <th>Pass %</th></tr>'''

Ready_To_Ship='Yes'
for key, value in scenario_owner.items():
    if sys.argv[3] != 'na' and sys.argv[3] != 'NA' and sys.argv[3] != 'Na':
        pass_perc = (scenario_owner_pass[key]/(scenario_owner_pass[key]+scenario_owner_fail[key])) * 100 if scenario_owner_pass[key]+scenario_owner_fail[key] >0 else 0
        pass_perc = round(pass_perc,2)
        html3 += """<tr bgcolor='#F3E4C6'><td bgcolor='#73C0F4'><b>{}</b></td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>""".format(key,str(scenario_owner_pass[key]+scenario_owner_fail[key]),str(scenario_owner_pass[key]),str(scenario_owner_fail[key]),str(pass_perc) )
    if scenario_owner_fail[key] >0:
        Ready_To_Ship='No'


if Ready_To_Ship=='No':
    html1 += "<b>Ready To Ship: <font color = 'red'>{}</font></b>".format(Ready_To_Ship)
else:
    html1 += "<b>Ready To Ship: <font color = 'green'>{}</font></b>".format(Ready_To_Ship)


html1 +='''<br><br><br><b><u><font size="4">Product wise Status:</font></u></b><br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<table border = "1"><tr bgcolor='#728CA3'><th >Product</th>
                            <th>Tags</th>
                         <th>Total Scenario Run</th>
                         <th>Scenario Passed</th>
                         <th>Scenario Failed</th>
                         <th>Pass %</th></tr>
'''



for key, value in tag.items():
    tag[key] += tag_pass[key]
    tag[key] += tag_fail[key]
    
for key, value in tag_pass.items():
    pass_perc = (tag_pass[key]/(tag_pass[key]+tag_fail[key]))*100 if (tag_pass[key]+tag_fail[key])>0 else 0
    pass_perc = round(pass_perc,2)
    if key == "none":
        html1 += """<tr bgcolor='#E6EFF3'><td><b>{}</b></td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>""".format(key,"None",str(tag_pass[key]+tag_fail[key]),str(tag_pass[key]),str(tag_fail[key]),str(pass_perc) )
    else:
        html1 += """<tr bgcolor='#E6EFF3'><td><b>{}</b></td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>""".format(key,dict1[key],str(tag_pass[key]+tag_fail[key]),str(tag_pass[key]),str(tag_fail[key]),str(pass_perc) )
        
    
#     if key == "CRM":
#         html1 += """<b><tr bgcolor='#73C0F4'><td><b>{}</b></td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr></b>""".format(key,"@CRMALL",str(tag_pass[key]+tag_fail[key]),str(tag_pass[key]),str(tag_fail[key]),str(pass_perc) )
#         html1 += "<b><tr bgcolor='#728CA3'><center><td colspan = '6'></td></center></tr></b>"
#     elif key == "Customer Service":
#         html1 += """<tr bgcolor='#E6EFF3'><td><b>{}</b></td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>""".format(key,"@CS-Regression",str(tag_pass[key]+tag_fail[key]),str(tag_pass[key]),str(tag_fail[key]),str(pass_perc) )
#     elif key == "Sales Automation":
#         html1 += """<tr bgcolor='#E6EFF3'><td><b>{}</b></td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>""".format(key,"@SA-REGRESSION",str(tag_pass[key]+tag_fail[key]),str(tag_pass[key]),str(tag_fail[key]),str(pass_perc) )
#     else:
#         html1 += """<tr bgcolor='#F3E4C6'><td><b>{}</b></td><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>""".format(key,"No Standard Tag Found",str(tag_pass[key]+tag_fail[key]),str(tag_pass[key]),str(tag_fail[key]),str(pass_perc) )

total_pass_perc = Decimal((scenario_result.count('passed')/total_scenarios)*100)
total_pass_perc = round(total_pass_perc,2)    
    
html1 += "</table>"
if sys.argv[3] != 'na' and sys.argv[3] != 'NA' and sys.argv[3] != 'Na':
    html1 += '''<br><br><b><u> <font size="4">Owner wise Status: </font></u></b>'''



for key, value in scenario_owner.items():
    scenario_owner[key] += scenario_owner_pass[key]
    scenario_owner[key] += scenario_owner_fail[key]




total_pass_perc = Decimal((scenario_result.count('passed')/total_scenarios)*100)
total_pass_perc = round(total_pass_perc,2)

if sys.argv[3] != 'na' and sys.argv[3] != 'NA' and sys.argv[3] != 'Na':
    html3 += "<tr bgcolor='#728CA3'><b><td >{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></b></tr></table>".format("Total",str(total_scenarios), str(scenario_result.count('passed')), str(scenario_result.count('failed')),str(total_pass_perc))

html3 += '''</br><b><u><font size="4">Scenario wise Status: </font></u></b>'''

html3 +='''<br/><br/>
       <font size="4"><b>Scenario execution chart: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
       &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
       &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
       &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
       Test-Cases execution chart:</b></font>
       <br/><br/>
        <img src="cid:image1" align="left" width="300" 
       height="205" ><img src="cid:image2" align="left" width="300" 
       height="205" >
    </br></br>'''


html = html1+html3+html2 
html = html+"</body></html>"

# Record the MIME types.
msgHtml = MIMEText(html, 'html')

img = open('scenarioCRM.png', 'rb').read()
msgImg = MIMEImage(img, 'png')
msgImg.add_header('Content-ID', '<image1>')
msgImg.add_header('Content-Disposition', 'inline', filename='scenarioCRM.png')

img = open('testCRM.png', 'rb').read()
msgImg1 = MIMEImage(img, 'png')
msgImg1.add_header('Content-ID', '<image2>')
msgImg1.add_header('Content-Disposition', 'inline', filename='testCRM.png')





strFrom = "emailID@gmail.com"
strTo = "whomSoeveryouWantToSend@abc.com"
strTo1 = "whomSoeveryouWantToSend@abc.com"
sub = "Automation Report:"


# Create message container.
msgRoot = MIMEMultipart('related')
msgRoot['Subject'] = sub
msgRoot['From'] = strFrom
msgRoot['To'] = strTo

msgRoot.attach(msgHtml)
msgRoot.attach(msgImg)
msgRoot.attach(msgImg1)


# Send the message via local SMTP server.
import smtplib
smtp = smtplib.SMTP()
smtp.connect('smtp.gmail.com')
smtp.ehlo()
smtp.starttls()
smtp.ehlo()
smtp.login("emailID@gmail.com", "password")
smtp.sendmail(strFrom, strTo, msgRoot.as_string())
smtp.sendmail(strFrom, strTo1, msgRoot.as_string())
smtp.quit()

