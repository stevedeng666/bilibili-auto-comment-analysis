package cn.experiment;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import javafx.application.Application;
import javafx.application.HostServices;
import javafx.application.Platform;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.control.Alert;
import javafx.scene.control.Button;
import javafx.scene.control.ListView;
import javafx.scene.control.TextField;
import javafx.scene.input.MouseButton;
import javafx.stage.Stage;
import java.net.URLEncoder;

import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.Map;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;

public class MainWindow extends Application{
    private ListView<String> listView;
    private Button button;
    private Button searchButton;
    private Button tsButton;
    private AnalysisWindow aw;
    private TextField searchInput;
    public static void main(String[] args){
        launch();
        database.connect();
    }

    @Override
    public void start(Stage primaryStage) throws Exception {
        // 加载 FXML
        Parent root = FXMLLoader.load(getClass().getResource("/main.fxml"));

        Scene scene = new Scene(root);
        primaryStage.setScene(scene);
        primaryStage.setTitle("Bilibili热搜大数据分析");
        this.listView = (ListView<String>) root.lookup("#display");
        this.listView.setOnMouseClicked(mouseEvent -> {
            if((mouseEvent.getClickCount()==2)&&(mouseEvent.getButton().equals(MouseButton.PRIMARY))){

                String keyword=listView.getSelectionModel().getSelectedItem();
                keyword=URLEncoder.encode(keyword, StandardCharsets.UTF_8);
                if(keyword != null){
                    this.aw=new AnalysisWindow(keyword);
                    try {
                        this.aw.show(primaryStage);
                    } catch (IOException | InterruptedException e) {
                        throw new RuntimeException(e);
                    }
                }
            }
        });

        this.button=(Button)root.lookup("#button");
        this.button.setOnAction(_ -> refresh());

        this.tsButton=(Button) root.lookup("#tsButton");
        this.tsButton.setOnAction(_ ->{
            HostServices hostServices = getHostServices();
            hostServices.showDocument("http://localhost:8000/getTrendingPlot");
        });

        this.searchButton=(Button) root.lookup("#searchButton");
        this.searchButton.setOnAction(_ ->{
            String keyword=this.searchInput.getText();
            keyword=URLEncoder.encode(keyword, StandardCharsets.UTF_8);
            if(keyword != null){
                this.aw=new AnalysisWindow(keyword);
                //String jsonStr=null;
                try {
                    this.aw.show(primaryStage);
                } catch (IOException | InterruptedException e) {
                    throw new RuntimeException(e);
                }
            }
        });

        this.searchInput=(TextField) root.lookup("#searchInput");
        java.util.concurrent.ScheduledExecutorService executor = Executors.newScheduledThreadPool(1);
        Runnable task = this::refresh;
        executor.scheduleAtFixedRate(task, 0,10, TimeUnit.MINUTES);
        primaryStage.setOnCloseRequest(_ ->{
            executor.shutdown();
        });
        primaryStage.show();
    }

    public static String getResult(String url) throws IOException, InterruptedException {
        HttpClient client = HttpClient.newHttpClient();
        System.out.println("client established");
        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create(url))
                .build();
        System.out.println("request built");
        HttpResponse<String> response = client.send(
                request,
                HttpResponse.BodyHandlers.ofString()
        );
        System.out.println("request sent");
        return response.body();
    }

    public void refresh(){
        Platform.runLater(() -> {
            this.listView.getItems().clear();
        });
        //this.listView.getItems().clear();
        String jsonStr;
        //这里以后要添加服务器未启动时的报错信息
        try {
            jsonStr = getResult("http://127.0.0.1:8000/getData");
        } catch (IOException | InterruptedException e) {
            Alert alert=new Alert(Alert.AlertType.INFORMATION);
            alert.setTitle("提示");
            alert.setContentText("服务器未启动");
            alert.showAndWait();
            throw new RuntimeException(e);
        }
        ObjectMapper mapper = new ObjectMapper();
        Map<String, Object> result;
        try {
            result = mapper.readValue(jsonStr, Map.class);
        } catch (JsonProcessingException e) {
            throw new RuntimeException(e);
        }
        ArrayList<String> keywordList=(ArrayList<String>) result.get("data");
        Platform.runLater(() -> {
            for(String keyword: keywordList){
                this.listView.getItems().add(keyword);
            }
        });
        //database.insert(result);
        /*
        for(String keyword: keywordList){
            this.listView.getItems().add(keyword);
        }*/
    }

}