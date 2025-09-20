package cn.experiment;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import javafx.application.Platform;
import javafx.concurrent.Task;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.web.WebView;
import javafx.stage.Stage;
import kong.unirest.HttpResponse;
import kong.unirest.Unirest;

import java.io.IOException;
import java.net.URLDecoder;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.Base64;
import java.util.concurrent.CompletableFuture;


public class AnalysisWindow {
    private final Stage stage;
    private WebView webview;
    private Button pieButton;
    private Button wordCloudButton;
    private Button ldaButton;
    private Button aiButton;
    public String jsonStr;
    private final String keyword;
    private LDAWindow ldawindow;
    public AnalysisWindow(String keyword){
        this.keyword=keyword;
        //异步爬虫获取原始评论数据，以及获取成功和失败的回调函数
        new Thread(new Task<Boolean>() {
            @Override
            protected Boolean call() throws Exception {
                // 在后台线程执行耗时操作
                jsonStr = MainWindow.getResult(String.format("http://127.0.0.1:8000/search?keyword=%s", keyword));
                return true;
            }

            @Override
            protected void running() {
                // 在任务开始时更新UI（自动在FX线程执行）
                Platform.runLater(() -> {
                    pieButton.setText("加载中");
                    pieButton.setDisable(true);

                    wordCloudButton.setText("加载中");
                    wordCloudButton.setDisable(true);

                    ldaButton.setText("加载中");
                    ldaButton.setDisable(true);

                    aiButton.setText("加载中");
                    aiButton.setDisable(true);
                });
            }

            @Override
            protected void succeeded() {
                // 任务完成后更新UI（自动在FX线程执行）
                pieButton.setText("饼状图");
                pieButton.setDisable(false);

                wordCloudButton.setText("词云图");
                wordCloudButton.setDisable(false);

                ldaButton.setText("LDA");
                ldaButton.setDisable(false);

                aiButton.setText("生成报告");
                aiButton.setDisable(false);

                try {
                    plotPie(jsonStr);
                } catch (IOException | InterruptedException e) {
                    throw new RuntimeException(e);
                }

                // 这里可以处理jsonStr数据
            }

            @Override
            protected void failed() {
                // 错误处理（自动在FX线程执行）
                Platform.runLater(() -> {
                    pieButton.setText("加载失败");
                    pieButton.setDisable(false);

                    wordCloudButton.setText("加载失败");
                    wordCloudButton.setDisable(false);
                });
            }
        }).start();
        this.stage=new Stage();
        this.stage.setTitle("Bilibili大数据分析");
        try{
            Parent root=FXMLLoader.load(getClass().getResource("/AnalysisWindow.fxml"));
            stage.setScene(new Scene(root));
            webview=(WebView) root.lookup("#webview");

            pieButton=(Button) root.lookup("#pieButton");
            pieButton.setOnAction(_ ->{
                try {
                    plotPie(jsonStr);
                } catch (IOException | InterruptedException e) {
                    throw new RuntimeException(e);
                }
            });

            wordCloudButton =(Button) root.lookup("#wordCloudButton");
            wordCloudButton.setOnAction(_ -> plotWordCloud(jsonStr));

            ldaButton=(Button) root.lookup("#ldaButton");
            ldaButton.setOnAction(_ ->{
                try {
                    this.ldawindow=new LDAWindow(this.jsonStr,this.keyword);
                    this.ldawindow.show(this.stage);
                } catch (IOException e) {
                    throw new RuntimeException(e);
                }
            });

            aiButton=(Button) root.lookup("#reportButton");
            /*
            aiButton.setOnAction(_ ->{
                HttpResponse<String> response =  Unirest.post("http://localhost:8000/AITextAnalysis")
                        .header("Content-Type", "application/json")
                        .body(this.jsonStr)
                        .socketTimeout(120_000)  // 2 分钟读取超时
                        .connectTimeout(120_000) // 2 分钟连接超时
                        .asString();
                webview.getEngine().loadContent(response.getBody());
            });
            */
            aiButton.setOnAction(_ -> {
                // 创建异步任务
                CompletableFuture.supplyAsync(() -> {
                    try {
                        Platform.runLater(() ->{
                            aiButton.setText("处理中");
                            aiButton.setDisable(true);
                        });
                        return Unirest.post("http://localhost:8000/AITextAnalysis")
                                .header("Content-Type", "application/json")
                                .body(this.jsonStr)
                                .socketTimeout(240_000)
                                .connectTimeout(240_000)
                                .asString();
                    } catch (Exception e) {
                        throw new RuntimeException("API请求失败", e);
                    }
                }).thenAcceptAsync(response -> {
                    // 在JavaFX应用线程中更新UI
                    Platform.runLater(() -> {
                        aiButton.setText("保存本地");
                        aiButton.setDisable(false);
                        aiButton.setOnAction(_ ->{
                            try {
                                Files.write(Paths.get(String.format("bilibiliL%s 舆情分析报告.html", URLDecoder.decode(keyword, StandardCharsets.UTF_8))), response.getBody().getBytes());
                                System.out.println("保存成功!");
                                aiButton.setDisable(true);
                            } catch (IOException e) {
                                e.printStackTrace();
                            }
                        });
                        webview.getEngine().loadContent(response.getBody());
                    });
                }).exceptionally(ex -> {
                    // 处理异常
                    Platform.runLater(() -> {
                        // 这里可以显示错误信息，例如：
                        webview.getEngine().loadContent("<h1>错误: " + ex.getCause().getMessage() + "</h1>");
                    });
                    return null;
                });
            });
        } catch (Exception e){
            e.printStackTrace();
        }
    }
    public void show(Stage owner) throws IOException, InterruptedException {
        this.stage.initOwner(owner);  // 关联主窗口
        //plot(jsonStr);
        this.stage.show();
        this.stage.toFront();
    }

