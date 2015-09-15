# -*- coding: utf-8 -*-
import ROOT
import AbstractClasses.Helper.HistoGetter as HistoGetter
from AbstractClasses.GeneralTestResult import GeneralTestResult
import os

class TestResult(GeneralTestResult):
    def CustomInit(self):
        self.Name = 'CMSPixel_QualificationGroup_PurdueTest_Chips_Chip_TrimBits_TestResult'
        self.NameSingle = 'TrimBits'
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_PurdueTest_ROC'
        Directory = self.RawTestSessionDataPath
        for i in ['']+range(10,100,10):
        		TrimParametersFileName = "{Directory}/TrimParameters{TrimValue}_C{ChipNo}.dat".format(Directory=Directory,ChipNo=self.ParentObject.Attributes['ChipNo'],TrimValue=str(i))
        		if os.path.isfile(TrimParametersFileName):
        	        	        	TrimParametersFile = open(TrimParametersFileName, "r")
        	        	        	if TrimParametersFile:
        	        	        		self.ResultData['SubTestResultDictList'] += [
        	        	        		{
        	        	        			'Key':'TrimBitParameters'+str(i),
        	        	        			'Module': 'TrimBitParameters',
        	        	        			'InitialAttributes': {
        	        	        				'TrimParametersFile':TrimParametersFile,
        	        	        				'TrimBitValue':str(i)
        	        	        			},
        	        	        		},
        	        	        	]


    def PopulateResultData(self):
        ROOT.gStyle.SetOptStat(0)
        # self.ResultData['Plot']['ROOTObject'] =  ROOT.TH2D(self.GetUniqueID(), "", self.nCols, 0., self.nCols, self.nRows, 0., self.nRows ) # htm
        # TH2D

        ChipNo = self.ParentObject.Attributes['ChipNo']
        HistoDict = self.ParentObject.ParentObject.ParentObject.HistoDict
        if HistoDict.has_option(self.NameSingle, 'TrimBits'):
            histname = HistoDict.get(self.NameSingle, 'TrimBits')
            root_object = HistoGetter.get_histo(self.ParentObject.ParentObject.FileHandle, histname, rocNo=ChipNo)
            self.ResultData['Plot']['ROOTObject'] = root_object.Clone(self.GetUniqueID())
        else:
            histname = HistoDict.get(self.NameSingle, 'TrimBitMap')
            root_object = HistoGetter.get_histo(self.ParentObject.ParentObject.FileHandle, histname, rocNo=ChipNo)
            self.ResultData['Plot']['ROOTObject'] = ROOT.TH1F(self.GetUniqueID(), 'TrimBitDistribution', 17, -.5, 16.5)
            for col in range(self.nCols):  # Columns
                for row in range(self.nRows):  # Rows
                    entry = root_object.GetBinContent(col + 1, row + 1)
                    self.ResultData['Plot']['ROOTObject'].Fill(entry)
        mean = 0
        rms = 0

        if self.ResultData['Plot']['ROOTObject']:
            # for i in range(self.nCols): # Columns
            #    for j in range(self.nRows): # Rows
            #        self.ResultData['Plot']['ROOTObject'].SetBinContent(i+1, j+1, self.ResultData['Plot']['ROOTObject_TrimMap'].GetBinContent(i+1, j+1))

            self.ResultData['Plot']['ROOTObject'].SetTitle("")
            self.ResultData['Plot']['ROOTObject'].SetFillStyle(3002)
            self.ResultData['Plot']['ROOTObject'].SetLineColor(ROOT.kBlack)
            #self.ResultData['Plot']['ROOTObject'].GetZaxis().SetRangeUser(0., self.nTotalChips);
            self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("Trim bits")
            self.ResultData['Plot']['ROOTObject'].GetXaxis().SetRangeUser(0, 15)

            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle("entries")
            #            self.ResultData['Plot']['ROOTObject'].GetXaxis().SetTitle("Column No.");
            #            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitle("Row No.");
            self.ResultData['Plot']['ROOTObject'].GetXaxis().CenterTitle()
            self.ResultData['Plot']['ROOTObject'].GetYaxis().SetTitleOffset(1.5)
            self.ResultData['Plot']['ROOTObject'].GetYaxis().CenterTitle()
            self.ResultData['Plot']['ROOTObject'].Draw('')
            mean = self.ResultData['Plot']['ROOTObject'].GetMean()
            rms = self.ResultData['Plot']['ROOTObject'].GetRMS()
        self.ResultData['KeyValueDictPairs'] = {
            'mu': {
                'Value': '{0:1.2f}'.format(mean),
                'Label': 'μ'
            },
            'sigma': {
                'Value': '{0:1.2f}'.format(rms),
                'Label': 'σ'
            }
        }
        self.ResultData['KeyList'] = ['mu', 'sigma']

        if self.SavePlotFile:
            self.Canvas.SaveAs(self.GetPlotFileName())
        self.ResultData['Plot']['Enabled'] = 1
        self.Title = 'Trim Bits'
        self.ResultData['Plot']['ImageFile'] = self.GetPlotFileName()
