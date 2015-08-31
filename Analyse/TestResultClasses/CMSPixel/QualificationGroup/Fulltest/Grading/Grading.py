# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses


class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name = 'CMSPixel_QualificationGroup_Fulltest_Grading_TestResult'
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

        PixelDefectsRocsA = 0
        PixelDefectsRocsB = 0
        PixelDefectsRocsC = 0
        chipResults = self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResultDictList']
        SubGrading = []
        for i in chipResults:
            if int(i['TestResultObject'].ResultData['SubTestResults']['Summary'].ResultData['KeyValueDictPairs'][
                'Total']['Value']) > 0.04 * self.nCols * self.nRows:
                PixelDefectsRocsC += 1
            elif int(i['TestResultObject'].ResultData['SubTestResults']['Summary'].ResultData['KeyValueDictPairs'][
                'Total']['Value']) > 0.01 * self.nCols * self.nRows:
                PixelDefectsRocsB += 1
            else:
                PixelDefectsRocsA += 1

            SubGrading.append([
                i['TestResultObject'].ResultData['SubTestResults']['Summary'].ResultData['KeyValueDictPairs'][
                    'PixelDefectsGrade']['Value'] for i in chipResults])
        SubGradings['PixelDefects'] = SubGrading

        # Grading

        # performance parameters grading
        for i in ['Noise', 'VcalThresholdWidth', 'RelativeGainWidth', 'PedestalSpread', 'Parameter1']:
            if not self.ParentObject.ResultData['SubTestResults'].has_key(i):
                continue
            TestResultObject = self.ParentObject.ResultData['SubTestResults'][i]
            SubGrading = []
            ChipResults = self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResultDictList']
            for j in ChipResults:
                ChipGradingTestResultObject = j['TestResultObject'].ResultData['SubTestResults']['Grading']

                # Grading 
                ChipGrade = ChipGradingTestResultObject.GetSingleChipSubtestGrade(
                    TestResultObject.Attributes['SpecialPopulateDataParameters'], 1)
                SubGrading.append('%d' % ChipGrade)

                ModuleGrade = ChipGradingTestResultObject.GetSingleChipSubtestGrade(
                    TestResultObject.Attributes['SpecialPopulateDataParameters'], ModuleGrade)

            if self.verbose:
                print '%s: %s'%(i,SubGrading)
            SubGradings[i] = SubGrading

        # IV Grading
        IVGrade = 0
        CurrentAtVoltage150V = 0
        RecalculatedCurrentAtVoltage150V = 0
        RecalculatedCurrentVariation = 0
        CurrentVariation = 0
        if self.ParentObject.ResultData['SubTestResults'].has_key('IVCurve'):
            IVGrade = 1
            IVTestResult = self.ParentObject.ResultData['SubTestResults']['IVCurve']
            CurrentAtVoltage150V = float(IVTestResult.ResultData['KeyValueDictPairs']['CurrentAtVoltage150V']['Value'])
            if IVTestResult.ResultData['KeyValueDictPairs'].has_key('recalculatedCurrentAtVoltage150V'):
                RecalculatedCurrentAtVoltage150V = float(
                    IVTestResult.ResultData['KeyValueDictPairs']['recalculatedCurrentAtVoltage150V']['Value'])
            if IVTestResult.ResultData['KeyValueDictPairs'].has_key('recalculatedCurrentVariation'):
                RecalculatedCurrentVariation = float(
                    IVTestResult.ResultData['KeyValueDictPairs']['recalculatedCurrentVariation']['Value'])
            CurrentVariation = float(IVTestResult.ResultData['KeyValueDictPairs']['Variation']['Value'])

            # current
            if self.ParentObject.Attributes['TestType'] == 'p17_1':
                if IVGrade == 1 and CurrentAtVoltage150V > self.TestResultEnvironmentObject.GradingParameters['currentB']:
                    IVGrade = 2
                if CurrentAtVoltage150V > self.TestResultEnvironmentObject.GradingParameters['currentC']:
                    IVGrade = 3
            else:
                if IVGrade == 1 and RecalculatedCurrentAtVoltage150V > self.TestResultEnvironmentObject.GradingParameters['currentBm10']:
                    IVGrade = 2
                if RecalculatedCurrentAtVoltage150V > self.TestResultEnvironmentObject.GradingParameters['currentCm10']:
                    IVGrade = 3

            # slope
            if IVGrade == 1 and CurrentVariation > self.TestResultEnvironmentObject.GradingParameters['slopeivB']:
                IVGrade = 2
            if CurrentVariation > self.TestResultEnvironmentObject.GradingParameters['slopeivC']:
                IVGrade = 3

        else:
            pass

        # add pixel defects grading to final grade
        if ModuleGrade == 1 and PixelDefectsRocsB > 0:
            ModuleGrade = 2
        if PixelDefectsRocsC > 0:
            ModuleGrade = 3

        nPixelDefectsTotal = 0
        try:
            nPixelDefectsGradeA = self.getNumberOfRocsWithGrade('1', SubGradings['PixelDefects'])
            nPixelDefectsGradeB = self.getNumberOfRocsWithGrade('2', SubGradings['PixelDefects'])
            nPixelDefectsGradeC = self.getNumberOfRocsWithGrade('3', SubGradings['PixelDefects'])
        except KeyError as e:
            print 'Errror', e
            print SubGradings.keys()
            raise e

        # missing subtest results
        MissingSubtests = False
        nChips = len(self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResultDictList'])
        if nChips < 16:
            print "nChips: ", nChips
            MissingSubtests = True
            ModuleGrade = 3

        # electrical grade = ModuleGrade before IV
        ElectricalGrade = ModuleGrade

        # combine with IV grade
        if IVGrade > ModuleGrade:
            ModuleGrade = IVGrade

        print 'Fulltest Summary:'
        if MissingSubtests:
            print "\x1b[31mMISSING TESTS!\x1b[0m"
        print " %s: %s"%('Grade'.ljust(23), GradeMapping[ModuleGrade] if ModuleGrade in GradeMapping else 'None')
        print " SubGradings:"
        print "  %s: %s"%('Electrical'.ljust(22), GradeMapping[ElectricalGrade] if ElectricalGrade in GradeMapping else 'None')
        print "  %s: %s"%('IV'.ljust(22), GradeMapping[IVGrade] if IVGrade in GradeMapping else 'None')
        for i in SubGradings:
            print '  %s: %s/%s/%s' % (
                i.ljust(22), self.getNumberOfRocsWithGrade('1', SubGradings[i]),
                self.getNumberOfRocsWithGrade('2', SubGradings[i]),
                self.getNumberOfRocsWithGrade('3', SubGradings[i]))

        self.ResultData['KeyValueDictPairs'] = {
            'Module': {
                'Value': self.ParentObject.Attributes['ModuleID'],
                'Label': 'Module'
            },
            'ModuleGrade': {
                'Value': '{0:1.0f}'.format(ModuleGrade),
                'Label': 'Grade'
            },
            'ElectricalGrade': {
                'Value': '{0:1.0f}'.format(ElectricalGrade),
                'Label': 'Electrical Grade'
            },
            'IVGrade': {
                'Value': '{0:1.0f}'.format(IVGrade),
                'Label': 'IV Grade'
            },
            'PixelDefectsRocsA': {
                'Value': '{0:1.0f}'.format(PixelDefectsRocsA),
                'Label': 'ROCs < 1% defects'
            },
            'PixelDefectsRocsB': {
                'Value': '{0:1.0f}'.format(PixelDefectsRocsB),
                'Label': 'ROCs > 1% defects'
            },
            'PixelDefectsRocsC': {
                'Value': '{0:1.0f}'.format(PixelDefectsRocsC),
                'Label': 'ROCs < 4% defects'
            },
            'nPixelDefectsGradeA': {
                'Value': '{0:1.0f}'.format(nPixelDefectsGradeA),
                'Label': 'ROCs with Grade A'
            },
            'nPixelDefectsGradeB': {
                'Value': '{0:1.0f}'.format(nPixelDefectsGradeB),
                'Label': 'ROCs with Grade B'
            },
            'nPixelDefectsGradeC': {
                'Value': '{0:1.0f}'.format(nPixelDefectsGradeC),
                'Label': 'ROCs with Grade C'
            },
        }
        self.ResultData['HiddenData']['SubGradings'] = SubGradings
        self.ResultData['HiddenData']['MissingSubtests'] = {'Label': 'Missing Subtests', 'Value': '1' if MissingSubtests else '0'}
        self.ResultData['KeyList'] = ['Module', 'ModuleGrade', 'PixelDefectsRocsB']


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



