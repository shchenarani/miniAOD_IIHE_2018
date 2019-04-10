# In order to run the code for MC/DATA on lxplus
#[cmsRun IIHE.py grid=False DataProcessing="mc2016" DataFormat="mc" dataset="RunIISummer16MiniAODv2" sample="ST_tW_top_5f_NoFullyHadronicDecays_13TeV-powheg_TuneCUETP8M1" address="MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/120000" file="0E4CD60A-0FC3-E611-BCB5-0CC47A7C3420.root"  ]
#root://eoscms//cms/store/mc/RunIISummer16MiniAODv2/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/50000/36CDAE89-B3BE-E611-B022-0025905B8604.root

# In order to run the code for DATA on lxplus
#[cmsRun IIHE.py grid=False DataProcessing="rerecodata" DataFormat="data" dataset="Run2016D" sample="DoubleEG" address="MINIAOD/03Feb2017-v1/100000" file="CC7F39AC-F5EA-E611-A125-0CC47A13CDB0.root"  ]
#root://eoscms//cms/store/data/Run2015D/DoubleEG/MINIAOD/16Dec2015-v2/00000/F6E918C9-87A6-E511-B3D3-0CC47A4D76B2.root

import sys
import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as opts
import copy
import os
from os import environ


options = opts.VarParsing ("analysis")
options.register("sample",
                 "ST_tW_top_5f_NoFullyHadronicDecays_13TeV-powheg_TuneCUETP8M1", 
                 opts.VarParsing.multiplicity.singleton,
                 opts.VarParsing.varType.string,
                 "Sample to analyze")
options.register("address",
                 "MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/120000",
                 opts.VarParsing.multiplicity.singleton,
                 opts.VarParsing.varType.string,
                 "address of sample in eos like: MINIAODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/120000")
options.register("file",
                 "0E4CD60A-0FC3-E611-BCB5-0CC47A7C3420.root",
                 opts.VarParsing.multiplicity.singleton,
                 opts.VarParsing.varType.string,
                 "file to analyze")
options.register("DataProcessing",
                 "mc2017",
                 opts.VarParsing.multiplicity.singleton,
                 opts.VarParsing.varType.string,
                 "Data processing types. Options are:mc2016,rerecodata,promptdata")
options.register("dataset",
                 "RunIISummer16MiniAODv2",
                 opts.VarParsing.multiplicity.singleton,
                 opts.VarParsing.varType.string,
                 "datasets to analyze: RunIISummer16MiniAODv2, Run2016B-H")
options.register("DataFormat",
                 "mc",
                 opts.VarParsing.multiplicity.singleton,
                 opts.VarParsing.varType.string,
                 "Data format. Options are:mc,data")
options.register('grid',
                 True,
                 opts.VarParsing.multiplicity.singleton,
                 opts.VarParsing.varType.bool,
                 'If you run on grid or localy on eos')
options.parseArguments()

###########################################################################################
#os.system('wget https://github.com/rgoldouz/miniAOD_IIHE/archive/CMSSW_8_0_26_patch1.zip')
#os.system("unzip -a " + "CMSSW_8_0_26_patch1.zip" )
#os.system("mv " + "miniAOD_IIHE-CMSSW_8_0_26_patch1/data" + " ..")
#os.system("rm -rf CMSSW_8_0_26_patch1.zip miniAOD_IIHE-CMSSW_8_0_26_patch1")
##########################################################################################
#                                      Global tags                                       #
##########################################################################################
globalTag = "80"

if options.DataProcessing == "data2016":
  globalTag = "94X_dataRun2_v10"
if options.DataProcessing == "mc2016":
  globalTag = "94X_mcRun2_asymptotic_v3"

if options.DataProcessing == "data2017":
  globalTag = "94X_dataRun2_v11"
if options.DataProcessing == "mc2017":
  globalTag = "94X_mc2017_realistic_v17"

if options.DataProcessing == "data2018":
  globalTag = "102X_dataRun2_Sep2018Rereco_v1"
if options.DataProcessing == "mc2018":
  globalTag = "102X_upgrade2018_realistic_v12"
##########################################################################################
#                                  Start the sequences                                   #
##########################################################################################

process = cms.Process("IIHEAnalysis")

