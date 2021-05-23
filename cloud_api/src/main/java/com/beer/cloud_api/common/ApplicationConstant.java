package com.beer.cloud_api.common;

import com.beer.cloud_api.entity.StoragePath;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

import java.util.*;


@Component
public class ApplicationConstant implements CommandLineRunner {


    @Autowired
    private StoragePathConfig storagePathConfig;

    /**
     * all storagePath alias name
     */
    public static Map<String, String> storagePathMap;
    public static List<StoragePath> storageList;


    @Override
    public void run(String... var1) throws Exception {
        List<StoragePath> list = storagePathConfig.getStorages();
        storagePathMap = new HashMap<>(list.size());
        for (StoragePath storagePath : list) {
            storagePathMap.put(storagePath.getName(), storagePath.getPath());
            storagePath.setPath(null);
        }
        storageList = list;
    }
}