package com.beer.cloud_api.controller;


import com.beer.cloud_api.common.ApplicationConstant;
import com.beer.cloud_api.entity.PageHelper;
import com.beer.cloud_api.service.ListFileService;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.Set;

@RestController
public class ListFileController {


    private final ListFileService listFileService;

    public ListFileController(ListFileService listFileService) {
        this.listFileService = listFileService;
    }

    @GetMapping("list")
    public PageHelper listFile(
            @RequestParam(value = "prefix", required = false) String prefix,
            @RequestParam(value = "storage") String storage,
            @RequestParam("page") int page,
            @RequestParam("pageSize") int pageSize) {
        if (!ApplicationConstant.storagePathNames.contains(storage)) {
            return null;
        }
        return listFileService.listFile(page, pageSize, prefix, storage);
    }


    @GetMapping("storages")
    public Set<String> getStorages() {
        return ApplicationConstant.storagePathNames;
    }

}
