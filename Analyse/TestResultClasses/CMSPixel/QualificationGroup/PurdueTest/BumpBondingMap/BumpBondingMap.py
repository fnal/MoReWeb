import ROOT
import AbstractClasses
import ROOT
from ROOT import kRed, gStyle
from FPIXUtils.moduleSummaryPlottingTools import *

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_Purduetest_Chips_Chip_BumpBondingMap_TestResult'
        self.NameSingle='BumpBondingMap'
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'


    def PopulateResultData(self):
        ROOT.gPad.SetLogy(0);
        ROOT.gStyle.SetOptStat(0)
        plots = []
        for i in self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResults']:
            ChipTestResultObject = self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResults'][i]
            histo = ChipTestResultObject.ResultData['SubTestResults']['BumpBondingProblems'].ResultData['Plot']['ROOTObject']
            if not histo:
                print 'cannot get PixelMap histo for chip ',ChipTestResultObject.Attributes['ChipNo']
                continue
            chipNo = ChipTestResultObject.Attributes['ChipNo']
            histoName = 'BumpBonding_ROC%s' %chipNo
            histo.SetName(histoName)
            plots.append(histo)

        # sort the plot from ROC0 to ROC15, in order to be used for merging
        plots = sorted(plots, key=lambda h:int(h.GetName().split('ROC')[1]))
        summaryPlot = makeMergedPlot(plots)
        zRange = findZRange(plots)
        setZRange(summaryPlot,zRange)

        colors = array("i",[51+i for i in range(40)] + [kRed])
        gStyle.SetPalette(len(colors), colors);
        zMin=summaryPlot.GetMinimum()
        zMax=summaryPlot.GetMaximum()
        step=(zMax-zMin)/(len(colors)-1)
        levels = array('d',[zMin + i*step for i in range(len(colors)-1)]+[4.9999999])

        summaryPlot.SetContour(len(levels),levels)
        
        self.Canvas = setupSummaryCanvas(summaryPlot)

        self.ResultData['Plot']['Format'] = 'png'

        if self.SavePlotFile:
            self.Canvas.SaveAs(self.GetPlotFileName())
        print 'Saved ', self.GetPlotFileName()
        self.ResultData['Plot']['Enabled'] = 1
        self.Title = 'Bump Bonding Map'
        self.ResultData['Plot']['ImageFile'] = self.GetPlotFileName()