    public void plotPie(String data) throws IOException, InterruptedException {
        /*
        data格式为/search返回的，即{"keyword":... , "data":...}
        */
        HttpResponse<String> response =  Unirest.post("http://localhost:8000/plotPie")
                .header("Content-Type", "application/json")
                .body(data)
                .asString();
        webview.getEngine().loadContent(response.getBody());
    }

    public void plotWordCloud(String data){
        //data格式为/search返回的，即{"keyword":... , "data":...}
        HttpResponse<byte []> response =  Unirest.post("http://localhost:8000/plotWordCloud")
                .header("Content-Type", "application/json")
                .body(data)
                .asBytes();
        String html= """
                    <html>
                        <head>
                            <style>
                                body {
                                    margin: 0;
                                    padding: 20px;
                                    display: flex;
                                    flex-direction: column;
                                    align-items: center;
                                    font-family: Arial, sans-serif;
                                }
                                h2 {
                                    text-align: center;
                                    margin-bottom: 20px;
                                    color: #333;
                                    width: 85%%;
                                }
                                .img-container {
                                    max-width: 100%%;
                                    height: auto;
                                    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                                }
                            </style>
                        </head>
                        <body>
                            <h2>%s</h2>
                            <img class="img-container" src="data:image/png;base64,%s">
                        </body>
                    </html>
                    """;
        if (response.isSuccess()) {
            byte[] imageBytes = response.getBody();
            String base64Image = Base64.getEncoder().encodeToString(imageBytes);

            // 在 WebView 中嵌入 Base64 图片
            try {
                html = String.format(html, (new ObjectMapper()).readTree(jsonStr).get("keyword").asText(),base64Image);
            } catch (JsonProcessingException e) {
                throw new RuntimeException(e);
            }

            webview.getEngine().loadContent(html);
        } else {
            webview.getEngine().loadContent(
                    "<h1>Error: " + response.getStatus() + "</h1>" +
                            "<p>" + response.getStatusText() + "</p>"
            );
        }
    }
}
