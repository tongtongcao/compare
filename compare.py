#!/usr/bin/python
import sys, array
import getopt
from ROOT import gPad, gROOT, TCanvas, TPad, TF1, TFile, gStyle, TFormula, TGraph, TGraphErrors, TH1D, TCutG, TH2D, gDirectory, TLegend, TColor

def setStyle():
    #gStyle.SetOptStat(01)
    gStyle.SetOptFit(000000)

def makeLegend(histList, legendStringList):
    plot1DsSuperimposed(histList)
    legend = TLegend(0.7, 0.7, 0.98, 0.95)
    for i in range(len(histList)):
        legend.AddEntry(histList[i], legendStringList[i] + " (" + str(int(histList[i].GetEntries())) + ")", 'l')
    return legend

def plot1DsSuperimposed(histList):
    histList[0]
    histList[0].Draw()
    for i in range(len(histList)):
        histList[i].SetMarkerColor(i+1)
        histList[i].SetLineColor(i+1)
        if i == 0:
            histList[i].Draw()
        else:
            histList[i].Draw("same")

def plot1DsSuperimposedWithMax(histList, max):
    histList[0]
    histList[0].Draw()
    for i in range(len(histList)):
        histList[i].SetLineColor(i+1)
        if i == 0:
            histList[i].SetMaximum(max)
            histList[i].Draw()
        else:
            histList[i].Draw("same")

def plot1DsSuperimposedWithLegend(histList, legend):
    plot1DsSuperimposed(histList)
    legend.Draw()

def plot1DsSuperimposedWithMaxLegend(histList, max, legend):
    plot1DsSuperimposedWithMax(histList, max)
    legend.Draw()

def plot1DsSuperimposedOnPad(canv, histList):
    canv.cd()
    plot1DsSuperimposed(histList)

def plot1DsSuperimposedWithMaxOnPad(canv, histList, max):
    canv.cd()
    plot1DsSuperimposedWithMax(histList, max)

def plot1DsSuperimposedWithLegendOnPad(canv, histList, legend):
    canv.cd()
    plot1DsSuperimposed(histList)
    legend.Draw()

def plot1DsSuperimposedWithMaxLegendOnPad(canv, histList, max, legend):
    canv.cd()
    plot1DsSuperimposedWithMax(histList, max)
    legend.Draw()

def plotMult2DsOnPad(canv, histList, statusLogz = False):
    canv.cd()
    numHistos = len(histList)
    nRow = 2
    nColumn = numHistos / nRow + (int)(numHistos / nRow != 0)
    canv.Divide(nRow, nColumn)
    for i in range(numHistos):
        canv.cd(i+1)
        if statusLogz == True:
            gPad.SetLogz()
        histList.Draw("colz")

def plotMult2DsWithTitleChangeOnPad(canv, histList, titleList, statusLogz = False):
    canv.cd()
    numHistos = len(histList)
    nRow = 2
    nColumn = numHistos / nRow + (int)(numHistos / nRow != 0)
    canv.Divide(nRow, nColumn)
    for i in range(numHistos):
        canv.cd(i+1)
        if statusLogz == True:
            gPad.SetLogz()
        histList[i].SetTitle(titleList[i])
        histList[i].Draw("colz")

def makePDF(pdfName, dirList, histNameList, legendEntryNameList):
    histListList = []
    for histName in histNameList:
        histList = []
        for fileDir in dirList:
            histList.append(fileDir.Get(histName))
        histListList.append(histList)

    numHistList = len(histListList)
    for i in range(numHistList):
        histName = histListList[i][0].GetName()
        canv = TCanvas(histName, histName)
        if "hh" not in histName:
            legend = makeLegend(histListList[i], legendEntryNameList)
            maxList = []
            for hist in histListList[i]:
                maxList.append(hist.GetMaximum())
            maxmax = max(maxList)
            plot1DsSuperimposedWithMaxLegendOnPad(canv, histListList[i], maxmax, legend)
            if i == 0:
                canv.Print(pdfName + ".pdf(")
            elif i == numHistList - 1:
                canv.Print(pdfName + ".pdf)")
            else:
                canv.Print(pdfName + ".pdf")
        else:
            plotMult2DsWithTitleChangeOnPad(canv, histListList[i], legendEntryNameList)
            if i == 0:
                canv.Print(pdfName + ".pdf(")
            elif i == numHistList - 1:
                canv.Print(pdfName + ".pdf)")
            else:
                canv.Print(pdfName + ".pdf")

