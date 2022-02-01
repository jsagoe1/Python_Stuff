import os
import shutil
import gzip
import time

class PathError(Exception):
   pass

class MinMaxError(Exception):
   pass

def checkPathExists(path):
   if not os.path.exists(path):
      raise PathError("{} does not exist".format(path))


class Workarea:
   def __init__(self, full_path, cbb_name=None):
      checkPathExists(full_path)
      if not cbb_name:
         raise MissingArgumentError("Argument 'cbb_name' is missing. Please provide a cbb block name")
      self._path      = full_path
      self._primeroot = self._path + "/primetime"
      self._outputdir = self._primeroot + "/bucketlist/"
      self._minreplist= self._outputdir + "/min_reports_list.txt"
      self._maxreplist= self._outputdir + "/max_reports_list.txt"
      self._cbb = cbb_name
      print("Script initiated with WARD '{}' for the block '{}'".format(self._path, self._cbb))
     
   def getOutputDir(self):
      return self._outputdir.strip()
      
   def getAllCorners(self):
      checkPathExists(self._primeroot)
      # get all corners names from this level
      corners = []
      for i in os.listdir(self._primeroot):
         if i.startswith("analysis_"):
            corner = i[9:]
            corners.append(corner)
      return corners

   def setUpOutputs(self):
      if not os.path.exists(self._outputdir):
         # create cornerlist, logfile, report_combined to be used later in the flow
         os.mkdir(self._outputdir)
      if os.path.exists(self._minreplist):
         os.remove(self._minreplist)
      if os.path.exists(self._maxreplist):
         os.remove(self._maxreplist)

      with open(self._minreplist, "a") as f:
         pass
      with open(self._maxreplist, "a") as f:
         pass
      print("Setting up output directories and output files")

   def createReportList(self):
      min_corners = [i for i in self.getAllCorners() if i.startswith("min")]
      max_corners = [i for i in self.getAllCorners() if i.startswith("max")]
      print("{} corners found in WARD".format(len(self.getAllCorners())))
      with open(self._minreplist, "a") as f:
         for i in min_corners:
            repfile = self._primeroot+"/analysis_{}/reports/{}.{}.report_timing.min.gz".format(i, self._cbb, i)
            f.write(repfile+"\n")
      with open(self._maxreplist, "a") as f:
         for i in max_corners:
            repfile = self._primeroot+"/analysis_{}/reports/{}.{}.report_timing.max.gz".format(i, self._cbb, i)
            f.write(repfile+"\n")
      print("Populating report files with timing reports from WARD")

   def getViolations(self, vtype=None):
      if vtype is not None:
         if vtype.strip() != "max" and vtype.strip() != "min":
            raise MinMaxError("please enter 'min' or 'max'")
            
      min_violations = []
      max_violations = []
      violations = []
      with open(self._minreplist, "r") as f:
         for i in f:
            report = Timingreport(i)
            vbundle = report.getViolations()
            min_violations.append(vbundle)
      with open(self._maxreplist, "r") as f:
         for i in f:
            report = Timingreport(i)
            vbundle = report.getViolations()
            max_violations.append(vbundle)

      if vtype is None:
         violations = min_violations + max_violations
      else:
         if vtype.strip() == "min":
            violations = min_violations
         if vtype.strip() == "max":
            violations = max_violations
      
      print("Collecting violations from timing reports")
      return violations


class Timingreport:
   def __init__(self, path):
      checkPathExists(path.strip())
      self._path = path.strip()
      self._corner = self.getCorner()

   def getCorner(self):
      pivot = self._path.find("analysis")
      end = self._path.find("/reports/")
      return self._path[pivot+9:end]

   def getViolations(self):
      with gzip.open(self._path, "r") as repfile:
         lines = [line.decode('utf-8') for line in repfile]
         # check if report file has no violations         
         if lines[0].strip() == "# No paths found":
            return (self._corner, [], self._path)

         # get src, dest, slack, srcclock and destclk for violations
         violations = []
         startpoints = []
         endpoints = []
         src_clks = []
         dest_clks = []
         slacks_derate = []
         slacks_noderate = []
         for i in range(len(lines)):
            # get startpoint
            if lines[i].strip().startswith("Startpoint"):
               startpoint = lines[i].strip().split(":")[-1].strip()
               # get src clk
               srcclkline = lines[i+1]
               srcclk = srcclkline.strip().split(" ")[-1][:-1]
               if srcclk[-1] == "'":
                  srcclk = srcclk[:-1]
               startpoints.append(startpoint)
               src_clks.append(srcclk)

            # get destination
            if lines[i].strip().startswith("Endpoint"):
               endpoint = lines[i].strip().split(":")[-1].strip()
               # get dest clk
               destclkline = lines[i+1]
               destclk = destclkline.strip().split(" ")[-1][:-1]
               if destclk[-1] == "'":
                  destclk = destclk[:-1]
               endpoints.append(endpoint)
               dest_clks.append(destclk)

            # get derate slack
            lookup1, lookup2 = "slack (VIOLATED", "slack (MET"
            if lines[i].strip().startswith(lookup1.strip()) or lines[i].strip().startswith(lookup2.strip()):
               slackline = lines[i].strip()
               slack = slackline.split()[-1]
               slacks_derate.append(slack)
               
            # get noderate slack
            lookup = "slack (with no derating)"
            if lines[i].strip().startswith(lookup):
               slackline = lines[i].strip()
               slack = slackline.split()[-1]
               slacks_noderate.append(slack)

         # build violation objects
         for i in range(len(startpoints)):
            
            violation_obj = Violation(startpoints[i], endpoints[i], slacks_derate[i], slacks_noderate[i], src_clks[i], dest_clks[i])
            violations.append(violation_obj)

         # return violations bundle
         return (self._corner, violations, self._path)

         
