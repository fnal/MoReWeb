# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses


class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name = 'CMSPixel_QualificationGroup_XRayHRQualification_Grading_TestResult'
        self.NameSingle = 'Grading'
        self.Title = 'Grading'
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'


    def getNumberOfRocsWithGrade(self, Grade, GradeList):
        l = [i for i in GradeList if i == Grade]
        return len(l)


    def PopulateResultData(self):
        SubGradings = {}
        ModuleGrade = 1
        GradeMapping = {
            1: 'A',
            2: 'B',
            3: 'C'
        }
        BadRocs = 0
        chipResults = self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResultDictList']
       
        GradeHistogram = {
            'A': 0,
            'B': 0,
            'C': 0,
        }
        SubGrading = []

        PixelDefects = 0
        BumpBondingDefects = 0
        NoiseDefects = 0
        HotPixelDefects = 0
        ROCsLessThanOnePercent = 0
        ROCsMoreThanOnePercent = 0
        ROCsMoreThanFourPercent = 0
        ROCsWithReadoutProblems = 0
        ROCsWithUniformityProblems = 0
        MeanEfficiency50List = []
        MeanEfficiency120List = []

        for i in chipResults:
            ROCGrade = i['TestResultObject'].ResultData['SubTestResults']['Grading'].ResultData['KeyValueDictPairs']['ROCGrade']['Value']
            GradeHistogram[ROCGrade] += 1
            if ROCGrade == GradeMapping[2] and ModuleGrade < 2:
                ModuleGrade = 2
            if ROCGrade == GradeMapping[3] and ModuleGrade < 3:
                ModuleGrade = 3

            BumpBondingDefectsROC = i['TestResultObject'].ResultData['SubTestResults']['Grading'].ResultData['HiddenData']['BumpBondingDefects']['Value']
            NoiseDefectsROC = i['TestResultObject'].ResultData['SubTestResults']['Grading'].ResultData['HiddenData']['NoiseDefects']['Value']
            HotPixelDefectsROC = i['TestResultObject'].ResultData['SubTestResults']['Grading'].ResultData['HiddenData']['HotPixelDefects']['Value']

            BumpBondingDefectsROC = int(BumpBondingDefectsROC) if BumpBondingDefectsROC is not None else 0
            NoiseDefectsROC = int(NoiseDefectsROC) if NoiseDefectsROC is not None else 0
            HotPixelDefectsROC = int(HotPixelDefectsROC) if HotPixelDefectsROC is not None else 0

            # total pixel defects per ROC
            PixelDefectsROC = i['TestResultObject'].ResultData['SubTestResults']['Grading'].ResultData['HiddenData']['PixelDefects']['Value']

            PixelDefects += PixelDefectsROC
            if PixelDefectsROC > 166:
                ROCsMoreThanFourPercent += 1
            elif PixelDefectsROC > 41:
                ROCsMoreThanOnePercent += 1
            else:
                ROCsLessThanOnePercent += 1

            # count pixel defects per module
            BumpBondingDefects += BumpBondingDefectsROC
            NoiseDefects += NoiseDefectsROC
            HotPixelDefects += HotPixelDefectsROC

            # mean efficiency
            MeanEfficiency50List.append(float(i['TestResultObject'].ResultData['SubTestResults']['EfficiencyInterpolation'].ResultData['HiddenData']['InterpolatedEfficiency50']['Value']))
            MeanEfficiency120List.append(float(i['TestResultObject'].ResultData['SubTestResults']['EfficiencyInterpolation'].ResultData['HiddenData']['InterpolatedEfficiency120']['Value']))

            # column uniformity
            NonUniformColumnsROC = int(i['TestResultObject'].ResultData['SubTestResults']['Grading'].ResultData['KeyValueDictPairs']['NumberOfNonUniformColumns']['Value'])
            if NonUniformColumnsROC > 0:
                ROCsWithUniformityProblems += 1

            # readout uniformity
            NonUniformEventsROC = 0
            for Rate in self.ParentObject.Attributes['Rates']['HRData']:
                NonUniformEventsROC += int(i['TestResultObject'].ResultData['SubTestResults']['Grading'].ResultData['HiddenData']['NumberOfNonUniformEvents_{Rate}'.format(Rate=Rate)])
            if NonUniformEventsROC > 0:
                ROCsWithReadoutProblems += 1

        SubGradings['PixelDefects'] = SubGrading
        self.ResultData['KeyValueDictPairs'] = {
            'Module': {
                'Value': self.ParentObject.Attributes['ModuleID'],
                'Label': 'Module'
            },
            'ModuleGrade': {
                'Value': GradeMapping[ModuleGrade],
                'Label': 'Grade'
            },
            'BumpBondingDefects': {
                'Value': BumpBondingDefects,
                'Label': 'Bump Bonding Defects'
            },
            'NoiseDefects': {
                'Value': NoiseDefects,
                'Label': 'Noise Defects'
            },
            'HotPixelDefects': {
                'Value': HotPixelDefects,
                'Label': 'Hot Pixel Defects'
            },
            'PixelDefects': {
                'Value': PixelDefects,
                'Label': 'Total Pixel Defects'
            },
            'Efficiency_50': {
                'Value': '{0:1.2f}'.format(sum(MeanEfficiency50List)/float(len(MeanEfficiency50List))),
                'Label': 'Mean efficiency at 50 MHz/cm2'
            },
            'Efficiency_120': {
                'Value': '{0:1.2f}'.format(sum(MeanEfficiency120List)/float(len(MeanEfficiency120List))),
                'Label': 'Mean efficiency at 120 MHz/cm2'
            },
            'ROCGrades': {
                'Value': '%d/%d/%d'%(GradeHistogram['A'], GradeHistogram['B'], GradeHistogram['C']),
                'Label': 'ROC Grades A/B/C'
            },
            'ROCsLessThanOnePercent': {
                'Value': ROCsLessThanOnePercent,
                'Label': 'ROCs with <1 %% defects'
            },
            'ROCsMoreThanOnePercent': {
                'Value': ROCsMoreThanOnePercent,
                'Label': 'ROCs with >1 %% defects'
            },
            'ROCsMoreThanFourPercent': {
                'Value': ROCsMoreThanFourPercent,
                'Label': 'ROCs with >4 %% defects'
            },
            'ROCsWithReadoutProblems': {
                'Value': ROCsWithReadoutProblems,
                'Label': 'ROCs with r/o problems'
            },
            'ROCsWithUniformityProblems': {
                'Value': ROCsWithUniformityProblems,
                'Label': 'ROCs with unif. problems'
            },
        }
        self.ResultData['HiddenData']['SubGradings'] = SubGradings
        self.ResultData['KeyList'] = ['Module', 'ModuleGrade', 'ROCGrades']


        # needed in summary1
        if self.verbose:
            print 'SubGradings of ROCs:'
        for i in SubGradings:
            for Grade in GradeMapping:
                key = i + 'Grade' + GradeMapping[Grade] + "ROCs"
                try:
                    nRocs = self.getNumberOfRocsWithGrade('%d' % Grade, SubGradings[i])
                except:
                    nRocs = -1
                entry = {
                    'Value': nRocs,
                    'Label': '%s Grade %s ROCs' % (i, GradeMapping[Grade])
                }
                if self.verbose:
                    print key, entry
                self.ResultData['KeyValueDictPairs'][key] = entry



