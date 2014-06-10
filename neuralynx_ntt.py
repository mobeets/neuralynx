import numpy as np

NTT_HEADER_SIZE = (16 * 2**10)
NTT_PARAMS = ["ADChannel", "ADGain", "AmpGain", "AmpLowCut", "AmpHiCut", "SubSamplingInterleave", "SamplingFrequency", "ADBitVolts", "ADMaxValue", "AlignmentPt", "ThreshVal"]

def write_ntt((pre_lines, params, spikes), filename):
    """
    Writes a neuralynx .ntt tetrode spike file.
    """
    with open(filename, 'wb') as f:
        f.write(''.join(pre_lines))
        for key in NTT_PARAMS:
            if key in params:
                if key == 'ADBitVolts':
                    fcn = lambda val: '{0:0.12f}'.format(val)
                else:
                    fcn = str
                vals = [fcn(x) for x in params[key]]
                line = '\t-{0}\t{1}\t\n'.format(key, '\t'.join(vals))
                f.write(line)
        nnulls = (NTT_HEADER_SIZE - f.tell())
        f.write('\x00'*nnulls)
        spikes.tofile(f)

def mmap_ntt_file(f, offset=NTT_HEADER_SIZE): 
    """
    Read the post-header content of the Neuralynx .ntt file via memory-mapping
        n.b. Neuralynx writes little endian
    """
    ntt_dtype = np.dtype([ 
        ('timestamp'  , '<u8'), 
        ('sc_number'  , '<u4'), # "acquisition entity number"
        ('cell_number', '<u4'), 
        ('params'     , '<u4',   (8,)), 
        ('waveforms'  , '<i2', (32,4)), # "waveform points"
    ]) 
    return np.memmap(f, dtype=ntt_dtype, mode='r', offset=offset)

def read_ntt(filename, offset=NTT_HEADER_SIZE):
    """
    Loads a neuralynx .ntt tetrode spike file.

    Returns:
    - header lines before params
    - params, a dict
    - spikes as (num_spikes, length_waveform, num_channels) array
    """
    params = {}
    pre_lines = []
    found_params = False
    with open(filename, 'rb') as f:
        for raw_line in f:
            line = raw_line.replace('\t', ' ').strip().split()
            if not line:
                pre_lines.append(raw_line)
                continue
            key = line[0].replace('-', '')
            if key in NTT_PARAMS:
                found_params = True
                fcn = float if key == 'ADBitVolts' else int
                params[key] = [fcn(x) for x in line[1:]]
            elif found_params:
                break
            else:
                pre_lines.append(raw_line)
    spikes = mmap_ntt_file(filename, offset=offset)
    return pre_lines, params, spikes

def test():
    """
    Source: http://neuralynx.com/software/SampleTetrodeData.zip
    """
    import glob
    import os.path
    from tempfile import NamedTemporaryFile
    CURDIR = os.path.dirname(os.path.abspath(__file__))
    BASEDIR = os.path.abspath(os.path.join(CURDIR, 'SampleTetrodeData'))
    isequal = lambda d1, d2: all([a == b for a,b in zip(d1[-1], d2[-1])]) and d1[1] == d2[1]
    for infile in glob.glob(os.path.join(BASEDIR, '*.ntt')):
        infile = os.path.abspath(infile)
        o = NamedTemporaryFile()
        outfile = o.name
        d = read_ntt(infile)
        write_ntt(d, outfile)
        d2 = read_ntt(outfile)
        assert isequal(d, d2)

if __name__ == '__main__':
    test()
