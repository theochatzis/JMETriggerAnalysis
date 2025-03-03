#!/usr/bin/env python
import argparse, array, ROOT

def values(prc_type, rndm_gen):

    if prc_type == 0:

       val_x = rndm_gen.Gaus(50., 10.)
       val_y = rndm_gen.Gaus( 1., 30.)
       val_z = rndm_gen.Gaus(20., 10.)

    elif prc_type == 1:

       val_x = rndm_gen.Rndm() * 50.
       val_y = rndm_gen.Rndm() * 50.
       val_z = rndm_gen.Rndm() * 50.

    elif prc_type == 2:

       val_x = rndm_gen.Exp(30.)
       val_y = rndm_gen.Exp(20.)
       val_z = rndm_gen.Exp(25.)

    else:
       raise SystemExit('values: invalid process key: '+str(prc_type))

    return (val_x, val_y, val_z)

if __name__=='__main__':

   parser = argparse.ArgumentParser()

   parser.add_argument('-o', '--output', dest='output', action='store', default=None, type=str, required=True,
                       help='path to output ROOT file')

   parser.add_argument('-t', '--type', dest='type', action='store', default=None, type=int, required=True,
                       help='key for process type')

   parser.add_argument('-n', dest='n', required=False, action='store', default=int(10**5),
                       help='number of output events')

   parser.add_argument('-s', '--seed', dest='seed', action='store', default=int(1010), type=int, required=False,
                       help='seed for ROOT.TRandom3 generator')

   parser.add_argument('-u', '--uproot', dest='uproot', action='store_true', default=False,
                       help='enable settings geared towards uproot usage')

   opts, opts_unknown = parser.parse_known_args()

   ROOT.gROOT.SetBatch()

   opts.n = int(opts.n)

   rndm3 = ROOT.TRandom3(opts.seed)

   ofile = ROOT.TFile(opts.output, 'recreate')
   if not ofile: raise SystemExit(1)

   otree = ROOT.TTree('Events', 'Events')

   arr_X = array.array('f', [0.])
   arr_Y = array.array('f', [0.])
   arr_Z = array.array('f', [0.])

   otree.Branch('X', arr_X, 'X')
   otree.Branch('Y', arr_Y, 'Y')
   otree.Branch('Z', arr_Z, 'Z')

   if opts.uproot:

      ofile.SetCompressionAlgorithm(4)
      ofile.SetCompressionLevel(4)

      for tree_br in otree.GetListOfBranches():
          tree_br.SetBasketSize(1024*1024)

      if len(otree.GetListOfBranches()) > 0:
         otree.SetAutoFlush(-1024 * 1024 * len(otree.GetListOfBranches()))

   print otree.GetBranch('X').GetBasketSize()
   print otree.GetBranch('Y').GetBasketSize()
   print otree.GetBranch('Z').GetBasketSize()

   for i_evt in range(opts.n):

       x0, y0, z0 = values(opts.type, rndm3)

       arr_X[0] = x0
       arr_Y[0] = y0
       arr_Z[0] = z0

       otree.Fill()

       if not((i_evt+1) % (opts.n / 5.)): print '[type='+str(opts.type)+']', 'processing ...', i_evt+1

   ofile.Write()
   ofile.Close()

   print '> created output file [type='+str(opts.type)+']:', opts.output
