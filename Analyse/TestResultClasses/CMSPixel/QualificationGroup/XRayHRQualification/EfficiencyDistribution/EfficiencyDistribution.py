import ROOT
import AbstractClasses

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_XRayHRQualification_EfficiencyDistribution_TestResult'
        self.NameSingle='EfficiencyDistribution'
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'

    def PopulateResultData(self):
        self.Canvas.Clear()
        ROOT.gPad.SetLogy(1)
        ROOT.gStyle.SetOptStat(0)


        xBins = 8 * self.nCols + 1
        yBins = 2 * self.nRows + 1
        EfficiencyOverview = ROOT.TH2D(self.GetUniqueID(), "", xBins, 0., xBins, yBins, 0., yBins)

        # copy ROC data to module data
        for i in self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResults']:
            ChipTestResultObject = self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResults'][i]
            histo = ChipTestResultObject.ResultData['SubTestResults']['EfficiencyMap_{Rate}'.format(Rate=self.Attributes['Rate'])].ResultData['Plot']['ROOTObject']
            if not histo:
                print 'cannot get', 'EfficiencyMap_{Rate}'.format(Rate=self.Attributes['Rate']), 'histo for chip ',ChipTestResultObject.Attributes['ChipNo']
                continue
            chipNo = ChipTestResultObject.Attributes['ChipNo']

            for col in range(self.nCols):
                for row in range(self.nRows):
                    result = histo.GetBinContent(col + 1, row + 1)
                    self.UpdatePlot(EfficiencyOverview, chipNo, col, row, result)

        Ntrig = self.ParentObject.Attributes['Ntrig']['HREfficiency_{Rate}'.format(Rate=self.Attributes['Rate'])]
#        self.ResultData['Plot']['ROOTObject'] = ROOT.TH1D(self.GetUniqueID(), "", 100, 0, 100.01)
        self.ResultData['Plot']['ROOTObject'] = ROOT.TH1D(self.GetUniqueID(), "", 50, 0, 100.01)

        for col in range(self.nCols*8):
            for row in range(self.nRows*2):
                result = EfficiencyOverview.GetBinContent(col + 1, row + 1)
                self.ResultData['Plot']['ROOTObject'].Fill(result*100.0/Ntrig)

        if self.ResultData['Plot']['ROOTObject']:
            self.ResultData['Plot']['ROOTObject'].SetTitle("")
            self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("efficiency")
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle("")
            self.ResultData['Plot']['ROOTObject'].GetXaxis().CenterTitle()
            self.ResultData['Plot']['ROOTObject'].SetLineColor(ROOT.kBlue+2)
            self.ResultData['Plot']['ROOTObject'].Draw('')

        self.Title = 'Efficiency distribution {Rate}'.format(Rate=self.Attributes['Rate'])
        self.SaveCanvas()
        ROOT.gPad.SetLogy(0)

    def UpdatePlot(self, plot, chipNo, col, row, value):
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
        plot.Fill(tmpCol, tmpRow, result)