process.load("Configuration.StandardSequences.MagneticField_cff")
process.load("Configuration.Geometry.GeometryIdeal_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff")
process.load("FWCore.MessageService.MessageLogger_cfi")
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.load('Configuration.StandardSequences.Services_cff')

process.GlobalTag.globaltag = globalTag
print "Global Tag is ", process.GlobalTag.globaltag
#process.options = cms.untracked.PSet( allowUnscheduled = cms.untracked.bool(True) )
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100) )
process.MessageLogger.cerr.FwkReport.reportEvery = 1000
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )
##########################################################################################
#                                         Files                                          #
##########################################################################################
if options.DataFormat == "mc":
  path = "root://eoscms//eos/cms/store/"+ options.DataFormat + "/" + options.dataset  + "/" + options.sample + "/" + options.address + "/" + options.file

if options.DataFormat == "data":
  path = "root://eoscms//eos/cms/store/"+ options.DataFormat + "/" + options.dataset  + "/" + options.sample + "/" + options.address + "/" + options.file

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(),
#    eventsToProcess = cms.untracked.VEventRange('1:19792:3958249')
#    skipEvents=cms.untracked.uint32(17000)
)
#process.source.fileNames.append( "file:EGamma_Run2018C_17Sep2018_numEvent100.root" )
process.source.fileNames.append( "/store/data/Run2018A/EGamma/MINIAOD/17Sep2018-v2/270000/A3480122-01D1-3840-8E8E-E1B44ACE74E5.root")###
filename_out = "outfile.root"
if options.DataFormat == "mc" and not options.grid:
#  filename_out = "file:/tmp/output_%s" % (options.sample + "_" + options.file)
  filename_out = "outfile_MC.root"
if options.DataFormat == "data" and not options.grid:
  filename_out = "outfile_Data.root"

#filename_out = "outfile.root"
#process.out = cms.OutputModule("PoolOutputModule", fileName = cms.untracked.string(filename_out) )
process.TFileService = cms.Service("TFileService", fileName = cms.string(filename_out) )


##########################################################################################
#                                   NEW tau id disc.                                     #
##########################################################################################
from UserCode.IIHETree.runTauIdMVA import *
na = TauIDEmbedder(process, cms,
    debug=True,
    toKeep = ["2017v1", "2017v2", "newDM2017v2", "dR0p32017v2", "2016v1", "newDM2016v1"]
)
na.runTauID()

##########################################################################################
#                                  Jet Energy corrections.                               #
##########################################################################################

datadir = "%s/src/UserCode/IIHETree/test/data/" % environ['CMSSW_BASE']
jesdata = "0"
#from https://github.com/cms-jet/JRDatabase/tree/master/SQLiteFiles
jerdata = "0"
sampletorun='0'
if "2018" in options.DataProcessing:
    if "mc" in options.DataProcessing:
        jesdata = "JES_Autumn18_V8_MC"
        jerdata = "JER_Autumn18_V1_MC"
        sampletorun = "MC"
    else:
        jesdata = "JES_Autumn18_RunABCD_V8_DATA"
        jerdata = "JER_Autumn18_V1_DATA"
        sampletorun = "DATA"
    print "we are reading JEC from %s" % jesdata
    print "we are reading JER from %s" % jerdata


##### JES ####
    from CondCore.DBCommon.CondDBSetup_cfi import CondDBSetup
    process.jec = cms.ESSource('PoolDBESSource',
        CondDBSetup,
        connect = cms.string("sqlite_file:"+datadir+jesdata+".db"),
        toGet = cms.VPSet(
            cms.PSet(
                record = cms.string('JetCorrectionsRecord'),
                tag    = cms.string("JetCorrectorParametersCollection_"+jesdata[4:]+"_AK4PFchs"),
                label  = cms.untracked.string('AK4PFchs')
            )
        )
    )
# Add an ESPrefer to override JEC that might be available from the global tag
    process.es_prefer_jec = cms.ESPrefer('PoolDBESSource', 'jec')

