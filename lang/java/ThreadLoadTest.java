/**
 * java -Xss10k ThreadLoadTest 
 * java -Xss100k ThreadLoadTest 1900
 */
public class ThreadLoadTest {

    private static class RunThread extends Thread {
        public void run() {
            System.out.println("**************started, " + Thread.currentThread().getName());
            for(double i = 0.0; i < 500000000000000000.0; i++) {
                System.gc();
                System.out.println(Thread.currentThread().getName());
            }
            System.out.println("**************finished, " + Thread.currentThread().getName());
        }
    }

    public static void main(String[] args) {
        Thread.currentThread().setUncaughtExceptionHandler(new Thread.UncaughtExceptionHandler() {
            public void uncaughtException(final Thread t, final Throwable e) {
                System.err.println(e.getMessage());
                System.exit(1);
            }
        });

        int numThreads = 1000;
        if (args.length == 1) {
            numThreads = Integer.parseInt(args[0]);
        }

        for (int i=0; i<numThreads; i++) {
            try {
                RunThread demo = new RunThread();
                demo.start();
            } catch (final OutOfMemoryError e) {
                throw new RuntimeException("OOM", e);
            }
        }
    }

}

