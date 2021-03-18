#!/usr/bin/env python
import sys, math, ROOT

# switches
ev_max = 2

lep_ls = list()
lep_ls += [11]
lep_ls += [13]

#!### utils / histo
#!#def add_H1F(dc, name, nbin, xmin, xmax):
#!#    dc[name] = ROOT.TH1F(name, name, nbin, xmin, xmax)
#!#
#!#def get_H1F_dict():
#!#    h_ = dict()
#!#
#!#    for c in cut_ls:
#!#        add_H1F(h_, 'indv__'+c+'__gen_ttbar__M', 500, 0, 5000)
#!#        add_H1F(h_, 'cons__'+c+'__gen_ttbar__M', 500, 0, 5000)
#!#
#!#    return h_

def KILL(log):
    print '\n@@@ FATAL -- '+log
    print ' >> stopping execution\n'
    raise SystemExit

### utils
def p4(part):
    p = ROOT.TLorentzVector()
    p.SetPtEtaPhiM(part.pt, part.eta, part.phi, part.M)

    return p

### main
if __name__ == '__main__':

    if len(sys.argv)-1 != 2:
        KILL('two command-line arguments required: [1] input .root file(s), [2] output .root file')

    ROOT.gSystem.Load('$TTBSM_ENV/NtupleAnalysis/NtupleObjects/lib/libNtupleObjects.so')

    tree = ROOT.TChain('Events')
    tree.Add(sys.argv[1])

    #### hard-coded selection thresholds
    muo_pt_min  = 45.
    muo_eta_max =  2.1

    ele_pt_min  = 50.
    ele_eta_max =  2.5

    jet_pt_min  = 30.
    jet_eta_max =  2.4
    jet2_pt_min =  50.
    jet1_pt_min = 200.

    met_pt_min =  50.
    htlep_min  = 150.

    lep_2dcut = [.4, 25.]

    ####################################

    ### histograms #####################
#!#    h = get_H1F_dict()
    ####################################

    ev_done = 0
    for ev in tree:
        if (ev_max > 0) and (ev_done >= ev_max): break

        ev_done += 1
        if not ev_done%1000: print 'processing event #', ev_done
        ###

        muoN = ev.MUO.GetEntries()
        eleN = ev.ELE.GetEntries()
        if   muoN==1 and eleN==0: channel, lepton = 'muo', p4(ev.MUO.At(0))
        elif muoN==0 and eleN==1: channel, lepton = 'ele', p4(ev.ELE.At(0))

        jets = []
        for j in ev.JET_AK4:
            print j.pt
            if j.pt > jet_pt_min and abs(j.eta) < jet_eta_max:
                jets.append(p4(j))
        jets = sorted(jets, key=lambda x: x.Pt(), reverse=True)

        if len(jets) < 2: continue

        pass_jet2_pt = j[1].Pt() > jet2_pt_min

        pass_jet1_pt = j[0].Pt() > jet1_pt_min

        pass_met_pt = ev.MET.pt > met_pt_min

        pass_htlep  = ev.MET.pt+lepton.Pt() > htlep_min

#!#        print ev.lep1_CH_020_stand
#!#        print ev.lep1_NH_010_pfwgt

