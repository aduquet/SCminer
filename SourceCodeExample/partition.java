public class partition {
        public static int partition_m(final Double[] work, final Integer begin, final Integer end, final Integer pivot) {
                final double value = work[pivot];
                work[pivot] = work[begin];
                int i = begin + 1;
                int j = end - 1;
                while (i < j) {
                        while (i < j && work[j] > value) {
                                --j;
                        }
                        while (i < j && work[i] < value) {
                                ++i;
                        }
                        if (i < j) {
                                final double tmp = work[i];
                                work[i++] = work[j];
                                work[j--] = tmp;
                        }
                }
                if (i >= end || work[i] > value) {
                        --i;
                }
                work[begin] = work[i];
                work[i] = value;
                return i;

        }
}


