package cn.experiment;

import javafx.application.Platform;
import javafx.concurrent.Task;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.control.Alert;
import javafx.scene.control.Button;
import javafx.scene.control.TextField;
import javafx.scene.control.TextFormatter;
import javafx.scene.text.Text;
import javafx.scene.web.WebView;
import javafx.stage.Stage;
import javafx.util.converter.IntegerStringConverter;
import kong.unirest.HttpResponse;
import kong.unirest.Unirest;

import java.io.IOException;
import java.net.URLDecoder;
import java.nio.charset.StandardCharsets;

public class LDAWindow {
    private static String jsonStr;
    private final Stage stage;
    private WebView wv;
    private TextField ntopicInput;
    private Button modelingButton;
    private Button plotButton;
    private Text statusText;
    public LDAWindow(String jsonStr,String keyword) throws IOException {
        this.jsonStr=jsonStr;
        this.stage=new Stage();
        this.stage.setTitle(String.format("关键词：%s - LDA主题建模与可视化", URLDecoder.decode(keyword, StandardCharsets.UTF_8)));
        Parent root= FXMLLoader.load(getClass().getResource("/LDAWindow.fxml"));
        stage.setScene(new Scene(root));

        this.wv=(WebView) root.lookup("#wv");

        this.ntopicInput =(TextField) root.lookup("#ntopicInput");
        TextFormatter<Integer> formatter = new TextFormatter<>(
                new IntegerStringConverter(),  // 数字转换器
                2,                            // 默认值
                change -> {
                    String newText = change.getControlNewText();
                    if (newText.matches("\\d*")) { // 正则匹配：仅数字
                        return change; // 允许输入
                    }
                    return null; // 拒绝输入
                }
        );
        ntopicInput.setTextFormatter(formatter);

        this.modelingButton=(Button) root.lookup("#modelingButton");
        this.modelingButton.setOnAction(_ ->{
            int ntopics=Integer.parseInt(this.ntopicInput.getText());
            if (ntopics>1){plotLDA(jsonStr,ntopics);}
            else {
                this.ntopicInput.setText("2");
                Alert alert=new Alert(Alert.AlertType.INFORMATION);
                alert.setTitle("提示");
                alert.setContentText("主题数应不小于1");
                alert.showAndWait();
            }
        });

        this.plotButton=(Button) root.lookup("#plotButton");
        this.plotButton.setOnAction(_ ->{
            new Thread(new Task<Boolean>() {
                @Override
                protected Boolean call() throws Exception {
                    // 在后台线程执行耗时操作
                    plotMetrics(jsonStr);
                    return true;
                }

                @Override
                protected void running() {
                    // 在任务开始时更新UI（自动在FX线程执行）
                    Platform.runLater(() -> {
                        statusText.setText("加载LDA度量图片中...");
                    });
                }

                @Override
                protected void succeeded() {
                    Platform.runLater(() -> {
                        statusText.setText("完成!");
                    });
                }

                @Override
                protected void failed() {
                    // 错误处理（自动在FX线程执行）
                    Platform.runLater(() -> {
                        statusText.setText("失败!");
                    });
                }
            }).start();
        });

        this.statusText=(Text) root.lookup("#statusText");

    }
    public void show(Stage owner){
        this.stage.initOwner(owner);
        this.stage.show();
    }

    public void plotMetrics(String data){
        HttpResponse<String> response =  Unirest.post("http://localhost:8000/plotLDAp")
                .header("Content-Type", "application/json")
                .body(data)
                .asString();
        Platform.runLater(() -> {
            wv.getEngine().loadContent(response.getBody());
        });
    }

    public void plotLDA(String data, int ntopics){
        HttpResponse<String> response =  Unirest.post(String.format("http://localhost:8000/plotLDA/%s",ntopics))
                .header("Content-Type", "application/json")
                .body(data)
                .asString();
        wv.getEngine().loadContent(response.getBody());
        wv.getEngine().executeScript("""
            document.body.style.transform = 'scale(0.8)';
            document.body.style.transformOrigin = '0 0';
        """);
    }
}
