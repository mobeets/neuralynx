neuralynx
=========

reads and writes neuralynx tetrode files (.ntt)

### Requirements

* numpy

### Example .ntt header

    ######## Neuralynx Data File Header
    ## File Name: c:\Cheetah_Data\2005-10-19_13-34-0\Sc8.ntt 
    ## Time Opened: (m/d/y): 10/19/2005  At Time: 13:34:3.375 
    -CheetahRev 4.60.0 
    -NLX_Base_Class_Name    Sc8 
    -NLX_Base_Class_Type    TTScAcqEnt 
    -RecordSize  304 
        -ADChannel  28  29  30  31  
        -ADGain     2   2   2   2   
        -AmpGain    2000    2000    2000    2000    
        -AmpLowCut  600 600 600 600 
        -AmpHiCut   6000    6000    6000    6000    
        -SubSamplingInterleave  1
        -SamplingFrequency  32556
        -ADBitVolts 0.000000007630  0.000000007630  0.000000007630  0.000000007630
        -ADMaxValue 32767
        -AlignmentPt    8
        -ThreshVal  60  60  60  60
        
n.b. This header is always `2^14` bytes long. It is padded with `\x00`s at the end in order to reach this size.
