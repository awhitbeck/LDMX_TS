from ts_digi_container import *
import ROOT as r

## initialize container
cont = ts_digi_container('~whitbeck/raid/LDMX/v2.2.1/three_electron_tracks.root','LDMX_Events')
cont.get_digi_collection('trigScintDigisTag_reco')
cont.get_digi_collection('trigScintDigisUp_reco')
cont.get_digi_collection('trigScintDigisDn_reco')

cont.get_cluster_collection('TriggerPadTaggerClusters_digi')
cont.get_track_collection('TriggerPadTracks_digi')

## configuration for pretty root plots
r.gROOT.ProcessLine(".L tdrstyle.C")
r.gROOT.ProcessLine("setTDRStyle()")

## initialize root histogram
hist = r.TH1F("test","Title;Photo-electrons;Events",40,0,200)
hBeamEfrac = r.TH1F("hBeamEfrac","beam fraction histo;Fraction of energy deposited by beam electrons;Clusters",101,0,1.01)
hBeamEfracTracks = r.TH1F("hBeamEfracTracks","beam fraction histo;Fraction of energy deposited by beam electrons;Tracks",101,0,1.01)

print("n",cont.tree.numentries)
## loop over events
for i in range(cont.tree.numentries-1):
    ## get list of pe for tagger array for event i
    pes=cont.get_data('trigScintDigisTag_reco','pe',i)
    for pe in pes : 
        hist.Fill(pe)
    ## get list of pe for upstream array for event i
    pes=cont.get_data('trigScintDigisUp_reco','pe',i)
    for pe in pes : 
        hist.Fill(pe)
    ## get list of pe for downstream array for event i
    pes=cont.get_data('trigScintDigisDn_reco','pe',i)
    for pe in pes : 
        hist.Fill(pe)

    beamFracC=cont.get_data('TriggerPadTaggerClusters_digi', 'beamEfrac',i)
    for frac in beamFracC : 
        hBeamEfrac.Fill(frac)
    beamFracT=cont.get_data('TriggerPadTracks_digi', 'beamEfrac',i)
    for frac in beamFracT : 
        hBeamEfracTracks.Fill(frac)


#plot!
c1 = r.TCanvas("c1", "hist canvas", 600,  500)
hist.SetFillColor(2)
hist.SetLineColor(4)
hist.SetLineStyle(2)
hist.Draw()

c1.SaveAs( hist.GetName()+".png")
hBeamEfrac.SetLineWidth(3)
hBeamEfrac.GetYaxis().SetTitle("Entries")
hBeamEfrac.Draw()
hBeamEfracTracks.SetLineWidth(3)
hBeamEfracTracks.SetLineColor(7)
hBeamEfracTracks.Draw("same")

leg=r.TLegend(0.2, 0.5, 0.5, 0.9)
leg.AddEntry(hBeamEfrac, "Tagger clusters", "L")
leg.AddEntry(hBeamEfracTracks, "Tracks", "L")
leg.Draw()
c1.SetLogy();
c1.SaveAs( hBeamEfrac.GetName()+".png")
