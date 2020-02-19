import ltaController
import os
import time

from setVoltages import setVoltage

def init(lta, cdsout=2):
    # set up lta command incase you want to communicate from terminal
    os.chmod("lta.sh", 755)
    os.system('alias lta="$PWD/lta.sh {0}"'.format(lta.port))

    # set votlages
    setVoltage(lta)

    # Load sequencer
    lta.seq(lta.img_sequencer)

    # initialize some variables
    lta.set("sinit", 30)
    lta.set("pinit", 0)
    lta.set("ssamp", 200)
    lta.set("psamp", 200)
    lta.set("packSource", 9)
    lta.set("cdsout", cdsout)


def doClean(lta, vsub=70):
    lta.erase_and_purge()
    lta.set('vsub', vsub)
    lta.seq(lta.clear_sequencer)
    lta.runseq()


def doSkipper(lta, ncol, nrow, nsamp=1, ssamp=200, sinit=30, pinit=0):
    lta.seq(lta.img_sequencer)

    lta.set('psamp', ssamp)
    lta.set('ssamp', ssamp)
    lta.set('pinit', pinit)
    lta.set('sinit', sinit)

    # Make sure nothing gets cut off for pedistand and signal measurements
    lta.sendMsg('delay_Integ_ped {0}'.format(ssamp + 80))
    lta.sendMsg('delay_Integ_sig {0}'.format(ssamp + sinit + 5))

    # Set number of columns, rows and samples
    lta.NCOL(ncol)
    lta.NROW(nrow)
    lta.NSAMP(nsamp)

    lta.read()
    



lta = ltaController.lta()
init(lta)

doClean(lta)
doClean(lta)

lta.name("lta_img_")
doSkipper(lta, 50, 3272, 1)

exposure=30

for nsamp in [1, 100, 200, 300, 400]:
    doClean()
    
    print("Exposing the LTA for {0} seconds".format(exposure))
    time.sleep(exposure)

    lta.name("skp_nsamp_{0}".format{nsamp})
    doSkipper(lta, ncol, nrow, nsamp)
    
    









