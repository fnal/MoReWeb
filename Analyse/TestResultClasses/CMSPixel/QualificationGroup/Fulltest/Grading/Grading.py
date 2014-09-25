# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_Fulltest_Grading_TestResult'
        self.NameSingle='Grading'
        self.Title = 'Grading'
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'
        

    def getNumberOfRocsWithGrade(self,Grade,GradeList):
        l = [i for i in GradeList if i == Grade]
        return len(l)
        
    def GetSingleChipGrade(self, CurrentGrade, TestResultObject, Value, nValue):
    	ChipGrade = CurrentGrade
	if ChipGrade == 1 and Value > TestResultObject.ResultData['HiddenData']['LimitB']:
		ChipGrade = 2
	if Value > TestResultObject.ResultData['HiddenData']['LimitC']:
		ChipGrade = 3
	if ChipGrade == 1 and nValue < (8*self.nCols - self.TestResultEnvironmentObject.GradingParameters['defectsB']):
		ChipGrade = 2
	if nValue < (8*self.nCols - self.TestResultEnvironmentObject.GradingParameters['defectsC']):
		ChipGrade = 3
	return ChipGrade
	
    def PopulateResultData(self):
        SubGradings = {}
        ModuleGrade = 1 # 1 = A, 2 = B, 3 = C 
        GradeMapping = {
            1:'A',
            2:'B',
            3:'C'
        }
        BadRocs = 0
        chipResults = self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResultDictList']
        for i in chipResults:
            if int(i['TestResultObject'].ResultData['SubTestResults']['Summary'].ResultData['KeyValueDictPairs']['Total']['Value']) > 0.01 * self.nCols*self.nRows:
                BadRocs += 1
            SubGradings['PixelDefects'] =  [ i['TestResultObject'].ResultData['SubTestResults']['Summary'].ResultData['KeyValueDictPairs']['PixelDefectsGrade']['Value'] for i in chipResults]
       
        # Grading
        
        for i in ['Noise', 'VcalThresholdWidth', 'RelativeGainWidth', 'PedestalSpread', 'Parameter1']:
            if not self.ParentObject.ResultData['SubTestResults'].has_key(i):
                continue
            TestResultObject = self.ParentObject.ResultData['SubTestResults'][i]
            SubGrading = []
            for j in range(self.ParentObject.Attributes['NumberOfChips']-self.ParentObject.Attributes['StartChip']):
            
                Value= TestResultObject.ResultData['Plot']['ROOTObject'].GetBinContent(j+1) 
                nValue = TestResultObject.ResultData['Plot']['ROOTObject_h2'].GetBinContent(j+1) 
                
                
                # Grading 
                ChipGrade = self.GetSingleChipGrade(1, TestResultObject, Value, nValue)
                SubGrading.append('%d'%ChipGrade)
               
               	ModuleGrade = self.GetSingleChipGrade(ModuleGrade, TestResultObject, Value, nValue)
                
                '''
                # Failures reasons...
                if Value > criteriaB[i] and Value < criteriaC[i]:
                    fitsProblemB[i]++
                if Value > criteriaC[i]:
                    fitsProblemC[i]++
                '''
#             print '%s: %s'%(i,SubGrading)
            SubGradings[i] = SubGrading
            
            
        CurrentAtVoltage150V = 0
        CurrentVariation = 0
        if self.ParentObject.ResultData['SubTestResults'].has_key('IVCurve'):
            IVTestResult = self.ParentObject.ResultData['SubTestResults']['IVCurve']    
            CurrentAtVoltage150V = float(IVTestResult.ResultData['KeyValueDictPairs']['CurrentAtVoltage150V']['Value'])
            CurrentVariation = float(IVTestResult.ResultData['KeyValueDictPairs']['Variation']['Value'])
        else:
            pass
        
        for i in SubGradings:
            print '%s: %s/%s/%s'%(i,self.getNumberOfRocsWithGrade('1',SubGradings[i]),self.getNumberOfRocsWithGrade('2',SubGradings[i]),self.getNumberOfRocsWithGrade('3',SubGradings[i]))
            
