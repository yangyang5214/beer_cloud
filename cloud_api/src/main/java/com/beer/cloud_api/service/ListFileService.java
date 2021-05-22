package com.beer.cloud_api.service;


import com.beer.cloud_api.common.ApplicationConstant;
import com.beer.cloud_api.entity.FileEntity;
import com.beer.cloud_api.entity.PageHelper;
import com.beer.cloud_api.util.DateUtil;
import org.springframework.stereotype.Service;
import org.springframework.util.StringUtils;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.*;

@Service
public class ListFileService {

    private static Map<String, List<FileEntity>> dirMap = new HashMap<>();

    /**
     * list file by dir path
     *
     * @param page
     * @param pageSize
     * @param prefix
     * @param storage
     * @return
     */
    public PageHelper listFile(int page, int pageSize, String prefix, String storage) {
        if (!StringUtils.hasLength(prefix)) {
            prefix = "";
        }
        Path path = Paths.get(ApplicationConstant.storagePathMap.get(storage), prefix);
        String finalPath = path.getFileName().toString();
        List<FileEntity> list = dirMap.get(finalPath);
        if (list != null) {
            if (page > pageSize * list.size()) {
                page = 1;
            }
            return new PageHelper(page, pageSize, list.size(), list);
        } else {
            list = new ArrayList<>();
        }
        try {
            List<FileEntity> finalList = list;
            Files.list(path).forEach(p -> {
                FileEntity fileEntity = new FileEntity();
                File file = new File(p.toString());
                if (!file.getName().startsWith(".")) {
                    fileEntity.setDirFlag(file.isDirectory());
                    fileEntity.setName(file.getName());
                    fileEntity.setSize(file.length() + "B");
                    fileEntity.setDate(DateUtil.formatDate(new Date(file.lastModified())));
                    finalList.add(fileEntity);
                }
            });
        } catch (IOException ignored) {
        }
        dirMap.put(finalPath, list);
        return new PageHelper(page, pageSize, list.size(), list);
    }


}
