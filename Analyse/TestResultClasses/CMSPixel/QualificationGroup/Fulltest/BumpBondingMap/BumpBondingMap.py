import ROOT
import AbstractClasses
import ROOT
from FPIXUtils.moduleSummaryPlottingTools import *

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_Fulltest_Chips_Chip_BumpBondingMap_TestResult'
        self.NameSingle='BumpBondingMap'
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'

    def PopulateResultData(self):
        plots = [None] * 16
        for i in self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResults']:
            ChipTestResultObject = self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResults'][i]
            histo = ChipTestResultObject.ResultData['SubTestResults']['BumpBondingProblems'].ResultData['Plot']['ROOTObject']
            if not histo:
                print 'cannot get BumpBondingProblems histo for chip ',ChipTestResultObject.Attributes['ChipNo']
                continue
            chipNo = ChipTestResultObject.Attributes['ChipNo']
            histoName = 'rescaledThr_Summary%s' %chipNo
            histo.SetName(histoName)
            plots[chipNo] = histo

        summaryPlot = makeMergedPlot(plots)

        setZRange(summaryPlot,[-5.0,5.0])
        self.Canvas = setupSummaryCanvas(summaryPlot)

        colors = array("i",[51+i for i in range(40)] + [ROOT.kRed])
        ROOT.gStyle.SetPalette(len(colors), colors);
        zMin=summaryPlot.GetMinimum()
        zMax=summaryPlot.GetMaximum()
        step=(zMax-zMin)/(len(colors)-1)
        levels = array('d',[zMin + i*step for i in range(len(colors)-1)]+[4.9999999])
        summaryPlot.SetContour(len(levels),levels)

        self.ResultData['Plot']['Format'] = 'png'
        self.Title = 'Bump Bonding Map'
        self.SaveCanvas()
        
        # reset palette
        ROOT.gStyle.SetPalette(1)
