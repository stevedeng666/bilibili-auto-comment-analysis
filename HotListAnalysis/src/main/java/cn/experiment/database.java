package cn.experiment;

import com.mongodb.client.*;
import org.bson.Document;

import java.util.ArrayList;
import java.util.Map;

import static com.mongodb.client.model.Filters.*;

public class database {
    private static String dbName="bilibili";
    private static String collectionName="trending";
    private static MongoClient client;
    private static MongoDatabase db;
    private static MongoCollection<Document> collection;
    public static void connect(){
        client=MongoClients.create("mongodb://localhost:27017");
        db=client.getDatabase(dbName);
        collection = db.getCollection(collectionName);
    }
    public static void insert(Map map) {
        Document document = new Document(map);
        collection.insertOne(document);
    }

    public static void find(MongoCollection<Document> collection){
        MongoCursor<Document> cursor=collection.find().iterator();
        while(cursor.hasNext()){
            System.out.println(cursor.next().toJson());
        }
    }
    public static ArrayList<Document> getTrending(){
        MongoCursor<Document> cursor=collection.find().iterator();
        ArrayList<Document> docs=new ArrayList<>();
        while(cursor.hasNext()){
            docs.add(cursor.next());
        }
        return docs;
    }
}
