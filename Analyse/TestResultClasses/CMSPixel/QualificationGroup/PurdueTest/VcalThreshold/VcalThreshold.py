import ROOT
import AbstractClasses
import ROOT
import math
from FPIXUtils.moduleSummaryPlottingTools import *


class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_PurdueTest_VcalThreshold_TestResult'
        self.NameSingle='VcalThreshold'
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'
        self.Title = 'Vcal Threshold Map'


    def PopulateResultData(self):
        ROOT.gStyle.SetOptStat(0);
        #self.ResultData['Plot']['ROOTObject'] = ROOT.TH2D(self.GetUniqueID(), "", 8*self.nCols, 0., 8*self.nCols, 2*self.nRows, 0., 2*self.nRows); # mThreshold
        plots = [] 
        for i in self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResults']:
            ChipTestResultObject = self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResults'][i]
            histo = ChipTestResultObject.ResultData['SubTestResults']['VcalThresholdTrimmed'].ResultData['Plot']['ROOTObject_Map']
            if not histo:
                print 'cannot get VcalThresholdUntrimmed histo for chip ',ChipTestResultObject.Attributes['ChipNo']
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