#         print 'PixelDefects: %s'%SubGradings['PixelDefects']
#         print 'A:',self.getNumberOfRocsWithGrade('1',SubGradings['PixelDefects'])
#         print 'B:',self.getNumberOfRocsWithGrade('2',SubGradings['PixelDefects'])
#         print 'C:',self.getNumberOfRocsWithGrade('3',SubGradings['PixelDefects'])        
        #TODO
        
        
        if self.ParentObject.Attributes['TestType']  == 'p17_1':
            # Grading
            if ModuleGrade == 1 and BadRocs > 1:
                ModuleGrade = 2
            if ModuleGrade == 1 and CurrentAtVoltage150V > self.TestResultEnvironmentObject.GradingParameters['currentB']:
                    
                ModuleGrade = 2;
            if ModuleGrade == 1   and CurrentVariation >  self.TestResultEnvironmentObject.GradingParameters['slopeivB']:
                    
                ModuleGrade = 2
            if BadRocs > 2:
                ModuleGrade = 3
            if CurrentAtVoltage150V > self.TestResultEnvironmentObject.GradingParameters['currentC']:
                ModuleGrade = 3; 

            '''
            // Failures reasons...
            if( (i150> currentB) && (i150 < currentC) ) currentProblemB++;
            if( (i150> currentC) ) currentProblemC++;
            if( (ratio > slopeivB) ) slopeProblemB++;
 '''
        else:   
            # Grading
            if ModuleGrade == 1 and BadRocs > 1:
                ModuleGrade = 2
            if ModuleGrade == 1 and CurrentAtVoltage150V > self.TestResultEnvironmentObject.GradingParameters['currentBm10']:
                ModuleGrade = 2
            if ModuleGrade == 1 and CurrentVariation > self.TestResultEnvironmentObject.GradingParameters['slopeivB']:
                ModuleGrade = 2
            if BadRocs > 2:
                ModuleGrade = 3
            if CurrentAtVoltage150V > self.TestResultEnvironmentObject.GradingParameters['currentCm10']:
                ModuleGrade = 3
                
            '''
            # Failures reasons...
            if (i150> 1.5*currentB and i150 < 1.5*currentC)currentProblemB++;
            if (i150> 1.5*currentC) ){ currentProblemC++;}
            if (ratio > slopeivB) ){ slopeProblemB++;}
            '''
            
            
        
        nPixelDefectsTotal  = 0
        nPixelDefectsGradeA = self.getNumberOfRocsWithGrade('1',SubGradings['PixelDefects'])
        nPixelDefectsGradeB = self.getNumberOfRocsWithGrade('2',SubGradings['PixelDefects'])
        nPixelDefectsGradeC = self.getNumberOfRocsWithGrade('3',SubGradings['PixelDefects'])
        
        self.ResultData['KeyValueDictPairs'] = {
            'Module': {
                'Value':self.ParentObject.Attributes['ModuleID'], 
                'Label':'Module'
            },
            'ModuleGrade': {
                'Value':'{0:1.0f}'.format(ModuleGrade), 
                'Label':'Grade'
            },
            'BadRocs': {
                'Value':'{0:1.0f}'.format(BadRocs), 
                'Label':'ROCs > 1% defects'
            },
            'nPixelDefectsGradeA': {
                'Value':'{0:1.0f}'.format(nPixelDefectsGradeA), 
                'Label':'ROCs with Grade A'
            },
            'nPixelDefectsGradeB': {
                'Value':'{0:1.0f}'.format(nPixelDefectsGradeB), 
                'Label':'ROCs with Grade B'
            },
            'nPixelDefectsGradeC': {
                'Value':'{0:1.0f}'.format(nPixelDefectsGradeC), 
                'Label':'ROCs with Grade C'
            },
        }
        self.ResultData['HiddenData']['SubGradings'] = SubGradings
        #self.ResultData['HiddenData']['nPixelDefectsGradeA'] = nPixelDefectsGradeA
        #self.ResultData['HiddenData']['nPixelDefectsGradeB'] = nPixelDefectsGradeB
        #self.ResultData['HiddenData']['nPixelDefectsGradeC'] = nPixelDefectsGradeC
        
        self.ResultData['KeyList'] = ['Module','ModuleGrade','BadRocs']

