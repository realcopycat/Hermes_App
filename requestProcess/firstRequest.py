# process first request
from work1demo.requestProcess.esSearch import searchInES
import re

class req1Processor():
    def __init__(self, desOfcase, addrOfcase):
        #参数设置区
        self.index1 = "democriminal"
        self.index2 = "democase"
        self.index2key = "caseinfo"
        self.index1key = "addrcase"
        self.des = desOfcase
        self.addr = addrOfcase
        self.resnum = 4
        print(self.des)
        print(self.addr)
        self.caseResult = searchInES(self.des, self.index2, self.index2key, self.resnum + 10)
        self.criminalResult = searchInES(self.addr, self.index1, self.index1key, self.resnum)

    def main(self):

        mainAns = dict()
        mainAns['caseData'] = self.packCaseData()
        mainAns['criminalData'] = self.packCriminalData()
        return mainAns

    def packCaseData(self):
        finaldata = list()
        for item in self.caseResult:
            tmpresult = dict()
            tmpresult['caseBrife'] = item['_source']['caseinfo']
            tmpresult['caseDetail'] = item['_source']['casedetail']
            tmpresult['caseExp'] = item['_source']['casesummary']
            finaldata.append(tmpresult)
        return finaldata

    def packCriminalData(self):
        malecount = 0
        rescount = 0
        agesum = 0
        maxage = 0
        minage = 100
        edulevel = []

        rankList = sorted(self.criminalResult, key = lambda e:e.__getitem__('_score'))
        top3data = rankList[0:3]
        birthplaceList = []
        birthplacePattern = re.compile(r'.*村')
        for item in top3data:
            try:
                birthplaceList.append(re.search(birthplacePattern, item['_source']['birthplace']).group())
            except:
                print("出身地获取失败")

        genderPattern = re.compile(r'.*男.*')
        print(self.criminalResult)
        for item in self.criminalResult:
            agesum = agesum + int(item['_source']['age'])
            tmp_age = int(item['_source']['age'])
            if tmp_age > maxage:
                maxage = tmp_age
            if tmp_age < minage:
                minage = tmp_age
            if re.search(genderPattern, item['_source']['gender']):
                malecount = malecount + 1
            if item['_source']['edulevel'] not in edulevel:
                edulevel.append(item['_source']['edulevel'])    
            rescount = rescount + 1

        sexratioMen = malecount / rescount

        finalAnswer = dict()
        finalAnswer['ratioWomen'] = ( 1 - sexratioMen ) * 100
        if sexratioMen == 1:
            sexratioMen = 90 
        finalAnswer['ratioMen'] = sexratioMen
        finalAnswer['maxage'] = maxage
        finalAnswer['minage'] = minage
        finalAnswer['birthplace'] = birthplaceList
        finalAnswer['edu'] = edulevel

        return finalAnswer

            
            

            