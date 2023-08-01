import dask.array as da

def count_zero_crossings_per_lead(signal):
    from pprint import pprint
    print('SIGNAL')
    print('-' * 10)
    pprint(signal)
    print('-' * 10)
    signal_array = da.from_array(signal, chunks='auto')

    signs = da.sign(signal_array)

    # signs = da.compress(signs != 0, signs)  # Not working
    nonzero_indices = da.nonzero(signs)[0]
    signs = signs[nonzero_indices].compute()
    signs = da.from_array(signs, chunks='auto')

    # Calculate the differences between consecutive signs
    differences = da.diff(signs)

    # Find where differences are not equal to 0
    zero_crossings = differences != 0

    # Sum the occurrences of non-zero differences to get zero crossings count
    zero_crossing_count = zero_crossings.sum().compute()
    zero_crossing_count = int(zero_crossing_count)
    return zero_crossing_count

def process_all(ecg):
    output_ecg = dict(ecg)

    for idx, lead in enumerate(ecg["leads"]):
        signal = lead["signal"]
        output_ecg['leads'][idx]['count_zero_crossings'] = count_zero_crossings_per_lead(signal)

    return output_ecg