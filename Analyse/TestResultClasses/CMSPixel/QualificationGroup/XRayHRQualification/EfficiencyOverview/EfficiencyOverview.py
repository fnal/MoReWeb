import ROOT
import AbstractClasses
from FPIXUtils.moduleSummaryPlottingTools import *


class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_XRayHRQualification_EfficiencyOverview_TestResult'
        self.NameSingle='EfficiencyOverview'
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'

    def PopulateResultData(self):
        plots = [None] * 16
        hitMin = 50
        xBins = 8 * self.nCols + 1
        yBins = 2 * self.nRows + 1
        self.ResultData['Plot']['ROOTObject'] = ROOT.TH2D(self.GetUniqueID(), "", xBins, 0., xBins, yBins, 0., yBins)

        for i in self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResults']:
            ChipTestResultObject = self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResults'][i]
            histo = ChipTestResultObject.ResultData['SubTestResults']['EfficiencyMap_{Rate}'.format(Rate=self.Attributes['Rate'])].ResultData['Plot']['ROOTObject']
            if not histo:
                print 'cannot get', 'EfficiencyMap_{Rate}'.format(Rate=self.Attributes['Rate']), 'histo for chip ',ChipTestResultObject.Attributes['ChipNo']
                continue
            chipNo = ChipTestResultObject.Attributes['ChipNo']
            histoName = 'EfficiencyMap_%s' %self.Attributes['Rate'] + '_Summary%s'  %chipNo
            histo.SetName(histoName)
            plots[chipNo] = histo
            
            for col in range(self.nCols):
                for row in range(self.nRows):
                    if histo.GetBinContent(col + 1, row + 1) < hitMin:
                      hitMin = histo.GetBinContent(col + 1, row + 1)
                    result = histo.GetBinContent(col + 1, row + 1)
                    self.UpdatePlot(chipNo, col, row, result)
        lowRange = hitMin - 1
        summaryPlot = makeMergedPlot(plots)
#        zRange = findZRange(plots)
        setZRange(summaryPlot,[lowRange,50]) # don't ask me why...
        self.Canvas = setupSummaryCanvas(summaryPlot)

        self.ResultData['Plot']['Format'] = 'png'
        self.Title = 'HR Efficiency Map {Rate}'.format(Rate=self.Attributes['Rate'])
        self.SaveCanvas()


    def UpdatePlot(self, chipNo, col, row, value):
        result = value
        if chipNo < 8:
            tmpCol = 8 * self.nCols - 1 - chipNo * self.nCols - col
            tmpRow = 2 * self.nRows - 1 - row
        else:
            tmpCol = (chipNo % 8 * self.nCols + col)
            tmpRow = row
        # Get the data from the chip sub test result hitmap

        if result and self.verbose:
            print chipNo, col, row, '--->', tmpCol, tmpRow, result
        self.ResultData['Plot']['ROOTObject'].Fill(tmpCol, tmpRow, result)
