import numpy as np
from math import fabs
from numba import jit


def getRSI(close, n=14):
    # compute a vector for change between daily closing prices
    change = np.zeros(len(close))
    for i in range(1, len(close)):
        change[i] = close[i] - close[i-1] ##Reversed the order of these.

    # compute a vector of gains and losses
    gain = np.zeros(len(close))
    loss = np.zeros(len(close))

    for i in range(1, len(close)):
        if change[i] >= 0:
            gain[i] = change[i]
            loss[i] = 0.00 ##Each array element needs a value.
        else:
            gain[i] = 0.00 ##Each array element needs a value.
            loss[i] = fabs(change[i])

    avg_gain = np.zeros(len(close) - n) ##Array length was wrong.
    avg_loss = np.zeros(len(close) - n) ##Array length was wrong.

    avg_gain[0] = np.average(gain[1:n+1]) ##First array element has a different calculation.
    avg_loss[0] = np.average(loss[1:n+1]) ##First array element has a different calculation.

    for i in range(1, len(close) - n): ##Loop counter was wrong.
        avg_gain[i] = (avg_gain[i-1]*(n-1) + gain[i+n])/n ##Indexes were wrong.
        avg_loss[i] = (avg_loss[i-1]*(n-1) + loss[i+n])/n ##Indexes were wrong.

    RS = np.zeros(len(close) - n) ##Array length was wrong.
    for i in range(0, len(close) - n): ##Loop counter was wrong.
        RS[i] = avg_gain[i]/avg_loss[i]

    RSI = np.zeros(len(close) - n) ##Array length was wrong.
    for i in range(0, len(close) - n): ##Loop counter was wrong.
        if avg_loss[i] == 0: ##This was missing. Could throw an error without it.
            RSI[i] = 100
        else:
            RSI[i] = 100 - (100/(1+RS[i]))

    return pad_like(RSI, close)


def sma(a, n=3) :
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n


def pad_like(input, thing_to_match):
    return np.pad(input, (len(thing_to_match) - len(input), 0), 'mean')


@jit
def getMultiAverageHighAndLow(c, h, l, max_lookback=-1):
    size = len(c)
    out_size = max_lookback
    if max_lookback == -1 or max_lookback > out_size:
        out_size = size

    in_pos = size-1
    out_pos = 0
    out_min = np.zeros(out_size)
    out_max = np.zeros(out_size)
    out_avg = np.zeros(out_size)

    top_slice = 0
    bottom_slice = 0

    out_avg[out_pos] = out_max[out_pos] = out_min[out_pos] = c[in_pos]
    current_sum = c[in_pos]

    for i in range(out_size-1):
        out_pos += 1
        in_pos -= 1
        current_sum += c[in_pos]
        out_min[out_pos] = l[in_pos] if l[in_pos] < out_min[out_pos-1] else out_min[out_pos-1]
        out_max[out_pos] = h[in_pos] if h[in_pos] > out_max[out_pos - 1] else out_max[out_pos - 1]
        out_avg[out_pos] = current_sum / (out_pos + 1)
        top_slice += (out_max[out_pos] - out_avg[0]) * np.log(1+out_pos/size)
        bottom_slice += (out_avg[0] - out_min[out_pos]) * np.log(1+out_pos/size)

    return out_avg, out_max, out_min, top_slice/(top_slice + bottom_slice)


