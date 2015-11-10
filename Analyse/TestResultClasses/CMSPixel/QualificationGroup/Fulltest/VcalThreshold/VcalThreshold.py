import ROOT
import AbstractClasses
import ROOT
import math
from FPIXUtils.moduleSummaryPlottingTools import *

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_Fulltest_VcalThreshold_TestResult'
        self.NameSingle='VcalThreshold'
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'
        self.Title = 'Vcal Threshold'


    def PopulateResultData(self):
        ROOT.gStyle.SetOptStat(0);
        plots = [] 
        for i in self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResults']:
            ChipTestResultObject = self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResults'][i]
            histo = ChipTestResultObject.ResultData['SubTestResults']['VcalThresholdTrimmed'].ResultData['Plot']['ROOTObject_Map']
            if not histo:
                print 'cannot get VcalThresholdTrimmed histo for chip ',ChipTestResultObject.Attributes['ChipNo']
                continue

            chipNo = ChipTestResultObject.Attributes['ChipNo']
            histoName = 'VcalThreshold_ROC%s' %chipNo
            histo.SetName(histoName)
            plots.append(histo)

        plots = sorted(plots, key=lambda h:int(h.GetName().split('ROC')[1]))
        summaryPlot = makeMergedPlot(plots)
        zRange = findZRange(plots)
        setZRange(summaryPlot,zRange)
        self.Canvas = setupSummaryCanvas(summaryPlot)

        self.ResultData['Plot']['Format'] = 'png'

        if self.SavePlotFile:
            self.Canvas.SaveAs(self.GetPlotFileName())
            print 'Saved ', self.GetPlotFileName()
        self.ResultData['Plot']['Enabled'] = 1
        self.ResultData['Plot']['Caption'] = 'Vcal Threshold Map'
        self.ResultData['Plot']['ImageFile'] = self.GetPlotFileName()