##### JER ####
    process.load("JetMETCorrections.Modules.JetResolutionESProducer_cfi")
    process.jer = cms.ESSource("PoolDBESSource",
                               CondDBSetup,
                               toGet = cms.VPSet(
        # Resolution
        cms.PSet(
          record = cms.string('JetResolutionRcd'),
          tag    = cms.string('JR_Autumn18_V1_'+sampletorun+'_PtResolution_AK4PFchs'),
          label  = cms.untracked.string('AK4PFchs_pt')
          ),
        
        # Scale factors
        cms.PSet(
          record = cms.string('JetResolutionScaleFactorRcd'),
          tag    = cms.string('JR_Autumn18_V1_'+sampletorun+'_SF_AK4PFchs'),          
          label  = cms.untracked.string('AK4PFchs')
          ),
        ),
                               connect = cms.string("sqlite_file:"+datadir+jerdata+".db") 
                               )
    process.es_prefer_jer = cms.ESPrefer('PoolDBESSource', 'jer')


from PhysicsTools.PatAlgos.tools.jetTools import updateJetCollection

updateJetCollection(
   process,
   jetSource = cms.InputTag('slimmedJets'),
   labelName = 'UpdatedJEC',
   jetCorrections = ('AK4PFchs', cms.vstring(['L1FastJet', 'L2Relative', 'L3Absolute', 'L2L3Residual']), 'None')  # Update: Safe to always add 'L2L3Residual' as MC contains dummy L2L3Residual corrections (always set to 1)
)


##########################################################################################
#                                   2018 electron scale smearing                         #
##########################################################################################
from RecoEgamma.EgammaTools.EgammaPostRecoTools import setupEgammaPostRecoSeq
setupEgammaPostRecoSeq(process,
                       era='2018-Prompt')  


##########################################################################################
#                                   2018 MET corrections                                 #
##########################################################################################
from PhysicsTools.PatUtils.tools.runMETCorrectionsAndUncertainties import runMetCorAndUncFromMiniAOD
runMetCorAndUncFromMiniAOD(process,
                           isData="data" in options.DataProcessing,
)

##########################################################################################
#                            MY analysis input!                              ####
##########################################################################################
process.load("UserCode.IIHETree.IIHETree_cfi")
process.IIHEAnalysis.globalTag = cms.string(globalTag)
process.IIHEAnalysis.isData  = cms.untracked.bool("data" in options.DataProcessing)
process.IIHEAnalysis.isMC    = cms.untracked.bool("mc" in options.DataProcessing)
#****Collections added before the analysis
process.IIHEAnalysis.particleFlowEGammaGSFixedCollection         = cms.InputTag("particleFlowEGammaGSFixed", "dupECALClusters"              )
process.IIHEAnalysis.ecalMultiAndGSGlobalRecHitEBCollection      = cms.InputTag("ecalMultiAndGSGlobalRecHitEB","dupESClusters"        ,"PAT")
process.IIHEAnalysis.METsMuEGCleanCollection                     = cms.InputTag("slimmedMETsMuEGClean"                                      )
process.IIHEAnalysis.discardedMuonCollection                     = cms.InputTag("packedPFCandidatesDiscarded"                               )


#jet smeared collection
#process.IIHEAnalysis.JetCollection                   = cms.InputTag("updatedPatJetsUpdatedJEC")
#process.IIHEAnalysis.JetCollectionSmeared            = cms.InputTag("patSmearedJets"               ,"","IIHEAnalysis")
#process.IIHEAnalysis.JetCollectionEnUp               = cms.InputTag("shiftedPatJetEnUp"            ,"","IIHEAnalysis")
#process.IIHEAnalysis.JetCollectionEnDown             = cms.InputTag("shiftedPatJetEnDown"          ,"","IIHEAnalysis")
#process.IIHEAnalysis.JetCollectionSmearedJetResUp    = cms.InputTag("shiftedPatSmearedJetResUp"    ,"","IIHEAnalysis")
#process.IIHEAnalysis.JetCollectionSmearedJetResDown  = cms.InputTag("shiftedPatSmearedJetResDown"  ,"","IIHEAnalysis")

