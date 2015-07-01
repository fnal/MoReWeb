# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
import glob

class ProductionOverview(AbstractClasses.GeneralProductionOverview.GeneralProductionOverview):

    def CustomInit(self):
        self.NameSingle='DeadPixelOverlay'
        self.Name='CMSPixel_ProductionOverview_%s'%self.NameSingle
        self.Title = 'Dead Pixel Overlay, Test: %s Grade: %s'%(self.Attributes['Test'], self.Attributes['Grade'])
        self.DisplayOptions = {
            'Width': 2.5,
        }
        self.SubPages = []
        self.SavePlotFile = True
        self.Canvas.SetCanvasSize(1330, 430)
        self.Canvas.Update()

    def GenerateOverview(self):
        ROOT.gStyle.SetOptStat(0)

        TableData = []

        Rows = self.FetchData()

        ModuleIDsList = []
        for RowTuple in Rows:
            if not RowTuple['ModuleID'] in ModuleIDsList:
                ModuleIDsList.append(RowTuple['ModuleID'])

        nColsModule = 8 * self.nCols
        nRowsModule = 2 * self.nRows
        SummaryMap = ROOT.TH2D(self.GetUniqueID(), "", nColsModule, 0, nColsModule, nRowsModule, 0, nRowsModule)


        NModules = 0
        for ModuleID in ModuleIDsList:

            for RowTuple in Rows:
                if RowTuple['ModuleID'] == ModuleID:
                    TestType = RowTuple['TestType']
                    if TestType == self.Attributes['Test'] and (RowTuple['Grade'] == self.Attributes['Grade'] or self.Attributes['Grade'] == 'All'):
                        for Chip in range(0,16):
                            Path = '/'.join([self.GlobalOverviewPath, RowTuple['RelativeModuleFinalResultsPath'], RowTuple['FulltestSubfolder'], 'Chips' ,'Chip%s'%Chip, 'PixelMap', '*.root'])
                            RootFiles = glob.glob(Path)
                            if len(RootFiles) > 1:
                                print "WARNING: more than 1 root file found in: '%s"%Path
                            elif len(RootFiles) < 1:
                                print "WARNING: root file not found in: '%s"%Path
                            else:
                                ROOTObject = self.GetHistFromROOTFile(RootFiles[0], "PixelMap")
                                if ROOTObject:
                                    for col in range(0, self.nCols):
                                        for row in range(0, self.nRows):
                                            if ROOTObject.GetBinContent(1+col, 1+row) < 1:
                                                self.UpdatePlot(SummaryMap, Chip, col, row, 1)
                                else:
                                    print "WARNING: th2d in root file '%s' not found"%RootFiles[0]
                        
                        NModules += 1

        SummaryMap.Draw("colz")

        title = ROOT.TText()
        title.SetNDC()
        title.SetTextAlign(12)

        Subtitle = self.Attributes['Test']
        TestNames = {'m20_1' : 'Fulltest -20°C BTC', 'm20_2': 'Fulltest -20°C ATC', 'p17_1': 'Fulltest +17°C'}
        if TestNames.has_key(Subtitle):
            Subtitle = TestNames[Subtitle]
        Subtitle += ",  modules: %d, Grades: %s"%(NModules, self.Attributes['Grade'])
        title.DrawText(0.15,0.965,Subtitle)

        self.SaveCanvas()
        HTML = self.Image(self.Attributes['ImageFile']) + self.BoxFooter("Number of modules: %d"%NModules)

        AbstractClasses.GeneralProductionOverview.GeneralProductionOverview.GenerateOverview(self)
        return self.Boxed(HTML)

    def UpdatePlot(self, Plot, chipNo, col, row, value):
        result = value
        if chipNo < 8:
            tmpCol = 8 * self.nCols - 1 - chipNo * self.nCols - col
            tmpRow = 2 * self.nRows - 1 - row
        else:
            tmpCol = (chipNo % 8 * self.nCols + col)
            tmpRow = row
        Plot.Fill(tmpCol, tmpRow, result)