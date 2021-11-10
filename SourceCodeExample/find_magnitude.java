

public class find_magnitude {
    public static double find_magnitude_m(Integer[] a) {
        int i;
        double sum = 0;
        for (i = 0; i < a.length; i++) {
            sum += a[i] * a[i];
        }
        double result = Math.sqrt(sum);
        return result;
    }
}