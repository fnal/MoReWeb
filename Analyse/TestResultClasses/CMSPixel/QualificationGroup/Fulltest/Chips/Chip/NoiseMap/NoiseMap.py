# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses
import AbstractClasses.Helper.HistoGetter as HistoGetter
import ROOT
class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.NameSingle='NoiseMap'
        self.Name='CMSPixel_QualificationGroup_Fulltest_Chips_Chip_%s_TestResult'%self.NameSingle
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_Fulltest_ROC'


    def PopulateResultData(self):

        ROOT.gPad.SetLogy(0)
        ROOT.gStyle.SetOptStat(0)
        ChipNo=self.ParentObject.Attributes['ChipNo']

        try:
            HistoDict = self.ParentObject.ParentObject.ParentObject.HistoDict
            histname = HistoDict.get(self.NameSingle, 'NoiseMap')
            NoiseMap = HistoGetter.get_histo(self.ParentObject.ParentObject.FileHandle, histname, rocNo = ChipNo)
            self.ResultData['Plot']['ROOTObject'] = NoiseMap.Clone(self.GetUniqueID())
        except:
            self.ResultData['Plot']['ROOTObject'] = None
            print 'DID NOT FIND WIDTHS'

        if self.ResultData['Plot']['ROOTObject']:
            self.ResultData['Plot']['ROOTObject'].GetZaxis().SetRangeUser(0, 10)
            self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("Column No.")
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle("Row No.")
            self.ResultData['Plot']['ROOTObject'].GetXaxis().CenterTitle()
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleOffset(1.5)
            self.ResultData['Plot']['ROOTObject'].GetYaxis().CenterTitle()
            self.ResultData['Plot']['ROOTObject'].Draw('colz')


        self.ResultData['Plot']['Caption'] = 'Noise Map (Vcal)'
        if self.Canvas:
            self.Canvas.SetCanvasSize(500, 500)
        self.ResultData['Plot']['Format'] = 'png'
        self.SaveCanvas()