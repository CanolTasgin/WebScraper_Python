import pandas
import requests
from bs4 import BeautifulSoup

#CS Faculty Members
URL = 'https://fens.sabanciuniv.edu/tr/fakulte-uyeleri?group_id=281%2C301%2C303%2C285%2C861%2C282%2C681%2C721&prg_code=BSCS%2CPHDCS-UG%2CPHDCS%2CMSCS'

#URL = 'https://fens.sabanciuniv.edu/tr/fakulte-uyeleri' #ALL FENS members
page = requests.get(URL)

rawPageContent = page.text

soup = BeautifulSoup(page.content, 'html.parser')

#Names of members
names = soup.find_all('span', class_='card-title')
namesv2 = []
for name in names:
    namesv2 += name.text.strip().split('\n')

for name in namesv2:
    print(name)

#Mails of members
mails = soup.find_all('span', class_='mail contact')
str = ''
mailsv2 = []
for mail in mails:
    str = mail.text.strip().split('\n')
    str2 = str[0]
    str2 = str2[:str2.find('sabanciuniv')] + '@sabanciuniv.edu' #fixed format
    mailsv2.append(str2)

for mail in mailsv2:
    print(mail)



#Roles of members
roles = soup.find_all('span', class_='name')

roles2 = []
for role in roles:
    roles2 += role.text.strip().split('\n')

for role in roles2:
    print(role)

print(len(roles2))


#Research Areas of members
rA = soup.find_all('div', class_='work_content')
rA2 = []
for area in rA:
     rA2.append(area.text.strip().split('\n'))
# for area in rA:
#     for ele in area.text.strip().split('\n'):
#         rA2 += '\n' + ele

print(rA2)
print(len(rA2))


#Some members doesn't have any research area, fixed that here by typing 'No assigned Research Area' for them
checkRA = soup.find_all('a', class_='lesson-card big')

checkRA2 = []
raPositive = 0
for content in checkRA:
    children = content.findChildren("div", {'class':'work_content'})
    if len(children) == 0:
        checkRA2.append('- No assigned Research Area -')
    else:
        checkRA2.append(rA2[raPositive])
        raPositive += 1

for check in checkRA2:
    print(check)


# Python3 code here creating Faculty Members Class
class FacultyMembers:
    def __init__(self, name, role, mail, researchArea):
        self.name = name
        self.role = role
        self.mail = mail
        self.researchArea = researchArea

#for converting list into pandas dataframe
    def to_dict(self):
        return{
            'name':self.name,
            'role':self.role,
            'mail':self.mail,
            'researchArea':self.researchArea,
        }

memberList = []

#Cretaed list of members with object FacultyMembers
for name,mail,role,researchArea in zip(namesv2, mailsv2,roles2,checkRA2):
    memberList.append(FacultyMembers(name,role,mail,researchArea))

for member in memberList:
    print(member.name, member.role, member.mail, member.researchArea, sep=' --- ')

#Converted list into pandas Dataframe and exported excel file into Desktop
df = pandas.DataFrame.from_records([member.to_dict() for member in memberList])
df.columns = ['Name', 'Mail', 'Role', 'Research Area']
print(df)

df.to_excel(r'~/Desktop/CSMembers.xlsx', index = False)