if __name__=='__main__':
    options, remainder = getopt.gnu_getopt(sys.argv[1:], 'h', ['help',])
    print remainder
    for opt, arg in options:
        if opt in ('-h', '--help'):
            print "\nUsage: "+sys.argv[0]+" <output basename> <root files>"
            print "Arguments: "
            print "\n"
            sys.exit(0)

    setStyle()

    legendEntryNameList = ["Pure tritrig", "Tritrig_beam", "Tritrg_pulser", "physicsRun"]

    fileList = []
    for fileName in remainder:
        fileList.append(TFile(fileName))

    dirListRecoEcal = []
    dirListRecoTrack = []
    for file in fileList:
        dirListRecoEcal.append(file.Get("recoEcalAna"))
        dirListRecoTrack.append(file.Get("recoTrackAna"))

    histNameListRecoEcal = ["recoEcalAna_numEcalHits_h", "recoEcalAna_xyIndicesEcalHits_hh", "recoEcalAna_ecalHitEnergy_h", \
                            "recoEcalAna_numEcalClusters_h", "recoEcalAna_xyIndicesEcalSeeds_hh", "recoEcalAna_ecalSeeEnergy_h",
                            "recoEcalAna_ecalClusterNHits_h", "recoEcalAna_ecalClusterEnergy_h", "recoEcalAna_ecalClusterTime_h"]

    makePDF("recoEcal", dirListRecoEcal, histNameListRecoEcal, legendEntryNameList)

    histNameListRecoTrack = ["recoTrackAna_time_h", "recoTrackAna_chi2_h", "recoTrackAna_chi2ndf_h", \
                             "recoTrackAna_n_tracks_h", "recoTrackAna_nHits_2d_h", "recoTrackAna_strategy_h", "recoTrackAna_type_h", \
                             "recoTrackAna_nShared_h", "recoTrackAna_sharingHits_h", "recoTrackAna_p_h", "recoTrackAna_d0_h", \
                             "recoTrackAna_Phi_h", "recoTrackAna_Omega_h", "recoTrackAna_invpT_h", "recoTrackAna_pT_h", \
                             "recoTrackAna_TanLambda_h", "recoTrackAna_Z0_h", "recoTrackAna_d0_vs_p_hh", "recoTrackAna_d0_vs_phi0_hh", \
                             "recoTrackAna_d0_vs_tanlambda_hh", "recoTrackAna_z0_vs_p_hh", "recoTrackAna_z0_vs_phi0_hh", \
                             "recoTrackAna_z0_vs_tanlambda_hh", "recoTrackAna_phi0_vs_p_hh", "recoTrackAna_tanlambda_vs_phi0_hh"]

    makePDF("recoTrack", dirListRecoTrack, histNameListRecoTrack, legendEntryNameList)

    histNameListRecoVertex = ["recoTrackAna_n_vertices_h", "recoTrackAna_vtx_chi2_h", "recoTrackAna_vtx_X_h", "recoTrackAna_vtx_Y_h", \
                              "recoTrackAna_vtx_Z_h", "recoTrackAna_vtx_sigma_X_h", "recoTrackAna_vtx_sigma_Y_h", "recoTrackAna_vtx_sigma_Z_h", \
                              "recoTrackAna_vtx_InvM_h", "recoTrackAna_vtx_InvMErr_Z_h", "recoTrackAna_vtx_px_h", \
                              "recoTrackAna_vtx_py_h", "recoTrackAna_vtx_pz_h", "recoTrackAna_vtx_p_h", "recoTrackAna_vtx_InvM_vtx_z_hh", \
                              "recoTrackAna_vtx_XY_hh", "recoTrackAna_vtx_p_sigmaX_hh", "recoTrackAna_vtx_p_sigmaY_hh", "recoTrackAna_vtx_p_sigmaZ_hh"]

    makePDF("recoVertex", dirListRecoTrack, histNameListRecoVertex, legendEntryNameList)


