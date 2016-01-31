import ROOT
import AbstractClasses

class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_XRayHRQualification_HitOverview_TestResult'
        self.NameSingle='HitOverview'
        self.Attributes['TestedObjectType'] = 'CMSPixel_Module'

    def PopulateResultData(self):
        self.Canvas.Clear()
        ROOT.gPad.SetLogy(1)
        ROOT.gPad.SetLogx(1)
        ROOT.gStyle.SetOptStat(0)

        xBins = 8 * self.nCols + 1
        yBins = 2 * self.nRows + 1
        HitMapOverview = ROOT.TH2D(self.GetUniqueID(), "", xBins, 0., xBins, yBins, 0., yBins)

        # copy ROC data to module data
        for i in self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResults']:
            ChipTestResultObject = self.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResults'][i]
            histo = ChipTestResultObject.ResultData['SubTestResults']['HitMap_{Rate}'.format(Rate=self.Attributes['Rate'])].ResultData['Plot']['ROOTObject']
            if not histo:
                print 'cannot get', 'HitMap_{Rate}'.format(Rate=self.Attributes['Rate']), 'histo for chip ',ChipTestResultObject.Attributes['ChipNo']
                continue
            chipNo = ChipTestResultObject.Attributes['ChipNo']

            for col in range(self.nCols):
                for row in range(self.nRows):
                    result = histo.GetBinContent(col + 1, row + 1)
                    self.UpdatePlot(HitMapOverview, chipNo, col, row, result)

        HitMapOverview.GetZaxis().SetRangeUser(0, HitMapOverview.GetMaximum())
        self.ResultData['Plot']['ROOTObject'] = ROOT.TH1D(self.GetUniqueID(), "", int((HitMapOverview.GetMaximum()*1.05-HitMapOverview.GetMinimum()) / 100), float(HitMapOverview.GetMinimum()), float(HitMapOverview.GetMaximum()*1.05))
        GraphEdges = ROOT.TH1D(self.GetUniqueID(), "", int((HitMapOverview.GetMaximum()*1.05-HitMapOverview.GetMinimum()) / 100), float(HitMapOverview.GetMinimum()), float(HitMapOverview.GetMaximum()*1.05))
        GraphCorners = ROOT.TH1D(self.GetUniqueID(), "", int((HitMapOverview.GetMaximum()*1.05-HitMapOverview.GetMinimum()) / 100), float(HitMapOverview.GetMinimum()), float(HitMapOverview.GetMaximum()*1.05))


        for col in range(self.nCols*8):
            for row in range(self.nRows*2):
                result = HitMapOverview.GetBinContent(col + 1, row + 1)
                if (col % 52 == 0 or col % 52 == 51) and (row % 80 == 0 or row % 80 == 79):
                    GraphCorners.Fill(result)
                elif (col % 52 == 0 or col % 52 == 51) or (row % 80 == 0 or row % 80 == 79):
                    GraphEdges.Fill(result)
                else:
                    self.ResultData['Plot']['ROOTObject'].Fill(result)


        if self.ResultData['Plot']['ROOTObject']:
            self.ResultData['Plot']['ROOTObject'].SetTitle("")
            self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("#hits")
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle("")
            self.ResultData['Plot']['ROOTObject'].GetXaxis().CenterTitle()
            self.ResultData['Plot']['ROOTObject'].SetLineColor(ROOT.kBlue)
            self.ResultData['Plot']['ROOTObject'].Draw('')

            GraphEdges.SetTitle("")
            GraphEdges.GetXaxis().SetTitle("")
            GraphEdges.GetYaxis().SetTitle("")
            GraphEdges.SetLineColor(ROOT.kGreen+2)
            GraphEdges.Draw('SAME')

            GraphCorners.SetTitle("")
            GraphCorners.GetXaxis().SetTitle("")
            GraphCorners.GetYaxis().SetTitle("")
            GraphCorners.SetLineColor(ROOT.kRed)
            GraphCorners.Draw('SAME')


        self.Title = 'Hits distribution {Rate} inner/edge/corner'.format(Rate=self.Attributes['Rate'])
        self.SaveCanvas()
        ROOT.gPad.SetLogy(0)
        ROOT.gPad.SetLogx(0)

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



