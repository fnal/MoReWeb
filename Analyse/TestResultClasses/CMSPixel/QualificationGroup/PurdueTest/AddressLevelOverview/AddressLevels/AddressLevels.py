import ROOT
import AbstractClasses
class TestResult(AbstractClasses.GeneralTestResult.GeneralTestResult):
    def CustomInit(self):
        self.Name='CMSPixel_QualificationGroup_PurdueTest_AddressLevelOverview_AddressLevels_TestResult'
        self.NameSingle='AddressLevels'
        self.Attributes['TestedObjectType'] = 'CMSPixel_QualificationGroup_PurdueTest_ROC'
        
        
        

        
    def PopulateResultData(self):
        ChipNo = self.Attributes['ChipNo']
        ChipAddresLevelTestResultObject = self.ParentObject.ParentObject.ResultData['SubTestResults']['Chips'].ResultData['SubTestResults']['Chip'+str(ChipNo)].ResultData['SubTestResults']['AddressLevels']
        
        self.ResultData['Plot']['Format'] = ChipAddresLevelTestResultObject.ResultData['Plot']['Format']
        
        if self.SavePlotFile:
            
            # Copy the plot file
            f = open(ChipAddresLevelTestResultObject.ResultData['Plot']['ImageFile'],'r')
            PlotContent = f.read()
            f.close()
            
            f = open(self.GetPlotFileName(),'w')
            PlotContent = f.write(PlotContent)
            f.close()
            
        self.ResultData['Plot']['Enabled'] = 1
        self.Title = 'Address Levels: C{ChipNo}'.format(ChipNo=self.Attributes['ChipNo'])
        self.ResultData['Plot']['ImageFile'] = self.GetPlotFileName()