#        genp = ev.GenParticle
#        ttbar_lje_dc = get_index_dict_for_genttbar_ljets(genp, verbose=False)
#
#        if ev_max > 0 and ev_sel_indv['gen_tot'] >= ev_max: break
#        pass_cut['gen_tot'] = True
#
#        gen_mttbar = -1.
#        if (ttbar_lje_dc) and (abs(genp[ttbar_lje_dc['lep_fd']].PID) in lep_ls):
#            pass_cut['gen_lje'] = True
#            gen_mttbar = inv_mass(genp[ttbar_lje_dc['lep_t']], genp[ttbar_lje_dc['had_t']])
#
#            ###
#            muo_idx = get_indexes_from_genp_list(genp, [1], [13,-13], muo_pt_min, muo_eta_max)
#            ele_idx = get_indexes_from_genp_list(genp, [1], [11,-11], ele_pt_min, ele_eta_max)
#            if len(muo_idx) == 1 and len(ele_idx) == 0 and (13 in lep_ls):
#                ch_muon = True
#                pass_cut['lep_num'] = True
#                lepton = ROOT.TLorentzVector()
#                lepton.SetPx(genp[muo_idx[0]].Px)
#                lepton.SetPy(genp[muo_idx[0]].Py)
#                lepton.SetPz(genp[muo_idx[0]].Pz)
#                lepton.SetE(genp[muo_idx[0]].E)
#            elif len(ele_idx) == 1 and len(muo_idx) == 0 and (11 in lep_ls):
#                ch_elec = True
#                pass_cut['lep_num'] = True
#                lepton = ROOT.TLorentzVector()
#                lepton.SetPx(genp[ele_idx[0]].Px)
#                lepton.SetPy(genp[ele_idx[0]].Py)
#                lepton.SetPz(genp[ele_idx[0]].Pz)
#                lepton.SetE(genp[ele_idx[0]].E)
#            else:
#                pass_cut['lep_num'] = False
#                lepton = None
#
#            jets_pt25 = get_jets_p4_from_genp_list('cone', .5, genp, muo_idx+ele_idx, 25.)
#            met = get_met_p4_from_genp_list(genp)
#
#            pass_cut['met_pt'] = met.Pt() > met_pt_min
#            if lepton: htlep = met.Pt()+lepton.Pt()
#            else: htlep = met.Pt()
#            pass_cut['htlep'] = htlep > htlep_min
#            if lepton and jets_pt25:
#                dRmin_sel = dRmin(lepton, jets_pt25) > lep_2dcut[0]
#                pTrel_sel = pTrel(lepton, jets_pt25) > lep_2dcut[1]
#                pass_cut['lep_2dc'] = dRmin_sel or pTrel_sel
#
#            jets = get_kincleaned_jet_list(jets_pt25, jet_pt_min, jet_eta_max)
#            pass_cut['jet_num'] = len(jets) >= jet_num_min
#            if jets: pass_cut['jet1_pt'] = jets[0].Pt() > jet1_pt_min
#            pass_cut['jet_sel'] = pass_cut['jet_num'] and pass_cut['jet1_pt']
#
#            pass_triangc = False
#            if ch_elec and jets: pass_triangc = pass_triangular_cuts(lepton, jets[0], met)
#            elif ch_muon: pass_triangc = True
#
#            pass_cut['lep_sel'] = pass_cut['lep_num'] and pass_cut['lep_2dc'] and pass_triangc
#
#            ## leptonic top pT selection
#            if ch_muon: pass_cut['ltop_pt'] = True
#            elif ch_elec and ('lep_t' in ttbar_lje_dc):
#                if genp[ttbar_lje_dc['lep_t']].PT > toplep_pt_min:
#                    pass_cut['ltop_pt'] = True
#
#        ### update cutflow counters
#        for c in cut_ls:
#            if pass_cut[c]:
#                ev_sel_indv[c] += 1
#                h['indv__'+c+'__genMttbar'].Fill(gen_mttbar)
#
#        for i in range(0, len(cut_ls)):
#            add = pass_cut[cut_ls[i]]
#            for j in range(0, i): add = add and pass_cut[cut_ls[j]]
#            if add:
#                ev_sel_cons[cut_ls[i]] += 1
#                h['cons__'+cut_ls[i]+'__genMttbar'].Fill(gen_mttbar)

    ### printout
#    print '\n >> # event TOT =', ev_sel_indv['gen_tot'], '\n'
#    for c in cut_ls:
#        print '  ', cut_dc[c], ' | ',
#        print '%.3f'% (float(ev_sel_indv[c])/float(ev_sel_indv['gen_tot'])), ' | ',
#        print '%.3f'% (float(ev_sel_cons[c])/float(ev_sel_indv['gen_tot'])), ' |'

#!#    print '\n >> # event LJE =', ev_sel_indv['gen_lje'], lep_ls,
#!#    print ' ('+'%.1f'% (100*float(ev_sel_indv['gen_lje'])/float(ev_sel_indv['gen_tot']))+'%)\n'
#!#    for c in cut_ls:
#!#        print '  ', cut_dc[c], ' | ',
#!##        print '%.3f'% (float(ev_sel_indv[c])/float(ev_sel_indv['gen_lje'])), ' | ',
#!#        print '%.3f'% (float(ev_sel_cons[c])/float(ev_sel_indv['gen_lje'])), ' |'
#!#    print '\n'
#!#
#!#    ### output file
#!#    ofile = ROOT.TFile(sys.argv[2], 'recreate')
#!#    ofile.cd()
#!#
#!#    for ty in ['indv', 'cons']:
#!#        for c in cut_ls:
#!#            h0 = h[ty+'__'+c+'__genMttbar']
#!#            h0.Sumw2()
#!##            h0.Scale(1./h0.Integral(0,-1))
#!#            h0.Write()
#!#    ofile.Close()
#!#    print ' >> written output file: '+sys.argv[2]+'\n'
