import ROOT
import AbstractClasses
import AbstractClasses.Helper.HistoGetter as HistoGetter

try:
       set
except NameError:
       from sets import Set as set
class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_PurdueTest_Chips_Chip_Summary_TestResult'
        self.NameSingle='Summary'
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_PurdueTest_ROC'
        
    # grading and related functions (HasBumpBondingProblems, etc.) moved to Grading.py
    

    def PopulateResultData(self):


        self.ResultData['KeyValueDictPairs'] = {
            'Total': {
                'Value':'{0:1.0f}'.format(len(self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['HiddenData']['TotalList'])),
                'Label':'Total'
            },
            'nDeadPixel': {
                'Value':'{0:1.0f}'.format(len(self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['HiddenData']['DeadPixelList'])),
                'Label':' - Dead Pixels'
            },
            'nNoisy1Pixel': {
                'Value':'{0:1.0f}'.format(len(self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['HiddenData']['Noisy1PixelList'])),
                'Label':'Noisy Pixels 1'
            },
            'nMaskDefect': {
                'Value':'{0:1.0f}'.format(len(self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['HiddenData']['MaskDefectList'])),
                'Label':' - Mask Defects'
            },
            'nDeadBumps': {
                'Value':'{0:1.0f}'.format(len(self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['HiddenData']['DeadBumpList'])),
                'Label':' - Dead Bumps'
            },
            #'nDeadTrimbits': {
            #    'Value':'{0:1.0f}'.format(len(self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['HiddenData']['DeadTrimbitsList'])),
            #    'Label':' - Dead Trimbits'
            #},
            'nAddressProblems': {
                'Value':'{0:1.0f}'.format(len(self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['HiddenData']['AddressProblemList'])),
                'Label':' - Address Problems'
            },
            'nNoisy2Pixel': {
                'Value':'{0:1.0f}'.format(len(self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['HiddenData']['NoisyPixelSCurveList'])),
                'Label':'Noisy Pixels 2'
            },
            'nThrDefect': {
                'Value':'{0:1.0f}'.format(len(self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['HiddenData']['ThrDefectList'])),
                'Label':'Trim Problems'
            },
            'nGainDefect': {
                'Value':'{0:1.0f}'.format(len(self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['HiddenData']['GainDefectList'])),
                'Label':'PH Gain defects'
            },
            'nPedDefect': {
                'Value':'{0:1.0f}'.format(len(self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['HiddenData']['PedDefectList'])),
                'Label':'PH Pedestal defects'
            },
            'nPar1Defect': {
                'Value':'{0:1.0f}'.format(len(self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['HiddenData']['Par1DefectList'])),
                'Label':'PH Parameter1 Defects'
            },
            'PixelDefectsGrade':{
                'Value': self.ParentObject.ResultData['SubTestResults']['Grading'].ResultData['KeyValueDictPairs']['PixelDefectsGrade']['Value'],
                'Label': 'Pixel Defects Grade ROC'
            },
            'empty':{
                'Value': '',
                'Label': ''
            }
        }
        self.ResultData['KeyList'] = ['Total', 'nDeadPixel', 'nMaskDefect', 'nDeadBumps', 'nDeadTrimbits', 'nAddressProblems', 'empty',
                                      'nNoisy1Pixel', 'nNoisy2Pixel', 'nThrDefect', 'nGainDefect', 'nPedDefect', 'nPar1Defect', 'PixelDefectsGrade']