class Violation:
   def __init__(self, src, dest, slack_derate, slack_noderate, src_clk, dest_clk):
      self._src = src
      self._dest = dest
      self._slackderate = slack_derate
      self._slacknoderate = slack_noderate
      self._srcclk = src_clk
      self._destclk = dest_clk

   def getSource(self):
      return self._src

   def getDest(self):
      return self._dest

   def getSlackDerate(self):
      return self._slackderate

   def getSlackNoDerate(self):
      return self._slacknoderate

   def getSrcClk(self):
      return self._srcclk

   def getDestClk(self):
      return self._destclk
   

class Monitor:
   def __init__(self, violations=None):
      if not violations:
         self._violations = []
      self._violations = violations

   def isEmpty(self):
      total = 0
      for corner, group, path in self._violations:
         total += len(group)
      return total == 0

   def _printHelper(self, sumFile):
      with open(sumFile, 'a') as f:
         f.write("VIOLATIONS SUMMARY\n\n")

         if self.isEmpty():
            f.write("There are no violations !\n")
            return
         
         for corner, group, path in self._violations:
            if len(group) > 0:
               f.write("{:<60} {:<40} {:<60} {:<40} {:<20} {:<20}".format("startpoint", "start_clk", "endpoint", "end_clk", "slack(derate)", "slack(noderate)\n"))
               f.write("-"*240 + "\n")

               for violation in group:
                  src, dest = violation.getSource(), violation.getDest()
                  srcclk, destclk = violation.getSrcClk(), violation.getDestClk()
                  slackderate, slacknoderate = violation.getSlackDerate(), violation.getSlackNoDerate()
            
                  if float(slackderate) < 0 or float(slacknoderate) < 0:
                     f.write("{:<60} {:<40} {:60} {:<40} {:<20} {:<20}\n".format(src,srcclk,dest,destclk,slackderate,slacknoderate))


               f.write('\n')
               f.write("report: {}\n".format(path))
               f.write("\n\n") 
         
   def prettyPrint(self, minmax=None):
      if minmax == None or minmax not in ['min', 'max']:
         raise MinMaxError("Please provide minmax arg")

      minSumFile = WA.getOutputDir() + "/min_violations.txt"
      maxSumFile = WA.getOutputDir() + "/max_violations.txt"
      
      if minmax == 'min':
         if os.path.exists(minSumFile):
            os.remove(minSumFile)
      if minmax == 'max':
         if os.path.exists(maxSumFile):
            os.remove(maxSumFile)
      
      with open(minSumFile, "a") as f:
         pass
      with open(maxSumFile, 'a') as f:
         pass
      
      time.sleep(1)
      
      if minmax == 'min':
         print("writing min timing summary file to {}".format(minSumFile))
         self._printHelper(minSumFile)
         time.sleep(1)
      if minmax == 'max':
         print("writing max timing summary file to {}".format(maxSumFile))   
         self._printHelper(maxSumFile)
         time.sleep(1)


if __name__ == "__main__":
   # process WA
   WA = Workarea(r"/nfs/site/disks/mtl_jsagoe_wa_01/n6_cbb_timing_B0/", "ljpll3p50cbb")
   WA.setUpOutputs()
   WA.createReportList()

   # process report lists to get violations

   # min_violations
   minviolations = WA.getViolations('min')
   maxviolations = WA.getViolations('max')
   
   # pass violations to monitor and display
   MinMon = Monitor(minviolations)
   MaxMon = Monitor(maxviolations)

   MinMon.prettyPrint('min')
   MaxMon.prettyPrint('max')

   print("Done !!!!!")