#MET collections
process.IIHEAnalysis.patPFMetCollection                        = cms.InputTag("patPFMet"                  , ""                ,"IIHEAnalysis"  )
process.IIHEAnalysis.patPFMetT1Collection                      = cms.InputTag("patPFMetT1"                , ""                ,"IIHEAnalysis"  )
process.IIHEAnalysis.patPFMetT1JetEnDownCollection             = cms.InputTag("patPFMetT1JetEnDown"       , ""                ,"IIHEAnalysis"  )
process.IIHEAnalysis.patPFMetT1JetEnUpCollection               = cms.InputTag("patPFMetT1JetEnUp"         , ""                ,"IIHEAnalysis"  )
process.IIHEAnalysis.patPFMetT1SmearCollection                 = cms.InputTag("patPFMetT1Smear"           , ""                ,"IIHEAnalysis"  )
process.IIHEAnalysis.patPFMetT1SmearJetEnDownCollection        = cms.InputTag("patPFMetT1SmearJetEnDown"  , ""                ,"IIHEAnalysis"  )
process.IIHEAnalysis.patPFMetT1SmearJetEnUpCollection          = cms.InputTag("patPFMetT1SmearJetEnUp"    , ""                ,"IIHEAnalysis"  )
process.IIHEAnalysis.patPFMetT1SmearJetResDownCollection       = cms.InputTag("patPFMetT1SmearJetResDown" , ""                ,"IIHEAnalysis"  )
process.IIHEAnalysis.patPFMetT1SmearJetResUpCollection         = cms.InputTag("patPFMetT1SmearJetResUp"   , ""                ,"IIHEAnalysis"  )
process.IIHEAnalysis.patPFMetT1TxyCollection                   = cms.InputTag("patPFMetT1Txy"             , ""                ,"IIHEAnalysis"  )
process.IIHEAnalysis.patPFMetFinalCollection                   = cms.InputTag("slimmedMETs"               , ""                ,"IIHEAnalysis"  )

#particle level fiducial collections
process.IIHEAnalysis.particleLevelJetsCollection               = cms.InputTag("pseudoTop"       , "jets"     ,"IIHEAnalysis"  )
process.IIHEAnalysis.particleLevelak1DressedLeptonCollection   = cms.InputTag("pseudoTop"       , "leptons"  ,"IIHEAnalysis"  )
process.IIHEAnalysis.particleLevelMETCollection                = cms.InputTag("pseudoTop"       , "mets","IIHEAnalysis"  )

process.IIHEAnalysis.electronCollection                        = cms.InputTag("slimmedElectrons"          , ""                ,"IIHEAnalysis"  )

process.IIHEAnalysis.includeLeptonsAcceptModule  = cms.untracked.bool(True)
process.IIHEAnalysis.includeTriggerModule        = cms.untracked.bool(True)
process.IIHEAnalysis.includeEventModule          = cms.untracked.bool(True)
process.IIHEAnalysis.includeVertexModule         = cms.untracked.bool(True)
process.IIHEAnalysis.includeElectronModule       = cms.untracked.bool(True)
process.IIHEAnalysis.includeMuonModule           = cms.untracked.bool(True)
process.IIHEAnalysis.includeMETModule            = cms.untracked.bool(True)
process.IIHEAnalysis.includeJetModule            = cms.untracked.bool(True)
process.IIHEAnalysis.includeTauModule            = cms.untracked.bool(True)
#process.IIHEAnalysis.includeL1Module            = cms.untracked.bool(True)
process.IIHEAnalysis.includeMCTruthModule        = cms.untracked.bool("mc" in options.DataProcessing)
process.IIHEAnalysis.includeLHEWeightModule        = cms.untracked.bool("mc" in options.DataProcessing)
#process.IIHEAnalysis.includeDataModule            = cms.untracked.bool("data" in options.DataProcessing)


#process.IIHEAnalysis.includeAutoAcceptEventModule                = cms.untracked.bool(True)
##########################################################################################
#                            Woohoo!  We"re ready to start!                              #
##########################################################################################

process.p1 = cms.Path(
    process.egammaPostRecoSeq *
    process.rerunMvaIsolationSequence *
    process.NewTauIDsEmbedded * 
    process.patJetCorrFactorsUpdatedJEC * 
    process.updatedPatJetsUpdatedJEC *
    process.fullPatMetSequence *
    process.IIHEAnalysis
    )

process.out = cms.OutputModule(
    "PoolOutputModule",
    fileName = cms.untracked.string("EDM.root")
    )

process.outpath = cms.EndPath(process.out)
#
