import ROOT
import AbstractClasses
import ROOT
from FPIXUtils.moduleSummaryPlottingTools import *

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_Purduetest_Chips_Chip_PixelAliveMap_TestResult'
        self.NameSingle='PixelAliveMap'
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'



    def PopulateResultData(self):
        ROOT.gPad.SetLogy(0);
        ROOT.gStyle.SetOptStat(0)
        plots = [] 
        for i in self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResults']:
            ChipTestResultObject = self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResults'][i]
            histo = ChipTestResultObject.ResultData['SubTestResults']['PixelMap'].ResultData['Plot']['ROOTObject']
            if not histo:
                print 'cannot get PixelMap histo for chip ',ChipTestResultObject.Attributes['ChipNo']
                continue
            chipNo = ChipTestResultObject.Attributes['ChipNo']
            histoName = 'PixelAlive_ROC%s' %chipNo
            histo.SetName(histoName)
            plots.append(histo)

        # sort the plot from ROC0 to ROC15, in order to be used for merging
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
        self.Title = 'Pixel Alive Map'
        self.ResultData['Plot']['ImageFile'] = self.GetPlotFileName()