# From http://stackoverflow.com/a/40085052/3293881
def strided_app(a, L, S=1 ):  # Window len = L, Stride len/stepsize = S
    nrows = ((a.size-L)//S)+1
    n = a.strides[0]
    return np.lib.stride_tricks.as_strided(a, shape=(nrows,L), strides=(S*n,n))


def min_max(a, n=3):
    A = strided_app(a, n)
    min_array = np.min(A, axis=1)
    max_array = np.max(A, axis=1)
    return min_array, max_array


def max_min_before_max(a, n=3):
    A = strided_app(a, n)
    max_array = np.max(A, axis=1)
    arg_max_array = np.argmax(A, axis=1)

    min_array = [np.min(A[i][0:arg_max_array[i]]) if arg_max_array[i] > 0 else A[i][0] for i in range(len(A))]

    return min_array, max_array


# rolling_meansqdiff_numpy
def rolling_volatility_and_zscore(a, w):
    A = strided_app(a, w)
    B = sma(a, w)
    subs = A-B[:,None]
    sums = np.einsum('ij,ij->i',subs,subs)
    volatility = (sums/w)**0.5
    zscore = (a[w-1:] - B) / volatility
    return pad_like(volatility/B, a),  pad_like(zscore, a)


def linear_scale(v):
    return (v - v.min()) / (v.max() - v.min())


def correlation_matrix(df_dest, df_src):
    A = df_dest.astype(float)
    B = df_src.astype(float)

    # Rowwise mean of input arrays & subtract from input arrays themselves
    A_mA = A - A.mean(1)[:, None]
    B_mB = B - B.mean(1)[:, None]

    # Sum of squares across rows
    ssA = (A_mA ** 2).sum(1)
    ssB = (B_mB ** 2).sum(1)

    # Finally get corr coeff
    corr_output = np.dot(A_mA, B_mB.T) / np.sqrt(np.dot(ssA[:, None], ssB[None]))

    return corr_output


def resample(a, time_unit_seconds=15):
    return sma(a, time_unit_seconds)[::time_unit_seconds]


def ema(x, n):
    alpha = 2 / (n + 1)
    return ewma_vectorized_safe(x, alpha)


def macd(x, fast=12, slow=26, signal=9):
    f = ema(x, fast)
    s = ema(x, slow)
    macd = np.subtract(f, s)
    signal_line = ema(macd, signal)
    diff = np.subtract(macd, signal_line)
    return pad_like(macd, x), pad_like(signal_line, x), pad_like(diff, x)


def ppo(x, fast=12, slow=26, signal=9):
    f = ema(x, fast)
    s = ema(x, slow)
    macd = np.subtract(f, s)
    ppo = np.multiply(np.divide(macd, s), 100)
    signal_line = ema(ppo, signal)
    diff = np.subtract(ppo, signal_line)
    return pad_like(ppo, x), pad_like(signal_line, x), pad_like(diff, x)


def gain_ratio_last_seen(data):
    max_index = np.argmax(data)
    if max_index == 0:
        return 0;

    min = np.min(data[0:max_index])
    max = data[max_index]

    return max / min


def stochastic(a, window=60):
    min, max = min_max(a, window)
    min = pad_like(min, a)
    max = pad_like(max, a)
    pdi = (max - a) / (max - min)
    pdi[pdi > 1] = 1
    return pdi



def aroon(high, low, n=14):
    # Calculate Result

    Ah = strided_app(high, n)
    periods_from_hh = np.argmax(Ah, axis=1) * -1 + n

    Al = strided_app(low, n)
    periods_from_ll = np.argmin(Al, axis=1) * -1 + n

    aroon_up = aroon_down = 100
    aroon_up *= 1 - (periods_from_hh / n)
    aroon_down *= 1 - (periods_from_ll / n)
    aroon_osc = aroon_up - aroon_down

    return pad_like(aroon_up, high), pad_like(aroon_down, high), pad_like(aroon_osc, high)



def ewma_vectorized_safe(data, alpha, row_size=None, dtype=None, order='C', out=None):
    """
    Reshapes data before calculating EWMA, then iterates once over the rows
    to calculate the offset without precision issues
    :param data: Input data, will be flattened.
    :param alpha: scalar float in range (0,1)
        The alpha parameter for the moving average.
    :param row_size: int, optional
        The row size to use in the computation. High row sizes need higher precision,
        low values will impact performance. The optimal value depends on the
        platform and the alpha being used. Higher alpha values require lower
        row size. Default depends on dtype.
    :param dtype: optional
        Data type used for calculations. Defaults to float64 unless
        data.dtype is float32, then it will use float32.
    :param order: {'C', 'F', 'A'}, optional
        Order to use when flattening the data. Defaults to 'C'.
    :param out: ndarray, or None, optional
        A location into which the result is stored. If provided, it must have
        the same shape as the desired output. If not provided or `None`,
        a freshly-allocated array is returned.
    :return: The flattened result.
    """
    data = np.array(data, copy=False)

    if dtype is None:
        if data.dtype == np.float32:
            dtype = np.float32
        else:
            dtype = np.float
    else:
        dtype = np.dtype(dtype)

    row_size = int(row_size) if row_size is not None else get_max_row_size(alpha, dtype)

    if data.size <= row_size:
        # The normal function can handle this input, use that
        return ewma_vectorized(data, alpha, dtype=dtype, order=order, out=out)

    if data.ndim > 1:
        # flatten input
        data = np.reshape(data, -1, order=order)

    if out is None:
        out = np.empty_like(data, dtype=dtype)
    else:
        assert out.shape == data.shape
        assert out.dtype == dtype

    row_n = int(data.size // row_size)  # the number of rows to use
    trailing_n = int(data.size % row_size)  # the amount of data leftover
    first_offset = data[0]

    if trailing_n > 0:
        # set temporary results to slice view of out parameter
        out_main_view = np.reshape(out[:-trailing_n], (row_n, row_size))
        data_main_view = np.reshape(data[:-trailing_n], (row_n, row_size))
    else:
        out_main_view = out
        data_main_view = data

    # get all the scaled cumulative sums with 0 offset
    ewma_vectorized_2d(data_main_view, alpha, axis=1, offset=0, dtype=dtype,
                       order='C', out=out_main_view)

    scaling_factors = (1 - alpha) ** np.arange(1, row_size + 1)
    last_scaling_factor = scaling_factors[-1]

    # create offset array
    offsets = np.empty(out_main_view.shape[0], dtype=dtype)
    offsets[0] = first_offset
    # iteratively calculate offset for each row
    for i in range(1, out_main_view.shape[0]):
        offsets[i] = offsets[i - 1] * last_scaling_factor + out_main_view[i - 1, -1]

    # add the offsets to the result
    out_main_view += offsets[:, np.newaxis] * scaling_factors[np.newaxis, :]

    if trailing_n > 0:
        # process trailing data in the 2nd slice of the out parameter
        ewma_vectorized(data[-trailing_n:], alpha, offset=out_main_view[-1, -1],
                        dtype=dtype, order='C', out=out[-trailing_n:])
    return out


def get_max_row_size(alpha, dtype=float):
    assert 0. <= alpha < 1.
    # This will return the maximum row size possible on
    # your platform for the given dtype. I can find no impact on accuracy
    # at this value on my machine.
    # Might not be the optimal value for speed, which is hard to predict
    # due to numpy's optimizations
    # Use np.finfo(dtype).eps if you  are worried about accuracy
    # and want to be extra safe.
    epsilon = np.finfo(dtype).tiny
    # If this produces an OverflowError, make epsilon larger
    return int(np.log(epsilon)/np.log(1-alpha)) + 1


def ewma_vectorized(data, alpha, offset=None, dtype=None, order='C', out=None):
    """
    Calculates the exponential moving average over a vector.
    Will fail for large inputs.
    :param data: Input data
    :param alpha: scalar float in range (0,1)
        The alpha parameter for the moving average.
    :param offset: optional
        The offset for the moving average, scalar. Defaults to data[0].
    :param dtype: optional
        Data type used for calculations. Defaults to float64 unless
        data.dtype is float32, then it will use float32.
    :param order: {'C', 'F', 'A'}, optional
        Order to use when flattening the data. Defaults to 'C'.
    :param out: ndarray, or None, optional
        A location into which the result is stored. If provided, it must have
        the same shape as the input. If not provided or `None`,
        a freshly-allocated array is returned.
    """
    data = np.array(data, copy=False)

    if dtype is None:
        if data.dtype == np.float32:
            dtype = np.float32
        else:
            dtype = np.float64
    else:
        dtype = np.dtype(dtype)

    if data.ndim > 1:
        # flatten input
        data = data.reshape(-1, order)

    if out is None:
        out = np.empty_like(data, dtype=dtype)
    else:
        assert out.shape == data.shape
        assert out.dtype == dtype

    if data.size < 1:
        # empty input, return empty array
        return out

    if offset is None:
        offset = data[0]

    alpha = np.array(alpha, copy=False).astype(dtype, copy=False)

    # scaling_factors -> 0 as len(data) gets large
    # this leads to divide-by-zeros below
    scaling_factors = np.power(1. - alpha, np.arange(data.size + 1, dtype=dtype),
                               dtype=dtype)
    # create cumulative sum array
    np.multiply(data, (alpha * scaling_factors[-2]) / scaling_factors[:-1],
                dtype=dtype, out=out)
    np.cumsum(out, dtype=dtype, out=out)

    # cumsums / scaling
    out /= scaling_factors[-2::-1]

    if offset != 0:
        offset = np.array(offset, copy=False).astype(dtype, copy=False)
        # add offsets
        out += offset * scaling_factors[1:]

    return out


def ewma_vectorized_2d(data, alpha, axis=None, offset=None, dtype=None, order='C', out=None):
    """
    Calculates the exponential moving average over a given axis.
    :param data: Input data, must be 1D or 2D array.
    :param alpha: scalar float in range (0,1)
        The alpha parameter for the moving average.
    :param axis: The axis to apply the moving average on.
        If axis==None, the data is flattened.
    :param offset: optional
        The offset for the moving average. Must be scalar or a
        vector with one element for each row of data. If set to None,
        defaults to the first value of each row.
    :param dtype: optional
        Data type used for calculations. Defaults to float64 unless
        data.dtype is float32, then it will use float32.
    :param order: {'C', 'F', 'A'}, optional
        Order to use when flattening the data. Ignored if axis is not None.
    :param out: ndarray, or None, optional
        A location into which the result is stored. If provided, it must have
        the same shape as the desired output. If not provided or `None`,
        a freshly-allocated array is returned.
    """
    data = np.array(data, copy=False)

    assert data.ndim <= 2

    if dtype is None:
        if data.dtype == np.float32:
            dtype = np.float32
        else:
            dtype = np.float64
    else:
        dtype = np.dtype(dtype)

    if out is None:
        out = np.empty_like(data, dtype=dtype)
    else:
        assert out.shape == data.shape
        assert out.dtype == dtype

    if data.size < 1:
        # empty input, return empty array
        return out

    if axis is None or data.ndim < 2:
        # use 1D version
        if isinstance(offset, np.ndarray):
            offset = offset[0]
        return ewma_vectorized(data, alpha, offset, dtype=dtype, order=order,
                               out=out)

    assert -data.ndim <= axis < data.ndim

    # create reshaped data views
    out_view = out
    if axis < 0:
        axis = data.ndim - int(axis)

    if axis == 0:
        # transpose data views so columns are treated as rows
        data = data.T
        out_view = out_view.T

    if offset is None:
        # use the first element of each row as the offset
        offset = np.copy(data[:, 0])
    elif np.size(offset) == 1:
        offset = np.reshape(offset, (1,))

    alpha = np.array(alpha, copy=False).astype(dtype, copy=False)

    # calculate the moving average
    row_size = data.shape[1]
    row_n = data.shape[0]
    scaling_factors = np.power(1. - alpha, np.arange(row_size + 1, dtype=dtype),
                               dtype=dtype)
    # create a scaled cumulative sum array
    np.multiply(
        data,
        np.multiply(alpha * scaling_factors[-2], np.ones((row_n, 1), dtype=dtype),
                    dtype=dtype)
        / scaling_factors[np.newaxis, :-1],
        dtype=dtype, out=out_view
    )
    np.cumsum(out_view, axis=1, dtype=dtype, out=out_view)
    out_view /= scaling_factors[np.newaxis, -2::-1]

    if not (np.size(offset) == 1 and offset == 0):
        offset = offset.astype(dtype, copy=False)
        # add the offsets to the scaled cumulative sums
        out_view += offset[:, np.newaxis] * scaling_factors[np.newaxis, 1:]

    return out
