package cn.experiment;

public class Main {
    public static void main(String[] args) {
        database.connect();
        //System.out.println(database.getTrending());
        MainWindow.main(args);
    }
}