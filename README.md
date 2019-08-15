# Beautiful Automation Reports In Email
This project is for sending a beautiful HTML content in an email, from json file generated after selenium automation runs.

What is this project all about?
For sending Automation reports email notifications, We were using email-notification plugin in Jenkins. But, that plugin only sends raw data but no beautiful looking graphics attached.
So, Here you have a python script which will send an automation reports in an e-mail. This script is enriched with more features than email-notification plugin.

So now you will be wondering “Why Python?”
-	To keep it very short, will say, it has one of the most beautiful module “Matplotlib” which gives beautiful graphs(our project uses pie charts)

Main features of this report are:
1.	Beautiful automation reports are sent to stakeholders(or whom so ever it conerns) on daily basis.
2.	A single report which is a combination of “n” number of json files. This is very useful when we are  executing automation parallelly, a single report is created for multiple Json files, instead of multiple emails for every execution.
3.	Reports can be sent to multiple email ids depending on one’s requirement.

What all will be there in your automation report. Please find below the breakdown of the report in your e-mail.

1.	It gives a total count of scenarios, test cases including count of pass and failed ones.
2.  We have owner-wise report(when owners present for different scripts/features/scenarios), it works only if owners are specified in feature name.
2.	A pie chart which will contain percentage of passed, failed and skipped scenarios and test steps.
3.	A detailed report of features, scenarios and test cases along with their status.


A Quick overview about the design and configuration.

“How it works?”
-	Script will take three arguments.
Argument 1: location of cucumber files(works for windows): It takes json files location as argument1 and process all the data of all the json files present in given location.
Example: C:\\Users\\shara6\\Desktop\\AppliedAI

Argument 2: Product and tag combination as in below email
Example: '{"First Product Name":”Associated tag for first product”,”Second Product name”:" Associated tag for first product "}' 

Argument 3: Owner names as in below email.
Example: '"owner 1","owner 2"'

Example of how to run the code:
python C:\Users\shara6\Desktop\SendEmailArtifacts\Generic_report.py C:\Users\shara6\Desktop\SendEmailArtifacts\json_files '{"First Product Name":”Associated tag for first product”,”Second Product name”:" Associated tag for first product "}' '"owner 1","owner 2"'

Note: This will run on Python3 and need a matplotlib module imported first.
