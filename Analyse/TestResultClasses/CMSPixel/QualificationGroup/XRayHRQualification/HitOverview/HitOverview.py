import ROOT
import AbstractClasses
import array
from FPIXUtils.moduleSummaryPlottingTools import *

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_XRayHRQualification_HitOverview_TestResult'
        self.NameSingle='HitOverview'
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'


    def PopulateResultData(self):
        plots = [None] * 16
        self.Canvas.Clear()

        # copy ROC data to module data
        for i in self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResults']:
            ChipTestResultObject = self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResults'][i]
            histo = ChipTestResultObject.ResultData['SubTestResults']['HitMap_{Rate}'.format(Rate=self.Attributes['Rate'])].ResultData['Plot']['ROOTObject']
            if not histo:
                print 'cannot get', 'HitMap_{Rate}'.format(Rate=self.Attributes['Rate']), 'histo for chip ',ChipTestResultObject.Attributes['ChipNo']
                continue
            chipNo = ChipTestResultObject.Attributes['ChipNo']
            histoName = 'HitMap_%s' %self.Attributes['Rate'] + '_Summary%s'  %chipNo
            histo.SetName(histoName)
            plots[chipNo] = histo

        summaryPlot = makeMergedPlot(plots)
        zRange = findZRange(plots)
        setZRange(summaryPlot,zRange)
        self.Canvas = setupSummaryCanvas(summaryPlot)
        self.ResultData['Plot']['Format'] = 'png'
        self.Title = 'Hit Map {Rate}'.format(Rate=self.Attributes['Rate'])
        self.SaveCanvas()
